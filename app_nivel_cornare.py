"""
App Streamlit — Nivel de río/quebrada, Estación 38 (CORNARE / MARCO)
----------------------------------------------------------------------
Versión personalizada: trabaja SIEMPRE con la estación 38, no permite
cambiarla desde la app. Muestra información extra de la estación y un
diagrama simple de niveles de alerta como referencia visual.

Para correrla:
    streamlit run app_nivel_cornare_estacion38.py
"""
import requests
import pandas as pd
import numpy as np
import streamlit as st
import urllib3
import streamlit as st

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ------------------------------------------------------------------
# CONFIGURACIÓN FIJA DE LA ZONA/ESTACIÓN
# ------------------------------------------------------------------
# Antes esto era un st.sidebar.text_input() que el usuario podía editar.
# Como ahora SIEMPRE trabajamos con la zona 38, lo convertimos en una
# constante. Así nadie (ni yo por error) puede cambiarla desde la app.
CODIGO_ESTACION = "38"

# Coordenadas por defecto (Institución Universitaria Pascual Bravo)
# Se usan solo si la API no trae la latitud/longitud de la estación.
LAT_DEFECTO = 6.4988
LON_DEFECTO = -74.8315

API_BASE_URL = "https://marco.cornare.gov.co/api/v1/estaciones"
LLAVE_FECHA = "level_date"
LLAVE_VALOR = "level"
CANDIDATOS_LAT = ["lat", "latitude", "latitud"]
CANDIDATOS_LON = ["lng", "lon", "longitude", "longitud"]

# Nombres posibles que la API podría usar para describir la estación.
# Como no sabemos con certeza cuáles usa MARCO, probamos varios —
# si ninguno existe, simplemente no mostramos ese dato (no inventamos nada).
CANDIDATOS_NOMBRE = ["name", "nombre", "station_name"]
CANDIDATOS_CORRIENTE = ["corriente", "stream", "river", "fuente_hidrica"]
CANDIDATOS_MUNICIPIO = ["municipio", "municipality", "city"]

st.set_page_config(page_title="Nivel — Estación 38 (CORNARE)", page_icon="🌊", layout="wide")


# ------------------------------------------------------------------
# Funciones de consulta
# ------------------------------------------------------------------
def obtener_serie_nivel(codigo_estacion, desde, hasta, calidad=1, timeout=30):
    url = f"{API_BASE_URL}/{codigo_estacion}/nivel"
    params = {"desde": desde, "hasta": hasta, "calidad": calidad}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
    }
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=timeout, verify=False)
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"HTTP {resp.status_code}"
    except requests.exceptions.RequestException as e:
        return None, f"Error de red: {e}"


def obtener_metadata_estacion(codigo_estacion, timeout=15):
    """
    Intenta traer datos descriptivos de la estación (nombre, corriente,
    municipio) desde el endpoint base, sin el sufijo /nivel.
    Si la API no responde bien o no trae esos campos, devuelve un
    diccionario vacío — nunca inventamos datos que no vienen de la API.
    """
    url = f"{API_BASE_URL}/{codigo_estacion}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, verify=False)
        if resp.status_code == 200:
            return resp.json()
    except requests.exceptions.RequestException:
        pass
    return {}


def extraer_campo(datos_json, candidatos):
    """Busca la primera llave existente de una lista de candidatos."""
    if not isinstance(datos_json, dict):
        return None
    for llave in candidatos:
        if llave in datos_json and datos_json[llave] not in (None, ""):
            return datos_json[llave]
    return None


def obtener_todas_las_paginas(datos_json, timeout=30):
    registros = list(datos_json.get("values", []))
    siguiente_url = datos_json.get("next")
    while siguiente_url:
        try:
            resp = requests.get(siguiente_url, timeout=timeout, verify=False)
        except requests.exceptions.RequestException:
            break
        if resp.status_code != 200:
            break
        pagina = resp.json()
        registros.extend(pagina.get("values", []))
        siguiente_url = pagina.get("next")
    return registros


def detectar_coordenadas(datos_json):
    """Busca lat/lon en las llaves raíz de la respuesta. Si no las encuentra, usa el valor por defecto."""
    if not isinstance(datos_json, dict):
        return LAT_DEFECTO, LON_DEFECTO, False
    lat = next((datos_json[k] for k in CANDIDATOS_LAT if k in datos_json), None)
    lon = next((datos_json[k] for k in CANDIDATOS_LON if k in datos_json), None)
    if lat is not None and lon is not None:
        try:
            return float(lat), float(lon), True
        except (TypeError, ValueError):
            pass
    return LAT_DEFECTO, LON_DEFECTO, False


def calcular_indice_calidad(df):
    """Índice simple (0-100) combinando completitud de la serie y proporción de outliers."""
    if df.empty or len(df) < 2:
        return 0.0, 0, 0
    df_idx = df.set_index("fecha")
    frecuencia_tipica = df["fecha"].diff().dropna().mode()
    if len(frecuencia_tipica) == 0:
        return 0.0, 0, 0
    frecuencia_tipica = frecuencia_tipica[0]
    rango_completo = pd.date_range(start=df_idx.index.min(), end=df_idx.index.max(), freq=frecuencia_tipica)
    esperados = len(rango_completo)
    huecos = esperados - len(df_idx)
    completitud = max(0.0, 1 - (huecos / esperados)) if esperados > 0 else 0.0
    Q1, Q3 = df["nivel"].quantile(0.25), df["nivel"].quantile(0.75)
    IQR = Q3 - Q1
    lim_inf, lim_sup = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    es_outlier = (df["nivel"] < lim_inf) | (df["nivel"] > lim_sup) | (df["nivel"] < 0)
    proporcion_outliers = es_outlier.mean()
    indice = (completitud * 0.7 + (1 - proporcion_outliers) * 0.3) * 100
    return round(indice, 1), int(huecos), int(es_outlier.sum())


def clasificar_nivel_referencia(nivel_actual, serie):
    """
    Clasificación SIMPLE de referencia (no es la alerta oficial de Cornare,
    que usa umbrales calibrados por hidrólogos para cada estación).
    Compara el nivel actual contra los percentiles de la propia serie
    consultada, solo para dar una idea rápida de qué tan alto está.
    """
    p50 = serie.quantile(0.50)
    p80 = serie.quantile(0.80)
    p95 = serie.quantile(0.95)
    if nivel_actual >= p95:
        return "🔴 Alto (referencial)", "#e63946"
    elif nivel_actual >= p80:
        return "🟠 Atención (referencial)", "#f4a261"
    elif nivel_actual >= p50:
        return "🟡 Normal-alto (referencial)", "#e9c46a"
    else:
        return "🟢 Normal (referencial)", "#2a9d8f"


def diagrama_niveles_alerta():
    """
    Diagrama de referencia hecho con HTML/CSS simple (no depende de
    ninguna imagen externa, así que nunca se rompe ni se cae).
    Sirve solo como guía visual de qué significa cada color, NO como
    los umbrales oficiales de Cornare para la estación 38.
    """
    html = """
    <div style="display:flex; gap:6px; text-align:center; font-size:13px;">
      <div style="flex:1; background:#2a9d8f; color:white; padding:10px; border-radius:6px;">🟢 Normal</div>
      <div style="flex:1; background:#e9c46a; color:#3a3a3a; padding:10px; border-radius:6px;">🟡 Normal-alto</div>
      <div style="flex:1; background:#f4a261; color:#3a3a3a; padding:10px; border-radius:6px;">🟠 Atención</div>
      <div style="flex:1; background:#e63946; color:white; padding:10px; border-radius:6px;">🔴 Alto</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ------------------------------------------------------------------
# Sidebar — parámetros de la consulta
# ------------------------------------------------------------------
st.sidebar.header("Parámetros de tu consulta")
nombre_estudiante = st.sidebar.text_input("Nombre del estudiante", "Tu Nombre Aquí")

# Ya no hay input de código de estación: la mostramos fija, solo como info.
st.sidebar.markdown(f"**Estación fija:** `Zona {CODIGO_ESTACION}`")

fecha_desde = st.sidebar.date_input("Desde", pd.to_datetime("2026-08-23")).strftime("%Y-%m-%d")
fecha_hasta = st.sidebar.date_input("Hasta", pd.to_datetime("2026-08-30")).strftime("%Y-%m-%d")
calidad = st.sidebar.selectbox("Calidad", [1, 0], index=0, help="1 = solo datos validados")

st.sidebar.markdown("---")
st.sidebar.subheader("📷 Foto de referencia (opcional)")
st.sidebar.caption("Si tienes una foto real de la estación 38, súbela aquí para tenerla como referencia visual.")
st.image("rio_nus.png", caption="Estacion")
consultar = st.sidebar.button("🔍 Consultar", type="primary")

st.title("🌊 Nivel de río/quebrada — Estación 38 (CORNARE)")
st.caption(f"Estudiante: **{nombre_estudiante}** · Zona/estación: **{CODIGO_ESTACION}** (fija)")

# --- Metadata de la estación (nombre, corriente, municipio) ---
metadata = obtener_metadata_estacion(CODIGO_ESTACION)
nombre_est = extraer_campo(metadata, CANDIDATOS_NOMBRE)
corriente = extraer_campo(metadata, CANDIDATOS_CORRIENTE)
municipio = extraer_campo(metadata, CANDIDATOS_MUNICIPIO)

if nombre_est or corriente or municipio:
    partes = []
    if nombre_est:
        partes.append(f"**Nombre:** {nombre_est}")
    if corriente:
        partes.append(f"**Corriente:** {corriente}")
    if municipio:
        partes.append(f"**Municipio:** {municipio}")
    st.info(" · ".join(partes))
else:
    st.caption(
        "La API no trajo nombre/corriente/municipio para esta estación en el endpoint base. "
        "Si conoces el nombre real de esos campos, ajusta `CANDIDATOS_NOMBRE`, "
        "`CANDIDATOS_CORRIENTE` y `CANDIDATOS_MUNICIPIO` al inicio del archivo."
    )


    st.image(rio_nus.png, caption="Foto de referencia — Estación 38", width=350)

# ------------------------------------------------------------------
# Consulta y procesamiento
# ------------------------------------------------------------------
if consultar:
    with st.spinner("Consultando la API..."):
        datos_crudos, error = obtener_serie_nivel(CODIGO_ESTACION, fecha_desde, fecha_hasta, calidad)

    if error:
        st.error(f"❌ {error}")
    else:
        registros = obtener_todas_las_paginas(datos_crudos)
        if not registros:
            st.warning("No hay registros para la estación 38 en este rango de fechas. Prueba otro rango.")
        else:
            df = pd.DataFrame(registros)
            df = df.rename(columns={LLAVE_FECHA: "fecha", LLAVE_VALOR: "nivel"})
            df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
            df["nivel"] = pd.to_numeric(df["nivel"], errors="coerce")
            df = df.dropna(subset=["fecha", "nivel"]).sort_values("fecha").reset_index(drop=True)

            lat, lon, coords_reales = detectar_coordenadas(datos_crudos)
            indice_calidad, huecos, n_outliers = calcular_indice_calidad(df)

            nivel_actual = df["nivel"].iloc[-1]
            fecha_actual = df["fecha"].iloc[-1]
            etiqueta_alerta, color_alerta = clasificar_nivel_referencia(nivel_actual, df["nivel"])

            # --- Métricas principales (ahora con más info relevante) ---
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.metric("Lecturas", len(df))
            col2.metric("Nivel promedio", f"{df['nivel'].mean():.2f}")
            col3.metric("Nivel máximo", f"{df['nivel'].max():.2f}")
            col4.metric("Nivel mínimo", f"{df['nivel'].min():.2f}")
            col5.metric("Última lectura", f"{nivel_actual:.2f}", help=str(fecha_actual))
            col6.metric("Índice de calidad", f"{indice_calidad} / 100")

            st.markdown(
                f"**Clasificación de referencia del último dato:** "
                f"<span style='color:{color_alerta}; font-weight:bold;'>{etiqueta_alerta}</span>",
                unsafe_allow_html=True,
            )
            st.caption(
                "⚠️ Esta clasificación es solo una referencia calculada con los percentiles de "
                "esta misma consulta. No reemplaza los umbrales oficiales de alerta de Cornare."
            )

            # --- Diagrama de referencia de niveles ---
            st.subheader("Guía de referencia — niveles de alerta")
            diagrama_niveles_alerta()

            # --- Gráfico de la serie ---
            st.subheader("Serie de nivel")
            st.line_chart(df.set_index("fecha")["nivel"])

            # --- Mapa de la estación ---
            st.subheader("Ubicación de la estación")
            if not coords_reales:
                st.caption(
                    "La API no trajo latitud/longitud de la estación — se muestra el punto de partida "
                    "(Pascual Bravo). Ajusta `CANDIDATOS_LAT` / `CANDIDATOS_LON` si conoces el nombre "
                    "real de esas llaves."
                )
            st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}), zoom=10)

            # --- Detalle de calidad ---
            with st.expander("Detalle del índice de calidad"):
                st.write(f"- Huecos de reporte detectados: **{huecos}**")
                st.write(f"- Outliers (IQR + nivel negativo): **{n_outliers}** de {len(df)} lecturas")
                st.write("El índice combina completitud de la serie (70%) y proporción de datos sin outliers (30%).")

            # --- Tabla y descarga ---
            with st.expander("Ver datos crudos"):
                st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Descargar CSV",
                csv,
                file_name=f"nivel_estacion_{CODIGO_ESTACION}.csv",
                mime="text/csv",
            )
else:
    st.info("Ajusta las fechas en el sidebar y presiona **Consultar**. La estación ya está fija en 38.")
