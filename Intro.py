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
col1, col2, col3 = st.columns(3)

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
 st.write("En el enlace aprenderesmoa a analizar como la lógica, la complejidad Big-O"
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
 st.write("En la siguiente enlace veremos como se pueden analizar datos usando agentes.") 
 url = "https://progracionavanzada-5w22rqh6jx67mpfbbbbcf9.streamlit.app/"
 st.write(f"Datos: [Enlace]({url})")

 st.subheader("Series de Tiempo.")
 image = Image.open('OIG3.jpg')
 st.image(image, width=200)
 st.write("En la siguiente enlace veremos como realizamos transcripciones de audio/video.") 
 url = "https://progracionavanzada-series-de-tiempo.streamlit.app/"
 st.write(f"Transcriptor: [Enlace]({url})")


with col3: 
 st.subheader("Predicción y modelado de la calidad de aire.")
 image = Image.open('Chat_pdf.png')
 st.image(image, width=190)
 st.write("En la siguiente veremos una aplicación que usa RAG a partir de un documento (PDF).") 
 url = "https://creando-aplicaciones-web-dise-o-mvc-jgxuwyybxgguelrhactazj.streamlit.app/"
 st.write(f"RAG: [Enlace]({url})")

 st.subheader("Predicción de sensación térmica con IoT")
 image = Image.open('OIG4.jpg')
 st.image(image, width=200)
 st.write("En la siguiente enlace veremos la capacidad de análisis en Imágenes.") 
 url = "https://progracionavanzada-dmetcb9spjmh4upqwhpybh.streamlit.app/"
 st.write(f"Vision: [Enlace]({url})")
 
 st.subheader("De la regresión lineal a la logísitica")
 image = Image.open('OIG6.jpg')
 st.image(image, width=200)
 st.write("En la siguiente enlace veremos la capacidad de interacción con el mundo físico.") 
 url = "https://progracionavanzada-mxrqkwsffvardta7urb8y3.streamlit.app/"
 st.write(f"Vision: [Enlace]({url})")

with col4: 
 st.subheader("Aplicación Knn: Clasificación de fertilidad de  suelos")
 image = Image.open('Chat_pdf.png')
 st.image(image, width=190)
 st.write("En la siguiente veremos una aplicación que usa RAG a partir de un documento (PDF).") 
 url = "https://progracionavanzada-4nzepzddx3ylcabklzxs5b.streamlit.app/"
 st.write(f"RAG: [Enlace]({url})")

 


