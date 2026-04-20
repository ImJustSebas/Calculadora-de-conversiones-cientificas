# configuracion.py
# Variables globales y configuraciones de usuario

import os
import json

class ConfiguracionApp:
    _instancia = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia
    
    def _inicializar(self):
        # Ruta del archivo de configuracion
        self.ruta_config = os.path.join(os.path.dirname(__file__), "preferencias.json")
        
        # Valores por defecto
        self.config = {
            "precision_decimal": 6,
            "formato_incertidumbre": "ISO",  # ISO, compacto, expandido
            "cifras_incertidumbre": 2,
            "separador_decimal": "auto",  # auto, punto, coma
            "idioma": "es",
            "auto_convertir": True,
            "mostrar_historial": True,
            "validacion_limites": True,
            "temperatura_referencia": 20  # Para densidad del agua
        }
        self.cargar()
    
    def cargar(self):
        if os.path.exists(self.ruta_config):
            try:
                with open(self.ruta_config, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.config.update(datos)
            except:
                pass
    
    def guardar(self):
        try:
            with open(self.ruta_config, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def obtener(self, clave):
        return self.config.get(clave)
    
    def establecer(self, clave, valor):
        self.config[clave] = valor
        self.guardar()