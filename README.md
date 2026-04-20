# Conversor Cientifico Profesional

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)
![Plataforma](https://img.shields.io/badge/Plataforma-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

Herramienta de conversion de unidades disenada para laboratorios cientificos. Ofrece una interfaz grafica para convertir unidades en quimica, fisica y microbiologia, siguiendo estandares metrologicos: propagacion de incertidumbre, cifras significativas y registro de auditoria.

## Contenido

- [Caracteristicas](#caracteristicas)
- [Instalacion](#instalacion)
- [Uso](#uso)
  - [Conversor Principal](#conversor-principal)
  - [Calculadora de Diluciones](#calculadora-de-diluciones)
  - [Molaridad y Masa](#molaridad-y-masa)
  - [Herramientas de Microbiologia](#herramientas-de-microbiologia)
  - [Historial de Auditoria](#historial-de-auditoria)
- [Configuracion](#configuracion)
- [Estructura de Archivos](#estructura-de-archivos)
- [Personalizacion](#personalizacion)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Caracteristicas

### Motor de Conversion Principal
- **Amplia base de unidades**: Mas de 150 unidades en 15 categorias (longitud, masa, volumen, temperatura, presion, energia, concentracion, radiactividad, microbiologia, etc.).
- **Cifras significativas automaticas**: Detecta las cifras significativas del valor ingresado y ajusta el resultado. Se puede fijar manualmente.
- **Notacion cientifica opcional**: Muestra resultados en formato normal o cientifico con superindices.
- **Propagacion de incertidumbre**: Ingrese la incertidumbre de la medicion (±) y el programa calcula la incertidumbre del resultado usando el metodo de propagacion lineal. El resultado se muestra con formato ISO/IEC 17025 (ej. `1,234(12)`).

### Modulos Especializados
- **Base de datos de compuestos**: Mas de 40 reactivos comunes (NaCl, Tris, EDTA, antibioticos, etc.) con sus pesos moleculares. Seleccione un compuesto para cargar automaticamente su masa molar en calculos de concentracion.
- **Calculadora de diluciones**: Resuelve el parametro faltante en la ecuacion C1V1 = C2V2. Tambien genera series de dilucion.
- **Calculos de molaridad**: Convierta entre masa, volumen y molaridad para cualquier compuesto de la base de datos.
- **Herramientas de microbiologia**:
  - Conversion de OD600 a densidad celular para E. coli, S. cerevisiae, CHO, HEK293, entre otros.
  - Calculadora de MOI (Multiplicidad de Infeccion) para experimentos de transduccion viral.
- **Densidad del agua variable**: Corrige la densidad del agua segun la temperatura de referencia configurada para conversiones precisas masa/volumen.

### Trazabilidad y Calidad
- **Registro de auditoria**: Cada conversion se guarda con fecha, hora, valor de entrada, incertidumbre, unidades, resultado y factor utilizado.
- **Exportacion de historial**: Guarde el registro en formato CSV (compatible con LIMS) o JSON.
- **Alertas de limites fisicos**: Avisa si un valor supera limites fisicos (ej. temperatura bajo cero absoluto, velocidad mayor que c).
- **Avisos contextuales**: Diferencia entre presion absoluta y manometrica, advierte sobre el rango lineal del OD600.

### Interfaz de Usuario
- **Interfaz con pestanas**: Organizada en secciones logicas para acceso rapido.
- **Modo oscuro**: Alterne entre tema claro y oscuro para trabajar en ambientes con poca luz.
- **Atajos de teclado**:
  - `Ctrl+L` – Limpiar campos de entrada
  - `Ctrl+R` – Intercambiar unidades origen y destino
  - `Ctrl+C` – Copiar resultado al portapapeles
  - `Ctrl+Q` – Salir de la aplicacion
- **Separador decimal flexible**: Acepta tanto punto (1.23) como coma (1,23).

## Instalacion

### Requisitos
- Python 3.8 o superior
- Tkinter (incluido por defecto en Python para Windows y macOS; en Linux instalar con `sudo apt-get install python3-tk`)

### Pasos
1. Clone el repositorio:
   ```bash
   git clone https://github.com/suusuario/conversor-cientifico.git
   cd conversor-cientifico
No se requieren dependencias externas. Todo se ejecuta con la biblioteca estandar de Python.

Ejecute la aplicacion:

bash
python main.py
Uso
Conversor Principal
Seleccione una categoria del desplegable (ej. "Concentracion").

Ingrese el valor numerico (opcionalmente con incertidumbre en el campo "± Incertidumbre").

Elija las unidades de origen y destino.

El resultado se actualiza automaticamente si esta marcada la opcion "Convertir automaticamente", o pulse "Convertir".

Use el panel "Opciones" para alternar notacion cientifica o fijar cifras significativas.

Calculadora de Diluciones
Vaya a la pestana "Diluciones":

C1·V1 = C2·V2: Deje un campo en blanco y pulse "Calcular faltante".

Dilucion seriada: Ingrese concentracion inicial, factor de dilucion y numero de pasos para generar la secuencia.

Molaridad y Masa
Vaya a la pestana "Molaridad":

Seleccione un compuesto del desplegable para cargar su peso molecular.

Masa a Molaridad: Ingrese masa, volumen y unidad de volumen para calcular la concentracion.

Molaridad a Masa: Ingrese la concentracion deseada y el volumen para obtener la masa necesaria.

Herramientas de Microbiologia
Vaya a la pestana "Microbiologia":

Conversion OD600: Seleccione el organismo e ingrese el valor de OD para estimar celulas/mL.

Calculo de MOI: Proporcione titulo viral, volumen de inoculo y numero de celulas por pocillo.

Historial de Auditoria
La pestana "Historial" muestra todas las conversiones realizadas durante la sesion. Use los botones para:

Actualizar la vista.

Exportar a CSV o JSON.

Limpiar la vista (no borra el archivo de registro).

Configuracion
Las preferencias se guardan en el archivo preferencias.json (creado en la primera ejecucion) y se pueden modificar desde la pestana "Configuracion":

Apariencia: Activar modo oscuro.

Formato de incertidumbre: Elegir entre ISO, compacto o expandido.

Cifras para incertidumbre: Fijar en 1 o 2 (practica estandar).

Separador decimal: Automatico, forzar punto o forzar coma.

Temperatura de referencia: Usada para correcciones de densidad del agua (por defecto 20 °C).

Estructura de Archivos
text
conversor_profesional/
├── main.py                     # Punto de entrada de la aplicacion
├── ventana_principal.py        # Interfaz grafica y manejo de eventos
├── logica_conversion.py        # Factores de conversion y motor principal
├── calculos_auxiliares.py      # Calculadoras especializadas (diluciones, MOI, etc.)
├── gestor_incertidumbre.py     # Rutinas de propagacion de errores
├── registro_auditoria.py       # Registro de auditoria y exportacion
├── utilidades.py               # Formateo, analisis y validacion
├── configuracion.py            # Gestion de preferencias de usuario
├── constantes.py               # Constantes fisicas y datos de referencia
├── datos/
│   ├── compuestos_quimicos.csv # Base de datos de compuestos (nombre, formula, PM, categoria)
│   ├── factores_od.csv         # Factores de conversion OD600 por organismo
│   └── unidades_personalizadas.txt # Definiciones de unidades propias del usuario
└── historial_conversiones.csv  # Registro de auditoria persistente (auto-generado)
Personalizacion
Agregar Nuevos Compuestos
Edite el archivo datos/compuestos_quimicos.csv y anada una nueva linea con el formato:

text
nombre,formula,peso_molecular,categoria
Agregar Unidades Propias
Abra datos/unidades_personalizadas.txt.

Anada una linea siguiendo el formato: Categoria | Unidad | FactorBase | UnidadBase

Reinicie la aplicacion.

Ampliar Categorias de Conversion
Modifique el metodo _inicializar_categorias en logica_conversion.py para incluir nuevos diccionarios de categoria. Para conversiones no lineales (como temperatura), agregue el manejo especial en el metodo convertir.

Contribuciones
Las contribuciones son bienvenidas. Siga estos pasos:

Haga un fork del repositorio.

Cree una rama para su funcionalidad (git checkout -b feature/nueva-funcionalidad).

Realice sus cambios con mensajes de commit claros y descriptivos.

Envie un Pull Request.

Antes de enviar, asegurese de que:

El codigo sigue las recomendaciones de estilo PEP 8.

Las nuevas funcionalidades incluyen comentarios en espanol (idioma principal del proyecto).

La aplicacion se ejecuta sin errores en una instalacion limpia.
