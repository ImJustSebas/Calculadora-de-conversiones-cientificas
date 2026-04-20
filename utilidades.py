# utilidades.py
# Funciones de apoyo para formato, validacion y calculos basicos

import re
import math
from decimal import Decimal, localcontext

def contar_cifras_significativas(texto_numero):
    """
    Cuenta cifras significativas de una cadena.
    Reconoce notacion cientifica.
    """
    if not texto_numero or texto_numero.strip() == "":
        return 0
    
    texto = texto_numero.strip().lower()
    
    # Notacion cientifica: extraer mantisa
    match = re.match(r'^([+-]?\d*\.?\d+)[eE]([+-]?\d+)$', texto)
    if match:
        texto = match.group(1)
    
    # Eliminar signo
    if texto.startswith('+') or texto.startswith('-'):
        texto = texto[1:]
    
    # Eliminar ceros a la izquierda
    texto_sin_ceros_izq = texto.lstrip('0')
    
    # Caso especial: solo ceros
    if not texto_sin_ceros_izq or texto_sin_ceros_izq == '.':
        if '.' in texto:
            # 0.0 tiene 1 cifra significativa si hay punto
            return 1
        return 0
    
    if '.' in texto:
        # Con punto decimal: todos los digitos cuentan
        digitos = texto_sin_ceros_izq.replace('.', '')
        return len(digitos)
    else:
        # Sin punto: ceros finales ambiguos, no se cuentan
        digitos = texto_sin_ceros_izq.rstrip('0')
        return len(digitos)

def redondear_cifras_significativas(valor, n_cifras):
    """Redondea un numero a n cifras significativas."""
    if valor == 0:
        return 0.0
    if n_cifras <= 0:
        return valor
    
    # Usar Decimal para mayor precision en calculos criticos
    with localcontext() as ctx:
        ctx.prec = n_cifras + 5
        dec = Decimal(str(valor))
        signo, digitos, exponente = dec.as_tuple()
        
        if digitos == (0,):
            return 0.0
        
        magnitud = len(digitos) + exponente - 1
        factor = 10 ** (n_cifras - 1 - magnitud)
        return round(valor * factor) / factor

def formatear_numero(valor, cientifico=False, n_cifras=None):
    """
    Formatea un numero segun preferencias.
    Devuelve cadena formateada.
    """
    if n_cifras is not None and n_cifras > 0:
        valor = redondear_cifras_significativas(valor, n_cifras)
    
    if cientifico:
        if valor == 0:
            return "0.0×10⁰"
        
        exponente = int(math.floor(math.log10(abs(valor))))
        mantisa = valor / (10 ** exponente)
        
        # Superindices para el exponente
        mapa_super = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
        exp_str = str(exponente).translate(mapa_super)
        
        if n_cifras:
            formato = f"{{:.{n_cifras-1}f}}"
            mantisa_str = formato.format(mantisa)
        else:
            mantisa_str = f"{mantisa:.6f}".rstrip('0').rstrip('.')
        
        return f"{mantisa_str}×10{exp_str}"
    else:
        if n_cifras:
            if valor == 0:
                decimales = n_cifras - 1
            else:
                magnitud = int(math.floor(math.log10(abs(valor))))
                decimales = max(0, n_cifras - 1 - magnitud)
            return f"{valor:.{decimales}f}"
        else:
            return f"{valor:.6g}"

def interpretar_numero(texto):
    """
    Convierte texto a float, aceptando coma o punto decimal.
    """
    if not texto:
        raise ValueError("Texto vacio")
    
    # Normalizar separadores
    texto = texto.strip()
    texto = texto.replace(',', '.')
    
    # Manejar notacion con ×10
    if '×10' in texto:
        texto = texto.replace('×10', 'e')
    
    # Manejar superindices comunes (copiar/pegar)
    texto = texto.replace('⁻', '-').replace('⁺', '+')
    for i, sup in enumerate('⁰¹²³⁴⁵⁶⁷⁸⁹'):
        texto = texto.replace(sup, str(i))
    
    return float(texto)

def formato_incertidumbre(valor, incertidumbre, estilo="ISO"):
    """
    Formatea valor ± incertidumbre segun normas.
    estilo: "ISO", "compacto", "expandido"
    """
    if incertidumbre == 0:
        return str(valor)
    
    if estilo == "ISO":
        # Formato ISO: 1.234(12) para 1.234 ± 0.012
        # Encontrar la posicion del ultimo digito significativo de la incertidumbre
        inc_str = f"{incertidumbre:.10f}".rstrip('0')
        if '.' in inc_str:
            decimales_inc = len(inc_str.split('.')[1])
        else:
            decimales_inc = 0
        
        valor_str = f"{valor:.{decimales_inc}f}"
        # Extraer los digitos de la incertidumbre sin punto
        digitos_inc = inc_str.replace('.', '').lstrip('0')
        return f"{valor_str}({digitos_inc})"
    
    elif estilo == "compacto":
        return f"{valor}±{incertidumbre}"
    
    else:  # expandido
        return f"{valor} ± {incertidumbre}"

def validar_temperatura(valor, unidad):
    """Verifica que la temperatura no este por debajo del cero absoluto."""
    if unidad == "K" and valor < 0:
        return False, "La temperatura en Kelvin no puede ser negativa."
    if unidad == "°C" and valor < CERO_ABSOLUTO:
        return False, f"Temperatura bajo cero absoluto ({CERO_ABSOLUTO} °C)"
    if unidad == "°F" and valor < -459.67:
        return False, "Temperatura bajo cero absoluto (-459.67 °F)"
    return True, ""