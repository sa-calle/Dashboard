import numpy as np
import pint

# Asegúrate de tener el archivo Modulos.py en la misma carpeta
from Modulos import Calcular_D, coeficiente_drenaje_rango_D, obtener_serviciabilidad_final_D 

ureg = pint.UnitRegistry()

# =====================================================================
# 1. ZONA DE DATOS (Ingresa aquí todos tus parámetros)
# =====================================================================

# --- Tráfico y Confiabilidad ---
W_18 = 6e6                        # Número de ejes equivalentes (ESALs)
Zr = -1.282                       # Confiabilidad (-1.282 para 90%)
S0 = 0.35                         # Error estándar combinado          

# --- Serviciabilidad ---
Tipo_de_via = "Autopista"
Po = 4.2                          # Serviciabilidad inicial

# --- Propiedades del Concreto ---
Modulo_rotura_concreto_MPa = 4.2  # Módulo de rotura (Mr) en Megapascales
Ec_psi = 3.6e6      
# Módulo de elasticidad (Ec) en PSI
J = 2.7                           # Coeficiente de transferencia de carga

# --- Subrasante, Base y Drenaje ---
Modulo_de_reccion_combinado = 147 # Valor de K módulo de reacción de la subrasante en pci
Calidad_drenaje = "Regular"       # "Excelente", "Bueno", "Regular", "Pobre", "Muy malo"
Dias_que_lleve_al_ano = 200       # Para calcular el porcentaje de saturación
cd = 0.9                          # Coeficiente de drenaje elegido


# =====================================================================
# 2. PROCESAMIENTO Y CONVERSIONES (No necesitas modificar esto)
# =====================================================================

# Conversión del módulo de rotura de MPa a PSI
Modulo_rotura_concreto = Modulo_rotura_concreto_MPa * ureg.megapascal 
Modulo_rotura_concreto = Modulo_rotura_concreto.to(ureg.psi)

# Conversión del módulo de elasticidad usando pint
Ec = Ec_psi * ureg.psi
Ec = Ec.to(ureg.psi).magnitude 

# Cálculo de Serviciabilidad final y Delta PSI
Pf = obtener_serviciabilidad_final_D(Tipo_de_via)
delta_psi = Po - Pf

# Cálculo de humedad y drenaje
Porcentaje_saturacion = (Dias_que_lleve_al_ano / 365) * 100
rango, categoria = coeficiente_drenaje_rango_D(Calidad_drenaje, Porcentaje_saturacion)


# =====================================================================
# 3. IMPRESIÓN DE RESULTADOS Y RESUMEN
# =====================================================================

print(f"Módulo de reacción de la subrasante (K inicial): {Modulo_de_reccion_combinado:.2f} pci")
print(f"Pf para {Tipo_de_via}: {Pf} (Índice PSI)")
print(f"Categoría de humedad: {categoria}")
print(f"Rango de coeficiente de drenaje: {rango}")

print("\n--- RESUMEN DE PARÁMETROS PARA EL CÁLCULO DE D ---")
print(f"1. Tráfico (W_18): {W_18:.2e}")
print(f"2. Confiabilidad (Zr): {Zr}")
print(f"3. Error estándar (S0): {S0}")
print(f"4. Diferencia de serviciabilidad (Delta PSI): {delta_psi:.2f}")
print(f"5. Serviciabilidad final (Pf): {Pf}")
print(f"6. Módulo de rotura del concreto (Mr): {Modulo_rotura_concreto.magnitude:.2f} psi")
print(f"7. Coeficiente de drenaje (Cd): {cd}")
print(f"8. Coeficiente de transferencia de carga (J): {J}")
print(f"9. Módulo de elasticidad (Ec): {Ec:.2e} psi")
print(f"10. Módulo de reacción combinado (K): {Modulo_de_reccion_combinado} pci")
print("--------------------------------------------------")


# =====================================================================
# 4. LLAMADO A LA FUNCIÓN DE CÁLCULO
# =====================================================================

D = Calcular_D(
    W_18,                                # 1. Tráfico
    Zr,                                  # 2. Confiabilidad
    S0,                                  # 3. Error estándar
    delta_psi,                           # 4. Diferencia de serviciabilidad
    Pf,                                  # 5. Serviciabilidad final
    Modulo_rotura_concreto.magnitude,    # 6. Módulo de rotura (Mr)
    cd,                                  # 7. Coeficiente de drenaje
    J,                                   # 8. Transferencia de carga
    Ec,                                  # 9. Módulo de elasticidad
    Modulo_de_reccion_combinado          # 10. Módulo de reacción combinado (K)
)

print(f"\nEspesor mínimo requerido (D): {D:.2f} pulgadas")