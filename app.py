import streamlit as st
import numpy as np
from Modulos import (
    calcular_sn,
    espesores_minimos,
    in_a_cm_constructivo,
    coeficiente_drenaje_rango
)

# =========================================
# CONFIGURACIÓN
# =========================================
st.set_page_config(
    page_title="Diseño de Pavimento Flexible - AASHTO",
    layout="wide"
)

# Estilo visual
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("Diseño de Pavimento Flexible - Método AASHTO")

# =========================================
# SIDEBAR
# =========================================
st.sidebar.header("Parámetros de entrada")

# Tránsito
st.sidebar.subheader("Tránsito")
W_18 = st.sidebar.number_input("W18 (ESAL)", value=1.8e6, format="%.2e")

# Parámetros AASHTO
st.sidebar.subheader("Parámetros AASHTO")
confiabilidad = st.sidebar.number_input("Zr", value=-1.282)
error_estandar = st.sidebar.number_input("S0", value=0.45)
Po = st.sidebar.number_input("Po", value=4.2)
Pf = st.sidebar.number_input("Pf", value=2.2)
dpsi = Po - Pf

# Materiales
st.sidebar.subheader("Módulos resilientes")
Mr_subrasante = st.sidebar.number_input("MR Subrasante (psi)", value=12000)
Mr_subbase = st.sidebar.number_input("MR Subbase (psi)", value=15000)
Mr_base = st.sidebar.number_input("MR Base (psi)", value=27000)
MR_asfalto = st.sidebar.number_input("MR Asfalto", value=3.83e5)

# Drenaje
st.sidebar.subheader("Drenaje")
calidad = st.sidebar.selectbox(
    "Calidad de drenaje",
    ["excellent", "good", "fair", "poor", "very_poor"]
)
porcentaje = st.sidebar.number_input("Saturación (%)", value=15.0)

usar_manual = st.sidebar.checkbox("Definir m2 y m3 manualmente")

# =========================================
# DRENAJE
# =========================================
rango, categoria = coeficiente_drenaje_rango(calidad, porcentaje)

if usar_manual:
    m2 = st.sidebar.number_input("m2", value=0.9)
    m3 = st.sidebar.number_input("m3", value=0.9)
else:
    m2 = (rango[0] + rango[1]) / 2
    m3 = m2

# =========================================
# SECCIÓN: DRENAJE
# =========================================
with st.container():
    st.subheader("Drenaje")
    col1, col2, col3 = st.columns(3)

    col1.metric("Categoría", categoria)
    col2.metric("Rango", f"{rango}")
    col3.metric("Coeficiente usado", f"{m2:.3f}")

st.divider()

# =========================================
# SN
# =========================================
SN3 = calcular_sn(W_18, confiabilidad, error_estandar, dpsi, Mr_subrasante)
SN2 = calcular_sn(W_18, confiabilidad, error_estandar, dpsi, Mr_subbase)
SN1 = calcular_sn(W_18, confiabilidad, error_estandar, dpsi, Mr_base)

with st.container():
    st.subheader("Número estructural (SN)")
    col1, col2, col3 = st.columns(3)

    col1.metric("Subrasante", f"{SN3:.2f}")
    col2.metric("Subbase", f"{SN2:.2f}")
    col3.metric("Base", f"{SN1:.2f}")

st.divider()

# =========================================
# COEFICIENTES
# =========================================
a1 = 0.184 * np.log(MR_asfalto) - 1.9547
a2 = 0.249 * np.log10(Mr_base) - 0.977
a3 = 0.227 * np.log10(Mr_subbase) - 0.839

with st.container():
    st.subheader("Coeficientes estructurales")
    col1, col2, col3 = st.columns(3)

    col1.metric("a1", f"{a1:.3f}")
    col2.metric("a2", f"{a2:.3f}")
    col3.metric("a3", f"{a3:.3f}")

st.divider()

# =========================================
# ESPESORES MÍNIMOS
# =========================================
h1_min, h2_min = espesores_minimos(W_18)
h1_min_cm = in_a_cm_constructivo(h1_min)
h2_min_cm = in_a_cm_constructivo(h2_min)

with st.container():
    st.subheader("Espesores mínimos")
    col1, col2 = st.columns(2)

    col1.metric("Carpeta (cm)", f"{h1_min_cm:.2f}")
    col2.metric("Base (cm)", f"{h2_min_cm:.2f}")

st.divider()

# =========================================
# CÁLCULO DE ESPESORES
# =========================================
h1 = SN1 / a1
if h1 < h1_min:
    h1 = h1_min
else:
    h1 = h1_min_cm * (2.54**-1)
    SN1 = h1 * a1
h1 = h1 * 2.54

h2 = (SN2 - SN1) / (a2 * m2)
if h2 < 6.0:
    h2 = 6.0
else:
    h2 = h2_min_cm * (2.54**-1)
    SN2 = h2 * a2 * m2 + SN1
h2 = h2 * 2.54

h3 = (SN3 - SN2) / (a3 * m3)
h3 = (h3 * 2.54 + 1).round(0)

# =========================================
# RESULTADOS
# =========================================
with st.container():
    st.subheader("Resultados finales")
    col1, col2, col3 = st.columns(3)

    col1.metric("Carpeta (cm)", f"{h1:.2f}")
    col2.metric("Base (cm)", f"{h2:.2f}")
    col3.metric("Subbase (cm)", f"{h3:.2f}")