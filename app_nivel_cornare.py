"""
App Streamlit — Nivel de río/quebrada, Estación 38 (CORNARE / MARCO)
----------------------------------------------------------------------
Versión personalizada: trabaja SIEMPRE con la estación 38 (Río Nus).
Muestra información extra de la estación y un diagrama simple de
niveles de alerta como referencia visual.

Para correrla:
    streamlit run app_nivel_cornare_estacion38.py

IMPORTANTE: el archivo "rio_nus.png" debe estar en la MISMA carpeta
que este script, si no, la imagen no va a cargar.
"""
import requests
import pandas as pd
import numpy as np
import streamlit as st
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ------------------------------------------------------------------
# CONFIGURACIÓN FIJA DE LA ZONA/ESTACIÓN
# ------------------------------------------------------------------
CODIGO_ESTACION = "38"

# Coordenadas Río Nus (estación 38)
LAT_DEFECTO = 6.4988
LON_DEFECTO = -74.8315

# Foto fija de referencia de la estación 38. Debe existir en la misma
# carpeta que este script. Si no la tienes, deja RUTA_FOTO = None y
# la app mostrará un aviso en vez de romperse.
RUTA_FOTO = "rio_nus.png"

API_BASE_URL = "https://marco.cornare.gov.co/api/v1/estaciones"
LLAVE_FECHA = "level_date"
LLAVE_VALOR = "level"
CANDIDATOS_LAT = ["lat", "latitude", "latitud"]
CANDIDATOS_LON = ["lng", "lon", "longitude", "longitud"]

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


def calcular_tendencia(df, ventana=5):
    """
    Compara el promedio de las últimas 'ventana' lecturas contra el
    promedio de las 'ventana' lecturas justo anteriores a esas.
    Es como comparar "cómo iba en los últimos minutos" contra "cómo
    iba un rato antes" para saber si el río está subiendo, bajando o
    quieto. Si no hay suficientes datos para comparar, avisa en vez
    de inventar una tendencia.
    """
    if len(df) < ventana * 2:
        return "➖ Datos insuficientes para calcular tendencia", None

    ultimas = df["nivel"].iloc[-ventana:].mean()
    anteriores = df["nivel"].iloc[-ventana * 2:-ventana].mean()
    diferencia = ultimas - anteriores

    # Umbral pequeño para no marcar "subiendo/bajando" por ruido mínimo
    # del sensor. Se basa en la variabilidad típica de la propia serie.
    umbral = df["nivel"].std() * 0.15 if df["nivel"].std() > 0 else 0.01

    if diferencia > umbral:
        return "📈 Subiendo", diferencia
    elif diferencia < -umbral:
        return "📉 Bajando", diferencia
    else:
        return "➡️ Estable", diferencia


def calcular_velocidad_cambio(df):
    """
    Toma las dos últimas lecturas y calcula cuánto cambió el nivel
    por hora entre ellas. Es como el velocímetro de un carro, pero
    para el río: no importa qué tan alto está, importa qué tan rápido
    se está moviendo.
    """
    if len(df) < 2:
        return None
    ultimo = df.iloc[-1]
    penultimo = df.iloc[-2]
    delta_nivel = ultimo["nivel"] - penultimo["nivel"]
    delta_horas = (ultimo["fecha"] - penultimo["fecha"]).total_seconds() / 3600
    if delta_horas <= 0:
        return None
    return delta_nivel / delta_horas


def calcular_frescura(fecha_ultima_lectura):
    """
    Calcula hace cuánto tiempo llegó el último dato, comparándolo con
    la hora actual. Si el último dato es muy viejo, probablemente el
    sensor dejó de reportar (por ejemplo, después del robo de una
    estación, como pasó con la de Viboral en 2023).
    
    """
    # La fecha que llega de la API puede tener zona horaria (ej. "-05:00")
    # o no tenerla, según cómo la haya parseado pandas. Si tiene zona
    # horaria, generamos "ahora" con esa MISMA zona horaria; si no,
    # generamos "ahora" sin zona horaria. Así siempre son comparables.
    if fecha_ultima_lectura.tzinfo is not None:
        ahora = pd.Timestamp.now(tz=fecha_ultima_lectura.tzinfo)
    else:
        ahora = pd.Timestamp.now()

    diferencia = ahora - fecha_ultima_lectura
    minutos = diferencia.total_seconds() / 60

    if minutos < 0:
        return "Dato con fecha futura (revisar reloj/zona horaria)", "⚠️", "#f4a261"
    elif minutos < 30:
        return f"hace {int(minutos)} min", "🟢", "#2a9d8f"
    elif minutos < 180:
        horas = minutos / 60
        return f"hace {horas:.1f} h", "🟡", "#e9c46a"
    elif minutos < 1440:
        horas = minutos / 60
        return f"hace {horas:.1f} h", "🟠", "#f4a261"
    else:
        dias = minutos / 1440
        return f"hace {dias:.1f} días", "🔴", "#e63946"


def diagrama_niveles_alerta():
    """
    Diagrama de referencia hecho con HTML/CSS simple (no depende de
    ninguna imagen externa, así que nunca se rompe ni se cae).
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
st.sidebar.markdown(f"**Estación fija:** `Zona {CODIGO_ESTACION}` · Río Nus")

fecha_desde = st.sidebar.date_input("Desde", pd.to_datetime("2026-08-23")).strftime("%Y-%m-%d")
fecha_hasta = st.sidebar.date_input("Hasta", pd.to_datetime("2026-08-30")).strftime("%Y-%m-%d")
calidad = st.sidebar.selectbox("Calidad", [1, 0], index=0, help="1 = solo datos validados")

consultar = st.sidebar.button("🔍 Consultar", type="primary")

# ------------------------------------------------------------------
# Encabezado: imagen a la izquierda, título/subtítulo/info a la derecha
# ------------------------------------------------------------------
col_imagen, col_texto = st.columns([1, 2])

with col_imagen:
    # Nota los try/except: si el archivo no existe, no se cae la app,
    # solo muestra un aviso.
    try:
        if RUTA_FOTO:
            st.image(RUTA_FOTO, caption="Estación 38 — Río Nus", use_container_width=True)
        else:
            st.info("📷 No hay foto configurada (RUTA_FOTO = None).")
    except Exception:
        st.warning(f"No pude cargar la imagen '{RUTA_FOTO}'. Verifica que el archivo esté en esta carpeta.")

with col_texto:
    st.title("🌊 Nivel de río/quebrada — Estación 38 (CORNARE)")
    st.caption(f"Estudiante: **{nombre_estudiante}** · Zona/estación: **{CODIGO_ESTACION}** (fija) · Río Nus")

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
            partes.append(f"**Municipio (código):** {municipio}")
        st.info(" · ".join(partes))
    else:
        st.caption(
            "La API no trajo nombre/corriente/municipio para esta estación en el endpoint base. "
            "Si conoces el nombre real de esos campos, ajusta `CANDIDATOS_NOMBRE`, "
            "`CANDIDATOS_CORRIENTE` y `CANDIDATOS_MUNICIPIO` al inicio del archivo."
        )

    st.markdown("Ajusta las fechas en el sidebar y presiona **Consultar**. La estación ya está fija en 38.")

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
            

            # --- Tendencia, velocidad de cambio y frescura del dato ---
            tendencia_texto, diferencia_tendencia = calcular_tendencia(df)
            velocidad = calcular_velocidad_cambio(df)
            frescura_texto, frescura_icono, frescura_color = calcular_frescura(fecha_actual)

            st.subheader("Tendencia y estado del último dato")
            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.metric(
                    "Tendencia (últimas 5 vs 5 anteriores)",
                    tendencia_texto,
                    delta=f"{diferencia_tendencia:.2f}" if diferencia_tendencia is not None else None,
                )

            with col_b:
                if velocidad is not None:
                    st.metric("Velocidad de cambio", f"{velocidad:+.2f} / hora")
                else:
                    st.metric("Velocidad de cambio", "N/D")

            with col_c:
                st.markdown(
                    f"**Última lectura reportada:**<br>"
                    f"<span style='color:{frescura_color}; font-weight:bold; font-size:18px;'>"
                    f"{frescura_icono} {frescura_texto}</span>",
                    unsafe_allow_html=True,
                )

            st.caption(
                "La tendencia compara el promedio de las últimas 5 lecturas contra las 5 anteriores. "
                "La velocidad de cambio es la diferencia entre las dos últimas lecturas, expresada por hora. "
                "La frescura te dice hace cuánto llegó el dato más reciente — si es de hace mucho, "
                "el sensor puede estar fallando o desconectado."
            )

            st.subheader("Guía de referencia — niveles de alerta")
            diagrama_niveles_alerta()

            st.subheader("Serie de nivel")
            st.line_chart(df.set_index("fecha")["nivel"])

            st.subheader("Ubicación de la estación")
            if not coords_reales:
                st.caption(
                    "La API no trajo latitud/longitud de la estación — se muestra la ubicación de "
                    "referencia del Río Nus. Ajusta `CANDIDATOS_LAT` / `CANDIDATOS_LON` si conoces el "
                    "nombre real de esas llaves."
                )
            st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}), zoom=10)

            with st.expander("Detalle del índice de calidad"):
                st.write(f"- Huecos de reporte detectados: **{huecos}**")
                st.write(f"- Outliers (IQR + nivel negativo): **{n_outliers}** de {len(df)} lecturas")
                st.write("El índice combina completitud de la serie (70%) y proporción de datos sin outliers (30%).")

            with st.expander("Ver datos crudos"):
                st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Descargar CSV",
                csv,
                file_name=f"nivel_estacion_{CODIGO_ESTACION}.csv",
                mime="text/csv",
            )
