import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Detector de Anomalías — Módulo 4",
    layout="wide"
)

st.title("🚨 Detector de Anomalías: Lógica + Big-O + NumPy")
st.caption(
    "Módulo 4 — Matemáticas Discretas y Complejidad. "
    "La misma decisión lógica, evaluada de forma ingenua vs. vectorizada."
)

tab1, tab2, tab3 = st.tabs(
    ["🔎 Simulación de alarma", "📈 Notación Big-O", "⚡ Benchmark en vivo"]
)


# ---------------------------------------------------------------------------
# Utilidades compartidas
# ---------------------------------------------------------------------------

def generar_datos(n, seed=42):
    """
    Genera n lecturas de temperatura, humedad y
    si la lectura corresponde a un fin de semana.
    """
    rng = np.random.default_rng(seed)

    temperaturas = rng.uniform(15, 40, n)
    humedades = rng.uniform(20, 80, n)

    # False = día entre semana
    # True  = fin de semana
    es_fin_de_semana = rng.integers(0, 2, n).astype(bool)

    return temperaturas, humedades, es_fin_de_semana


# ---------------------------------------------------------------------------
# Versión LOOP
# ---------------------------------------------------------------------------

def alarma_logica_loop(
    temperaturas,
    humedades,
    es_fin_de_semana,
    temp_umbral,
    hum_umbral
):
    """
    Evalúa la condición usando un loop de Python.

    Alarma:
        temperatura > umbral
        Y humedad < umbral
        Y NO es_fin_de_semana
    """

    resultados = []

    for temp, hum, fin_de_semana in zip(
        temperaturas,
        humedades,
        es_fin_de_semana
    ):
        alarma = (
            temp > temp_umbral
            and hum < hum_umbral
            and not fin_de_semana
        )

        resultados.append(alarma)

    return np.array(resultados)


# ---------------------------------------------------------------------------
# Versión VECTORIZADA CON NUMPY
# ---------------------------------------------------------------------------

def alarma_logica_vectorizada(
    temperaturas,
    humedades,
    es_fin_de_semana,
    temp_umbral,
    hum_umbral
):
    """
    Evalúa la misma condición usando operaciones vectorizadas de NumPy.

    Alarma:
        temperatura > umbral
        Y humedad < umbral
        Y NO es_fin_de_semana
    """

    return (
        (temperaturas > temp_umbral)
        & (humedades < hum_umbral)
        & (~es_fin_de_semana)
    )


# ---------------------------------------------------------------------------
# Tab 1: Simulación de alarma
# ---------------------------------------------------------------------------

with tab1:

    st.subheader("Alarma por regla lógica")

    st.write(
        "La alarma se activa cuando se cumplen las tres condiciones:"
    )

    st.markdown(
        """
        **temperatura > umbral**
        
        **Y humedad < umbral**
        
        **Y NOT es_fin_de_semana**
        """
    )

    col_cfg, col_data = st.columns([1, 2])

    # -----------------------------------------------------------------------
    # Configuración
    # -----------------------------------------------------------------------

    with col_cfg:

        n = st.slider(
            "Número de lecturas (n)",
            50,
            5000,
            500,
            step=50
        )

        temp_umbral = st.slider(
            "Umbral temperatura (°C) — mayor que",
            15,
            40,
            30
        )

        hum_umbral = st.slider(
            "Umbral humedad (%) — menor que",
            20,
            80,
            40
        )

    # -----------------------------------------------------------------------
    # Generar datos
    # -----------------------------------------------------------------------

    temps, hums, fines = generar_datos(n)

    # -----------------------------------------------------------------------
    # Calcular alarmas usando NumPy
    # -----------------------------------------------------------------------

    alarmas = alarma_logica_vectorizada(
        temps,
        hums,
        fines,
        temp_umbral,
        hum_umbral
    )

    with col_cfg:

        st.metric(
            "Alarmas detectadas",
            f"{alarmas.sum()} / {n}"
        )

        st.info(
            "La alarma solo se activa si la temperatura es mayor al "
            "umbral, la humedad es menor al umbral y NO es fin de semana."
        )

    # -----------------------------------------------------------------------
    # Gráfica
    # -----------------------------------------------------------------------

    with col_data:

        fig, ax = plt.subplots(figsize=(6, 4.5))

        ax.scatter(
            temps[~alarmas],
            hums[~alarmas],
            c="steelblue",
            alpha=0.5,
            label="Normal",
            s=15,
        )

        ax.scatter(
            temps[alarmas],
            hums[alarmas],
            c="crimson",
            alpha=0.8,
            label="Alarma / anomalía",
            s=25,
        )

        ax.set_xlabel("Temperatura (°C)")
        ax.set_ylabel("Humedad (%)")

        ax.legend()
        ax.grid(alpha=0.3)

        st.pyplot(fig)

    # -----------------------------------------------------------------------
    # Mostrar datos
    # -----------------------------------------------------------------------

    with st.expander("Ver datos y lógica aplicada"):

        df = pd.DataFrame({
            "temperatura": temps.round(2),
            "humedad": hums.round(2),
            "es_fin_de_semana": fines,
            "alarma": alarmas,
        })

        st.dataframe(
            df,
            use_container_width=True,
            height=300
        )


# ---------------------------------------------------------------------------
# Tab 2: Notación Big-O
# ---------------------------------------------------------------------------

with tab2:

    st.subheader("¿Por qué importa la complejidad?")

    st.write(
        "El detector recorre las n lecturas una sola vez. "
        "Aunque ahora agregamos una tercera condición lógica, "
        "la complejidad sigue siendo O(n)."
    )

    st.markdown(
        """
        ### Condición original

        ```text
        temperatura > 30
        Y
        humedad < 40
        ```

        ### Nueva condición

        ```text
        temperatura > 30
        Y
        humedad < 40
        Y
        NOT(es_fin_de_semana)
        ```

        Agregar una condición aumenta la cantidad de operaciones por
        lectura, pero no cambia la cantidad de lecturas que debemos recorrer.

        Por eso:

        ```text
        O(2n) = O(n)
        O(3n) = O(n)
        ```
        """
    )

    n_max = st.slider(
        "Tamaño máximo de n para la gráfica",
        10,
        200,
        50
    )

    n_valores = np.arange(1, n_max + 1)

    fig2, ax2 = plt.subplots(figsize=(8, 5))

    ax2.plot(
        n_valores,
        np.ones_like(n_valores),
        label="O(1) — constante"
    )

    ax2.plot(
        n_valores,
        n_valores,
        label="O(n) — lineal (nuestro detector)"
    )

    ax2.plot(
        n_valores,
        n_valores * np.log2(
            np.maximum(n_valores, 2)
        ),
        label="O(n log n)"
    )

    ax2.plot(
        n_valores,
        n_valores ** 2,
        label="O(n²) — cuadrática"
    )

    ax2.set_xlabel("Tamaño de los datos (n)")
    ax2.set_ylabel("Operaciones (teórico)")

    ax2.legend()
    ax2.grid(alpha=0.3)

    st.pyplot(fig2)

    st.info(
        "Conclusión: el detector sigue siendo O(n) tanto con loop "
        "como con NumPy. Lo que cambia es la constante de trabajo "
        "por cada elemento."
    )


# ---------------------------------------------------------------------------
# Tab 3: Benchmark en vivo
# ---------------------------------------------------------------------------

with tab3:

    st.subheader(
        "Loop vs. NumPy: misma lógica, distinta velocidad real"
    )

    st.write(
        "Aquí comparamos cuánto tarda Python recorriendo los datos "
        "uno por uno frente a NumPy procesando los arrays de forma "
        "vectorizada."
    )

    # -----------------------------------------------------------------------
    # Tamaño del benchmark
    # -----------------------------------------------------------------------

    n_bench = st.select_slider(
        "Tamaño de datos para el benchmark",
        options=[
            1_000,
            10_000,
            100_000,
            500_000,
            1_000_000
        ],
        value=1_000_000,
    )

    temp_umbral_b = st.slider(
        "Umbral temperatura (°C)",
        15,
        40,
        30,
        key="temp_bench"
    )

    hum_umbral_b = st.slider(
        "Umbral humedad (%)",
        20,
        80,
        40,
        key="hum_bench"
    )

    # -----------------------------------------------------------------------
    # Ejecutar benchmark
    # -----------------------------------------------------------------------

    if st.button(
        "▶️ Ejecutar benchmark",
        type="primary"
    ):

        # Generar un millón de datos
        temps_b, hums_b, fines_b = generar_datos(
            n_bench
        )

        # Número de repeticiones
        #
        # El loop es más lento, por lo que normalmente basta
        # con una ejecución.
        #
        # NumPy es muy rápido, por lo que lo repetimos varias veces
        # para obtener una medición más estable.

        repeticiones_loop = 1
        repeticiones_vec = 20

        # -------------------------------------------------------------------
        # BENCHMARK LOOP
        # -------------------------------------------------------------------

        inicio = time.perf_counter()

        for _ in range(repeticiones_loop):

            alarma_logica_loop(
                temps_b,
                hums_b,
                fines_b,
                temp_umbral_b,
                hum_umbral_b
            )

        t_loop = (
            time.perf_counter() - inicio
        ) / repeticiones_loop

        # -------------------------------------------------------------------
        # BENCHMARK NUMPY
        # -------------------------------------------------------------------

        inicio = time.perf_counter()

        for _ in range(repeticiones_vec):

            alarma_logica_vectorizada(
                temps_b,
                hums_b,
                fines_b,
                temp_umbral_b,
                hum_umbral_b
            )

        t_vec = (
            time.perf_counter() - inicio
        ) / repeticiones_vec

        # -------------------------------------------------------------------
        # Resultados
        # -------------------------------------------------------------------

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Tiempo con loop",
            f"{t_loop * 1000:.3f} ms"
        )

        col2.metric(
            "Tiempo con NumPy",
            f"{t_vec * 1000:.3f} ms"
        )

        if t_vec > 0:

            speedup = t_loop / t_vec

            col3.metric(
                "NumPy es más rápido por",
                f"{speedup:,.0f}x"
            )

        else:

            col3.metric(
                "NumPy es más rápido por",
                "Demasiado rápido para medir"
            )

        # -------------------------------------------------------------------
        # Cantidad de alarmas
        # -------------------------------------------------------------------

        alarmas_b = alarma_logica_vectorizada(
            temps_b,
            hums_b,
            fines_b,
            temp_umbral_b,
            hum_umbral_b
        )

        st.metric(
            "Alarmas detectadas",
            f"{alarmas_b.sum():,} / {n_bench:,}"
        )

        # -------------------------------------------------------------------
        # Explicación
        # -------------------------------------------------------------------

        st.markdown(
            """
            ### Resultado del experimento

            Tanto el loop como NumPy tienen complejidad:

            **O(n)**

            La diferencia está en la implementación.

            - El **loop** procesa cada elemento desde Python.
            - **NumPy** realiza las operaciones sobre arrays de forma
              vectorizada.
            - Por eso NumPy normalmente obtiene un tiempo mucho menor,
              incluso teniendo la misma complejidad Big-O.
            """
        )

        # -------------------------------------------------------------------
        # Gráfica de tiempos
        # -------------------------------------------------------------------

        fig3, ax3 = plt.subplots(
            figsize=(6, 4)
        )

        ax3.bar(
            ["Loop (Python)", "NumPy (vectorizado)"],
            [
                t_loop * 1000,
                t_vec * 1000
            ],
            color=[
                "indianred",
                "seagreen"
            ]
        )

        ax3.set_ylabel(
            "Tiempo (milisegundos)"
        )

        ax3.set_title(
            f"Benchmark con n = {n_bench:,}"
        )

        ax3.grid(
            alpha=0.3,
            axis="y"
        )

        st.pyplot(fig3)

        # -------------------------------------------------------------------
        # Información de medición
        # -------------------------------------------------------------------

        st.caption(
            f"Loop: {repeticiones_loop} corrida(s). "
            f"NumPy: {repeticiones_vec} corridas. "
            "El tiempo mostrado para NumPy es el promedio."
        )

    else:

        st.caption(
            "Selecciona el tamaño de los datos y presiona "
            "**Ejecutar benchmark** para comparar los tiempos."
        )
