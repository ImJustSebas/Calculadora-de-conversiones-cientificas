# calculos_auxiliares.py
# Calculadoras especializadas para laboratorio

from logica_conversion import MotorConversiones
from gestor_incertidumbre import GestorIncertidumbre

class CalculadoraDiluciones:
    
    def __init__(self, motor=None):
        self.motor = motor if motor else MotorConversiones()
    
    def resolver_c1v1_c2v2(self, c1=None, v1=None, c2=None, v2=None):
        """
        Resuelve la ecuacion C1V1 = C2V2 para el parametro faltante.
        """
        parametros = [c1, v1, c2, v2]
        if parametros.count(None) != 1:
            return {"error": "Debe faltar exactamente un parametro"}
        
        if c1 is None:
            return {"c1": (c2 * v2) / v1}
        elif v1 is None:
            return {"v1": (c2 * v2) / c1}
        elif c2 is None:
            return {"c2": (c1 * v1) / v2}
        elif v2 is None:
            return {"v2": (c1 * v1) / c2}
    
    def dilucion_seriada(self, concentracion_inicial, factor_dilucion, num_pasos):
        """
        Calcula concentraciones en una dilucion seriada.
        Retorna lista de concentraciones.
        """
        concentraciones = []
        c_actual = concentracion_inicial
        
        for i in range(num_pasos + 1):
            concentraciones.append(c_actual)
            c_actual = c_actual / factor_dilucion
        
        return concentraciones
    
    def preparar_disolucion(self, concentracion_deseada, volumen_deseado, 
                           concentracion_stock, unidad_concentracion="M"):
        """
        Calcula el volumen de stock necesario.
        """
        # Verificar unidades compatibles
        volumen_stock = (concentracion_deseada * volumen_deseado) / concentracion_stock
        volumen_disolvente = volumen_deseado - volumen_stock
        
        return {
            "volumen_stock": volumen_stock,
            "volumen_disolvente": volumen_disolvente,
            "volumen_total": volumen_deseado
        }


class CalculadoraPesos:
    
    def __init__(self, motor=None):
        self.motor = motor if motor else MotorConversiones()
    
    def masa_para_molaridad(self, molaridad_deseada, volumen_L, peso_molecular):
        """Calcula masa necesaria para preparar una solucion molar."""
        moles_necesarios = molaridad_deseada * volumen_L
        masa_necesaria = moles_necesarios * peso_molecular
        return masa_necesaria
    
    def molaridad_desde_masa(self, masa_g, volumen_L, peso_molecular):
        """Calcula molaridad resultante."""
        moles = masa_g / peso_molecular
        return moles / volumen_L
    
    def porcentaje_peso_volumen(self, masa_soluto_g, volumen_total_mL):
        """Calcula % (p/v)."""
        return (masa_soluto_g / volumen_total_mL) * 100
    
    def ppm_desde_masa_volumen(self, masa_mg, volumen_L):
        """Calcula ppm (partes por millon)."""
        # 1 ppm = 1 mg/L para soluciones acuosas
        return masa_mg / volumen_L


class CalculadoraMOI:
    
    def __init__(self):
        self.factores_od = {}
    
    def calcular_moi(self, pfu_mL, volumen_inoculo_uL, celulas_por_pocillo):
        """
        Calcula MOI para infeccion viral.
        pfu_mL: titulo viral en PFU/mL
        volumen_inoculo_uL: volumen de virus añadido
        celulas_por_pocillo: numero de celulas en el pocillo
        """
        pfu_totales = pfu_mL * (volumen_inoculo_uL / 1000.0)
        moi = pfu_totales / celulas_por_pocillo
        return moi
    
    def volumen_para_moi(self, moi_deseado, celulas, pfu_mL):
        """Calcula volumen de virus necesario para un MOI especifico."""
        pfu_necesarias = moi_deseado * celulas
        volumen_uL = (pfu_necesarias / pfu_mL) * 1000.0
        return volumen_uL
    
    def celulas_desde_od(self, od600, organismo="E. coli", volumen_mL=1.0):
        """Estima numero de celulas a partir de OD600."""
        from constantes import FACTORES_OD600
        factor = FACTORES_OD600.get(organismo, 8e8)
        celulas_por_mL = od600 * factor
        return celulas_por_mL * volumen_mL


class CalculadoraTampones:
    """Calculos para preparacion de tampones."""
    
    @staticmethod
    def ph_henderson_hasselbalch(pka, concentracion_base, concentracion_acido):
        """Calcula pH de un tampon."""
        import math
        if concentracion_acido <= 0:
            return 14.0
        return pka + math.log10(concentracion_base / concentracion_acido)
    
    @staticmethod
    def fuerza_ionica(concentraciones, cargas):
        """
        Calcula fuerza ionica I = 0.5 * Σ(ci * zi²)
        concentraciones: lista de concentraciones molares
        cargas: lista de cargas correspondientes
        """
        if len(concentraciones) != len(cargas):
            raise ValueError("Listas de diferente longitud")
        
        suma = sum(c * (z ** 2) for c, z in zip(concentraciones, cargas))
        return 0.5 * suma