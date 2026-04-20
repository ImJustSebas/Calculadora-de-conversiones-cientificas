# ventana_principal.py
# Interfaz grafica principal

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

from logica_conversion import MotorConversiones
from calculos_auxiliares import (CalculadoraDiluciones, CalculadoraPesos, 
                                  CalculadoraMOI, CalculadoraTampones)
from registro_auditoria import RegistroAuditoria
from configuracion import ConfiguracionApp
from utilidades import (contar_cifras_significativas, formatear_numero, 
                        interpretar_numero, formato_incertidumbre)
from gestor_incertidumbre import GestorIncertidumbre

class VentanaPrincipal:
    
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Conversor Cientifico Profesional")
        self.raiz.geometry("850x650")
        self.raiz.minsize(800, 600)
        
        # Inicializar componentes
        self.config = ConfiguracionApp()
        self.motor = MotorConversiones()
        self.registro = RegistroAuditoria()
        self.calc_diluciones = CalculadoraDiluciones(self.motor)
        self.calc_pesos = CalculadoraPesos(self.motor)
        self.calc_moi = CalculadoraMOI()
        self.calc_tampones = CalculadoraTampones()
        
        # Variables de control
        self.categoria_actual = tk.StringVar()
        self.unidad_origen = tk.StringVar()
        self.unidad_destino = tk.StringVar()
        self.valor_entrada = tk.StringVar()
        self.incertidumbre_entrada = tk.StringVar(value="0")
        self.resultado_valor = tk.StringVar()
        self.resultado_incertidumbre = tk.StringVar()
        self.resultado_formato = tk.StringVar()
        
        self.usar_cientifico = tk.BooleanVar(value=False)
        self.cifras_sig = tk.StringVar(value="Auto")
        self.auto_convertir = tk.BooleanVar(value=self.config.obtener("auto_convertir"))
        self.compuesto_seleccionado = tk.StringVar()
        self.organismo_seleccionado = tk.StringVar(value="E. coli")
        
        self._crear_interfaz()
        self._configurar_estilo()
        self._cargar_preferencias()
        self._vincular_eventos()
        
        # Cargar categoria inicial
        categorias = self.motor.obtener_categorias()
        self.categoria_actual.set(categorias[0])
        self._actualizar_unidades()
    
    def _crear_interfaz(self):
        """Construye todos los widgets de la interfaz."""
        
        # Frame principal con scroll
        self.canvas = tk.Canvas(self.raiz)
        scrollbar = ttk.Scrollbar(self.raiz, orient="vertical", command=self.canvas.yview)
        self.frame_principal = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.canvas.create_window((0, 0), window=self.frame_principal, anchor="nw")
        self.frame_principal.bind("<Configure>", self._ajustar_scroll)
        
        self.raiz.grid_rowconfigure(0, weight=1)
        self.raiz.grid_columnconfigure(0, weight=1)
        
        # Notebook para organizar secciones
        self.notebook = ttk.Notebook(self.frame_principal)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Pestana Conversor Principal
        self.pestana_conversor = ttk.Frame(self.notebook)
        self.notebook.add(self.pestana_conversor, text="Conversor")
        self._crear_pestana_conversor()
        
        # Pestana Diluciones
        self.pestana_diluciones = ttk.Frame(self.notebook)
        self.notebook.add(self.pestana_diluciones, text="Diluciones")
        self._crear_pestana_diluciones()
        
        # Pestana Molaridad
        self.pestana_molaridad = ttk.Frame(self.notebook)
        self.notebook.add(self.pestana_molaridad, text="Molaridad")
        self._crear_pestana_molaridad()
        
        # Pestana Microbiologia
        self.pestana_micro = ttk.Frame(self.notebook)
        self.notebook.add(self.pestana_micro, text="Microbiologia")
        self._crear_pestana_micro()
        
        # Pestana Historial
        self.pestana_historial = ttk.Frame(self.notebook)
        self.notebook.add(self.pestana_historial, text="Historial")
        self._crear_pestana_historial()
        
        # Pestana Configuracion
        self.pestana_config = ttk.Frame(self.notebook)
        self.notebook.add(self.pestana_config, text="Configuracion")
        self._crear_pestana_config()
        
        # Barra de estado
        self.barra_estado = ttk.Label(self.raiz, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.barra_estado.grid(row=1, column=0, columnspan=2, sticky="ew")
    
    def _crear_pestana_conversor(self):
        """Pestana principal de conversion."""
        frame = ttk.Frame(self.pestana_conversor, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Fila 0: Categoria
        ttk.Label(frame, text="Categoria:").grid(row=0, column=0, sticky="w", pady=3)
        combo_cat = ttk.Combobox(frame, textvariable=self.categoria_actual, 
                                 values=self.motor.obtener_categorias(), state="readonly")
        combo_cat.grid(row=0, column=1, columnspan=3, sticky="ew", pady=3)
        
        # Fila 1: Valor entrada
        ttk.Label(frame, text="Valor:").grid(row=1, column=0, sticky="w", pady=3)
        self.entry_valor = ttk.Entry(frame, textvariable=self.valor_entrada, width=20)
        self.entry_valor.grid(row=1, column=1, sticky="ew", pady=3)
        
        ttk.Label(frame, text="± Incertidumbre:").grid(row=1, column=2, sticky="e", padx=(10,0))
        self.entry_inc = ttk.Entry(frame, textvariable=self.incertidumbre_entrada, width=10)
        self.entry_inc.grid(row=1, column=3, sticky="w", pady=3)
        
        # Fila 2: Unidad origen
        ttk.Label(frame, text="De:").grid(row=2, column=0, sticky="w", pady=3)
        self.combo_origen = ttk.Combobox(frame, textvariable=self.unidad_origen, state="readonly")
        self.combo_origen.grid(row=2, column=1, sticky="ew", pady=3)
        
        # Boton invertir
        ttk.Button(frame, text="⇄", width=3, command=self._invertir_unidades).grid(row=2, column=2)
        
        # Fila 3: Unidad destino
        ttk.Label(frame, text="A:").grid(row=3, column=0, sticky="w", pady=3)
        self.combo_destino = ttk.Combobox(frame, textvariable=self.unidad_destino, state="readonly")
        self.combo_destino.grid(row=3, column=1, sticky="ew", pady=3)
        
        # Fila 4: Opciones
        frame_opciones = ttk.LabelFrame(frame, text="Opciones", padding="5")
        frame_opciones.grid(row=4, column=0, columnspan=4, sticky="ew", pady=10)
        
        ttk.Checkbutton(frame_opciones, text="Notacion cientifica", 
                       variable=self.usar_cientifico).grid(row=0, column=0, sticky="w")
        
        ttk.Label(frame_opciones, text="Cifras significativas:").grid(row=0, column=1, padx=(20,5))
        spin_sig = ttk.Spinbox(frame_opciones, from_=1, to=10, textvariable=self.cifras_sig, 
                              width=5, state="readonly")
        spin_sig.grid(row=0, column=2)
        ttk.Label(frame_opciones, text="(Auto = desde entrada)").grid(row=0, column=3, padx=5)
        
        ttk.Checkbutton(frame_opciones, text="Convertir automaticamente", 
                       variable=self.auto_convertir).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
        
        # Fila 5: Boton convertir
        self.btn_convertir = ttk.Button(frame, text="Convertir", command=self._ejecutar_conversion)
        self.btn_convertir.grid(row=5, column=0, columnspan=4, pady=10)
        
        # Fila 6: Resultado
        frame_resultado = ttk.LabelFrame(frame, text="Resultado", padding="10")
        frame_resultado.grid(row=6, column=0, columnspan=4, sticky="ew", pady=10)
        
        self.label_resultado = ttk.Label(frame_resultado, textvariable=self.resultado_formato, 
                                         font=("Segoe UI", 12, "bold"))
        self.label_resultado.pack()
        
        # Fila 7: Selector de compuesto (visible solo para ciertas categorias)
        self.frame_compuesto = ttk.Frame(frame)
        self.frame_compuesto.grid(row=7, column=0, columnspan=4, sticky="ew", pady=5)
        ttk.Label(self.frame_compuesto, text="Compuesto:").pack(side="left", padx=5)
        self.combo_compuesto = ttk.Combobox(self.frame_compuesto, 
                                           textvariable=self.compuesto_seleccionado,
                                           values=list(self.motor.compuestos.keys()),
                                           state="readonly", width=30)
        self.combo_compuesto.pack(side="left", fill="x", expand=True, padx=5)
        self.frame_compuesto.grid_remove()  # Ocultar inicialmente
        
        # Configurar pesos
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)
    
    def _crear_pestana_diluciones(self):
        """Pestana para calculos de diluciones."""
        frame = ttk.Frame(self.pestana_diluciones, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Seccion C1V1 = C2V2
        lbl_frame = ttk.LabelFrame(frame, text="C1·V1 = C2·V2", padding="10")
        lbl_frame.pack(fill="x", pady=5)
        
        # Entradas
        campos = [
            ("C1 (inicial):", "c1", 0),
            ("V1 (inicial):", "v1", 1),
            ("C2 (final):", "c2", 2),
            ("V2 (final):", "v2", 3)
        ]
        
        self.entradas_dilucion = {}
        for texto, clave, fila in campos:
            ttk.Label(lbl_frame, text=texto).grid(row=fila, column=0, sticky="e", pady=2, padx=5)
            entry = ttk.Entry(lbl_frame, width=15)
            entry.grid(row=fila, column=1, sticky="w", pady=2)
            self.entradas_dilucion[clave] = entry
        
        # Botones
        frame_botones = ttk.Frame(lbl_frame)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botones, text="Calcular faltante", 
                  command=self._calcular_dilucion).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Limpiar", 
                  command=self._limpiar_dilucion).pack(side="left", padx=5)
        
        # Resultado
        self.resultado_dilucion = ttk.Label(lbl_frame, text="", font=("Segoe UI", 10))
        self.resultado_dilucion.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Seccion Dilucion seriada
        lbl_seriada = ttk.LabelFrame(frame, text="Dilucion seriada", padding="10")
        lbl_seriada.pack(fill="x", pady=10)
        
        ttk.Label(lbl_seriada, text="Concentracion inicial:").grid(row=0, column=0, sticky="e")
        self.entrada_c_inicial = ttk.Entry(lbl_seriada, width=15)
        self.entrada_c_inicial.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(lbl_seriada, text="Factor dilucion:").grid(row=1, column=0, sticky="e", pady=5)
        self.entrada_factor = ttk.Entry(lbl_seriada, width=15)
        self.entrada_factor.insert(0, "10")
        self.entrada_factor.grid(row=1, column=1, sticky="w", padx=5)
        
        ttk.Label(lbl_seriada, text="Numero de pasos:").grid(row=2, column=0, sticky="e")
        self.entrada_pasos = ttk.Spinbox(lbl_seriada, from_=1, to=20, width=13)
        self.entrada_pasos.insert(0, "5")
        self.entrada_pasos.grid(row=2, column=1, sticky="w", padx=5)
        
        ttk.Button(lbl_seriada, text="Calcular serie", 
                  command=self._calcular_seriada).grid(row=3, column=0, columnspan=2, pady=10)
        
        self.texto_seriada = tk.Text(lbl_seriada, height=6, width=40)
        self.texto_seriada.grid(row=4, column=0, columnspan=2, pady=5)
    
    def _crear_pestana_molaridad(self):
        """Pestana para calculos de molaridad y masa."""
        frame = ttk.Frame(self.pestana_molaridad, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Selector de compuesto
        ttk.Label(frame, text="Seleccionar compuesto:").pack(anchor="w", pady=5)
        self.combo_comp_molar = ttk.Combobox(frame, 
                                            values=list(self.motor.compuestos.keys()),
                                            state="readonly", width=30)
        self.combo_comp_molar.pack(fill="x", pady=5)
        self.combo_comp_molar.bind('<<ComboboxSelected>>', self._mostrar_info_compuesto)
        
        self.info_compuesto = ttk.Label(frame, text="")
        self.info_compuesto.pack(anchor="w", pady=5)
        
        # Seccion masa -> molaridad
        frame_masa = ttk.LabelFrame(frame, text="Calcular molaridad desde masa", padding="10")
        frame_masa.pack(fill="x", pady=10)
        
        ttk.Label(frame_masa, text="Masa (g):").grid(row=0, column=0, sticky="e")
        self.entrada_masa = ttk.Entry(frame_masa, width=15)
        self.entrada_masa.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(frame_masa, text="Volumen:").grid(row=1, column=0, sticky="e", pady=5)
        self.entrada_volumen = ttk.Entry(frame_masa, width=15)
        self.entrada_volumen.grid(row=1, column=1, sticky="w", padx=5)
        
        self.combo_unidad_vol = ttk.Combobox(frame_masa, values=["L", "mL", "µL"], 
                                            state="readonly", width=5)
        self.combo_unidad_vol.set("L")
        self.combo_unidad_vol.grid(row=1, column=2, padx=5)
        
        ttk.Button(frame_masa, text="Calcular Molaridad", 
                  command=self._calcular_molaridad).grid(row=2, column=0, columnspan=3, pady=10)
        
        self.resultado_molaridad = ttk.Label(frame_masa, text="", font=("Segoe UI", 10))
        self.resultado_molaridad.grid(row=3, column=0, columnspan=3)
        
        # Seccion molaridad -> masa
        frame_molar = ttk.LabelFrame(frame, text="Calcular masa para molaridad deseada", padding="10")
        frame_molar.pack(fill="x", pady=10)
        
        ttk.Label(frame_molar, text="Molaridad deseada (M):").grid(row=0, column=0, sticky="e")
        self.entrada_molar_deseada = ttk.Entry(frame_molar, width=15)
        self.entrada_molar_deseada.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(frame_molar, text="Volumen (L):").grid(row=1, column=0, sticky="e", pady=5)
        self.entrada_vol_molar = ttk.Entry(frame_molar, width=15)
        self.entrada_vol_molar.grid(row=1, column=1, sticky="w", padx=5)
        
        ttk.Button(frame_molar, text="Calcular Masa necesaria", 
                  command=self._calcular_masa_necesaria).grid(row=2, column=0, columnspan=2, pady=10)
        
        self.resultado_masa = ttk.Label(frame_molar, text="", font=("Segoe UI", 10))
        self.resultado_masa.grid(row=3, column=0, columnspan=2)
    
    def _crear_pestana_micro(self):
        """Pestana para calculos microbiologicos."""
        frame = ttk.Frame(self.pestana_micro, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Seccion OD600
        frame_od = ttk.LabelFrame(frame, text="Conversion OD600", padding="10")
        frame_od.pack(fill="x", pady=5)
        
        ttk.Label(frame_od, text="Organismo:").grid(row=0, column=0, sticky="e")
        combo_org = ttk.Combobox(frame_od, textvariable=self.organismo_seleccionado,
                                values=list(self.motor.factores_od.keys()),
                                state="readonly", width=20)
        combo_org.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(frame_od, text="Valor OD600:").grid(row=1, column=0, sticky="e", pady=5)
        self.entrada_od = ttk.Entry(frame_od, width=15)
        self.entrada_od.grid(row=1, column=1, sticky="w", padx=5)
        
        ttk.Button(frame_od, text="Convertir a celulas/mL", 
                  command=self._convertir_od).grid(row=2, column=0, columnspan=2, pady=10)
        
        self.resultado_od = ttk.Label(frame_od, text="", font=("Segoe UI", 10))
        self.resultado_od.grid(row=3, column=0, columnspan=2)
        
        # Seccion MOI
        frame_moi = ttk.LabelFrame(frame, text="Calculadora MOI", padding="10")
        frame_moi.pack(fill="x", pady=10)
        
        ttk.Label(frame_moi, text="Titulo viral (PFU/mL):").grid(row=0, column=0, sticky="e")
        self.entrada_pfu = ttk.Entry(frame_moi, width=15)
        self.entrada_pfu.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(frame_moi, text="Volumen inoculo (µL):").grid(row=1, column=0, sticky="e", pady=5)
        self.entrada_vol_moi = ttk.Entry(frame_moi, width=15)
        self.entrada_vol_moi.grid(row=1, column=1, sticky="w", padx=5)
        
        ttk.Label(frame_moi, text="Celulas por pocillo:").grid(row=2, column=0, sticky="e")
        self.entrada_celulas = ttk.Entry(frame_moi, width=15)
        self.entrada_celulas.grid(row=2, column=1, sticky="w", padx=5)
        
        ttk.Button(frame_moi, text="Calcular MOI", 
                  command=self._calcular_moi).grid(row=3, column=0, columnspan=2, pady=10)
        
        self.resultado_moi = ttk.Label(frame_moi, text="", font=("Segoe UI", 10))
        self.resultado_moi.grid(row=4, column=0, columnspan=2)
    
    def _crear_pestana_historial(self):
        """Pestana de historial de conversiones."""
        frame = ttk.Frame(self.pestana_historial, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Botones de exportacion
        frame_botones = ttk.Frame(frame)
        frame_botones.pack(fill="x", pady=5)
        
        ttk.Button(frame_botones, text="Exportar CSV", 
                  command=self._exportar_historial_csv).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Exportar JSON", 
                  command=self._exportar_historial_json).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Actualizar", 
                  command=self._actualizar_historial).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Limpiar vista", 
                  command=self._limpiar_historial).pack(side="left", padx=5)
        
        # Treeview para historial
        frame_tree = ttk.Frame(frame)
        frame_tree.pack(fill="both", expand=True)
        
        scroll_y = ttk.Scrollbar(frame_tree)
        scroll_y.pack(side="right", fill="y")
        
        scroll_x = ttk.Scrollbar(frame_tree, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        columnas = ("Fecha", "Categoria", "Valor", "De", "Resultado", "A")
        self.tree_historial = ttk.Treeview(frame_tree, columns=columnas, 
                                           show="headings",
                                           yscrollcommand=scroll_y.set,
                                           xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree_historial.yview)
        scroll_x.config(command=self.tree_historial.xview)
        
        for col in columnas:
            self.tree_historial.heading(col, text=col)
            self.tree_historial.column(col, width=120)
        
        self.tree_historial.pack(fill="both", expand=True)
    
    def _crear_pestana_config(self):
        """Pestana de configuracion."""
        frame = ttk.Frame(self.pestana_config, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Preferencias de formato
        frame_formato = ttk.LabelFrame(frame, text="Formato de resultados", padding="10")
        frame_formato.pack(fill="x", pady=5)
        
        ttk.Label(frame_formato, text="Estilo incertidumbre:").grid(row=0, column=0, sticky="e", pady=2)
        self.combo_estilo_inc = ttk.Combobox(frame_formato, 
                                            values=["ISO", "compacto", "expandido"],
                                            state="readonly", width=15)
        self.combo_estilo_inc.set(self.config.obtener("formato_incertidumbre"))
        self.combo_estilo_inc.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(frame_formato, text="Cifras en incertidumbre:").grid(row=1, column=0, sticky="e", pady=2)
        self.spin_cifras_inc = ttk.Spinbox(frame_formato, from_=1, to=2, width=5)
        self.spin_cifras_inc.insert(0, str(self.config.obtener("cifras_incertidumbre")))
        self.spin_cifras_inc.grid(row=1, column=1, sticky="w", padx=5)
        
        ttk.Label(frame_formato, text="Separador decimal:").grid(row=2, column=0, sticky="e", pady=2)
        self.combo_sep_decimal = ttk.Combobox(frame_formato, 
                                             values=["auto", "punto", "coma"],
                                             state="readonly", width=10)
        self.combo_sep_decimal.set(self.config.obtener("separador_decimal"))
        self.combo_sep_decimal.grid(row=2, column=1, sticky="w", padx=5)
        
        ttk.Label(frame_formato, text="Temperatura referencia (°C):").grid(row=3, column=0, sticky="e", pady=2)
        self.spin_temp_ref = ttk.Spinbox(frame_formato, from_=0, to=100, width=5)
        self.spin_temp_ref.insert(0, str(self.config.obtener("temperatura_referencia")))
        self.spin_temp_ref.grid(row=3, column=1, sticky="w", padx=5)
        
        # Boton guardar
        ttk.Button(frame, text="Guardar configuracion", 
                  command=self._guardar_configuracion).pack(pady=20)
    
    def _configurar_estilo(self):
        """Configura el estilo visual."""
        self.estilo = ttk.Style()
    
    
    def _cargar_preferencias(self):
        """Carga preferencias guardadas."""
        pass
    
    def _vincular_eventos(self):
        """Vincula eventos de la interfaz."""
        self.categoria_actual.trace('w', lambda *a: self._actualizar_unidades())
        self.valor_entrada.trace('w', lambda *a: self._auto_convertir_si_activo())
        self.unidad_origen.trace('w', lambda *a: self._auto_convertir_si_activo())
        self.unidad_destino.trace('w', lambda *a: self._auto_convertir_si_activo())
        
        # Atajos de teclado
        self.raiz.bind('<Control-l>', lambda e: self._limpiar_campos())
        self.raiz.bind('<Control-r>', lambda e: self._invertir_unidades())
        self.raiz.bind('<Control-c>', lambda e: self._copiar_resultado())
        self.raiz.bind('<Control-q>', lambda e: self.raiz.quit())
    
    def _ajustar_scroll(self, event):
        """Ajusta el area de scroll."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _actualizar_unidades(self):
        """Actualiza las listas de unidades segun categoria."""
        cat = self.categoria_actual.get()
        if not cat:
            return
        
        unidades = self.motor.obtener_unidades(cat)
        self.combo_origen['values'] = unidades
        self.combo_destino['values'] = unidades
        
        if unidades:
            self.unidad_origen.set(unidades[0])
            self.unidad_destino.set(unidades[1] if len(unidades) > 1 else unidades[0])
        
        # Mostrar selector de compuesto para categorias relevantes
        if cat in ["Concentracion", "Masa"]:
            self.frame_compuesto.grid()
        else:
            self.frame_compuesto.grid_remove()
    
    def _auto_convertir_si_activo(self):
        """Ejecuta conversion si auto_convertir esta activo."""
        if self.auto_convertir.get():
            self._ejecutar_conversion()
    
    def _ejecutar_conversion(self):
        """Realiza la conversion y muestra el resultado."""
        try:
            valor = interpretar_numero(self.valor_entrada.get())
            inc = interpretar_numero(self.incertidumbre_entrada.get() or "0")
        except ValueError:
            self.resultado_formato.set("Error: Valor numerico invalido")
            return
        
        cat = self.categoria_actual.get()
        origen = self.unidad_origen.get()
        destino = self.unidad_destino.get()
        
        if not cat or not origen or not destino:
            return
        
        # Ejecutar conversion
        resultado, inc_resultado, advertencia = self.motor.convertir(
            valor, origen, destino, cat, inc
        )
        
        # Determinar cifras significativas
        cifras = None
        if self.cifras_sig.get() != "Auto":
            try:
                cifras = int(self.cifras_sig.get())
            except:
                pass
        else:
            cifras = contar_cifras_significativas(self.valor_entrada.get())
        
        # Formatear resultado
        if inc_resultado > 0:
            # Redondear incertidumbre
            inc_red, decimales = GestorIncertidumbre.redondear_incertidumbre(
                inc_resultado, 
                self.config.obtener("cifras_incertidumbre")
            )
            valor_red = round(resultado, decimales)
            
            estilo = self.config.obtener("formato_incertidumbre")
            texto = formato_incertidumbre(valor_red, inc_red, estilo)
        else:
            texto = formatear_numero(resultado, self.usar_cientifico.get(), cifras)
        
        self.resultado_formato.set(texto)
        
        # Registrar en historial
        self.registro.registrar_conversion(
            cat, valor, inc, origen, resultado, inc_resultado, destino, cifras
        )
        
        # Mostrar advertencia si existe
        if advertencia:
            self.barra_estado.config(text=f"Advertencia: {advertencia}")
        else:
            self.barra_estado.config(text="Conversion exitosa")
    
    def _invertir_unidades(self):
        """Intercambia unidades origen y destino."""
        org = self.unidad_origen.get()
        dst = self.unidad_destino.get()
        self.unidad_origen.set(dst)
        self.unidad_destino.set(org)
        self._auto_convertir_si_activo()
    
    def _limpiar_campos(self):
        """Limpia los campos de entrada."""
        self.valor_entrada.set("")
        self.incertidumbre_entrada.set("0")
        self.resultado_formato.set("")
    
    def _copiar_resultado(self):
        """Copia el resultado al portapapeles."""
        self.raiz.clipboard_clear()
        self.raiz.clipboard_append(self.resultado_formato.get())
        self.barra_estado.config(text="Resultado copiado")
    
    def _calcular_dilucion(self):
        """Calcula el parametro faltante en C1V1=C2V2."""
        try:
            c1 = float(self.entradas_dilucion['c1'].get()) if self.entradas_dilucion['c1'].get() else None
            v1 = float(self.entradas_dilucion['v1'].get()) if self.entradas_dilucion['v1'].get() else None
            c2 = float(self.entradas_dilucion['c2'].get()) if self.entradas_dilucion['c2'].get() else None
            v2 = float(self.entradas_dilucion['v2'].get()) if self.entradas_dilucion['v2'].get() else None
            
            resultado = self.calc_diluciones.resolver_c1v1_c2v2(c1, v1, c2, v2)
            
            if "error" in resultado:
                self.resultado_dilucion.config(text=resultado["error"])
            else:
                clave, valor = list(resultado.items())[0]
                self.resultado_dilucion.config(text=f"{clave} = {valor:.6g}")
        except ValueError:
            self.resultado_dilucion.config(text="Error: Valores invalidos")
    
    def _limpiar_dilucion(self):
        """Limpia campos de dilucion."""
        for entry in self.entradas_dilucion.values():
            entry.delete(0, tk.END)
        self.resultado_dilucion.config(text="")
    
    def _calcular_seriada(self):
        """Calcula dilucion seriada."""
        try:
            c_inicial = float(self.entrada_c_inicial.get())
            factor = float(self.entrada_factor.get())
            pasos = int(self.entrada_pasos.get())
            
            concentraciones = self.calc_diluciones.dilucion_seriada(c_inicial, factor, pasos)
            
            self.texto_seriada.delete(1.0, tk.END)
            for i, c in enumerate(concentraciones):
                self.texto_seriada.insert(tk.END, f"Paso {i}: {c:.4e}\n")
        except ValueError:
            self.texto_seriada.delete(1.0, tk.END)
            self.texto_seriada.insert(tk.END, "Error: Valores invalidos")
    
    def _mostrar_info_compuesto(self, event=None):
        """Muestra informacion del compuesto seleccionado."""
        nombre = self.combo_comp_molar.get()
        if nombre in self.motor.compuestos:
            comp = self.motor.compuestos[nombre]
            self.info_compuesto.config(
                text=f"Formula: {comp['formula']} | PM: {comp['peso']} g/mol"
            )
    
    def _calcular_molaridad(self):
        """Calcula molaridad a partir de masa."""
        try:
            masa = float(self.entrada_masa.get())
            volumen = float(self.entrada_volumen.get())
            unidad = self.combo_unidad_vol.get()
            compuesto = self.combo_comp_molar.get()
            
            if compuesto not in self.motor.compuestos:
                self.resultado_molaridad.config(text="Seleccione un compuesto")
                return
            
            pm = self.motor.compuestos[compuesto]['peso']
            molaridad = self.calc_pesos.molaridad_desde_masa(masa, volumen, pm)
            
            # Ajustar por unidad de volumen
            if unidad == "mL":
                molaridad = molaridad * 1000
            elif unidad == "µL":
                molaridad = molaridad * 1e6
            
            self.resultado_molaridad.config(text=f"Molaridad = {molaridad:.4f} M")
        except ValueError:
            self.resultado_molaridad.config(text="Error: Valores invalidos")
    
    def _calcular_masa_necesaria(self):
        """Calcula masa necesaria para molaridad deseada."""
        try:
            molaridad = float(self.entrada_molar_deseada.get())
            volumen = float(self.entrada_vol_molar.get())
            compuesto = self.combo_comp_molar.get()
            
            if compuesto not in self.motor.compuestos:
                self.resultado_masa.config(text="Seleccione un compuesto")
                return
            
            pm = self.motor.compuestos[compuesto]['peso']
            masa = self.calc_pesos.masa_para_molaridad(molaridad, volumen, pm)
            
            self.resultado_masa.config(text=f"Masa necesaria = {masa:.4f} g")
        except ValueError:
            self.resultado_masa.config(text="Error: Valores invalidos")
    
    def _convertir_od(self):
        """Convierte OD600 a celulas/mL."""
        try:
            od = float(self.entrada_od.get())
            organismo = self.organismo_seleccionado.get()
            
            if od < 0 or od > 4:
                self.resultado_od.config(text="Advertencia: OD fuera de rango lineal (0-4)")
            
            celulas = self.calc_moi.celulas_desde_od(od, organismo)
            self.resultado_od.config(text=f"{celulas:.2e} celulas/mL")
        except ValueError:
            self.resultado_od.config(text="Error: Valor invalido")
    
    def _calcular_moi(self):
        """Calcula MOI."""
        try:
            pfu = float(self.entrada_pfu.get())
            vol = float(self.entrada_vol_moi.get())
            celulas = float(self.entrada_celulas.get())
            
            moi = self.calc_moi.calcular_moi(pfu, vol, celulas)
            self.resultado_moi.config(text=f"MOI = {moi:.2f}")
        except ValueError:
            self.resultado_moi.config(text="Error: Valores invalidos")
    
    def _actualizar_historial(self):
        """Actualiza la vista del historial."""
        for item in self.tree_historial.get_children():
            self.tree_historial.delete(item)
        
        for reg in self.registro.obtener_historial(50):
            self.tree_historial.insert("", "end", values=(
                reg['fecha_hora'][:19],
                reg['categoria'],
                f"{reg['valor_entrada']:.4g}",
                reg['unidad_origen'],
                f"{reg['valor_salida']:.4g}",
                reg['unidad_destino']
            ))
    
    def _limpiar_historial(self):
        """Limpia la vista del historial."""
        for item in self.tree_historial.get_children():
            self.tree_historial.delete(item)
    
    def _exportar_historial_csv(self):
        """Exporta historial a CSV."""
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", 
                                            filetypes=[("CSV", "*.csv")])
        if ruta:
            self.registro.exportar_csv(ruta)
            messagebox.showinfo("Exportado", f"Historial guardado en {ruta}")
    
    def _exportar_historial_json(self):
        """Exporta historial a JSON."""
        ruta = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON", "*.json")])
        if ruta:
            self.registro.exportar_json(ruta)
            messagebox.showinfo("Exportado", f"Historial guardado en {ruta}")
    
    
    def _guardar_configuracion(self):
        """Guarda la configuracion actual."""
        self.config.establecer("formato_incertidumbre", self.combo_estilo_inc.get())
        self.config.establecer("cifras_incertidumbre", int(self.spin_cifras_inc.get()))
        self.config.establecer("separador_decimal", self.combo_sep_decimal.get())
        self.config.establecer("temperatura_referencia", int(self.spin_temp_ref.get()))
        messagebox.showinfo("Configuracion", "Preferencias guardadas")