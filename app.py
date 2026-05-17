import streamlit as st
import numpy as np
import pint
import pandas as pd 

# =========================================
# IMPORTACIONES DE TUS MÓDULOS
# =========================================
from Modulos import (
    calcular_sn,
    espesores_minimos,
    in_a_cm_constructivo,
    coeficiente_drenaje_rango,
    Calcular_D, 
    coeficiente_drenaje_rango_D, 
    obtener_serviciabilidad_final_D
)

# Inicializar registro de unidades
ureg = pint.UnitRegistry()

# =========================================
# CONFIGURACIÓN VISUAL Y ESTILOS (CSS)
# =========================================
st.set_page_config(
    page_title="Dashboard de Diseño de Pavimentos - AASHTO",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #f4f7fe; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    
    /* Menú lateral */
    [data-testid="stSidebar"] { background-color: #171721; }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    
    /* Títulos y texto general */
    h1, h2, h3, p, li { color: #2b3674 !important; font-weight: 700 !important; }
    
    /* Forzar color oscuro en las fórmulas matemáticas (KaTeX) */
    .katex * { color: #2b3674 !important; font-weight: bold !important; }
    
    /* Tarjetas de métricas */
    .stMetric {
        background-color: #ffffff; padding: 20px 25px;
        border-radius: 20px; box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.05);
        border: none; margin-bottom: 10px;
    }
    [data-testid="stMetricValue"] { color: #2b3674 !important; font-size: 28px !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #a3aed1 !important; font-size: 14px !important; font-weight: 500 !important; text-transform: uppercase; }
    hr { border-color: #e2e8f0 !important; margin-top: 2rem; margin-bottom: 2rem; }
    
    /* =========================================
       ESTILOS DEFINITIVOS PARA TABLAS
       ========================================= */
    div[data-testid="stTable"] { margin-bottom: 2rem; }
    
    /* Forzar color en celdas normales (cuerpo de la tabla) */
    [data-testid="stTable"] td, 
    [data-testid="stTable"] td * {
        background-color: #ffffff !important;
        color: #171721 !important; 
    }
    
    /* Forzar color en encabezados de la tabla */
    [data-testid="stTable"] th, 
    [data-testid="stTable"] th * {
        background-color: #2b3674 !important;
        color: #ffffff !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Dashboard Integrado de Pavimentos (AASHTO 1993)")

# =========================================
# SIDEBAR - SELECCIÓN PRINCIPAL
# =========================================
st.sidebar.header("Configuración Principal")
tipo_pavimento = st.sidebar.radio(
    "Seleccione el método de diseño:",
    ("Pavimento Flexible", "Pavimento Rígido")
)

st.sidebar.divider()

# =========================================
# LÓGICA: PAVIMENTO FLEXIBLE
# =========================================
if tipo_pavimento == "Pavimento Flexible":
    st.sidebar.subheader("Tránsito y Confiabilidad")
    W_18 = st.sidebar.number_input("W18 (ESAL)", value=1.8e6, format="%.2e")
    confiabilidad = st.sidebar.number_input("Confiabilidad (Zr)", value=-1.282)
    error_estandar = st.sidebar.number_input("Error Estándar (S0)", value=0.45)
    
    st.sidebar.subheader("Serviciabilidad")
    Po = st.sidebar.number_input("Po", value=4.2)
    Pf = st.sidebar.number_input("Pf", value=2.2)
    dpsi = Po - Pf

    st.sidebar.subheader("Módulos resilientes")
    Mr_subrasante = st.sidebar.number_input("MR Subrasante (psi)", value=12000)
    Mr_subbase = st.sidebar.number_input("MR Subbase (psi)", value=15000)
    Mr_base = st.sidebar.number_input("MR Base (psi)", value=27000)
    MR_asfalto = st.sidebar.number_input("MR Asfalto (psi)", value=3.83e5)

    st.sidebar.subheader("Drenaje")
    calidad = st.sidebar.selectbox("Calidad de drenaje", ["excellent", "good", "fair", "poor", "very_poor"])
    porcentaje = st.sidebar.number_input("Saturación (%)", value=15.0)
    usar_manual = st.sidebar.checkbox("Definir m2 y m3 manualmente")

    # Cálculos Drenaje Flexible
    rango, categoria = coeficiente_drenaje_rango(calidad, porcentaje)
    if usar_manual:
        m2 = st.sidebar.number_input("m2", value=0.9)
        m3 = st.sidebar.number_input("m3", value=0.9)
    else:
        m2 = (rango[0] + rango[1]) / 2
        m3 = m2

    # Cálculos Estructurales Flexible
    SN3 = calcular_sn(W_18, confiabilidad, error_estandar, dpsi, Mr_subrasante)
    SN2 = calcular_sn(W_18, confiabilidad, error_estandar, dpsi, Mr_subbase)
    SN1 = calcular_sn(W_18, confiabilidad, error_estandar, dpsi, Mr_base)

    a1 = 0.184 * np.log(MR_asfalto) - 1.9547
    a2 = 0.249 * np.log10(Mr_base) - 0.977
    a3 = 0.227 * np.log10(Mr_subbase) - 0.839

    h1_min, h2_min = espesores_minimos(W_18)
    h1_min_cm = in_a_cm_constructivo(h1_min)
    h2_min_cm = in_a_cm_constructivo(h2_min)

    h1 = SN1 / a1
    if h1 < h1_min: h1 = h1_min
    else: h1 = h1_min_cm * (2.54**-1); SN1 = h1 * a1
    h1 = h1 * 2.54

    h2 = (SN2 - SN1) / (a2 * m2)
    if h2 < 6.0: h2 = 6.0
    else: h2 = h2_min_cm * (2.54**-1); SN2 = h2 * a2 * m2 + SN1
    h2 = h2 * 2.54

    h3 = (SN3 - SN2) / (a3 * m3)
    h3 = (h3 * 2.54 + 1).round(0)

    # Mostrar Resultados Flexible
    st.subheader("Análisis de Drenaje")
    col1, col2, col3 = st.columns(3)
    col1.metric("Categoría", categoria)
    col2.metric("Rango", f"{rango}")
    col3.metric("Coeficiente usado", f"{m2:.3f}")
    
    st.divider()

    st.subheader("Resultados Estructurales (SN)")
    col1, col2, col3 = st.columns(3)
    col1.metric("SN Subrasante", f"{SN3:.2f}")
    col2.metric("SN Subbase", f"{SN2:.2f}")
    col3.metric("SN Base", f"{SN1:.2f}")

    st.subheader("Diseño Final de Espesores (Flexible)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Carpeta Asfáltica", f"{h1:.2f} cm")
    col2.metric("Base Granular", f"{h2:.2f} cm")
    col3.metric("Subbase Granular", f"{h3:.2f} cm")

    st.divider()
    
    # =========================================
    # SECCIÓN DE TABLAS DE REFERENCIA (FLEXIBLE)
    # =========================================
    st.header("Tablas de Referencia AASHTO 1993 - Flexible")
    
    with st.expander("Ver Tablas Guía de Diseño (Desplegar)"):
        st.write("### Tabla 1. Periodo de análisis (años)")
        df_periodo = pd.DataFrame({
            "Condición de la vía": ["Vía urbana de alto volumen", "Vía rural de alto volumen", "Vía pavimentada de bajo volumen", "Vía no pavimentada de bajo volumen"],
            "Periodo de análisis (Años)": ["30-50", "20-50", "15-25", "10-20"]
        })
        st.table(df_periodo)

        st.write("### Tabla 2. Factor de distribución por carril (FDC)")
        df_fdc = pd.DataFrame({
            "Número de carriles": ["1", "2", "3", "4"],
            "Porcentaje de ejes de 18k a diseño": ["100", "80-100", "60-80", "50-75"]
        })
        st.table(df_fdc)

        st.write("### Tabla 3. Nivel de Confiabilidad R (%) recomendado")
        df_confiabilidad = pd.DataFrame({
            "Clasificación funcional": ["Autopista", "Arteria principal", "Colectora", "Local"],
            "Urbano": ["85-99.9", "80-99", "80-95", "50-80"],
            "Rural": ["80-99.9", "75-95", "75-95", "50-80"]
        })
        st.table(df_confiabilidad)

        st.write("### Tabla 4. Error estándar combinado (So) recomendado")
        df_error = pd.DataFrame({
            "Condición": ["Construcción nueva", "Sobrecapa (Rehabilitación)"],
            "Flexible": ["0.45", "0.50"],
            "Rígido": ["0.35", "0.40"]
        })
        st.table(df_error)
        
        st.write("### Serviciabilidad Final (Pf) recomendada")
        df_serviciabilidad = pd.DataFrame({
            "Tipo de Vía": ["Autopista", "Carretera", "Zonas industriales", "Pavimento urbano principal", "Pavimento urbano secundario"],
            "Serviciabilidad (Pf)": ["2.5 a 3.0", "2.0 a 2.5", "2.0 a 2.5", "2.0 a 2.5", "1.5 a 2.0"]
        })
        st.table(df_serviciabilidad)
        
        st.write("### Desviación Estándar Normal (Zr)")
        df_zr = pd.DataFrame({
            "Reliability (%)": ["50", "60", "70", "75", "80", "85", "90", "95", "99", "99.9", "99.99"],
            "Standard Normal Deviate (Zr)": ["0.000", "-0.253", "-0.524", "-0.674", "-0.841", "-1.037", "-1.282", "-1.645", "-2.327", "-3.090", "-3.750"]
        })
        st.table(df_zr)

        st.write("### Coeficiente de drenaje mi para pavimentos flexibles")
        df_drenaje_mi = pd.DataFrame({
            "Calidad del Drenaje": ["Excellent (Excelente)", "Good (Bueno)", "Fair (Regular)", "Poor (Pobre)", "Very Poor (Muy Malo)"],
            "Agua removida en": ["2 horas", "1 día", "1 semana", "1 mes", "Nunca drena"],
            "< 1%": ["1.40 – 1.35", "1.35 – 1.25", "1.25 – 1.15", "1.15 – 1.05", "1.05 – 0.95"],
            "1 – 5%": ["1.35 – 1.30", "1.25 – 1.15", "1.15 – 1.05", "1.05 – 0.80", "0.95 – 0.75"],
            "5 – 25%": ["1.30 – 1.20", "1.15 – 1.00", "1.00 – 0.80", "0.80 – 0.60", "0.75 – 0.40"],
            "> 25%": ["1.20", "1.00", "0.80", "0.60", "0.40"]
        })
        st.table(df_drenaje_mi)


# =========================================
# LÓGICA: PAVIMENTO RÍGIDO
# =========================================
else:
    st.sidebar.subheader("Tránsito y Confiabilidad")
    W_18 = st.sidebar.number_input("W18 (ESAL)", value=6.0e6, format="%.2e")
    Zr = st.sidebar.number_input("Confiabilidad (Zr)", value=-1.282)
    S0 = st.sidebar.number_input("Error Estándar (S0)", value=0.35)

    st.sidebar.subheader("Serviciabilidad y Vía")
    Tipo_de_via = st.sidebar.selectbox("Tipo de Vía", ["Autopista", "Colectoras", "Calles comerciales", "Calles residenciales"])
    Po = st.sidebar.number_input("Serviciabilidad inicial (Po)", value=4.2)
    
    st.sidebar.subheader("Propiedades del Concreto")
    Modulo_rotura_concreto_MPa = st.sidebar.number_input("Módulo de rotura (MPa)", value=4.2)
    Ec_psi = st.sidebar.number_input("Módulo elasticidad Ec (psi)", value=3.6e6, format="%.2e")
    J = st.sidebar.number_input("Coef. Transf. Carga (J)", value=2.7)

    st.sidebar.subheader("Subrasante y Drenaje")
    Modulo_de_reccion_combinado = st.sidebar.number_input("Módulo Reacción k (pci)", value=147)
    Calidad_drenaje = st.sidebar.selectbox("Calidad de drenaje ", ["Excelente", "Bueno", "Regular", "Pobre", "Muy malo"], index=2)
    Dias_que_lleve_al_ano = st.sidebar.number_input("Días de lluvia al año", value=200)
    cd = st.sidebar.number_input("Coeficiente de drenaje (Cd) a usar", value=0.9)

    # Procesamiento y Conversiones Rígido
    Modulo_rotura_concreto = (Modulo_rotura_concreto_MPa * ureg.megapascal).to(ureg.psi)
    Ec = (Ec_psi * ureg.psi).to(ureg.psi).magnitude 

    Pf = obtener_serviciabilidad_final_D(Tipo_de_via)
    delta_psi = Po - Pf
    Porcentaje_saturacion = (Dias_que_lleve_al_ano / 365) * 100
    rango_D, categoria_D = coeficiente_drenaje_rango_D(Calidad_drenaje, Porcentaje_saturacion)

    # Cálculo final
    D = Calcular_D(
        W_18, Zr, S0, delta_psi, Pf, Modulo_rotura_concreto.magnitude, 
        cd, J, Ec, Modulo_de_reccion_combinado
    )

    D_cm = D * 2.54  # Conversión a centímetros

    # Mostrar Resultados Rígido
    st.subheader("Análisis de Variables de Diseño")
    col1, col2, col3 = st.columns(3)
    col1.metric("Serviciabilidad Final (Pf)", f"{Pf}")
    col2.metric("Δ PSI", f"{delta_psi:.2f}")
    col3.metric("Humedad Estimada", f"{categoria_D}")

    st.divider()

    st.subheader("Resultados de Espesor (Losa de Concreto)")
    col1, col2 = st.columns(2)
    col1.metric("Espesor Requerido (D)", f"{D:.2f} pulgadas")
    col2.metric("Espesor Constructivo (D)", f"{D_cm:.2f} cm")

    st.divider()

    # =========================================
    # SECCIÓN DE TABLAS DE REFERENCIA (NUEVAS RÍGIDO)
    # =========================================
    st.header("Tablas de Referencia AASHTO 1993 - Rígido")
    
    with st.expander("Ver Tablas Guía de Diseño Rígido (Desplegar)"):
        
        st.write("### 1. Estimación del Módulo de Reacción (K) mediante CBR y Efecto de la Subbase")
        st.markdown("Fórmulas para estimar empíricamente el valor del módulo de reacción de la subrasante **$K$ (en MPa/m)** basándose en el ensayo CBR del suelo:")
        st.latex(r"K = 2.55 + 52.5 \times \log_{10}(CBR) \quad \text{para } CBR \le 10")
        st.latex(r"K = 46 + 9.08 \times (\log_{10}(CBR))^{4.34} \quad \text{para } CBR > 10")
        
        st.markdown("**Efecto del espesor de la subbase granular sobre el incremento de los valores de K:**")
        df_k_subbase = pd.DataFrame({
            "K subrasante (MPa/m)": ["20", "40", "60", "80"],
            "K subrasante (pci)": ["73", "147", "220", "295"],
            "100 mm (MPa/m)": ["23", "45", "64", "87"],
            "100 mm (pci)": ["85", "165", "235", "320"],
            "150 mm (MPa/m)": ["26", "49", "66", "90"],
            "150 mm (pci)": ["96", "180", "245", "330"],
            "225 mm (MPa/m)": ["32", "57", "76", "100"],
            "225 mm (pci)": ["117", "210", "280", "370"],
            "300 mm (MPa/m)": ["38", "66", "90", "117"],
            "300 mm (pci)": ["140", "245", "330", "430"]
        })
        st.table(df_k_subbase)
        st.info("Nota: Lb/pulg³ equivale a **pci** (pounds per cubic inch). Esta tabla muestra cómo el módulo de reacción combinado (efectivo) del sistema de soporte se eleva al colocar capas granulares de subbase (100 a 300 mm) sobre la subrasante natural.")

        st.write("### 2. Factor de distribución por carril (FDC)")
        df_fdc_rigido = pd.DataFrame({
            "Número de carriles": ["1", "2", "3", "4"],
            "% de ejes equivalentes en el carril de diseño": ["100", "80 – 100", "60 – 80", "50 – 75"]
        })
        st.table(df_fdc_rigido)

        st.write("### 3. Resistencia del concreto – Módulo de rotura (MR)")
        df_mr = pd.DataFrame({
            "Número de camiones por día": ["> 300", "150 – 300", "25 – 150", "< 25"],
            "MR a flexión (MPa)": ["4.5", "4.2", "4.0", "3.8"]
        })
        st.table(df_mr)

        st.write("### 4. Coeficiente de drenaje (Cd)")
        df_cd = pd.DataFrame({
            "Características del drenaje": ["Excelente", "Bueno", "Regular", "Pobre", "Muy malo"],
            "< 1%": ["1.25 – 1.20", "1.20 – 1.15", "1.15 – 1.10", "1.10 – 1.00", "1.00 – 0.90"],
            "1 – 5%": ["1.20 – 1.15", "1.15 – 1.10", "1.10 – 1.00", "1.00 – 0.90", "0.90 – 0.80"],
            "5 – 25%": ["1.15 – 1.10", "1.10 – 1.00", "1.00 – 0.90", "0.90 – 0.80", "0.80 – 0.70"],
            "> 25%": ["1.10", "1.00", "0.90", "0.80", "0.70"]
        })
        st.table(df_cd)

        st.write("### 5. Valores típicos de serviciabilidad final (Pf)")
        df_pf = pd.DataFrame({
            "Tipo de vía": ["Autopista", "Colectoras", "Calles comerciales", "Calles residenciales"],
            "Pf": ["3.0", "2.5", "2.25", "2.0"]
        })
        st.table(df_pf)

        st.write("### 6. Nivel de confiabilidad recomendado")
        df_conf = pd.DataFrame({
            "Clasificación funcional": ["Autopista", "Arteria principal", "Colectora", "Local"],
            "Urbana": ["85 – 99.9", "80 – 99.9", "80 – 95", "50 – 80"],
            "Rural": ["80 – 99.9", "75 – 95", "75 – 95", "50 – 80"]
        })
        st.table(df_conf)

        st.write("### 7. Error estándar combinado (So)")
        df_so = pd.DataFrame({
            "Proyecto": ["Construcción nueva", "Sobre capas"],
            "Flexible": ["0.40 – 0.50", "0.50"],
            "Rígido": ["0.30 – 0.40", "0.40"]
        })
        st.table(df_so)

        st.write("### 8. Periodo de diseño estructural")
        df_periodo_rigido = pd.DataFrame({
            "Condición de la vía": ["Urbana alto volumen", "Rural alto volumen", "Pavimentada bajo volumen", "Bajo volumen agregado"],
            "Periodo (años)": ["30 – 50", "20 – 50", "15 – 25", "10 – 20"]
        })
        st.table(df_periodo_rigido)

        st.write("### 9. Tabla de pasadores")
        df_pasadores = pd.DataFrame({
            "Espesor de losa (cm)": ["14 – 15", "16 – 18", "19 – 20", "21 – 23", "24 – 25", "26 – 28", "29 – 30"],
            "Diámetro del pasador (pulg)": ["3/4", "7/8", "1", "1 1/8", "1 1/4", "1 3/8", "1 1/2"],
            "Longitud pasador (cm)": ["35", "35", "35", "40", "45", "45", "50"],
            "Separación centros (cm)": ["30", "30", "30", "30", "30", "30", "30"]
        })
        st.table(df_pasadores)

        st.write("### 10. Barras de Anclaje (Acero fy = 280 MPa)")
        df_anclaje_280 = pd.DataFrame({
            "Barra": ["3/8\"", "3/8\"", "3/8\"", "3/8\"", "3/8\"", "1/2\"", "1/2\"", "1/2\"", "1/2\"", "1/2\"", "5/8\"", "5/8\"", "5/8\"", "5/8\"", "5/8\""],
            "L (cm)": [45, 45, 45, 45, 45, 60, 60, 60, 60, 60, 70, 70, 70, 70, 70],
            "H (cm)": [15, 17.5, 20, 22.5, 25, 15, 17.5, 20, 22.5, 25, 15, 17.5, 20, 22.5, 25],
            "S = 3.05 m": [80, 70, 60, 55, 45, 120, 120, 105, 95, 85, 120, 120, 120, 120, 120],
            "S = 3.35 m": [75, 60, 55, 50, 45, 120, 110, 100, 85, 80, 120, 120, 120, 120, 120],
            "S = 3.65 m": [65, 55, 50, 45, 40, 120, 100, 90, 80, 70, 120, 120, 120, 120, 120]
        })
        st.table(df_anclaje_280)
        
        st.write("### 10.1 Barras de Anclaje (Acero fy = 420 MPa)")
        df_anclaje_420 = pd.DataFrame({
            "Barra": ["3/8\"", "3/8\"", "3/8\"", "3/8\"", "3/8\"", "1/2\"", "1/2\"", "1/2\"", "1/2\"", "1/2\"", "5/8\"", "5/8\"", "5/8\"", "5/8\"", "5/8\""],
            "L (cm)": [65, 65, 65, 65, 65, 85, 85, 85, 85, 85, 100, 100, 100, 100, 100],
            "H (cm)": [15, 17.5, 20, 22.5, 25, 15, 17.5, 20, 22.5, 25, 15, 17.5, 20, 22.5, 25],
            "S = 3.05 m": [120, 105, 90, 80, 70, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120],
            "S = 3.35 m": [110, 95, 80, 75, 65, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120],
            "S = 3.65 m": [100, 85, 75, 65, 60, 120, 120, 120, 120, 115, 120, 120, 120, 120, 120]
        })
        st.table(df_anclaje_420)

        st.info("""
        **Convenciones de la tabla:**
        * **H** = espesor de la losa (cm)
        * **L** = longitud de barra (cm)
        * **S** = separación entre barras/juntas (m)
        * Los valores numéricos bajo S indican la separación (cm) recomendada entre las barras de anclaje.
        
        **Nota:** Si se usa barra lisa en vez de corrugada: $L_{nueva} = 1.5L$
        """)

        st.write("### 11. Criterios de longitud máxima de losa")
        st.latex(r"L_{max} = 1.25 \times b")
        st.latex(r"L_{max} = 25 \times h")
        st.latex(r"L_{max} = 6 \text{ m}")
