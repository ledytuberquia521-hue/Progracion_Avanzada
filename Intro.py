import os

import streamlit as st
from PIL import Image

# ---------------------------------------------------------------
# Configuración de la página (debe ser la primera llamada a st.)
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Portafolio | Programación Avanzada 2026",
    page_icon="💻",
    layout="wide",
)

# ---------------------------------------------------------------
# Datos: cada proyecto es un diccionario. Para agregar uno nuevo
# solo añades un elemento a la lista, sin tocar el resto del código.
# ---------------------------------------------------------------
URL_SITIO_IA = "https://sites.google.com/view/aplicacionesdeia/inicio"

PROYECTOS = [
    {
        "titulo": "Cálculo aplicado: gradiente",
        "categoria": "Fundamentos",
        "imagen": "1.png",
        "descripcion": (
            "Analizamos el paso de la derivada al descenso de gradiente para "
            "comprender cómo los algoritmos buscan mínimos. Una mirada analítica "
            "a la regresión lineal y al ajuste iterativo para reducir el error."
        ),
        "url": "https://programaci-navanzada-n9yfwwcsyp9odtksrrdis8.streamlit.app/",
    },
    {
        "titulo": "Lógica, Big-O y vectorización",
        "categoria": "Fundamentos",
        "imagen": "2.png",
        "descripcion": (
            "Aprenderemos cómo la lógica, la complejidad Big-O y la vectorización "
            "impactan el rendimiento del hardware en sistemas de IA masivos."
        ),
        "url": "https://progracionavanzada-5g5vy49gqp9uxog9dwjmec.streamlit.app/",
    },
    {
        "titulo": "Preparación de datos",
        "categoria": "Datos",
        "imagen": "3.jpg",
        "descripcion": (
            "La preparación de datos como fundamento de la computación avanzada."
        ),
        "url": "https://progracionavanzada-m8tg6vcnxqttxqx3mgws8j.streamlit.app/",
    },
    {
        "titulo": "Aplicación: preparación de datos (Cornare)",
        "categoria": "Datos",
        "imagen": "OIG8.jpg",
        "descripcion": (
            "Análisis de datos reales de Cornare vía API aplicando las fases de "
            "comprensión y preparación de CRISP-DM con Python y Streamlit. Se "
            "procesan, limpian y evalúan los datos mediante un Índice de Calidad "
            "de Datos (ICD) por estación."
        ),
        "url": "https://sesion6estacion41.streamlit.app/",
    },
    {
        "titulo": "Regresión lineal",
        "categoria": "Modelos predictivos",
        "imagen": "data_analisis.png",
        "descripcion": (
            "La regresión permite predecir valores numéricos a partir de datos "
            "históricos, identificando relaciones entre variables mediante "
            "modelos matemáticos."
        ),
        "url": "https://progracionavanzada-5w22rqh6jx67mpfbbbbcf9.streamlit.app/",
    },
    {
        "titulo": "Series de tiempo",
        "categoria": "Modelos predictivos",
        "imagen": "OIG3.jpg",
        "descripcion": (
            "El análisis de series de tiempo permite anticipar comportamientos "
            "futuros a partir de datos históricos, identificando tendencias y "
            "estacionalidades mediante modelos estadísticos."
        ),
        "url": "https://progracionavanzada-series-de-tiempo.streamlit.app/",
    },
    {
        "titulo": "Predicción y modelado de la calidad del aire",
        "categoria": "Modelos predictivos",
        "imagen": "Chat_pdf.png",
        "descripcion": (
            "La predicción de la calidad del aire permite anticipar niveles de "
            "contaminación con modelos de series de tiempo que identifican "
            "patrones y generan pronósticos confiables."
        ),
        "url": "https://creando-aplicaciones-web-dise-o-mvc-jgxuwyybxgguelrhactazj.streamlit.app/",
    },
    {
        "titulo": "Predicción de sensación térmica con IoT",
        "categoria": "IoT",
        "imagen": "OIG4.jpg",
        "descripcion": (
            "Sistema de IoT para captura y procesamiento de datos. Usamos "
            "tecnologías de IoT para obtener datos propios."
        ),
        "url": "https://progracionavanzada-dmetcb9spjmh4upqwhpybh.streamlit.app/",
    },
    {
        "titulo": "De la regresión lineal a la logística",
        "categoria": "Clasificación",
        "imagen": "OIG6.jpg",
        "descripcion": (
            "Cómo pasar de predecir un número a elegir entre clases."
        ),
        "url": "https://progracionavanzada-mxrqkwsffvardta7urb8y3.streamlit.app/",
    },
    {
        "titulo": "KNN: clasificación de fertilidad de suelos",
        "categoria": "Clasificación",
        "imagen": "Chat_pdf.png",
        "descripcion": (
            "El algoritmo KNN realiza predicciones y clasificaciones según la "
            "similitud entre datos: una técnica sencilla y efectiva para "
            "identificar patrones en problemas del mundo real."
        ),
        "url": "https://progracionavanzada-4nzepzddx3ylcabklzxs5b.streamlit.app/",
    },
  
    {
        "titulo": "KNN: vecinos más cercanos",
        "categoria": "Clasificación",
        "imagen": "OIG6.jpg",
        "descripcion": (
            "KNN clasifica datos según la similitud con ejemplos conocidos, "
            "usando los vecinos más cercanos para realizar predicciones."
        ),
        "url": "https://progracionavanzada-4nzepzddx3ylcabklzxs5b.streamlit.app/",
    },
]

COLUMNAS = 3  # tarjetas por fila


# ---------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------
@st.cache_resource
def cargar_imagen(ruta):
    """Carga la imagen una sola vez; devuelve None si no existe."""
    if ruta and os.path.exists(ruta):
        return Image.open(ruta)
    return None


def tarjeta(proyecto):
    """Dibuja un proyecto dentro de un contenedor con borde."""
    with st.container(border=True):
        st.subheader(proyecto["titulo"])
        st.caption(f"🏷️ {proyecto['categoria']}")

        imagen = cargar_imagen(proyecto["imagen"])
        if imagen:
            st.image(imagen, use_container_width=True)

        st.write(proyecto["descripcion"])

        if proyecto["url"]:
            st.link_button("Abrir aplicación 🚀", proyecto["url"], use_container_width=True)
        else:
            st.button("Próximamente", disabled=True, key=proyecto["titulo"], use_container_width=True)


# ---------------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------------
with st.sidebar:
    st.header("👩‍💻 Sobre mí")
    st.write(
        "¡Hola! Bienvenido a mi portafolio digital. "
        "Soy estudiante de Ingeniería de Desarrollo de Software y este espacio "
        "está diseñado para documentar mi proceso de aprendizaje. Aquí encontrarás "
        "las evidencias, proyectos y prácticas que he desarrollado en clase, "
        "aplicando conceptos de desarrollo, algoritmos y resolución de problemas "
        "reales. Mi objetivo es transformar la teoría en soluciones de software "
        "funcionales y escalables."
    )
    st.link_button("Páginas y ejercicios prácticos", URL_SITIO_IA, use_container_width=True)

    st.divider()
    categorias = ["Todas"] + sorted({p["categoria"] for p in PROYECTOS})
    filtro = st.selectbox("Filtrar por categoría", categorias)


# ---------------------------------------------------------------
# Contenido principal
# ---------------------------------------------------------------
st.title("PROGRAMACIÓN AVANZADA 2026")
st.markdown(
    "Colección de aplicaciones desarrolladas durante el curso. "
    "Cada tarjeta lleva a una app desplegada en Streamlit."
)

visibles = [p for p in PROYECTOS if filtro == "Todas" or p["categoria"] == filtro]
st.caption(f"Mostrando {len(visibles)} de {len(PROYECTOS)} proyectos")

for i in range(0, len(visibles), COLUMNAS):
    fila = visibles[i : i + COLUMNAS]
    columnas = st.columns(COLUMNAS)
    for col, proyecto in zip(columnas, fila):
        with col:
            tarjeta(proyecto)

st.divider()
st.caption("Hecho con Streamlit · Programación Avanzada 2026")
