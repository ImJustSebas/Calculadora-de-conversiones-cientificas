# registro_auditoria.py
# Sistema de trazabilidad y registro de conversiones

import os
import csv
import json
from datetime import datetime

class RegistroAuditoria:
    
    def __init__(self):
        self.ruta_log = os.path.join(os.path.dirname(__file__), "historial_conversiones.csv")
        self.historial_memoria = []
        self.max_registros_memoria = 100
        self._inicializar_archivo()
    
    def _inicializar_archivo(self):
        """Crea el archivo CSV con cabeceras si no existe."""
        if not os.path.exists(self.ruta_log):
            with open(self.ruta_log, 'w', newline='', encoding='utf-8') as f:
                escritor = csv.writer(f)
                escritor.writerow([
                    "fecha_hora", "categoria", "valor_entrada", "incertidumbre_entrada",
                    "unidad_origen", "valor_salida", "incertidumbre_salida", 
                    "unidad_destino", "factor_conversion", "cifras_significativas", "notas"
                ])
    
    def registrar_conversion(self, categoria, valor_entrada, inc_entrada, unidad_origen,
                            valor_salida, inc_salida, unidad_destino, 
                            cifras=None, notas=""):
        """
        Registra una conversion en el historial.
        """
        fecha = datetime.now().isoformat(timespec='seconds')
        factor = valor_salida / valor_entrada if valor_entrada != 0 else 0
        
        registro = {
            "fecha_hora": fecha,
            "categoria": categoria,
            "valor_entrada": valor_entrada,
            "incertidumbre_entrada": inc_entrada,
            "unidad_origen": unidad_origen,
            "valor_salida": valor_salida,
            "incertidumbre_salida": inc_salida,
            "unidad_destino": unidad_destino,
            "factor_conversion": factor,
            "cifras_significativas": cifras,
            "notas": notas
        }
        
        # Guardar en memoria
        self.historial_memoria.append(registro)
        if len(self.historial_memoria) > self.max_registros_memoria:
            self.historial_memoria.pop(0)
        
        # Guardar en archivo
        try:
            with open(self.ruta_log, 'a', newline='', encoding='utf-8') as f:
                escritor = csv.writer(f)
                escritor.writerow([
                    fecha, categoria, valor_entrada, inc_entrada, unidad_origen,
                    valor_salida, inc_salida, unidad_destino, factor, cifras, notas
                ])
        except Exception as e:
            print(f"Error al registrar: {e}")
    
    def obtener_historial(self, limite=20):
        """Retorna los ultimos n registros."""
        return self.historial_memoria[-limite:]
    
    def exportar_csv(self, ruta_destino=None):
        """Exporta el historial completo a un archivo CSV."""
        if ruta_destino is None:
            ruta_destino = self.ruta_log
        
        # Leer todo y copiar
        try:
            with open(self.ruta_log, 'r', encoding='utf-8') as origen:
                contenido = origen.read()
            with open(ruta_destino, 'w', encoding='utf-8') as destino:
                destino.write(contenido)
            return True
        except:
            return False
    
    def exportar_json(self, ruta_destino):
        """Exporta el historial en formato JSON."""
        try:
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                json.dump(self.historial_memoria, f, indent=2, default=str)
            return True
        except:
            return False
    
    def limpiar_historial(self):
        """Limpia el historial en memoria (el archivo se mantiene)."""
        self.historial_memoria = []