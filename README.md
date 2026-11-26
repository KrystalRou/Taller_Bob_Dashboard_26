# 📊 Construye tu primer dashboard con IBM Bob

Taller híbrido · Viernes 27 de noviembre · ITVER y BUAP
Embajadores Estudiantiles de IBM SkillsBuild

En este taller vas a correr un dashboard hecho en Python con datos reales de ventas (ElectroMarket) y le vas a pedir a **IBM Bob**, un asistente de programación con IA, que lo mejore.

🌐 **Ver los dashboards sin instalar nada:** [krystalrou.github.io/Taller_Bob_Dashboard_26](https://krystalrou.github.io/Taller_Bob_Dashboard_26/)

📽️ **Sigue la presentación aquí:** [[Presentacion_Taller.pdf](https://docs.google.com/presentation/d/1MB-WsTL2hDBKNTcGNmS_J0_5Nv2OXHoGuluRwPTgcSM/edit?usp=sharing)](Presentacion_Taller.pdf)

---

## 📁 Qué hay en este repositorio

| Archivo | Para qué sirve |
|---|---|
| `app.py` | **La app web del dashboard** (Streamlit): la que se abre en el navegador |
| `Dashboard_ElectroMarket.ipynb` | El notebook: el mismo análisis explicado paso a paso |
| `ElectroMarket.xlsx` | Los datos de ventas |
| `requirements.txt` | Las librerías que necesita el código |
| `Presentacion_Taller.pdf` | La presentación del taller |
| `retos.md` | Ideas de cambios para pedirle a Bob |
| `Dashboard_ElectroMarket_Completo.ipynb` | **Versión extendida** (después del taller): 15 gráficas, KPIs y página web de una sola pantalla |
| `Aplicacion_Ingenieria_Mecanica.ipynb` | **Aplicación a la ingeniería mecánica:** mantenimiento predictivo de una fresadora |
| `ai4i2020.csv` | Datos de la fresadora (AI4I 2020, UCI) |
| `index.html` y los `.html` | Las páginas web que publica GitHub Pages |

---

## ✅ Antes del taller (hazlo un día antes)

1. **Instala Python** desde [python.org](https://www.python.org/downloads/). En Windows marca la casilla **Add Python to PATH**.
2. **Crea tu cuenta de IBM SkillsBuild** e **instala IBM Bob** desde **ibm.biz/university-bob**.
3. **Crea tu cuenta de GitHub** en [github.com](https://github.com) (plan Free). Para descargar los archivos no la necesitas, pero sí para guardar tu propio proyecto.

---

## 🚀 Durante el taller

### Task 1 · Descarga los archivos
1. En esta página toca el botón verde **Code → Download ZIP**.
2. Descomprime el ZIP en tu **Escritorio**.

### Task 2 · Abre el proyecto en Bob
1. Abre Bob y ve a **File → Open Folder**. Elige la carpeta que descomprimiste.
2. Toca **Trust** para que Bob pueda leer y editar los archivos.
3. Si Bob te pide instalar la extensión **Jupyter** o **Python**, acéptala.

### Task 3 · Corre el dashboard

**Opción A: pídeselo a Bob** (en modo **Agent**):
```
Instala las librerías de requirements.txt y corre Dashboard_ElectroMarket.ipynb.
Si hay errores, arréglalos y explícame qué cambiaste.
```

**Opción B: tú mismo, con un entorno solo para el taller**

Un *entorno virtual* es una carpeta con su propio Python y sus propias librerías. Así no chocan con lo que ya tengas instalado.

1. Abre una terminal: **Terminal → New Terminal**. Ya debe estar en la carpeta del taller.
2. Crea y activa el entorno:

   **Mac / Linux**
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   **Windows**
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
   Si funcionó, al inicio de la línea aparece `(.venv)`.
3. Instala las librerías:
   ```
   pip install -r requirements.txt
   ```
4. Abre `Dashboard_ElectroMarket.ipynb`, toca **Select Kernel → Python Environments** y elige **.venv**. Luego toca **Run All**.

En el notebook vas a ver un **panel de KPIs** con indicadores y velocímetros, **10 gráficas de 10 tipos distintos** (barras, líneas, anillo, columnas 100%, burbujas, mapa, treemap, mapa de calor, cascada y cajas) y, al final, el **dashboard con filtros** de Mercado, Año y Segmento.

### Task 3b · Abre la app del dashboard 🌐
Esta es la versión que puede consultar cualquier persona: se abre en el navegador, con filtros y pestañas.

Con el entorno activado (`(.venv)` o `(taller_bob)` al inicio de la línea), escribe en la terminal:
```
streamlit run app.py
```
Se abre sola en tu navegador (`http://localhost:8501`). Para detenerla, vuelve a la terminal y presiona **Ctrl + C**.

**¿Cómo la ven otras personas?**
- **En la misma red (salón o junta):** la terminal muestra un **Network URL**, por ejemplo `http://192.168.1.25:8501`. Quien esté en el mismo Wi-Fi lo abre en su navegador o celular mientras tu app siga corriendo.
- **Desde cualquier lugar:** entra a **share.streamlit.io** con tu cuenta de GitHub, toca **Create app**, elige tu repositorio y el archivo `app.py`. En unos minutos te da un enlace público que funciona aunque tu compu esté apagada.

O pídeselo a Bob:
```
Instala las librerías de requirements.txt y corre la app con streamlit run app.py.
```

### Task 4 · Pídele cambios a Bob
Escríbele como se lo dirías a una persona. Revisa [retos.md](retos.md) para ver ideas.

**Cuatro reglas para trabajar con Bob:**
1. **Un cambio a la vez.** Pide algo, revisa y luego pide lo siguiente.
2. **Di qué, dónde y cómo.** "En la gráfica de ventas por mercado, cambia el color a azul."
3. **Revisa antes de aceptar.** Lee lo que Bob cambió. Tú decides.
4. **¿Error? Pégaselo.** Copia el mensaje de error y pídele que te lo explique.

### Task 5 · Comparte tu dashboard
1. Toma una captura de tu dashboard terminado. También puedes usar el archivo `dashboard_electromarket.html` que crea el notebook.
2. Publica en **LinkedIn** qué construiste y qué le pediste a Bob.
3. Etiqueta a **@IBM SkillsBuild** y usa **#IBMSkillsBuild #IBMBOB**.

---

## 🆘 Si algo falla

| Problema | Qué hacer |
|---|---|
| `pip` no se reconoce | Reinstala Python marcando **Add Python to PATH**, o usa `python -m pip install -r requirements.txt` |
| `No module named 'pandas.core...'` (pandas roto, pasa mucho con Anaconda) | Usa el entorno `.venv` de la opción B y elígelo en **Select Kernel** |
| `No module named ...` | Corre otra vez `pip install -r requirements.txt` y elige ese mismo Python en **Select Kernel** |
| `FileNotFoundError: ElectroMarket.xlsx` | El Excel debe estar en la misma carpeta que el notebook y llamarse `ElectroMarket.xlsx` |
| `No encontré la columna ...` | El mensaje te dice qué columnas tiene tu archivo. Pégaselo a Bob |
| `streamlit: command not found` | Activa el entorno y corre `pip install -r requirements.txt` otra vez |
| La app dice que no encuentra el Excel | `ElectroMarket.xlsx` debe estar junto a `app.py`, o súbelo en la barra lateral de la app |
| No se ven los filtros | Instala la extensión **Jupyter** y vuelve a correr todo |
| No puedes instalar Bob | Haz equipo con quien tengas al lado y sigan juntos en su computadora |

---

## 🌟 Después del taller: versión completa e ingeniería mecánica

| Notebook | Qué analiza | Ver (sin instalar) | Correr (sin instalar) |
|---|---|---|---|
| `Dashboard_ElectroMarket_Completo.ipynb` | Ventas en 147 países: 8 KPIs y 15 gráficas | [Ver dashboard](https://krystalrou.github.io/Taller_Bob_Dashboard_26/dashboard_electromarket_completo.html) | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KrystalRou/Taller_Bob_Dashboard_26/blob/main/Dashboard_ElectroMarket_Completo.ipynb) |
| `Aplicacion_Ingenieria_Mecanica.ipynb` | Mantenimiento predictivo de una fresadora: Pareto, Cp/Cpk, carta de control, curvas de potencia | [Ver dashboard](https://krystalrou.github.io/Taller_Bob_Dashboard_26/aplicacion_ingenieria_mecanica.html) | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/KrystalRou/Taller_Bob_Dashboard_26/blob/main/Aplicacion_Ingenieria_Mecanica.ipynb) |

**Ver:** los enlaces abren la página web en cualquier navegador, incluso en el celular. Toca una gráfica para verla en grande, usa ◀ ▶ para pasar a la siguiente y **Esc** para regresar.

**Correr en Google Colab:** solo necesitas una cuenta de Google.
1. Toca **Abrir en Colab**.
2. Corre la primera celda, **"¿Lo abriste en Google Colab?"**: descarga este repositorio con los datos y activa los filtros.
3. Ve a **Entorno de ejecución → Ejecutar todas**. La última celda descarga la página web del dashboard.

**Correr y modificar con IBM Bob en tu computadora:** sigue los pasos de las Tasks 1 a 3 y abre cualquiera de los dos notebooks.
- **Cierra el notebook antes de pedirle un cambio a Bob** y vuelve a abrirlo después. Si queda abierto, el editor puede guardar la versión vieja encima del cambio de Bob.
- Nombra el archivo con `@` y termina el prompt con *"No cambies nada más"*:
  ```
  @Aplicacion_Ingenieria_Mecanica.ipynb Agrega una carta de control R (rangos) junto a g_carta_control y súmala a GRAFICAS. No cambies nada más.
  ```
- Más ideas para la versión de mecánica: cambiar los límites `LIE` y `LSE` para ver cómo cambia el **Cpk**, o entrenar un modelo que prediga la falla con `scikit-learn`.

Datos de la fresadora: *AI4I 2020 Predictive Maintenance Dataset*, S. Matzka, UCI Machine Learning Repository (2020), licencia CC BY 4.0. Es una base sintética creada para reflejar datos reales de mantenimiento en la industria.

---

## 📚 Sigue aprendiendo
Aprende gratis con IBM Bob e IBM SkillsBuild: **[tu enlace UTM]**
