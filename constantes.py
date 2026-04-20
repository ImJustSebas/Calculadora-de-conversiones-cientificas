# constantes.py
# Valores fundamentales y factores de conversion exactos

# Temperatura
CERO_ABSOLUTO = -273.15  # °C
KELVIN_OFFSET = 273.15
RANKINE_OFFSET = 459.67

# Factores de temperatura
FACTOR_C_A_F = 9.0 / 5.0
FACTOR_F_A_C = 5.0 / 9.0

# Velocidad de la luz (m/s) - para validacion
VELOCIDAD_LUZ = 299792458.0

# Constante de Planck y otras fisicas para futuras conversiones
MASA_ATOMICA = 1.66053906660e-27  # kg
CARGA_ELEMENTAL = 1.602176634e-19  # C

# Densidad del agua a diferentes temperaturas (°C -> g/mL)
DENSIDAD_AGUA = {
    4: 1.00000,
    10: 0.99970,
    15: 0.99910,
    20: 0.99821,
    25: 0.99705,
    30: 0.99565,
    37: 0.99333,  # Temperatura corporal
    100: 0.95840
}

# OD600 - Factores de conversion para diferentes organismos
FACTORES_OD600 = {
    "E. coli": 8.0e8,           # celulas/mL por OD
    "S. cerevisiae": 1.0e7,     # levadura
    "P. pastoris": 5.0e7,
    "CHO (mamifero)": 1.2e6,
    "HEK293": 2.5e6
}