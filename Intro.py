import streamlit as st
from PIL import Image
st.title("PROGRAMACIÓN AVANZADA 2026.")

with st.sidebar:
  st.subheader("Calculo aplicado, gradiente..")
  parrafo = (
"¡Hola! Bienvenido a mi portafolio digital."
"Soy estudiante de Ingeniería de Desarrollo de Software y este espacio está diseñado"
" para documentar mi proceso de aprendizaje. Aquí encontrarás las evidencias,"
" proyectos y prácticas que he desarrollado en clase, aplicando conceptos de desarrollo,"
" algoritmos y resolución de problemas reales. Mi objetivo es transformar la teoría en"
" soluciones de software funcionales y escalables."
  )
  st.write(parrafo)

url_ia="https://sites.google.com/view/aplicacionesdeia/inicio"
st.subheader("En el siguiente enlace puedes encontrar páginas y ejercicios prácticos")
st.write(f"Enlace para páginas y ejercicios: [Enlace]({url_ia})")
col1, col2, col3, col4  = st.columns(3)

with col1:
 
 st.subheader("Calculo aplicado, gradiente.")
 image = Image.open('txt_to_audio2.png')
 st.image(image, width=190)
 st.write("Analizamos el paso de la derivada al descenso de gradiente"
" para comprender cómo los algoritmos buscan mínimos."
" Una mirada analítica a la regresión lineal y al ajuste iterativo para reducir el error.") 
 url = "https://programaci-navanzada-n9yfwwcsyp9odtksrrdis8.streamlit.app/"
 st.write(f"Calculo aplicado, gradiente: [Enlace]({url})")

 st.subheader("Lógica, Big-O y Vectorización")
 image = Image.open('txt_to_audio.png')
 st.image(image, width=200)
 st.write("En el enlace aprenderesmos a analizar como la lógica, la complejidad Big-O"
" y la vectorización impactan el rendimiento del hardware en sistemas de IA masivos.") 
 url = "https://progracionavanzada-5g5vy49gqp9uxog9dwjmec.streamlit.app/"
 st.write(f"YOLO: [Enlace]({url})")

 st.subheader("Preparación de datos")
 image = Image.open('OIG5.jpg')
 st.image(image, width=200)
 st.write("En el enlace veremos la preparación de datos como fundamento de la computación avanzada.") 
 url = "https://progracionavanzada-m8tg6vcnxqttxqx3mgws8j.streamlit.app/"
 st.write(f"YOLO: [Enlace]({url})")

with col2: 
 st.subheader("Aplicación Preparación de datos")
 image = Image.open('OIG8.jpg')
 st.image(image, width=200)
 st.write("Analizamos datos reales de Cornare vía API aplicando las fases de comprensión y preparación de "
"CRISP-DM con Python y Streamlit. El objetivo es procesar, limpiar y evaluar la calidad de la" "información mediante un Índice de Calidad de Datos (ICD) por estación.") 
 url = "https://sesion6estacion41.streamlit.app/"
 st.write(f"Voz a texto: [Enlace]({url})")

 st.subheader("Regresión Lineal")
 image = Image.open('data_analisis.png')
 st.image(image, width=190)
 st.write("En la siguiente enlace veremos como la regresión permite predecir valores numéricos a partir de datos históricos, "
 "identificando relaciones entre variables mediante modelos matemáticos.") 
 url = "https://progracionavanzada-5w22rqh6jx67mpfbbbbcf9.streamlit.app/"
 st.write(f"Datos: [Enlace]({url})")

 st.subheader("Series de Tiempo.")
 image = Image.open('OIG3.jpg')
 st.image(image, width=200)
 st.write("En la siguiente enlace veremos como el análisis de series de tiempo permite predecir comportamientos futuros a partir de datos históricos, "
 " identificando patrones como tendencias y estacionalidades mediante modelos estadísticos.") 
 url = "https://progracionavanzada-series-de-tiempo.streamlit.app/"
 st.write(f"Transcriptor: [Enlace]({url})")


with col3: 
 st.subheader("Predicción y modelado de la calidad de aire.")
 image = Image.open('Chat_pdf.png')
 st.image(image, width=190)
 st.write("En la siguiente veremos como La predicción de la calidad del aire permite anticipar niveles de contaminación a partir de datos históricos,"
 "utilizando modelos de series de tiempo para identificar patrones y generar pronósticos confiables.") 
 url = "https://creando-aplicaciones-web-dise-o-mvc-jgxuwyybxgguelrhactazj.streamlit.app/"
 st.write(f"RAG: [Enlace]({url})")

 st.subheader("Predicción de sensación térmica con IoT")
 image = Image.open('OIG4.jpg')
 st.image(image, width=200)
 st.write("En la siguiente enlace veremos un sistema de IoT Captura de datos y procesamiento. En esta sesión utilizaremos tecnologías de IoT para la obtención de datos propios.") 
 url = "https://progracionavanzada-dmetcb9spjmh4upqwhpybh.streamlit.app/"
 st.write(f"Vision: [Enlace]({url})")
 
 st.subheader("De la regresión lineal a la logísitica")
 image = Image.open('OIG6.jpg')
 st.image(image, width=200)
 st.write("En la siguiente enlace veremos como podemos pasar de predecir un número a la elección de clases.") 
 url = "https://progracionavanzada-mxrqkwsffvardta7urb8y3.streamlit.app/"
 st.write(f"Vision: [Enlace]({url})")

with col4: 
 st.subheader("Aplicación Knn: Clasificación de fertilidad de  suelos")
 image = Image.open('Chat_pdf.png')
 st.image(image, width=190)
 st.write("En la siguiente veremos como el algoritmo KNN permite realizar predicciones y clasificaciones basadas en la similitud entre datos, "
 "siendo una técnica sencilla y efectiva para identificar patrones y resolver problemas del mundo real.") 
 url = "https://progracionavanzada-4nzepzddx3ylcabklzxs5b.streamlit.app/"
 st.write(f"Vision: [Enlace]({url})")

 st.subheader("Aplicación Knn Clasificación de fertilidad de  suelos")
 image = Image.open('OIG6.jpg')
 st.image(image, width=200)
 st.write("En la siguiente enlace veremos como KNN clasifica datos según la similitud con ejemplos conocidos, utilizando los vecinos más cercanos para realizar predicciones.") 
 url = "https://progracionavanzada-mxrqkwsffvardta7urb8y3.streamlit.app/"
 st.write(f"Vision: [Enlace]({url})")

 


