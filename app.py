"""
Dashboard de Diseño de Pavimentos — AASHTO 1993
Ingeniería Vial — Entorno Académico
"""

import streamlit as st
import numpy as np
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
    obtener_serviciabilidad_final_D,
)

import pint
ureg = pint.UnitRegistry()


# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Diseño de Pavimentos AASHTO 1993",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────
# ESTILOS GLOBALES (mismo sistema de diseño)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:ital,wght@0,300;0,400;0,600;1,300&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Fondo y superficie */
.stApp { background-color: #F7F6F2; }
section[data-testid="stSidebar"] { background-color: #1C1C1E; }
section[data-testid="stSidebar"] * { color: #E8E4DC !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stNumberInput label,
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stCheckbox label {
    color: #A09888 !important;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stMultiSelect > div > div {
    background-color: #2C2C2E !important;
    border: 1px solid #3A3A3C !important;
    color: #E8E4DC !important;
}

/* Anular h1/h2/h3 genérico de Streamlit */
h1, h2, h3 {
    font-family: 'IBM Plex Serif', serif !important;
    font-weight: 300 !important;
    color: #1C1C1E !important;
}

/* Header principal */
.dash-title {
    font-family: 'IBM Plex Serif', serif;
    font-weight: 300;
    font-size: 2.4rem;
    color: #1C1C1E;
    letter-spacing: -0.02em;
    margin-bottom: 0;
    line-height: 1.2;
}
.dash-subtitle {
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 300;
    font-size: 0.85rem;
    color: #6B6459;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.3rem;
    margin-bottom: 1.8rem;
}
.dash-divider {
    border: none;
    border-top: 2px solid #1C1C1E;
    margin: 0.4rem 0 1.8rem 0;
}

/* Tarjetas de métricas */
.metric-card {
    background: #FFFFFF;
    border: 1px solid #E0DBD3;
    border-radius: 4px;
    padding: 1.2rem 1.4rem;
    text-align: left;
    height: 100%;
}
.metric-card .m-label {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8A8070;
    margin-bottom: 0.4rem;
}
.metric-card .m-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.8rem;
    font-weight: 500;
    color: #1C1C1E;
    line-height: 1;
}
.metric-card .m-unit {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.75rem;
    color: #8A8070;
    margin-top: 0.25rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid #D0CBC2;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8A8070;
    padding: 0.65rem 1.4rem;
    border: none;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    color: #1C1C1E !important;
    border-bottom: 2px solid #1C1C1E !important;
    font-weight: 500 !important;
}

/* Sección header */
.section-header {
    font-family: 'IBM Plex Serif', serif;
    font-weight: 400;
    font-size: 1.25rem;
    color: #1C1C1E;
    margin-top: 1.5rem;
    margin-bottom: 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #D0CBC2;
}
.section-note {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.78rem;
    color: #8A8070;
    font-style: italic;
    margin-bottom: 1rem;
}

/* Dataframes */
.stDataFrame { border: 1px solid #E0DBD3 !important; border-radius: 4px; }

/* Sidebar brand / secciones */
.sidebar-brand {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #5A5450 !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    padding: 0.5rem 0 1.2rem 0;
}
.sidebar-section {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #5A5450 !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    padding: 1rem 0 0.3rem 0;
    border-top: 1px solid #2C2C2E;
    margin-top: 0.8rem;
}

/* Formula box */
.formula-box {
    background: #FFFFFF;
    border-left: 3px solid #1C1C1E;
    border-radius: 0 4px 4px 0;
    padding: 1rem 1.4rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.88rem;
    color: #1C1C1E;
    margin: 1rem 0;
    line-height: 1.7;
}

/* Result highlight (negro) */
.result-highlight {
    background: #1C1C1E;
    color: #F7F6F2;
    border-radius: 4px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
}
.result-highlight .r-label {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #8A8070;
    margin-bottom: 0.4rem;
}
.result-highlight .r-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.4rem;
    font-weight: 500;
    color: #F7F6F2;
    line-height: 1.1;
}
.result-highlight .r-unit {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.8rem;
    color: #8A8070;
    margin-top: 0.3rem;
}

/* Capas de pavimento (diagrama visual) */
.layer-stack {
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin: 1rem 0;
}
.layer {
    border-radius: 4px;
    padding: 0.9rem 1.2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.layer-label {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.layer-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 500;
}
.layer-asfalto  { background: #1C1C1E; color: #F7F6F2; }
.layer-base     { background: #4A4035; color: #E8E4DC; }
.layer-subbase  { background: #7A6E5A; color: #F7F6F2; }
.layer-subrasante { background: #E0DBD3; color: #4A3F30; border: 1px solid #C8C2B8; }
.layer-rigido   { background: #2E3A4E; color: #E8EDF5; }

/* Info / note box */
.note-box {
    background: #FFFFFF;
    border: 1px solid #E0DBD3;
    border-radius: 4px;
    padding: 0.9rem 1.2rem;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.8rem;
    color: #6B6459;
    margin: 0.8rem 0;
}

/* Expander override */
.streamlit-expanderHeader,
[data-testid="stExpander"] summary,
details > summary {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: #1C1C1E !important;
    background-color: #EDEAE4 !important;
    border: 1px solid #D0CBC2 !important;
    border-radius: 4px !important;
    padding: 0.65rem 1rem !important;
}
[data-testid="stExpander"] summary:hover,
details > summary:hover {
    background-color: #E0DBD3 !important;
}
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary * {
    color: #1C1C1E !important;
}

/* KaTeX (fórmulas LaTeX) */
.katex * { color: #1C1C1E !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">// Ingeniería Vial</div>', unsafe_allow_html=True)
    st.markdown("### Diseño de Pavimentos")

    st.markdown('<div class="sidebar-section">Método de diseño</div>', unsafe_allow_html=True)
    tipo_pavimento = st.radio(
        "Tipo de pavimento",
        ("Pavimento Flexible", "Pavimento Rígido"),
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-section">Tránsito y confiabilidad</div>', unsafe_allow_html=True)
    W_18 = st.number_input(
        "W₁₈ (ESAL)" if tipo_pavimento == "Pavimento Rígido" else "W₁₈",
        value=2.84e+6 if tipo_pavimento == "Pavimento Rígido" else 2.84e+6,
        format="%.2e",
    )

    # Tabla de confiabilidad → Zr (AASHTO 93)
    _ZR_TABLE = {
        50:    0.000,
        60:   -0.253,
        70:   -0.524,
        75:   -0.674,
        80:   -0.841,
        85:   -1.037,
        90:   -1.282,
        95:   -1.645,
        99:   -2.327,
        99.9: -3.090,
        99.99:-3.750,
    }
    _conf_options = list(_ZR_TABLE.keys())
    _conf_labels  = [f"{r} %" for r in _conf_options]

    conf_sel = st.selectbox(
        "Confiabilidad R (%)",
        options=_conf_options,
        format_func=lambda r: f"{r} %",
        index=6,          # 90 % por defecto → Zr = −1.282
    )
    Zr_val = _ZR_TABLE[conf_sel]

    # Mostrar Zr derivado
    st.markdown(
        f'<div style="font-family:IBM Plex Mono,monospace; font-size:0.78rem; '
        f'color:#E8E4DC; background:#2C2C2E; border:1px solid #3A3A3C; '
        f'border-radius:4px; padding:0.45rem 0.8rem; margin-top:-0.3rem; margin-bottom:0.5rem;">'
        f'Zr = <strong>{Zr_val:+.3f}</strong></div>',
        unsafe_allow_html=True,
    )

    S0_val = st.number_input(
        "Error estándar (S₀)",
        value=0.35 if tipo_pavimento == "Pavimento Rígido" else 0.45,
    )

    st.markdown('<div class="sidebar-section">Serviciabilidad</div>', unsafe_allow_html=True)
    Po = st.number_input("Serviciabilidad inicial (Po)", value=4.2)

    # ── Flexible adicionales ─────────────────
    if tipo_pavimento == "Pavimento Flexible":
        Pf_flex = st.number_input("Serviciabilidad final (Pf)", value=2.2)

        st.markdown('<div class="sidebar-section">Módulos resilientes</div>', unsafe_allow_html=True)
        Mr_subrasante = st.number_input("MR Subrasante (psi)", value=12000)
        Mr_subbase    = st.number_input("MR Subbase (psi)",    value=15000)
        Mr_base       = st.number_input("MR Base (psi)",       value=27000)
        MR_asfalto    = st.number_input("MR Asfalto (psi)",    value=3.83e5, format="%.2e")

        st.markdown('<div class="sidebar-section">Drenaje</div>', unsafe_allow_html=True)
        calidad   = st.selectbox("Calidad de drenaje",
                                 ["excellent", "good", "fair", "poor", "very_poor"])
        porcentaje = st.number_input("Saturación (%)", value=15.0)
        usar_manual = st.checkbox("Definir m₂ y m₃ manualmente")
        if usar_manual:
            m2 = st.number_input("m₂", value=0.9)
            m3 = st.number_input("m₃", value=0.9)

    # ── Rígido adicionales ───────────────────
    else:
        Tipo_de_via = st.selectbox("Tipo de vía",
                                   ["Autopista", "Colectoras",
                                    "Calles comerciales", "Calles residenciales"])

        st.markdown('<div class="sidebar-section">Propiedades del concreto</div>',
                    unsafe_allow_html=True)
        Modulo_rotura_MPa = st.number_input("Módulo de rotura (MPa)", value=4.2)
        Ec_psi_val        = st.number_input("Módulo de elasticidad Ec (psi)",
                                            value=3.6e6, format="%.2e")
        J_val             = st.number_input("Coef. transferencia de carga (J)", value=2.7)

        st.markdown('<div class="sidebar-section">Subrasante y drenaje</div>',
                    unsafe_allow_html=True)
        k_val          = st.number_input("Módulo de reacción k (pci)", value=180)
        calidad_rigido = st.selectbox("Calidad de drenaje ",
                                      ["Excelente", "Bueno", "Regular", "Pobre", "Muy malo"],
                                      index=2)
        dias_lluvia    = st.number_input("Días de lluvia al año", value=200)
        cd_val         = st.number_input("Coeficiente de drenaje (Cd)", value=0.9)

    st.markdown("---")
    st.markdown(
        '<div style="font-family: IBM Plex Mono, monospace; font-size: 0.6rem; '
        'color: #5A5450; line-height: 1.6;">Metodología AASHTO 93<br>'
        'Guía de diseño de pavimentos</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# ENCABEZADO PRINCIPAL
# ─────────────────────────────────────────────
tipo_label = "Flexible" if tipo_pavimento == "Pavimento Flexible" else "Rígido"
st.markdown(
    f'<div class="dash-title">Diseño de Pavimento {tipo_label}</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="dash-subtitle">Método AASHTO 1993 &nbsp;·&nbsp; '
    f'W₁₈ = {W_18:.2e} ESAL &nbsp;·&nbsp; '
    f'R = {conf_sel} % &nbsp;→&nbsp; Zr = {Zr_val:+.3f}</div>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# RAMA: PAVIMENTO FLEXIBLE
# ══════════════════════════════════════════════
if tipo_pavimento == "Pavimento Flexible":

    # ── Cálculos ──────────────────────────────
    dpsi = Po - Pf_flex

    rango, categoria = coeficiente_drenaje_rango(calidad, porcentaje)
    if not usar_manual:
        m2 = (rango[0] + rango[1]) / 2
        m3 = m2

    SN3 = calcular_sn(W_18, Zr_val, S0_val, dpsi, Mr_subrasante)
    SN2 = calcular_sn(W_18, Zr_val, S0_val, dpsi, Mr_subbase)
    SN1 = calcular_sn(W_18, Zr_val, S0_val, dpsi, Mr_base)

    a1 = 0.184 * np.log(MR_asfalto) - 1.9547
    a2 = 0.249 * np.log10(Mr_base) - 0.977
    a3 = 0.227 * np.log10(Mr_subbase) - 0.839

    h1_min, h2_min = espesores_minimos(W_18)
    h1_min_cm = in_a_cm_constructivo(h1_min)
    h2_min_cm = in_a_cm_constructivo(h2_min)

    h1 = SN1 / a1
    if h1 < h1_min:
        h1 = h1_min
    else:
        h1 = h1_min_cm * (2.54 ** -1)
        SN1 = h1 * a1
    h1 = h1 * 2.54

    h2 = (SN2 - SN1) / (a2 * m2)
    if h2 < 6.0:
        h2 = 6.0
    else:
        h2 = h2_min_cm * (2.54 ** -1)
        SN2 = h2 * a2 * m2 + SN1
    h2 = h2 * 2.54

    h3 = (SN3 - SN2) / (a3 * m3)
    h3 = (h3 * 2.54 + 1)

    # ── KPIs globales ──────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">Δ PSI (pérdida de servicio)</div>
            <div class="m-value">{dpsi:.2f}</div>
            <div class="m-unit">Po = {Po} → Pf = {Pf_flex}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">Drenaje — categoría</div>
            <div class="m-value">{m2:.3f}</div>
            <div class="m-unit">{categoria} · coef. m₂ = m₃</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">SN subrasante (SN₃)</div>
            <div class="m-value">{SN3:.3f}</div>
            <div class="m-unit">número estructural requerido</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">Espesor total estimado</div>
            <div class="m-value">{(h1 + h2 + h3):.1f}</div>
            <div class="m-unit">cm (Σ carpeta + base + subbase)</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Pestañas ──────────────────────────────
    tab1, tab2, tab3 = st.tabs([
        "1 · Números Estructurales (SN)",
        "2 · Espesores de Diseño",
        "3 · Tablas de Referencia",
    ])

    SN3 = calcular_sn(W_18, Zr_val, S0_val, dpsi, Mr_subrasante)
    SN2 = calcular_sn(W_18, Zr_val, S0_val, dpsi, Mr_subbase)
    SN1 = calcular_sn(W_18, Zr_val, S0_val, dpsi, Mr_base)


    # ── Tab 1: SN ─────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">Números Estructurales Requeridos</div>',
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="section-note">Calculados iterativamente con la ecuación AASHTO 93 '
            'para cada nivel de soporte (subrasante, subbase, base).</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="formula-box">'
                    'log(W₁₈) = Zr·S₀ + 9.36·log(SN+1) − 0.20 + log[ΔPSI/(4.2−1.5)] / (0.40 + 1094/(SN+1)⁵·¹⁹) + 2.32·log(Mᴿ) − 8.07'
                    '</div>', unsafe_allow_html=True)

        col_sn1, col_sn2, col_sn3 = st.columns(3)
        with col_sn1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="m-label">SN₁ — sobre la base</div>
                <div class="m-value">{SN1:.3f}</div>
                <div class="m-unit">MR base = {Mr_base:,} psi</div>
            </div>""", unsafe_allow_html=True)
        with col_sn2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="m-label">SN₂ — sobre la subbase</div>
                <div class="m-value">{SN2:.3f}</div>
                <div class="m-unit">MR subbase = {Mr_subbase:,} psi</div>
            </div>""", unsafe_allow_html=True)
        with col_sn3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="m-label">SN₃ — sobre la subrasante</div>
                <div class="m-value">{SN3:.3f}</div>
                <div class="m-unit">MR subrasante = {Mr_subrasante:,} psi</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:2rem;">Coeficientes Estructurales</div>',
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="section-note">Derivados de los módulos resilientes mediante las '
            'correlaciones empíricas del Manual AASHTO 93.</div>',
            unsafe_allow_html=True,
        )

        df_coef = pd.DataFrame({
            "Capa": ["Carpeta asfáltica", "Base granular", "Subbase granular"],
            "Símbolo": ["a₁", "a₂", "a₃"],
            "MR (psi)": [f"{MR_asfalto:,.0f}", f"{Mr_base:,}", f"{Mr_subbase:,}"],
            "Coeficiente": [f"{a1:.4f}", f"{a2:.4f}", f"{a3:.4f}"],
            "Coef. drenaje": ["—", f"m₂ = {m2:.3f}", f"m₃ = {m3:.3f}"],
        })
        st.dataframe(df_coef, use_container_width=True, hide_index=True)

    # ── Tab 2: Espesores ───────────────────────
    with tab2:
        st.markdown('<div class="section-header">Diseño Final de Espesores</div>',
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="section-note">Espesores constructivos obtenidos tras aplicar los '
            'espesores mínimos de la guía AASHTO y redondear al centímetro constructivo.</div>',
            unsafe_allow_html=True,
        )

        col_diag, col_res = st.columns([1, 1])

        with col_diag:
            st.markdown('<div class="section-header" style="font-size:1rem; margin-top:0;">Diagrama de capas</div>',
                        unsafe_allow_html=True)
            st.markdown(f"""
            <div class="layer-stack">
                <div class="layer layer-asfalto">
                    <span class="layer-label">Carpeta Asfáltica</span>
                    <span class="layer-value">{h1:.2f} cm</span>
                </div>
                <div class="layer layer-base">
                    <span class="layer-label">Base Granular</span>
                    <span class="layer-value">{h2:.2f} cm</span>
                </div>
                <div class="layer layer-subbase">
                    <span class="layer-label">Subbase Granular</span>
                    <span class="layer-value">{h3:.2f} cm</span>
                </div>
                <div class="layer layer-subrasante">
                    <span class="layer-label">Subrasante (MR = {Mr_subrasante:,} psi)</span>
                    <span class="layer-value">∞</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_res:
            st.markdown('<div class="section-header" style="font-size:1rem; margin-top:0;">Verificación SN</div>',
                        unsafe_allow_html=True)

            SN1_prov = a1 * (h1 / 2.54)
            SN2_prov = SN1_prov + a2 * m2 * (h2 / 2.54)
            SN3_prov = SN2_prov + a3 * m3 * (h3 / 2.54)

            df_verif = pd.DataFrame({
                "Nivel": ["SN₁ (carpeta)", "SN₂ (+ base)", "SN₃ (+ subbase)"],
                "SN requerido": [f"{SN1:.3f}", f"{SN2:.3f}", f"{SN3:.3f}"],
                "SN provisto":  [f"{SN1_prov:.3f}", f"{SN2_prov:.3f}", f"{SN3_prov:.3f}"],
                "¿Cumple?": [
                    "✓" if SN1_prov >= SN1 else "✗",
                    "✓" if SN2_prov >= SN2 else "✗",
                    "✓" if SN3_prov >= SN3 else "✗",
                ],
            })
            st.dataframe(df_verif, use_container_width=True, hide_index=True)

            st.markdown(f"""
            <div class="result-highlight" style="margin-top:1rem;">
                <div class="r-label">Espesor total de la estructura</div>
                <div class="r-value">{(h1 + h2 + h3):.1f} cm</div>
                <div class="r-unit">{h1:.2f} + {h2:.2f} + {h3:.2f} cm</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 3: Tablas de referencia flexible ──
    with tab3:
        st.markdown('<div class="section-header">Tablas de Referencia — AASHTO 1993 Flexible</div>',
                    unsafe_allow_html=True)

        with st.expander("Periodo de análisis"):
            df_p = pd.DataFrame({
                "Condición de la vía": ["Urbana alto volumen", "Rural alto volumen",
                                         "Pavimentada bajo volumen", "No pavimentada bajo volumen"],
                "Período (años)": ["30–50", "20–50", "15–25", "10–20"],
            })
            st.dataframe(df_p, use_container_width=True, hide_index=True)

        with st.expander("Factor de distribución por carril (FDC)"):
            df_fdc = pd.DataFrame({
                "Número de carriles": ["1", "2", "3", "4"],
                "% de ejes en carril de diseño": ["100", "80–100", "60–80", "50–75"],
            })
            st.dataframe(df_fdc, use_container_width=True, hide_index=True)

        with st.expander("Nivel de confiabilidad R (%) recomendado"):
            df_conf = pd.DataFrame({
                "Clasificación funcional": ["Autopista", "Arteria principal", "Colectora", "Local"],
                "Urbano": ["85–99.9", "80–99", "80–95", "50–80"],
                "Rural":  ["80–99.9", "75–95", "75–95", "50–80"],
            })
            st.dataframe(df_conf, use_container_width=True, hide_index=True)

        with st.expander("Desviación estándar normal (Zr)"):
            df_zr = pd.DataFrame({
                "Confiabilidad (%)": ["50", "60", "70", "75", "80",
                                       "85", "90", "95", "99", "99.9", "99.99"],
                "Zr": ["0.000", "−0.253", "−0.524", "−0.674", "−0.841",
                        "−1.037", "−1.282", "−1.645", "−2.327", "−3.090", "−3.750"],
            })
            st.dataframe(df_zr, use_container_width=True, hide_index=True)

        with st.expander("Error estándar combinado (S₀)"):
            df_s0 = pd.DataFrame({
                "Condición": ["Construcción nueva", "Sobrecapa (rehabilitación)"],
                "Flexible": ["0.45", "0.50"],
                "Rígido":   ["0.35", "0.40"],
            })
            st.dataframe(df_s0, use_container_width=True, hide_index=True)

        with st.expander("Serviciabilidad final recomendada (Pf)"):
            df_pf = pd.DataFrame({
                "Tipo de vía": ["Autopista", "Carretera", "Zonas industriales",
                                 "Urbano principal", "Urbano secundario"],
                "Pf": ["2.5–3.0", "2.0–2.5", "2.0–2.5", "2.0–2.5", "1.5–2.0"],
            })
            st.dataframe(df_pf, use_container_width=True, hide_index=True)

        with st.expander("Coeficiente de drenaje mᵢ — pavimentos flexibles"):
            df_mi = pd.DataFrame({
                "Calidad del drenaje": ["Excellent", "Good", "Fair", "Poor", "Very Poor"],
                "Tiempo de drenaje":   ["2 horas", "1 día", "1 semana", "1 mes", "Nunca"],
                "< 1%":    ["1.40–1.35", "1.35–1.25", "1.25–1.15", "1.15–1.05", "1.05–0.95"],
                "1–5%":    ["1.35–1.30", "1.25–1.15", "1.15–1.05", "1.05–0.80", "0.95–0.75"],
                "5–25%":   ["1.30–1.20", "1.15–1.00", "1.00–0.80", "0.80–0.60", "0.75–0.40"],
                "> 25%":   ["1.20",       "1.00",       "0.80",       "0.60",       "0.40"],
            })
            st.dataframe(df_mi, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# RAMA: PAVIMENTO RÍGIDO
# ══════════════════════════════════════════════
else:

    # ── Cálculos ──────────────────────────────
    Modulo_rotura_psi = (Modulo_rotura_MPa * ureg.megapascal).to(ureg.psi).magnitude
    Ec_val = Ec_psi_val

    Pf_rig = obtener_serviciabilidad_final_D(Tipo_de_via)
    delta_psi = Po - Pf_rig
    Porcentaje_sat = (dias_lluvia / 365) * 100
    rango_D, categoria_D = coeficiente_drenaje_rango_D(calidad_rigido, Porcentaje_sat)

    D = Calcular_D(
        W_18, Zr_val, S0_val, delta_psi, Pf_rig,
        Modulo_rotura_psi, cd_val, J_val, Ec_val, k_val,
    )
    D_cm = D * 2.54

    # ── KPIs globales ──────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">Serviciabilidad final (Pf)</div>
            <div class="m-value">{Pf_rig}</div>
            <div class="m-unit">Tipo de vía: {Tipo_de_via}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">Δ PSI — pérdida de servicio</div>
            <div class="m-value">{delta_psi:.2f}</div>
            <div class="m-unit">Po = {Po} → Pf = {Pf_rig}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">Humedad estimada</div>
            <div class="m-value">{Porcentaje_sat:.1f}%</div>
            <div class="m-unit">{categoria_D} · {dias_lluvia} días/año</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-label">Espesor de losa</div>
            <div class="m-value">{D_cm:.1f}</div>
            <div class="m-unit">cm &nbsp;({D:.2f} pulgadas)</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Pestañas ──────────────────────────────
    tab1, tab2, tab3 = st.tabs([
        "1 · Parámetros de Diseño",
        "2 · Espesor de Losa",
        "3 · Tablas de Referencia",
    ])

    # ── Tab 1: Parámetros ─────────────────────
    with tab1:
        st.markdown('<div class="section-header">Parámetros Ingresados al Modelo AASHTO 93</div>',
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="section-note">La ecuación de diseño para pavimento rígido relaciona '
            'el número de ejes equivalentes W₁₈ con el espesor D de la losa de concreto.</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="formula-box">'
            'log(W₁₈) = Zr·S₀ + 7.35·log(D+1) − 0.06 + log[ΔPSI/(4.5−1.5)] / (1 + 1.624×10⁷/(D+1)⁸·⁴⁶) '
            '+ (4.22 − 0.32·Pₜ)·log[Sc·Cd·(D⁰·⁷⁵ − 1.132) / (215.63·J·(D⁰·⁷⁵ − 18.42/(Ec/k)⁰·²⁵))]'
            '</div>',
            unsafe_allow_html=True,
        )

        col_pa, col_pb = st.columns(2)
        with col_pa:
            df_params = pd.DataFrame({
                "Parámetro": ["W₁₈ (ESAL)", "Zr", "S₀", "Po", "Pf", "Δ PSI"],
                "Valor": [f"{W_18:.2e}", f"{Zr_val}", f"{S0_val}",
                           f"{Po}", f"{Pf_rig}", f"{delta_psi:.2f}"],
            })
            st.dataframe(df_params, use_container_width=True, hide_index=True)
        with col_pb:
            df_params2 = pd.DataFrame({
                "Parámetro": ["Módulo de rotura Sc (MPa)", "Sc (psi)", "Ec (psi)",
                               "k (pci)", "J", "Cd"],
                "Valor": [f"{Modulo_rotura_MPa}", f"{Modulo_rotura_psi:.1f}",
                           f"{Ec_val:.2e}", f"{k_val}", f"{J_val}", f"{cd_val}"],
            })
            st.dataframe(df_params2, use_container_width=True, hide_index=True)

        st.markdown('<div class="section-header">Análisis de Drenaje</div>',
                    unsafe_allow_html=True)
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="m-label">Calidad del drenaje</div>
                <div class="m-value">{calidad_rigido}</div>
                <div class="m-unit">Categoría asignada</div>
            </div>""", unsafe_allow_html=True)
        with col_d2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="m-label">% tiempo con saturación</div>
                <div class="m-value">{Porcentaje_sat:.1f}%</div>
                <div class="m-unit">{dias_lluvia} días/año de lluvia</div>
            </div>""", unsafe_allow_html=True)
        with col_d3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="m-label">Coeficiente Cd usado</div>
                <div class="m-value">{cd_val}</div>
                <div class="m-unit">Rango: {rango_D}</div>
            </div>""", unsafe_allow_html=True)

    # ── Tab 2: Espesor ────────────────────────
    with tab2:
        st.markdown('<div class="section-header">Resultado del Espesor de Losa</div>',
                    unsafe_allow_html=True)

        col_vis, col_det = st.columns([1, 1])

        with col_vis:
            st.markdown('<div class="section-header" style="font-size:1rem; margin-top:0;">Sección transversal</div>',
                        unsafe_allow_html=True)
            st.markdown(f"""
            <div class="layer-stack">
                <div class="layer layer-rigido">
                    <span class="layer-label">Losa de Concreto — D</span>
                    <span class="layer-value">{D_cm:.1f} cm</span>
                </div>
                <div class="layer layer-subbase">
                    <span class="layer-label">Subbase / Capa de apoyo</span>
                    <span class="layer-value">k = {k_val} pci</span>
                </div>
                <div class="layer layer-subrasante">
                    <span class="layer-label">Subrasante</span>
                    <span class="layer-value">∞</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_det:
            st.markdown(f"""
            <div class="result-highlight">
                <div class="r-label">Espesor requerido de losa</div>
                <div class="r-value">{D_cm:.2f} cm</div>
                <div class="r-unit">{D:.2f} pulgadas &nbsp;·&nbsp; Vía: {Tipo_de_via}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-header" style="font-size:1rem;">Pasadores recomendados</div>',
                        unsafe_allow_html=True)

            def recomendar_pasador(D_cm_val):
                rangos = [
                    ((14, 15), ('3/4"', 35, 30)),
                    ((16, 18), ('7/8"', 35, 30)),
                    ((19, 20), ('1"',   35, 30)),
                    ((21, 23), ('1 1/8"', 40, 30)),
                    ((24, 25), ('1 1/4"', 45, 30)),
                    ((26, 28), ('1 3/8"', 45, 30)),
                    ((29, 30), ('1 1/2"', 50, 30)),
                ]
                for (lo, hi), datos in rangos:
                    if lo <= D_cm_val <= hi:
                        return datos
                return ("Ver tabla", "—", 30)

            diam, lp, sep = recomendar_pasador(D_cm)
            df_pas = pd.DataFrame({
                "Espesor losa": [f"{D_cm:.1f} cm"],
                "Diámetro pasador": [diam],
                "Longitud (cm)": [lp],
                "Separación (cm)": [sep],
            })
            st.dataframe(df_pas, use_container_width=True, hide_index=True)

    # ── Tab 3: Tablas referencia rígido ───────
    with tab3:
        st.markdown('<div class="section-header">Tablas de Referencia — AASHTO 1993 Rígido</div>',
                    unsafe_allow_html=True)

        with st.expander("Módulo de reacción K — estimación por CBR"):
            st.markdown(
                '<div class="section-note">Correlaciones empíricas para estimar K (MPa/m) a partir del CBR.</div>',
                unsafe_allow_html=True,
            )
            st.latex(r"K = 2.55 + 52.5 \times \log_{10}(CBR) \quad (CBR \le 10)")
            st.latex(r"K = 46 + 9.08 \times (\log_{10}(CBR))^{4.34} \quad (CBR > 10)")
            df_k = pd.DataFrame({
                "K subrasante (MPa/m)": ["20", "40", "60", "80"],
                "K subrasante (pci)":   ["73",  "147", "220", "295"],
                "100 mm (pci)": ["85",  "165", "235", "320"],
                "150 mm (pci)": ["96",  "180", "245", "330"],
                "225 mm (pci)": ["117", "210", "280", "370"],
                "300 mm (pci)": ["140", "245", "330", "430"],
            })
            st.dataframe(df_k, use_container_width=True, hide_index=True)

        with st.expander("Desviación estándar normal (Zr)"):
            df_zr = pd.DataFrame({
                "Confiabilidad (%)": ["50", "60", "70", "75", "80",
                                       "85", "90", "95", "99", "99.9", "99.99"],
                "Zr": ["0.000", "−0.253", "−0.524", "−0.674", "−0.841",
                        "−1.037", "−1.282", "−1.645", "−2.327", "−3.090", "−3.750"],
            })
            st.dataframe(df_zr, use_container_width=True, hide_index=True)

        with st.expander("Módulo de rotura recomendado (Sc)"):
            df_mr = pd.DataFrame({
                "Camiones/día": ["> 300", "150–300", "25–150", "< 25"],
                "MR a flexión (MPa)": ["4.5", "4.2", "4.0", "3.8"],
            })
            st.dataframe(df_mr, use_container_width=True, hide_index=True)

        with st.expander("Coeficiente de drenaje Cd — pavimento rígido"):
            df_cd = pd.DataFrame({
                "Calidad": ["Excelente", "Bueno", "Regular", "Pobre", "Muy malo"],
                "< 1%":   ["1.25–1.20", "1.20–1.15", "1.15–1.10", "1.10–1.00", "1.00–0.90"],
                "1–5%":   ["1.20–1.15", "1.15–1.10", "1.10–1.00", "1.00–0.90", "0.90–0.80"],
                "5–25%":  ["1.15–1.10", "1.10–1.00", "1.00–0.90", "0.90–0.80", "0.80–0.70"],
                "> 25%":  ["1.10",       "1.00",       "0.90",       "0.80",       "0.70"],
            })
            st.dataframe(df_cd, use_container_width=True, hide_index=True)

        with st.expander("Serviciabilidad final (Pf) y nivel de confiabilidad"):
            col_a, col_b = st.columns(2)
            with col_a:
                df_pf = pd.DataFrame({
                    "Tipo de vía": ["Autopista", "Colectoras",
                                     "Calles comerciales", "Calles residenciales"],
                    "Pf": ["3.0", "2.5", "2.25", "2.0"],
                })
                st.dataframe(df_pf, use_container_width=True, hide_index=True)
            with col_b:
                df_conf = pd.DataFrame({
                    "Clasificación": ["Autopista", "Arteria principal", "Colectora", "Local"],
                    "Urbana": ["85–99.9", "80–99.9", "80–95", "50–80"],
                    "Rural":  ["80–99.9", "75–95",   "75–95", "50–80"],
                })
                st.dataframe(df_conf, use_container_width=True, hide_index=True)

        with st.expander("Coeficiente de transferencia de carga (J)"):
            st.markdown(
                '<div class="note-box">'
                '<strong>J = 2.7–3.2</strong> → pavimentos con pasadores y confinamiento lateral '
                '(bermas, bordillos). Condición más común.<br>'
                '<strong>J = 4.2–4.4</strong> → pavimentos sin confinamiento lateral. '
                'Casi nunca aplicable en la práctica.<br><br>'
                '⚠ A mayor J, mayor espesor calculado.'
                '</div>',
                unsafe_allow_html=True,
            )

        with st.expander("Tabla de pasadores (dowel bars)"):
            df_pas_full = pd.DataFrame({
                "Espesor losa (cm)": ["14–15", "16–18", "19–20", "21–23",
                                       "24–25", "26–28", "29–30"],
                "Diámetro (pulg)": ['3/4"', '7/8"', '1"', '1 1/8"',
                                    '1 1/4"', '1 3/8"', '1 1/2"'],
                "Longitud (cm)": [35, 35, 35, 40, 45, 45, 50],
                "Separación (cm)": [30, 30, 30, 30, 30, 30, 30],
            })
            st.dataframe(df_pas_full, use_container_width=True, hide_index=True)

        with st.expander("Barras de anclaje — fy = 280 MPa"):
            df_anc_280 = pd.DataFrame({
                "Barra": ['3/8"']*5 + ['1/2"']*5 + ['5/8"']*5,
                "L (cm)": [45]*5 + [60]*5 + [70]*5,
                "H (cm)": [15, 17.5, 20, 22.5, 25]*3,
                "S = 3.05 m": [80, 70, 60, 55, 45, 120, 120, 105, 95, 85,
                                120, 120, 120, 120, 120],
                "S = 3.35 m": [75, 60, 55, 50, 45, 120, 110, 100, 85, 80,
                                120, 120, 120, 120, 120],
                "S = 3.65 m": [65, 55, 50, 45, 40, 120, 100, 90, 80, 70,
                                120, 120, 120, 120, 120],
            })
            st.dataframe(df_anc_280, use_container_width=True, hide_index=True)

        with st.expander("Barras de anclaje — fy = 420 MPa"):
            df_anc_420 = pd.DataFrame({
                "Barra": ['3/8"']*5 + ['1/2"']*5 + ['5/8"']*5,
                "L (cm)": [65]*5 + [85]*5 + [100]*5,
                "H (cm)": [15, 17.5, 20, 22.5, 25]*3,
                "S = 3.05 m": [120, 105, 90, 80, 70, 120, 120, 120, 120, 120,
                                120, 120, 120, 120, 120],
                "S = 3.35 m": [110, 95, 80, 75, 65, 120, 120, 120, 120, 120,
                                120, 120, 120, 120, 120],
                "S = 3.65 m": [100, 85, 75, 65, 60, 120, 120, 120, 115, 120,
                                120, 120, 120, 120, 120],
            })
            st.dataframe(df_anc_420, use_container_width=True, hide_index=True)
            st.markdown(
                '<div class="note-box">H = espesor de losa · L = longitud de barra · '
                'S = separación entre juntas. '
                'Si se usa barra lisa: L_nueva = 1.5 × L</div>',
                unsafe_allow_html=True,
            )

        with st.expander("Criterios de longitud máxima de losa"):
            st.latex(r"L_{max} = 1.25 \times b")
            st.latex(r"L_{max} = 25 \times h")
            st.latex(r"L_{max} = 6 \text{ m (máximo absoluto)}")