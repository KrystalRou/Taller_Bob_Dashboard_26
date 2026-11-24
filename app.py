"""
📊 Dashboard ElectroMarket — app web con Streamlit

Cómo correrla (con el entorno del taller activado):
    streamlit run app.py

Se abre sola en el navegador (http://localhost:8501).
Para que la vean otras personas en la misma red, usa el enlace "Network URL" que aparece en la terminal.
"""
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(page_title="Dashboard ElectroMarket", page_icon="📊", layout="wide")

ARCHIVO = Path(__file__).parent / "ElectroMarket.xlsx"
COLORES = px.colors.qualitative.Set2
MESES_CORTOS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
ORDEN_PRIORIDAD = ["Critical", "High", "Medium", "Low"]


# ───────────────────────── 1. Cargar y limpiar los datos ─────────────────────────
def normalizar(texto):
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(texto.lower().replace("_", " ").split())


def buscar_columna(df, *opciones, obligatoria=True):
    mapa = {normalizar(c): c for c in df.columns}
    for op in opciones:
        if normalizar(op) in mapa:
            return mapa[normalizar(op)]
    for op in opciones:
        for n, original in mapa.items():
            if normalizar(op) in n:
                return original
    if obligatoria:
        raise KeyError(f"No encontré la columna {opciones}. Columnas: {list(df.columns)}")
    return None


@st.cache_data(show_spinner="Leyendo el Excel…")
def cargar(origen):
    hojas = pd.ExcelFile(origen).sheet_names
    hoja = "Ventas Supermercado" if "Ventas Supermercado" in hojas else hojas[0]
    crudo = pd.read_excel(origen, sheet_name=hoja)

    col = lambda *o, ob=True: buscar_columna(crudo, *o, obligatoria=ob)
    envio = col("Método de Envio2", ob=False) or col("Método de Envio", "Metodo Envio")
    df = pd.DataFrame({
        "Mercado":   crudo[col("Mercado")].astype(str).str.strip(),
        "País":      crudo[col("País", "Pais")].astype(str).str.strip(),
        "Ventas":    pd.to_numeric(crudo[col("Ventas")], errors="coerce"),
        "Utilidad":  pd.to_numeric(crudo[col("Utilidad")], errors="coerce"),
        "Prioridad": crudo[col("Prioridad Envio", "Prioridad")].astype(str).str.strip(),
        "Envío":     crudo[envio].astype(str).str.strip().str.title(),
        "Fecha":     pd.to_datetime(crudo[col("Fecha Salida")], errors="coerce", dayfirst=True),
    })
    extras = {
        "Pedido":        (col("ID Venta", ob=False) or col("Número Venta", ob=False), None),
        "Segmento":      (col("Segmento", ob=False), "texto"),
        "Categoría":     (col("Categoría", "Categoria", ob=False), "texto"),
        "Sub-Categoría": (col("Sub-Categoría", "Sub-Categoria", ob=False), "texto"),
        "Descuento":     (col("Descuento", ob=False), "numero"),
        "Llegada":       (col("Status Llegada", ob=False), "texto"),
        "Días":          (col("Días Transcurridos", "Dias Transcurridos", ob=False), "numero"),
        "Costo Envío":   (col("Costo Envío", "Costo Envio", ob=False), "numero"),
    }
    for nombre, (c, tipo) in extras.items():
        if c:
            s = crudo[c]
            df[nombre] = s.astype(str).str.strip() if tipo == "texto" else (
                pd.to_numeric(s, errors="coerce") if tipo == "numero" else s)
    df = df.dropna(subset=["Ventas", "Fecha"])
    df["Año"] = df["Fecha"].dt.year
    return df


# ───────────────────────── 2. KPIs ─────────────────────────
META_MARGEN_DEF, META_A_TIEMPO_DEF = 12, 95


def calcular(d):
    ventas, utilidad = d["Ventas"].sum(), d["Utilidad"].sum()
    pedidos = d["Pedido"].nunique() if "Pedido" in d else len(d)
    return {
        "ventas": ventas, "utilidad": utilidad, "pedidos": pedidos,
        "ticket": ventas / pedidos if pedidos else 0,
        "margen": utilidad / ventas * 100 if ventas else 0,
        "a_tiempo": (d["Llegada"].str.lower() == "on time").mean() * 100 if "Llegada" in d else None,
        "dias": d["Días"].mean() if "Días" in d else None,
        "costo_env": d["Costo Envío"].sum() if "Costo Envío" in d else None,
    }


def dinero(x):
    """$4.30 M, $504 K, $503: cifras cortas para que quepan en las tarjetas."""
    if abs(x) >= 1e6:
        return f"${x / 1e6:,.2f} M"
    if abs(x) >= 1e4:
        return f"${x / 1e3:,.0f} K"
    return f"${x:,.0f}"


def tarjetas(actual, previo):
    """Fila de tarjetas con flecha contra el año anterior."""
    a = calcular(actual)
    p = calcular(previo) if len(previo) else None
    filas = [
        ("💵 Ventas", "ventas", dinero, False),
        ("💰 Utilidad", "utilidad", dinero, False),
        ("🧾 Pedidos", "pedidos", "{:,.0f}".format, False),
        ("🛒 Ticket promedio", "ticket", dinero, False),
        ("🚚 Días de entrega", "dias", "{:.1f}".format, True),
        ("📦 Costo de envío", "costo_env", dinero, True),
    ]
    columnas = st.columns(len(filas))
    for colm, (titulo, clave, fmt, menos_es_mejor) in zip(columnas, filas):
        if a[clave] is None:
            continue
        delta = None
        if p and p[clave]:
            delta = f"{(a[clave] / p[clave] - 1):+.1%}"
        colm.metric(titulo, fmt(a[clave]), delta,
                    delta_color="inverse" if menos_es_mejor else "normal", border=True)


def velocimetro(valor, titulo, meta, maximo):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta", value=valor,
        number=dict(suffix="%", valueformat=".1f"),
        delta=dict(reference=meta, valueformat=".1f", suffix=" pts vs meta"),
        title=dict(text=titulo, font_size=16),
        gauge=dict(axis=dict(range=[0, maximo]), bar=dict(color="#1f3b73"),
                   steps=[dict(range=[0, meta * 0.8], color="#f8d7da"),
                          dict(range=[meta * 0.8, meta], color="#fff3cd"),
                          dict(range=[meta, maximo], color="#d4edda")],
                   threshold=dict(line=dict(color="black", width=4), value=meta))))
    return fig.update_layout(height=260, margin=dict(t=60, b=10, l=30, r=30))


# ───────────────────────── 3. Las 10 gráficas ─────────────────────────
def g_mercado(d):
    t = d.groupby("Mercado", as_index=False)["Ventas"].sum().sort_values("Ventas")
    fig = px.bar(t, x="Ventas", y="Mercado", orientation="h", text_auto=".3s",
                 title="Ventas por mercado · Barras", color_discrete_sequence=[COLORES[0]])
    return fig.update_layout(xaxis_title="Ventas (USD)", yaxis_title="")


def g_mensual(d):
    t = d.groupby([d["Fecha"].dt.year.rename("Año"), d["Fecha"].dt.month.rename("Mes")])["Ventas"].sum().reset_index()
    t["Año"] = t["Año"].astype(str)
    fig = px.line(t, x="Mes", y="Ventas", color="Año", markers=True,
                  title="Ventas mensuales por año · Líneas", color_discrete_sequence=COLORES)
    return fig.update_xaxes(tickvals=list(range(1, 13)), ticktext=MESES_CORTOS).update_layout(yaxis_title="Ventas (USD)")


def g_envio(d):
    t = d.groupby("Envío", as_index=False)["Ventas"].sum()
    fig = px.pie(t, names="Envío", values="Ventas", hole=0.5,
                 title="Ventas por método de envío · Anillo", color_discrete_sequence=COLORES)
    return fig.update_traces(textinfo="percent+label")


def g_prioridad(d):
    t = d.pivot_table(index="Mercado", columns="Prioridad", values="Ventas", aggfunc="sum", fill_value=0)
    t = (t.div(t.sum(axis=1), axis=0) * 100).reset_index()
    largo = t.melt(id_vars="Mercado", var_name="Prioridad", value_name="%")
    orden = [p for p in ORDEN_PRIORIDAD if p in largo["Prioridad"].unique()] or None
    fig = px.bar(largo, x="Mercado", y="%", color="Prioridad", text_auto=".0f",
                 category_orders={"Prioridad": orden} if orden else None,
                 title="Prioridad de envío por mercado · Columnas 100%", color_discrete_sequence=COLORES)
    return fig.update_layout(barmode="stack", yaxis_title="% de las ventas", yaxis_range=[0, 100])


def g_dispersion(d):
    t = d.groupby(["País", "Mercado"]).agg(Ventas=("Ventas", "sum"), Utilidad=("Utilidad", "sum"),
                                            Pedidos=("Ventas", "count")).reset_index()
    fig = px.scatter(t, x="Ventas", y="Utilidad", color="Mercado", size="Pedidos", size_max=40,
                     hover_name="País", title="Ventas vs. utilidad por país · Burbujas",
                     color_discrete_sequence=COLORES)
    if len(t) > 1:
        m, b = np.polyfit(t["Ventas"], t["Utilidad"], 1)
        xs = np.linspace(t["Ventas"].min(), t["Ventas"].max(), 50)
        fig.add_scatter(x=xs, y=m * xs + b, mode="lines", name="Tendencia", line=dict(color="gray", dash="dash"))
    fig.add_hline(y=0, line_color="red", line_width=1)
    return fig.update_layout(xaxis_title="Ventas (USD)", yaxis_title="Utilidad (USD)")


def g_mapa(d):
    t = d.groupby("País", as_index=False)[["Ventas", "Utilidad"]].sum()
    lim = t["Utilidad"].abs().quantile(0.95) or 1
    fig = px.choropleth(t, locations="País", locationmode="country names", color="Utilidad",
                        hover_data={"Ventas": ":$,.0f", "Utilidad": ":$,.0f"},
                        color_continuous_scale="RdYlGn", range_color=[-lim, lim],
                        title="Utilidad por país · Mapa")
    return fig.update_geos(showframe=False, projection_type="natural earth").update_layout(margin=dict(l=0, r=0))


def g_treemap(d):
    if "Categoría" not in d:
        return None
    niveles = ["Categoría", "Sub-Categoría"] if "Sub-Categoría" in d else ["Categoría"]
    t = d.groupby(niveles, as_index=False)[["Ventas", "Utilidad"]].sum()
    t["Margen %"] = t["Utilidad"] / t["Ventas"] * 100
    fig = px.treemap(t, path=[px.Constant("Todos")] + niveles, values="Ventas", color="Margen %",
                     color_continuous_scale="RdYlGn", color_continuous_midpoint=0,
                     title="Ventas y margen por categoría · Treemap")
    return fig.update_traces(texttemplate="<b>%{label}</b><br>$%{value:,.3s}").update_layout(margin=dict(l=10, r=10))


def g_calor(d):
    if "Categoría" not in d:
        return None
    v = d.pivot_table(index="Mercado", columns="Categoría", values="Ventas", aggfunc="sum")
    u = d.pivot_table(index="Mercado", columns="Categoría", values="Utilidad", aggfunc="sum")
    fig = px.imshow((u / v * 100).round(1), text_auto=".1f", aspect="auto",
                    color_continuous_scale="RdYlGn", color_continuous_midpoint=0,
                    title="Margen % por mercado y categoría · Mapa de calor")
    return fig.update_layout(coloraxis_colorbar_title="Margen %", xaxis_title="", yaxis_title="")


def g_cascada(d):
    if d["Año"].nunique() > 1:
        t = d.groupby("Año")["Utilidad"].sum()
        etiquetas = [str(a) for a in t.index]
    else:
        t = d.groupby(d["Fecha"].dt.quarter)["Utilidad"].sum()
        etiquetas = [f"T{q}" for q in t.index]
    valores = [t.iloc[0]] + list(t.diff().iloc[1:]) + [t.iloc[-1]]
    medidas = ["absolute"] + ["relative"] * (len(t) - 1) + ["total"]
    fig = go.Figure(go.Waterfall(x=etiquetas + [f"Cierre {etiquetas[-1]}"], y=valores, measure=medidas,
                                 text=[f"${v:,.0f}" for v in valores], textposition="outside",
                                 increasing_marker_color="#2ca02c", decreasing_marker_color="#d62728",
                                 totals_marker_color="#1f3b73"))
    return fig.update_layout(title="Cómo cambió la utilidad · Cascada", yaxis_title="Utilidad (USD)")


def g_descuento(d):
    if "Descuento" not in d:
        return None
    rangos = pd.cut(d["Descuento"], bins=[-0.01, 0, 0.2, 0.4, 1],
                    labels=["Sin descuento", "1–20%", "21–40%", "Más de 40%"])
    t = d.assign(Rango=rangos)
    fig = px.box(t, x="Rango", y="Utilidad", color="Rango", points=False,
                 category_orders={"Rango": list(rangos.cat.categories)},
                 title="Utilidad por venta según el descuento · Cajas", color_discrete_sequence=COLORES)
    bajo, alto = t["Utilidad"].quantile([0.02, 0.98])
    fig.add_hline(y=0, line_color="red", line_width=1)
    return fig.update_layout(yaxis_range=[bajo, alto], showlegend=False, xaxis_title="Descuento",
                             yaxis_title="Utilidad por venta (USD)")


def dibujar(columna, funcion, d, alto=420):
    fig = funcion(d)
    if fig is None:
        columna.info("Esta gráfica necesita una columna que tu Excel no tiene.")
    else:
        columna.plotly_chart(fig.update_layout(height=alto, template="plotly_white"), width="stretch")


# ───────────────────────── 4. La página ─────────────────────────
st.sidebar.title("📊 ElectroMarket")
subido = st.sidebar.file_uploader("¿Otro Excel? Súbelo aquí", type=["xlsx"])
if subido is not None:
    df = cargar(subido)
elif ARCHIVO.exists():
    df = cargar(str(ARCHIVO))
else:
    st.error(f"No encuentro {ARCHIVO.name}. Ponlo en la misma carpeta que app.py o súbelo en la barra lateral.")
    st.stop()

st.sidebar.header("Filtros")
mercados = st.sidebar.multiselect("Mercado", sorted(df["Mercado"].unique()), placeholder="Todos")
anios = sorted(df["Año"].unique())
anio = st.sidebar.selectbox("Año", ["Todos"] + anios)
segmentos = st.sidebar.multiselect("Segmento", sorted(df["Segmento"].unique()), placeholder="Todos") \
    if "Segmento" in df else []
st.sidebar.header("Metas")
meta_margen = st.sidebar.slider("Meta de margen (%)", 0, 30, META_MARGEN_DEF)
meta_tiempo = st.sidebar.slider("Meta de entregas a tiempo (%)", 50, 100, META_A_TIEMPO_DEF)

base = df
if mercados:
    base = base[base["Mercado"].isin(mercados)]
if segmentos:
    base = base[base["Segmento"].isin(segmentos)]
d = base if anio == "Todos" else base[base["Año"] == anio]

if d.empty:
    st.warning("No hay datos con esos filtros 🙃")
    st.stop()

anio_kpi = int(base["Año"].max()) if anio == "Todos" else int(anio)
actual, previo = base[base["Año"] == anio_kpi], base[base["Año"] == anio_kpi - 1]

st.title("📊 Dashboard ElectroMarket")
st.caption(f"KPIs de {anio_kpi}" + (f" · las flechas comparan contra {anio_kpi - 1}" if len(previo) else "")
           + " · las gráficas usan todos los filtros de la izquierda")

tarjetas(actual, previo)
k = calcular(actual)
c1, c2, c3 = st.columns([1, 1, 1.2])
c1.plotly_chart(velocimetro(k["margen"], "Margen de utilidad", meta_margen, 30), width="stretch")
if k["a_tiempo"] is not None:
    c2.plotly_chart(velocimetro(k["a_tiempo"], "Entregas a tiempo", meta_tiempo, 100), width="stretch")
dibujar(c3, g_envio, d, alto=300)

tab1, tab2, tab3, tab4 = st.tabs(["🏆 Ventas", "💰 Rentabilidad", "🌎 Países", "📦 Productos y envíos"])
with tab1:
    a, b = st.columns(2)
    dibujar(a, g_mercado, d)
    dibujar(b, g_mensual, d)
    dibujar(st, g_prioridad, d)
with tab2:
    a, b = st.columns(2)
    dibujar(a, g_cascada, d)
    dibujar(b, g_calor, d)
    dibujar(st, g_descuento, d)
with tab3:
    dibujar(st, g_mapa, d, alto=520)
    dibujar(st, g_dispersion, d, alto=480)
with tab4:
    dibujar(st, g_treemap, d, alto=520)

with st.expander("🔎 Ver los datos filtrados"):
    st.dataframe(d, width="stretch", height=300)
    st.download_button("⬇️ Descargar CSV", d.to_csv(index=False).encode("utf-8"),
                       "electromarket_filtrado.csv", "text/csv")
