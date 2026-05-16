import numpy as np
from scipy.optimize import fsolve

def calcular_trafico_maximo(sn, zr, s0, delta_psi, mr):
    """
    Calcula el W18 (Ejes equivalentes) despejando la fórmula AASHTO 93.
    """
    # 1. Calculamos los términos de la derecha de la ecuación
    termino_base = zr * s0 + 9.36 * np.log10(sn + 1) - 0.20
    
    # Término de serviciabilidad
    numerador_psi = np.log10(delta_psi / (4.2 - 1.5))
    denominador_psi = 0.4 + (1094 / (sn + 1)**5.19)
    termino_psi = numerador_psi / denominador_psi
    
    # Término del suelo (Módulo Resiliente)
    termino_mr = 2.32 * np.log10(mr) - 8.07
    
    # 2. Sumamos todo para obtener el Log10(W18)
    log_w18 = termino_base + termino_psi + termino_mr
    
    # 3. Despejamos W18 usando la potencia de 10
    w18 = 10**log_w18
    
    return w18

def calcular_sn(w18, zr, s0, delta_psi, mr):
    def ecuacion(sn):
        
        termino_base = zr * s0 + 9.36 * np.log10(sn + 1) - 0.20
        termino_psi = np.log10(delta_psi / (4.2 - 1.5)) / (0.4 + (1094 / (sn + 1)**5.19))
        termino_mr = 2.32 * np.log10(mr) - 8.07

        return (termino_base + termino_psi + termino_mr) - np.log10(w18)

    sn_inicial = 3  # Valor inicial pequeño
    resultado = fsolve(ecuacion, sn_inicial)
    
    return resultado[0]

def Calcular_D(W_18, Zr, So, dela_psi, pf, Mr, Cd, J, Ec, K):

    def ecuacion(D):
        termino_base = (
            Zr * So + 7.35 * np.log10(D + 1) - 0.06
        )

        termino_psi = (
            np.log10(dela_psi / (4.5 - 1.5))
            /
            (1 + ((1.624e7) / ((D + 1) ** 8.46)))
        )

        numerador = (Mr * Cd * ((D ** 0.75) - 1.132))

        denominador = (
            215.63
            * J
            * (
                (D ** 0.75)
                -
                (
                    18.42
                    /
                    ((Ec / K) ** 0.25)
                )
            )
        )

        # Protección contra números negativos
        if numerador <= 0 or denominador <= 0:
            return 1e10

        termino_3 = (
            (4.22 - 0.32 * pf)
            *
            np.log10(numerador / denominador)
        )

        return (
            termino_base
            + termino_psi
            + termino_3
            - np.log10(W_18)
        )

    limite_inferior_matematico = (18.42 / ((Ec / K) ** 0.25)) ** (1 / 0.75)
    
    D_inicial = limite_inferior_matematico + 1.0

    resultado = fsolve(ecuacion, D_inicial)

    return resultado[0]

def obtener_serviciabilidad_final_D(tipo_via):
    valores_pf = {
        "Autopista": 3.0,
        "Colectoras": 2.5,
        "Calles comerciales": 2.25,
        "Calles residenciales": 2.0
    }
    return valores_pf.get(tipo_via, "Error: Tipo de vía no encontrado")

def coeficiente_drenaje_rango_D(calidad, porcentaje):
    calidad = calidad.lower().strip()

    if porcentaje < 1:
        col = 0
        categoria = "<1%"
    elif porcentaje <= 5:
        col = 1
        categoria = "1-5%"
    elif porcentaje <= 25:
        col = 2
        categoria = "5-25%"
    else:
        col = 3
        categoria = ">25%"

    tabla = {
        "excelente": [(1.25, 1.20), (1.20, 1.15), (1.15, 1.10), (1.10, 1.10)],
        "bueno": [(1.20, 1.15), (1.15, 1.10), (1.10, 1.00), (1.00, 1.00)],
        "regular": [(1.15, 1.10), (1.10, 1.00), (1.00, 0.90), (0.90, 0.90)],
        "pobre": [(1.10, 1.00), (1.00, 0.90), (0.90, 0.80), (0.80, 0.80)],
        "muy malo": [(1.00, 0.90), (0.90, 0.80), (0.80, 0.70), (0.70, 0.70)]
    }

    if calidad not in tabla:
        raise ValueError(f"Calidad de drenaje '{calidad}' no válida.")

    rango = tabla[calidad][col]
    return rango, categoria






def espesores_minimos(W18):

    if W18 < 50000:
        return 1.0, 4.0
    
    elif W18 < 150000:
        return 2.0, 4.0
    
    elif W18 < 500000:
        return 2.5, 4.0
    
    elif W18 < 2000000:
        return 3.0, 6.0
    
    elif W18 < 7000000:
        return 3.5, 6.0
    
    else:
        return 4.0, 6.0

def in_a_cm_constructivo(pulg):
    cm = round(pulg * 2.54*2)/2
    return cm


def coeficiente_drenaje_rango(calidad, porcentaje):
    """
    Retorna el rango (min, max) del coeficiente de drenaje (m2 o m3)

    Parámetros:
    calidad   : str  -> 'excellent', 'good', 'fair', 'poor', 'very_poor'
    porcentaje: float -> porcentaje de saturación

    Retorna:
    (min, max, categoria_porcentaje)
    """

    calidad = calidad.lower()

    # Clasificación del porcentaje
    if porcentaje < 1:
        col = 0
        categoria = "<1%"
    elif porcentaje <= 5:
        col = 1
        categoria = "1-5%"
    elif porcentaje <= 25:
        col = 2
        categoria = "5-25%"
    else:
        col = 3
        categoria = ">25%"

    # Tabla AASHTO
    tabla = {
        "excellent": [
            (1.40, 1.35),
            (1.35, 1.30),
            (1.30, 1.15),
            (1.20, 1.20)
        ],
        "good": [
            (1.35, 1.25),
            (1.25, 1.15),
            (1.15, 1.00),
            (1.00, 1.00)
        ],
        "fair": [
            (1.25, 1.15),
            (1.15, 1.05),
            (1.00, 0.80),
            (0.80, 0.80)
        ],
        "poor": [
            (1.15, 1.05),
            (1.05, 0.80),
            (0.80, 0.60),
            (0.60, 0.60)
        ],
        "very_poor": [
            (1.05, 0.95),
            (0.95, 0.75),
            (0.75, 0.40),
            (0.40, 0.40)
        ]
    }

    if calidad not in tabla:
        raise ValueError("Calidad no válida")

    rango = tabla[calidad][col]

    return rango, categoria