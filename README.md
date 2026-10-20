# Eficiencia y paralelismo en Python

App de apoyo al Colab introductorio (Módulo 11 · Computación Avanzada).

## Archivos
- `app.py`: la app (pestañas Inicio, Hilos, Procesos, NumPy, Ley de Amdahl y Preguntas).
- `tareas.py`: funciones que ejecutan los workers. Deben estar en un archivo aparte para que los procesos funcionen.
- `requirements.txt`: dependencias.

## Ejecutar localmente
```
pip install -r requirements.txt
streamlit run app.py
```

## Desplegar en Streamlit Cloud
1. Suba estos tres archivos a un repositorio de GitHub.
2. En https://share.streamlit.io, elija **Create app**, el repositorio y `app.py` como archivo principal.
3. Pulse **Deploy**.
