# gestor_incertidumbre.py
# Calculo de propagacion de errores

import math

class GestorIncertidumbre:
    
    @staticmethod
    def propagar_lineal(valor, incertidumbre, factor):
        """
        Para conversion lineal: y = a * x
        Incertidumbre: u(y) = |a| * u(x)
        """
        return abs(factor) * incertidumbre
    
    @staticmethod
    def propagar_suma(valores, incertidumbres):
        """
        Para suma/resta: u² = Σ u_i²
        """
        suma_cuadrados = sum(u**2 for u in incertidumbres)
        return math.sqrt(suma_cuadrados)
    
    @staticmethod
    def propagar_producto(valor1, inc1, valor2, inc2):
        """
        Para multiplicacion: u(y)/|y| = sqrt((u1/x1)² + (u2/x2)²)
        """
        if valor1 == 0 or valor2 == 0:
            return 0
        relativa1 = inc1 / abs(valor1)
        relativa2 = inc2 / abs(valor2)
        relativa_total = math.sqrt(relativa1**2 + relativa2**2)
        return abs(valor1 * valor2) * relativa_total
    
    @staticmethod
    def propagar_potencia(valor, incertidumbre, exponente):
        """
        Para potencia: u(y)/|y| = |n| * u(x)/|x|
        """
        if valor == 0:
            return 0
        return abs(valor) * abs(exponente) * (incertidumbre / abs(valor))
    
    @staticmethod
    def propagar_logaritmo(valor, incertidumbre, base='e'):
        """
        Para logaritmo natural: u(y) = u(x) / |x|
        """
        if valor == 0:
            return float('inf')
        inc = incertidumbre / abs(valor)
        if base != 'e':
            inc = inc / math.log(base)
        return inc
    
    @staticmethod
    def redondear_incertidumbre(incertidumbre, n_cifras=2):
        """
        Redondea la incertidumbre a n cifras significativas.
        Por convencion se usan 1 o 2 cifras.
        """
        if incertidumbre == 0:
            return 0.0, 0
        
        # Encontrar el primer digito significativo
        orden = int(math.floor(math.log10(incertidumbre)))
        
        # Normalizar
        normalizado = incertidumbre / (10 ** orden)
        
        # Redondear segun el numero de cifras deseado
        if n_cifras == 1:
            if normalizado < 1.5:
                redondeado = 1
            elif normalizado < 2.5:
                redondeado = 2
            elif normalizado < 3.5:
                redondeado = 3
            elif normalizado < 4.5:
                redondeado = 4
            elif normalizado < 6:
                redondeado = 5
            elif normalizado < 8:
                redondeado = 6
            else:
                redondeado = 10
        else:
            redondeado = round(normalizado, n_cifras - 1)
        
        inc_redondeada = redondeado * (10 ** orden)
        
        # Determinar decimales para el valor principal
        if inc_redondeada >= 1:
            decimales = 0
        else:
            decimales = abs(orden) + (n_cifras - 1)
        
        return inc_redondeada, decimales