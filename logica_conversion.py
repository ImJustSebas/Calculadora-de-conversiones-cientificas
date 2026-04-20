# logica_conversion.py
# Motor principal de conversiones y factores

import os
import csv
from constantes import *
from utilidades import validar_temperatura
from gestor_incertidumbre import GestorIncertidumbre

class MotorConversiones:
    
    def __init__(self):
        self.categorias = {}
        self.compuestos = {}
        self.factores_od = {}
        
        self._inicializar_categorias()
        self._cargar_compuestos()
        self._cargar_factores_od()
    
    def _inicializar_categorias(self):
        """Define todas las categorias y sus factores de conversion."""
        
        # Base: metro
        self.categorias["Longitud"] = {
            "m": 1.0, "cm": 1e-2, "mm": 1e-3, "µm": 1e-6, "nm": 1e-9,
            "pm": 1e-12, "fm": 1e-15, "Å": 1e-10, "km": 1e3,
            "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344,
            "AU": 149597870700, "ly": 9.4607304725808e15, "pc": 3.08567758149137e16
        }
        
        # Base: kilogramo
        self.categorias["Masa"] = {
            "kg": 1.0, "g": 1e-3, "mg": 1e-6, "µg": 1e-9, "ng": 1e-12,
            "pg": 1e-15, "fg": 1e-18, "lb": 0.45359237, "oz": 0.028349523125,
            "ton": 1000.0, "tonne": 1000.0, "Da": 1.66053906660e-27, "kDa": 1.66053906660e-24
        }
        
        # Base: litro
        self.categorias["Volumen"] = {
            "L": 1.0, "mL": 1e-3, "µL": 1e-6, "nL": 1e-9, "pL": 1e-12,
            "fL": 1e-15, "m³": 1000.0, "cm³": 1e-3, "mm³": 1e-6,
            "gal": 3.785411784, "qt": 0.946352946, "pt": 0.473176473,
            "cup": 0.2365882365, "fl oz": 0.0295735295625, "tbsp": 0.01478676478125,
            "tsp": 0.00492892159375
        }
        
        # Temperatura - manejo especial
        self.categorias["Temperatura"] = {
            "°C": "especial", "K": "especial", "°F": "especial", "°R": "especial"
        }
        
        # Base: Pascal
        self.categorias["Presion"] = {
            "Pa": 1.0, "kPa": 1e3, "MPa": 1e6, "GPa": 1e9,
            "atm": 101325.0, "mmHg": 133.322387415, "torr": 133.322368421,
            "bar": 1e5, "mbar": 100, "psi": 6894.757293168, "psia": 6894.757293168,
            "psig": "manometrica"  # Requiere presion atmosferica
        }
        
        # Base: Joule
        self.categorias["Energia"] = {
            "J": 1.0, "kJ": 1e3, "MJ": 1e6, "GJ": 1e9,
            "cal": 4.184, "kcal": 4184.0, "eV": 1.602176634e-19,
            "MeV": 1.602176634e-13, "GeV": 1.602176634e-10,
            "Wh": 3600.0, "kWh": 3.6e6, "BTU": 1055.05585262,
            "erg": 1e-7, "Hartree": 4.3597447222071e-18
        }
        
        # Base: Watt
        self.categorias["Potencia"] = {
            "W": 1.0, "kW": 1e3, "MW": 1e6, "GW": 1e9,
            "hp": 745.699871582, "hp_metrico": 735.49875,
            "BTU_h": 0.29307107, "cal_s": 4.184
        }
        
        # Base: Newton
        self.categorias["Fuerza"] = {
            "N": 1.0, "kN": 1e3, "dyn": 1e-5, "lbf": 4.4482216152605,
            "pdl": 0.138254954376, "kgf": 9.80665
        }
        
        # Base: m²
        self.categorias["Area"] = {
            "m²": 1.0, "cm²": 1e-4, "mm²": 1e-6, "km²": 1e6,
            "ha": 1e4, "acre": 4046.8564224, "ft²": 0.09290304,
            "in²": 0.00064516, "yd²": 0.83612736
        }
        
        # Base: m/s
        self.categorias["Velocidad"] = {
            "m/s": 1.0, "km/h": 0.27777777777778, "mph": 0.44704,
            "knot": 0.51444444444444, "ft/s": 0.3048, "cm/s": 0.01,
            "c": 299792458.0  # Velocidad de la luz
        }
        
        # Base: kg/m³
        self.categorias["Densidad"] = {
            "kg/m³": 1.0, "g/cm³": 1000.0, "g/mL": 1000.0,
            "g/L": 1.0, "mg/mL": 1.0, "µg/mL": 0.001,
            "lb/ft³": 16.01846337396, "lb/gal": 119.8264273
        }
        
        # Base: mol/L (M)
        self.categorias["Concentracion"] = {
            "M": 1.0, "mM": 1e-3, "µM": 1e-6, "nM": 1e-9, "pM": 1e-12,
            "fM": 1e-15, "mol/L": 1.0, "mmol/L": 1e-3,
            "ppm": 1e-6, "ppb": 1e-9, "ppt": 1e-12,
            "% (p/v)": 0.01,  # g/100mL -> g/mL
            "mg/mL": "masa_volumen", "µg/mL": "masa_volumen",
            "ng/mL": "masa_volumen", "g/L": "masa_volumen"
        }
        
        # Base: Bq
        self.categorias["Radiactividad"] = {
            "Bq": 1.0, "kBq": 1e3, "MBq": 1e6, "GBq": 1e9,
            "Ci": 3.7e10, "mCi": 3.7e7, "µCi": 3.7e4,
            "dpm": 1.0/60.0, "cpm": "depende_eficiencia"
        }
        
        # Microbiologia
        self.categorias["Microbiologia"] = {
            "CFU/mL": 1.0, "celulas/mL": 1.0, "OD600": "especial",
            "MOI": "especial", "PFU/mL": 1.0, "UFC/mL": 1.0
        }
        
        # Cantidad de sustancia
        self.categorias["Cantidad sustancia"] = {
            "mol": 1.0, "mmol": 1e-3, "µmol": 1e-6, "nmol": 1e-9,
            "pmol": 1e-12, "fmol": 1e-15
        }
        
        # Viscosidad
        self.categorias["Viscosidad"] = {
            "Pa·s": 1.0, "mPa·s": 1e-3, "P": 0.1, "cP": 1e-3,
            "kg/(m·s)": 1.0
        }
        
        # Conductividad electrica
        self.categorias["Conductividad"] = {
            "S/m": 1.0, "mS/cm": 0.1, "µS/cm": 1e-4,
            "S/cm": 100.0, "mS/m": 0.001
        }
    
    def _cargar_compuestos(self):
        """Carga la base de datos de compuestos quimicos."""
        ruta = os.path.join(os.path.dirname(__file__), "datos", "compuestos_quimicos.csv")
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    nombre = fila['nombre']
                    self.compuestos[nombre] = {
                        'formula': fila['formula'],
                        'peso': float(fila['peso_molecular']),
                        'categoria': fila['categoria']
                    }
        except:
            # Datos minimos por defecto si falla el archivo
            self.compuestos = {
                "NaCl": {'formula': 'NaCl', 'peso': 58.44, 'categoria': 'sal'},
                "KCl": {'formula': 'KCl', 'peso': 74.55, 'categoria': 'sal'},
                "Glucosa": {'formula': 'C6H12O6', 'peso': 180.16, 'categoria': 'azucar'}
            }
    
    def _cargar_factores_od(self):
        """Carga factores de conversion OD600 para diferentes organismos."""
        ruta = os.path.join(os.path.dirname(__file__), "datos", "factores_od.csv")
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    self.factores_od[fila['organismo']] = float(fila['factor_cel_ml'])
        except:
            self.factores_od = FACTORES_OD600
    
    def obtener_categorias(self):
        return list(self.categorias.keys())
    
    def obtener_unidades(self, categoria):
        if categoria in self.categorias:
            return list(self.categorias[categoria].keys())
        return []
    
    def convertir(self, valor, desde, hacia, categoria, incertidumbre=0.0):
        """
        Convierte un valor entre unidades.
        Retorna: (resultado, incertidumbre_resultado, advertencia)
        """
        advertencia = ""
        
        # Validaciones
        if categoria == "Temperatura":
            valido, msg = validar_temperatura(valor, desde)
            if not valido:
                return 0.0, 0.0, msg
        
        if categoria == "Velocidad" and desde == "c":
            if valor > 1.0:
                advertencia = "Velocidad mayor que c (relatividad)"
        
        # Conversion
        if categoria == "Temperatura":
            resultado = self._convertir_temperatura(valor, desde, hacia)
            factor_efectivo = resultado / valor if valor != 0 else 1.0
        elif categoria == "Microbiologia":
            resultado = self._convertir_microbiologia(valor, desde, hacia)
            factor_efectivo = resultado / valor if valor != 0 else 1.0
        elif categoria == "Concentracion":
            resultado = self._convertir_concentracion(valor, desde, hacia)
            factor_efectivo = resultado / valor if valor != 0 else 1.0
        else:
            factores = self.categorias[categoria]
            factor_desde = factores[desde]
            factor_hacia = factores[hacia]
            
            if factor_desde == "manometrica":
                advertencia = "Conversion psig requiere presion atmosferica. Asumiendo 1 atm."
                factor_desde = 6894.757293168 + 101325.0
            
            resultado = valor * factor_desde / factor_hacia
            factor_efectivo = factor_desde / factor_hacia
        
        # Propagar incertidumbre
        inc_resultado = GestorIncertidumbre.propagar_lineal(valor, incertidumbre, factor_efectivo)
        
        return resultado, inc_resultado, advertencia
    
    def _convertir_temperatura(self, valor, desde, hacia):
        """Conversion especial para temperaturas."""
        # Convertir a Kelvin
        if desde == "°C":
            kelvin = valor + KELVIN_OFFSET
        elif desde == "K":
            kelvin = valor
        elif desde == "°F":
            kelvin = (valor - 32) * FACTOR_F_A_C + KELVIN_OFFSET
        elif desde == "°R":
            kelvin = valor * FACTOR_F_A_C
        else:
            return valor
        
        # Convertir a unidad destino
        if hacia == "°C":
            return kelvin - KELVIN_OFFSET
        elif hacia == "K":
            return kelvin
        elif hacia == "°F":
            return (kelvin - KELVIN_OFFSET) * FACTOR_C_A_F + 32
        elif hacia == "°R":
            return kelvin * FACTOR_C_A_F
        return kelvin
    
    def _convertir_microbiologia(self, valor, desde, hacia):
        """Conversiones microbiologicas especiales."""
        if desde == hacia:
            return valor
        
        # Si es OD600, convertir a celulas/mL
        if desde == "OD600" or hacia == "OD600":
            if valor < 0 or valor > 4.0:
                # Advertencia: fuera de rango lineal
                pass
            
            # Usar factor E. coli por defecto
            factor = self.factores_od.get("E. coli", 8e8)
            
            if desde == "OD600":
                return valor * factor if hacia == "celulas/mL" else valor * factor
            else:
                return valor / factor
    
    def _convertir_concentracion(self, valor, desde, hacia):
        """Conversion de concentraciones con manejo de unidades masa/volumen."""
        factores = self.categorias["Concentracion"]
        
        # Si ambas son molares normales
        if desde in factores and hacia in factores:
            f_desde = factores[desde]
            f_hacia = factores[hacia]
            if isinstance(f_desde, (int, float)) and isinstance(f_hacia, (int, float)):
                return valor * f_desde / f_hacia
        
        return valor  # Placeholder
    
    def calcular_dilucion(self, c1, v1, c2, v2, inc_c1=0, inc_v1=0):
        """
        Calcula el parametro faltante en C1V1 = C2V2.
        Retorna diccionario con resultado e incertidumbre.
        """
        if c1 is None:
            c1 = (c2 * v2) / v1
            inc = GestorIncertidumbre.propagar_producto(c2, inc_c1, v2/v1, 0)
            return {'c1': c1, 'incertidumbre': inc}
        elif v1 is None:
            v1 = (c2 * v2) / c1
            inc = GestorIncertidumbre.propagar_producto(c2, 0, v2/c1, inc_v1)
            return {'v1': v1, 'incertidumbre': inc}
        elif c2 is None:
            c2 = (c1 * v1) / v2
            inc = GestorIncertidumbre.propagar_producto(c1, inc_c1, v1/v2, 0)
            return {'c2': c2, 'incertidumbre': inc}
        elif v2 is None:
            v2 = (c1 * v1) / c2
            inc = GestorIncertidumbre.propagar_producto(c1, inc_c1, v1/c2, 0)
            return {'v2': v2, 'incertidumbre': inc}
        else:
            return {'error': 'Todos los parametros especificados'}
    
    def calcular_molaridad(self, masa, volumen, peso_molecular, unidad_volumen="L"):
        """
        Calcula molaridad a partir de masa y volumen.
        """
        # Convertir volumen a litros
        if unidad_volumen == "mL":
            vol_L = volumen / 1000.0
        elif unidad_volumen == "µL":
            vol_L = volumen / 1e6
        else:
            vol_L = volumen
        
        moles = masa / peso_molecular
        molaridad = moles / vol_L
        
        return molaridad
    
    def calcular_moi(self, vp, celulas, factor_dilucion=1.0):
        """
        Calcula MOI (Multiplicity of Infection).
        MOI = (PFU * factor_dilucion) / numero_celulas
        """
        if celulas == 0:
            return float('inf')
        return (vp * factor_dilucion) / celulas
    
    def obtener_densidad_agua(self, temperatura_c):
        """Interpola la densidad del agua a una temperatura dada."""
        if temperatura_c in DENSIDAD_AGUA:
            return DENSIDAD_AGUA[temperatura_c]
        
        # Interpolacion lineal simple
        temps = sorted(DENSIDAD_AGUA.keys())
        if temperatura_c <= temps[0]:
            return DENSIDAD_AGUA[temps[0]]
        if temperatura_c >= temps[-1]:
            return DENSIDAD_AGUA[temps[-1]]
        
        for i in range(len(temps) - 1):
            if temps[i] <= temperatura_c <= temps[i + 1]:
                t1, t2 = temps[i], temps[i + 1]
                d1, d2 = DENSIDAD_AGUA[t1], DENSIDAD_AGUA[t2]
                return d1 + (d2 - d1) * (temperatura_c - t1) / (t2 - t1)
        
        return 0.997  # Valor por defecto