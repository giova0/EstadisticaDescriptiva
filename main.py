import tkinter as tk
from tkinter import messagebox

class AplicacionEstadistica:
    def __init__(self, root):
        self.root = root
        self.root.title("Estadística Descriptiva")
        self.root.geometry("1200x720")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar el estilo de los botones
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'bg': '#4CAF50',
            'fg': 'white',
            'width': 15,
            'height': 2,
            'relief': 'raised',
            'borderwidth': 3
        }
        
        # Crear el título principal
        titulo = tk.Label(
            root, 
            text="ESTADÍSTICA DESCRIPTIVA", 
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#2E86AB'
        )
        titulo.pack(pady=30)
        
        # Frame para los botones
        button_frame = tk.Frame(root, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        # Botón 1: OVAS
        btn_ovas = tk.Button(
            button_frame,
            text="OVAS",
            command=self.funcion_ovas,
            **button_style
        )
        btn_ovas.pack(pady=10)
        
        # Botón 2: Análisis de Datos
        btn_analisis = tk.Button(
            button_frame,
            text="Análisis de Datos",
            command=self.funcion_analisis,
            **button_style
        )
        btn_analisis.pack(pady=10)
        
        # Botón 3: Gráficos
        btn_graficos = tk.Button(
            button_frame,
            text="Gráficos",
            command=self.funcion_graficos,
            **button_style
        )
        btn_graficos.pack(pady=10)
        
        # Botón 4: Reportes
        btn_reportes = tk.Button(
            button_frame,
            text="Reportes",
            command=self.funcion_reportes,
            **button_style
        )
        btn_reportes.pack(pady=10)
        
        # Botón 5: Configuración
        btn_config = tk.Button(
            button_frame,
            text="Configuración",
            command=self.funcion_configuracion,
            **button_style
        )
        btn_config.pack(pady=10)
        
        # Configurar eventos de hover para los botones
        self.configurar_hover(btn_ovas)
        self.configurar_hover(btn_analisis)
        self.configurar_hover(btn_graficos)
        self.configurar_hover(btn_reportes)
        self.configurar_hover(btn_config)
    
    def configurar_hover(self, boton):
        """Configura efectos de hover para los botones"""
        def on_enter(e):
            boton['bg'] = '#45a049'
        
        def on_leave(e):
            boton['bg'] = '#4CAF50'
        
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)
    
    def funcion_ovas(self):
        """Función del botón OVAS"""
        self.mostrar_ovas_en_pantalla_principal()
    
    def mostrar_ovas_en_pantalla_principal(self):
        """Muestra el contenido de OVAS en la pantalla principal"""
        # Limpiar la pantalla principal
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configurar el fondo de la pantalla principal
        self.root.configure(bg='#f8f9fa')
        
        # Título principal
        titulo_ovas = tk.Label(
            self.root,
            text="OVAS - BIOESTADÍSTICA PARA SALUD",
            font=('Arial', 22, 'bold'),
            bg='#f8f9fa',
            fg='#2E86AB'
        )
        titulo_ovas.pack(pady=30)
        
        # Frame principal con scrollbar
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Lista de temas con sus números
        temas_ovas = [
            "Bioestadística esencial para salud",
            "Calidad y limpieza de datos clínicos",
            "Tablas de frecuencias y resúmenes categóricos",
            "Medidas de tendencia central y posición",
            "Dispersión y variabilidad clínica",
            "Asimetría, curtosis y normalidad práctica",
            "Visualización para salud I: gráficos categóricos",
            "Visualización para salud II: gráficos numéricos",
            "Comparaciones descriptivas entre grupos",
            "Tablas 2x2 y 2xk en epidemio",
            "Indicadores de frecuencia en salud",
            "Curvas epidémicas y series de tiempo",
            "Evaluación descriptiva de pruebas diagnósticas",
            "Diseño y sesgos en estudios descriptivos",
            "Gestión ética y anonimización de datos",
            "Flujo de trabajo reproducible",
            "Resúmenes ejecutivos y escritura científica",
            "Dashboard descriptivo básico",
            "Visualización de inequidades en salud",
            "Mini–metodología de reporte gráfico"
        ]
        
        # Estilo para los botones de temas
        tema_button_style = {
            'font': ('Arial', 12, 'bold'),
            'bg': '#007bff',
            'fg': 'white',
            'width': 80,
            'height': 2,
            'relief': 'raised',
            'borderwidth': 2,
            'justify': 'left',
            'anchor': 'w'
        }
        
        # Crear botones para cada tema
        for i, tema in enumerate(temas_ovas, 1):
            # Frame para cada fila
            row_frame = tk.Frame(scrollable_frame, bg='#f8f9fa')
            row_frame.pack(fill='x', pady=5)
            
            # Número del tema
            numero = tk.Label(
                row_frame,
                text=f"{i:2d}.",
                font=('Arial', 12, 'bold'),
                bg='#f8f9fa',
                fg='#495057',
                width=3
            )
            numero.pack(side='left', padx=(0, 10))
            
            # Botón del tema
            btn_tema = tk.Button(
                row_frame,
                text=tema,
                command=lambda t=tema, n=i: self.abrir_tema_ovas(t, n),
                **tema_button_style
            )
            btn_tema.pack(side='left', fill='x', expand=True)
            
            # Configurar hover para cada botón
            self.configurar_hover_tema(btn_tema)
        
        # Configurar scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Botón para volver al menú principal
        btn_volver = tk.Button(
            self.root,
            text="Volver al Menú Principal",
            font=('Arial', 12, 'bold'),
            bg='#28a745',
            fg='white',
            width=20,
            height=2,
            command=self.volver_al_menu_principal
        )
        btn_volver.pack(pady=20)
    
    def volver_al_menu_principal(self):
        """Vuelve al menú principal"""
        # Limpiar la pantalla
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Recrear la interfaz principal
        self.__init__(self.root)
    
    def configurar_hover_tema(self, boton):
        """Configura efectos de hover para los botones de temas"""
        def on_enter(e):
            boton['bg'] = '#0056b3'
        
        def on_leave(e):
            boton['bg'] = '#007bff'
        
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)
    
    def abrir_tema_ovas(self, tema, numero):
        """Abre la ventana específica de cada tema"""
        if numero == 1:
            # Para el primer tema: Bioestadística esencial para salud
            self.ejecutar_ova_bioestadistica()
        elif numero == 2:
            # Para el segundo tema: Calidad y limpieza de datos clínicos
            self.ejecutar_ova_calidad_datos()
        elif numero == 3:
            # Para el tercer tema: Tablas de frecuencias y resúmenes categóricos
            self.ejecutar_ova_tablas_frecuencias()
        elif numero == 4:
            # Para el cuarto tema: Medidas de tendencia central y posición
            self.ejecutar_ova_medidas_tendencia_central()
        elif numero == 5:
            # Para el quinto tema: Dispersión y variabilidad clínica
            self.ejecutar_ova_dispersion_variabilidad()
        elif numero == 6:
            # Para el sexto tema: Asimetría, curtosis y normalidad práctica
            self.ejecutar_ova_asimetria_curtosis()
        elif numero == 7:
            # Para el séptimo tema: Visualización para salud I: gráficos categóricos
            self.ejecutar_ova_visualizacion_categoricos()
        elif numero == 8:
            # Para el octavo tema: Visualización para salud II: gráficos numéricos
            self.ejecutar_ova_visualizacion_numerica()
        else:
            # Para otros temas, mostrar mensaje informativo
            messagebox.showinfo(
                f"Tema {numero}",
                f"Abriendo: {tema}\n\nEste tema se abrirá en una nueva ventana con contenido específico."
            )
    
    def ejecutar_ova_bioestadistica(self):
        """Ejecuta la OVA de Bioestadística esencial para salud en la misma pantalla"""
        try:
            # Limpiar la pantalla actual
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Configurar la pantalla para mostrar el contenido de la OVA
            self.root.title("OVA 1: Bioestadística Esencial para Salud")
            self.root.configure(bg='#f8f9fa')
            
            # Crear interfaz de la OVA en la misma pantalla
            self.mostrar_ova_bioestadistica_en_pantalla()
            
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Error al cargar la OVA:\n{str(e)}"
            )
    
    def mostrar_ova_bioestadistica_en_pantalla(self):
        """Muestra el contenido de la OVA en la pantalla principal"""
        
        # Header de la OVA
        header_ova = tk.Frame(self.root, bg='#1e3a8a', height=120)
        header_ova.pack(fill='x', pady=(0, 20))
        header_ova.pack_propagate(False)
        
        # Título principal de la OVA
        titulo_ova = tk.Label(
            header_ova,
            text="OVA 1: Bioestadística Esencial para Salud",
            font=('Arial', 24, 'bold'),
            bg='#1e3a8a',
            fg='white'
        )
        titulo_ova.pack(pady=30)
        
        # Subtítulo
        subtitulo_ova = tk.Label(
            header_ova,
            text="Universidad Antonio Nariño - Estadística Descriptiva para Ciencias de la Salud",
            font=('Arial', 12),
            bg='#1e3a8a',
            fg='#bfdbfe'
        )
        subtitulo_ova.pack()
        
        # Frame principal con scrollbar
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de la OVA
        self.crear_contenido_ova(scrollable_frame)
        
        # Configurar scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Botón para volver al menú principal
        btn_volver = tk.Button(
            self.root,
            text="Volver al Menú Principal",
            font=('Arial', 12, 'bold'),
            bg='#28a745',
            fg='white',
            width=20,
            height=2,
            command=self.volver_al_menu_principal
        )
        btn_volver.pack(pady=20)
    
    def crear_contenido_ova(self, parent_frame):
        """Crea el contenido de la OVA en la pantalla principal"""
        
        # Sección 1: Introducción
        intro_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        intro_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            intro_frame,
            text="1. Introducción a la Bioestadística",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#1e3a8a'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            intro_frame,
            text="La bioestadística es el lenguaje fundamental para generar, interpretar y validar el conocimiento científico en las ciencias de la salud.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Caso clínico
        caso_frame = tk.Frame(intro_frame, bg='#dbeafe', relief='sunken', bd=1)
        caso_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            caso_frame,
            text="Caso Clínico: Estudio de Diabetes Tipo 2",
            font=('Arial', 12, 'bold'),
            bg='#dbeafe',
            fg='#1e40af'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            caso_frame,
            text="Un hospital quiere evaluar la efectividad de un nuevo protocolo de atención para pacientes con diabetes tipo 2.",
            font=('Arial', 10),
            bg='#dbeafe',
            fg='#1e40af',
            wraplength=750,
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 2: Tipos de Variables
        variables_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        variables_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            variables_frame,
            text="2. Clasificación de Variables",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#059669'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Variables cualitativas
        cual_frame = tk.Frame(variables_frame, bg='#d1fae5', relief='sunken', bd=1)
        cual_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            cual_frame,
            text="Variables Cualitativas:",
            font=('Arial', 12, 'bold'),
            bg='#d1fae5',
            fg='#047857'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            cual_frame,
            text="• Nominales: Sin orden (sexo, grupo sanguíneo)\n• Ordinales: Con orden (grado de dolor, estadio del cáncer)",
            font=('Arial', 10),
            bg='#d1fae5',
            fg='#047857',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Variables cuantitativas
        cuant_frame = tk.Frame(variables_frame, bg='#fef3c7', relief='sunken', bd=1)
        cuant_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            cuant_frame,
            text="Variables Cuantitativas:",
            font=('Arial', 12, 'bold'),
            bg='#fef3c7',
            fg='#d97706'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            cuant_frame,
            text="• Discretas: Valores enteros (número de hijos, episodios)\n• Continuas: Cualquier valor (peso, presión arterial)",
            font=('Arial', 10),
            bg='#fef3c7',
            fg='#d97706',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 3: Ejemplos Prácticos
        ejemplos_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        ejemplos_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            ejemplos_frame,
            text="3. Ejemplos en Ciencias de la Salud",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#7c3aed'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Ejemplos específicos
        ejemplos_lista = [
            "• Presión arterial: Cuantitativa continua (escala de razón)",
            "• Grado de dolor (1-10): Cualitativa ordinal",
            "• Tipo de sangre: Cualitativa nominal",
            "• Edad del paciente: Cuantitativa continua (escala de razón)",
            "• Estadio del cáncer: Cualitativa ordinal"
        ]
        
        for ejemplo in ejemplos_lista:
            tk.Label(
                ejemplos_frame,
                text=ejemplo,
                font=('Arial', 10),
                bg='white',
                fg='#6b7280',
                justify='left'
            ).pack(pady=2, padx=15, anchor='w')
        
        # Sección 4: Actividad Interactiva
        actividad_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        actividad_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            actividad_frame,
            text="4. Actividad Interactiva",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#dc2626'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            actividad_frame,
            text="Clasifica las siguientes variables médicas:",
            font=('Arial', 12),
            bg='white',
            fg='#374151'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Variables para clasificar
        variables_clasificar = [
            "Temperatura corporal (°C)",
            "Nivel de glucosa (mg/dL)",
            "Estado civil",
            "Número de embarazos",
            "Grado de hipertensión"
        ]
        
        for i, variable in enumerate(variables_clasificar, 1):
            var_frame = tk.Frame(actividad_frame, bg='#f3f4f6', relief='sunken', bd=1)
            var_frame.pack(fill='x', padx=15, pady=2)
            
            tk.Label(
                var_frame,
                text=f"{i}. {variable}",
                font=('Arial', 10, 'bold'),
                bg='#f3f4f6',
                fg='#374151'
            ).pack(side='left', pady=10, padx=10)
            
            # Botones de clasificación
            tk.Button(
                var_frame,
                text="Cualitativa",
                font=('Arial', 9),
                bg='#3b82f6',
                fg='white',
                command=lambda v=variable, t="cualitativa": self.clasificar_variable(v, t)
            ).pack(side='right', padx=5)
            
            tk.Button(
                var_frame,
                text="Cuantitativa",
                font=('Arial', 9),
                bg='#10b981',
                fg='white',
                command=lambda v=variable, t="cuantitativa": self.clasificar_variable(v, t)
            ).pack(side='right', padx=5)
        
        # Área de retroalimentación
        self.feedback_area = tk.Text(
            actividad_frame,
            height=6,
            width=80,
            font=('Arial', 9),
            bg='#f9fafb',
            fg='#374151',
            state='disabled'
        )
        self.feedback_area.pack(pady=15, padx=15, fill='x')
        
        # Botón para limpiar retroalimentación
        tk.Button(
            actividad_frame,
            text="Limpiar Retroalimentación",
            font=('Arial', 10),
            bg='#6b7280',
            fg='white',
            command=self.limpiar_retroalimentacion
        ).pack(pady=(0, 15))
    
    def clasificar_variable(self, variable, tipo):
        """Clasifica una variable y muestra retroalimentación"""
        # Respuestas correctas
        respuestas_correctas = {
            "Temperatura corporal (°C)": "cuantitativa",
            "Nivel de glucosa (mg/dL)": "cuantitativa",
            "Estado civil": "cualitativa",
            "Número de embarazos": "cuantitativa",
            "Grado de hipertensión": "cualitativa"
        }
        
        respuesta_correcta = respuestas_correctas.get(variable, "desconocida")
        es_correcta = tipo == respuesta_correcta
        
        # Habilitar área de texto para escribir
        self.feedback_area.config(state='normal')
        
        # Agregar retroalimentación
        if es_correcta:
            feedback = f"✓ ¡Correcto! {variable} es una variable {tipo}.\n"
            self.feedback_area.insert('end', feedback)
        else:
            feedback = f"✗ Incorrecto. {variable} es una variable {respuesta_correcta}.\n"
            self.feedback_area.insert('end', feedback)
        
        # Deshabilitar área de texto
        self.feedback_area.config(state='disabled')
        
        # Hacer scroll hacia abajo
        self.feedback_area.see('end')
    
    def limpiar_retroalimentacion(self):
        """Limpia el área de retroalimentación"""
        self.feedback_area.config(state='normal')
        self.feedback_area.delete(1.0, 'end')
        self.feedback_area.config(state='disabled')
    
    def ejecutar_ova_calidad_datos(self):
        """Ejecuta la OVA de Calidad y limpieza de datos clínicos en la misma pantalla"""
        try:
            # Limpiar la pantalla actual
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Configurar la pantalla para mostrar el contenido de la OVA
            self.root.title("OVA 2: Calidad y Limpieza de Datos Clínicos")
            self.root.configure(bg='#f8f9fa')
            
            # Crear interfaz de la OVA en la misma pantalla
            self.mostrar_ova_calidad_datos_en_pantalla()
            
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Error al cargar la OVA:\n{str(e)}"
            )
    
    def mostrar_ova_calidad_datos_en_pantalla(self):
        """Muestra el contenido de la OVA de Calidad de Datos en la pantalla principal"""
        
        # Header de la OVA
        header_ova = tk.Frame(self.root, bg='#059669', height=120)
        header_ova.pack(fill='x', pady=(0, 20))
        header_ova.pack_propagate(False)
        
        # Título principal de la OVA
        titulo_ova = tk.Label(
            header_ova,
            text="OVA 2: Calidad y Limpieza de Datos Clínicos",
            font=('Arial', 24, 'bold'),
            bg='#059669',
            fg='white'
        )
        titulo_ova.pack(pady=30)
        
        # Subtítulo
        subtitulo_ova = tk.Label(
            header_ova,
            text="Universidad Antonio Nariño - Estadística Descriptiva para Ciencias de la Salud",
            font=('Arial', 12),
            bg='#059669',
            fg='#a7f3d0'
        )
        subtitulo_ova.pack()
        
        # Frame principal con scrollbar
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de la OVA
        self.crear_contenido_ova_calidad_datos(scrollable_frame)
        
        # Configurar scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Botón para volver al menú principal
        btn_volver = tk.Button(
            self.root,
            text="Volver al Menú Principal",
            font=('Arial', 12, 'bold'),
            bg='#28a745',
            fg='white',
            width=20,
            height=2,
            command=self.volver_al_menu_principal
        )
        btn_volver.pack(pady=20)
    
    def crear_contenido_ova_calidad_datos(self, parent_frame):
        """Crea el contenido de la OVA de Calidad de Datos en la pantalla principal"""
        
        # Sección 1: Introducción a la Calidad de Datos
        intro_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        intro_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            intro_frame,
            text="1. Importancia de la Calidad de Datos en Salud",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#059669'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            intro_frame,
            text="La calidad de los datos es fundamental en la investigación en ciencias de la salud. Datos de mala calidad pueden llevar a conclusiones erróneas y decisiones clínicas incorrectas.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Caso clínico
        caso_frame = tk.Frame(intro_frame, bg='#d1fae5', relief='sunken', bd=1)
        caso_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            caso_frame,
            text="Caso Clínico: Estudio de Efectividad de Medicamentos",
            font=('Arial', 12, 'bold'),
            bg='#d1fae5',
            fg='#047857'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            caso_frame,
            text="Un estudio clínico sobre la efectividad de un nuevo medicamento para la hipertensión presenta inconsistencias en la recolección de datos de presión arterial.",
            font=('Arial', 10),
            bg='#d1fae5',
            fg='#047857',
            wraplength=750,
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 2: Tipos de Errores en Datos
        errores_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        errores_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            errores_frame,
            text="2. Tipos de Errores Comunes en Datos Clínicos",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#dc2626'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Errores de entrada
        entrada_frame = tk.Frame(errores_frame, bg='#fee2e2', relief='sunken', bd=1)
        entrada_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            entrada_frame,
            text="Errores de Entrada de Datos:",
            font=('Arial', 12, 'bold'),
            bg='#fee2e2',
            fg='#dc2626'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            entrada_frame,
            text="• Errores de transcripción (ej: 150 mmHg vs 15 mmHg)\n• Errores de unidades (ej: kg vs libras)\n• Valores fuera de rango (ej: edad 150 años)",
            font=('Arial', 10),
            bg='#fee2e2',
            fg='#dc2626',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Errores de medición
        medicion_frame = tk.Frame(errores_frame, bg='#fef3c7', relief='sunken', bd=1)
        medicion_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            medicion_frame,
            text="Errores de Medición:",
            font=('Arial', 12, 'bold'),
            bg='#fef3c7',
            fg='#d97706'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            medicion_frame,
            text="• Calibración incorrecta de instrumentos\n• Variabilidad entre observadores\n• Condiciones ambientales inadecuadas",
            font=('Arial', 10),
            bg='#fef3c7',
            fg='#d97706',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 3: Estrategias de Limpieza
        limpieza_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        limpieza_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            limpieza_frame,
            text="3. Estrategias de Limpieza y Validación",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#7c3aed'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Estrategias específicas
        estrategias_lista = [
            "• Validación de rangos lógicos para variables clínicas",
            "• Detección de valores atípicos (outliers)",
            "• Verificación de consistencia entre variables relacionadas",
            "• Manejo de datos faltantes (missing data)",
            "• Documentación de todas las modificaciones realizadas"
        ]
        
        for estrategia in estrategias_lista:
            tk.Label(
                limpieza_frame,
                text=estrategia,
                font=('Arial', 10),
                bg='white',
                fg='#6b7280',
                justify='left'
            ).pack(pady=2, padx=15, anchor='w')
        
        # Sección 4: Actividad Interactiva
        actividad_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        actividad_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            actividad_frame,
            text="4. Actividad: Identificar Problemas de Calidad",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#1e40af'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            actividad_frame,
            text="Revisa el siguiente dataset y identifica los problemas de calidad:",
            font=('Arial', 12),
            bg='white',
            fg='#374151'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Dataset de ejemplo con problemas
        dataset_frame = tk.Frame(actividad_frame, bg='#f3f4f6', relief='sunken', bd=1)
        dataset_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Crear tabla de datos
        headers = ["ID", "Edad", "Presión Sistólica", "Peso (kg)", "Diabetes"]
        data = [
            ["001", "45", "120", "70", "No"],
            ["002", "32", "15", "65", "Sí"],
            ["003", "67", "140", "85", "No"],
            ["004", "28", "130", "55", "No"],
            ["005", "55", "160", "120", "Sí"],
            ["006", "42", "125", "72", "No"],
            ["007", "71", "135", "78", "Sí"],
            ["008", "38", "128", "68", "No"]
        ]
        
        # Crear encabezados
        for i, header in enumerate(headers):
            tk.Label(
                dataset_frame,
                text=header,
                font=('Arial', 10, 'bold'),
                bg='#d1d5db',
                fg='#374151',
                width=12
            ).grid(row=0, column=i, padx=2, pady=2, sticky='ew')
        
        # Crear filas de datos
        for row_idx, row_data in enumerate(data, 1):
            for col_idx, cell_data in enumerate(row_data):
                bg_color = '#f9fafb' if row_idx % 2 == 0 else '#ffffff'
                tk.Label(
                    dataset_frame,
                    text=cell_data,
                    font=('Arial', 9),
                    bg=bg_color,
                    fg='#374151',
                    width=12
                ).grid(row=row_idx, column=col_idx, padx=2, pady=1, sticky='ew')
        
        # Configurar columnas para que se expandan
        for i in range(len(headers)):
            dataset_frame.grid_columnconfigure(i, weight=1)
        
        # Área de retroalimentación para la actividad
        self.feedback_area_calidad = tk.Text(
            actividad_frame,
            height=8,
            width=80,
            font=('Arial', 9),
            bg='#f9fafb',
            fg='#374151',
            state='disabled'
        )
        self.feedback_area_calidad.pack(pady=15, padx=15, fill='x')
        
        # Botones para identificar problemas
        botones_frame = tk.Frame(actividad_frame)
        botones_frame.pack(pady=(0, 15))
        
        problemas = [
            "Valor atípico en edad",
            "Presión arterial incorrecta",
            "Peso fuera de rango",
            "Inconsistencia en datos"
        ]
        
        for problema in problemas:
            tk.Button(
                botones_frame,
                text=problema,
                font=('Arial', 9),
                bg='#3b82f6',
                fg='white',
                command=lambda p=problema: self.identificar_problema_calidad(p)
            ).pack(side='left', padx=5)
        
        # Botón para limpiar retroalimentación
        tk.Button(
            actividad_frame,
            text="Limpiar Retroalimentación",
            font=('Arial', 10),
            bg='#6b7280',
            fg='white',
            command=self.limpiar_retroalimentacion_calidad
        ).pack(pady=(0, 15))
    
    def identificar_problema_calidad(self, problema):
        """Identifica un problema de calidad en el dataset"""
        # Habilitar área de texto para escribir
        self.feedback_area_calidad.config(state='normal')
        
        # Agregar retroalimentación según el problema
        if problema == "Valor atípico en edad":
            feedback = "✓ Correcto: El paciente 003 tiene 67 años, lo cual es plausible pero requiere verificación.\n"
        elif problema == "Presión arterial incorrecta":
            feedback = "✓ Correcto: El paciente 002 tiene presión sistólica de 15 mmHg, lo cual es imposible (error de transcripción).\n"
        elif problema == "Peso fuera de rango":
            feedback = "✓ Correcto: El paciente 005 pesa 120 kg, lo cual es alto pero posible. Verificar si es correcto.\n"
        elif problema == "Inconsistencia en datos":
            feedback = "✓ Correcto: Hay inconsistencias entre edad y peso en varios pacientes que requieren verificación.\n"
        
        self.feedback_area_calidad.insert('end', feedback)
        
        # Deshabilitar área de texto
        self.feedback_area_calidad.config(state='disabled')
        
        # Hacer scroll hacia abajo
        self.feedback_area_calidad.see('end')
    
    def limpiar_retroalimentacion_calidad(self):
        """Limpia el área de retroalimentación de calidad de datos"""
        self.feedback_area_calidad.config(state='normal')
        self.feedback_area_calidad.delete(1.0, 'end')
        self.feedback_area_calidad.config(state='disabled')
    
    def ejecutar_ova_medidas_tendencia_central(self):
        """Ejecuta la OVA de Medidas de tendencia central y posición en la misma pantalla"""
        try:
            # Limpiar la pantalla actual
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Configurar la pantalla para mostrar el contenido de la OVA
            self.root.title("OVA 4: Medidas de Tendencia Central y Posición")
            self.root.configure(bg='#f8f9fa')
            
            # Crear interfaz de la OVA en la misma pantalla
            self.mostrar_ova_medidas_tendencia_central_en_pantalla()
            
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Error al cargar la OVA:\n{str(e)}"
            )
    
    def mostrar_ova_medidas_tendencia_central_en_pantalla(self):
        """Muestra el contenido de la OVA de Medidas de Tendencia Central en la pantalla principal"""
        
        # Header de la OVA
        header_ova = tk.Frame(self.root, bg='#7c3aed', height=120)
        header_ova.pack(fill='x', pady=(0, 20))
        header_ova.pack_propagate(False)
        
        # Título principal de la OVA
        titulo_ova = tk.Label(
            header_ova,
            text="OVA 4: Medidas de Tendencia Central y Posición",
            font=('Arial', 24, 'bold'),
            bg='#7c3aed',
            fg='white'
        )
        titulo_ova.pack(pady=30)
        
        # Subtítulo
        subtitulo_ova = tk.Label(
            header_ova,
            text="Universidad Antonio Nariño - Estadística Descriptiva para Ciencias de la Salud",
            font=('Arial', 12),
            bg='#7c3aed',
            fg='#c4b5fd'
        )
        subtitulo_ova.pack()
        
        # Frame principal con scrollbar
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de la OVA
        self.crear_contenido_ova_medidas_tendencia_central(scrollable_frame)
        
        # Configurar scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Botón para volver al menú principal
        btn_volver = tk.Button(
            self.root,
            text="Volver al Menú Principal",
            font=('Arial', 12, 'bold'),
            bg='#28a745',
            fg='white',
            width=20,
            height=2,
            command=self.volver_al_menu_principal
        )
        btn_volver.pack(pady=20)
    
    def crear_contenido_ova_medidas_tendencia_central(self, parent_frame):
        """Crea el contenido de la OVA de Medidas de Tendencia Central en la pantalla principal"""
        
        # Sección 1: Introducción a las Medidas de Tendencia Central
        intro_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        intro_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            intro_frame,
            text="1. ¿Qué son las Medidas de Tendencia Central?",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#7c3aed'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            intro_frame,
            text="Las medidas de tendencia central son valores que representan el centro o punto medio de un conjunto de datos. Son fundamentales para resumir y entender la distribución de variables en estudios de salud.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Caso clínico
        caso_frame = tk.Frame(intro_frame, bg='#ede9fe', relief='sunken', bd=1)
        caso_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            caso_frame,
            text="Caso Clínico: Estudio de Presión Arterial en Pacientes Hipertensos",
            font=('Arial', 12, 'bold'),
            bg='#ede9fe',
            fg='#5b21b6'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            caso_frame,
            text="Un cardiólogo quiere resumir la presión arterial sistólica de 50 pacientes con hipertensión para determinar el valor típico y la variabilidad en su consulta.",
            font=('Arial', 10),
            bg='#ede9fe',
            fg='#5b21b6',
            wraplength=750,
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 2: Tipos de Medidas de Tendencia Central
        medidas_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        medidas_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            medidas_frame,
            text="2. Principales Medidas de Tendencia Central",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#059669'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Media aritmética
        media_frame = tk.Frame(medidas_frame, bg='#d1fae5', relief='sunken', bd=1)
        media_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            media_frame,
            text="Media Aritmética (Promedio):",
            font=('Arial', 12, 'bold'),
            bg='#d1fae5',
            fg='#047857'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            media_frame,
            text="• Suma de todos los valores dividida por el número de observaciones\n• Sensible a valores extremos (outliers)\n• Ideal para datos con distribución normal\n• Fórmula: x̄ = Σx/n",
            font=('Arial', 10),
            bg='#d1fae5',
            fg='#047857',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Mediana
        mediana_frame = tk.Frame(medidas_frame, bg='#fef3c7', relief='sunken', bd=1)
        mediana_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            mediana_frame,
            text="Mediana:",
            font=('Arial', 12, 'bold'),
            bg='#fef3c7',
            fg='#d97706'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            mediana_frame,
            text="• Valor que divide los datos en dos grupos iguales\n• No se ve afectada por valores extremos\n• Ideal para datos asimétricos o con outliers\n• Se calcula ordenando los datos y tomando el valor central",
            font=('Arial', 10),
            bg='#fef3c7',
            fg='#d97706',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Moda
        moda_frame = tk.Frame(medidas_frame, bg='#fce7f3', relief='sunken', bd=1)
        moda_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            moda_frame,
            text="Moda:",
            font=('Arial', 12, 'bold'),
            bg='#fce7f3',
            fg='#be185d'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            moda_frame,
            text="• Valor que aparece con mayor frecuencia\n• Útil para datos cualitativos y cuantitativos\n• Puede no existir o haber múltiples modas\n• No se ve afectada por valores extremos",
            font=('Arial', 10),
            bg='#fce7f3',
            fg='#be185d',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 3: Medidas de Posición
        posicion_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        posicion_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            posicion_frame,
            text="3. Medidas de Posición: Cuartiles y Percentiles",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#dc2626'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Cuartiles
        cuartiles_frame = tk.Frame(posicion_frame, bg='#fee2e2', relief='sunken', bd=1)
        cuartiles_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            cuartiles_frame,
            text="Cuartiles:",
            font=('Arial', 12, 'bold'),
            bg='#fee2e2',
            fg='#dc2626'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            cuartiles_frame,
            text="• Q1 (25%): 25% de los datos están por debajo\n• Q2 (50%): Coincide con la mediana\n• Q3 (75%): 75% de los datos están por debajo\n• Rango intercuartílico (RIQ) = Q3 - Q1",
            font=('Arial', 10),
            bg='#fee2e2',
            fg='#dc2626',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Percentiles
        percentiles_frame = tk.Frame(posicion_frame, bg='#dbeafe', relief='sunken', bd=1)
        percentiles_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            percentiles_frame,
            text="Percentiles:",
            font=('Arial', 12, 'bold'),
            bg='#dbeafe',
            fg='#1e40af'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            percentiles_frame,
            text="• P10: 10% de los datos están por debajo\n• P50: Coincide con la mediana\n• P90: 90% de los datos están por debajo\n• Útiles para identificar valores atípicos",
            font=('Arial', 10),
            bg='#dbeafe',
            fg='#1e40af',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 4: Actividad Interactiva
        actividad_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        actividad_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            actividad_frame,
            text="4. Actividad: Calcular Medidas de Tendencia Central",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#1e40af'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            actividad_frame,
            text="Calcula las medidas de tendencia central para el siguiente conjunto de datos de presión arterial sistólica (mmHg):",
            font=('Arial', 12),
            bg='white',
            fg='#374151'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Dataset de presión arterial
        dataset_frame = tk.Frame(actividad_frame, bg='#f3f4f6', relief='sunken', bd=1)
        dataset_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Datos de presión arterial
        presiones = [120, 135, 118, 142, 125, 130, 128, 140, 115, 132, 138, 122, 136, 129, 134]
        
        # Crear encabezado
        tk.Label(
            dataset_frame,
            text="Presión Arterial Sistólica (mmHg)",
            font=('Arial', 10, 'bold'),
            bg='#d1d5db',
            fg='#374151'
        ).pack(pady=10, padx=10)
        
        # Mostrar datos en filas
        datos_frame = tk.Frame(dataset_frame, bg='#f3f4f6')
        datos_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        for i, presion in enumerate(presiones):
            bg_color = '#f9fafb' if i % 2 == 0 else '#ffffff'
            tk.Label(
                datos_frame,
                text=str(presion),
                font=('Arial', 9),
                bg=bg_color,
                fg='#374151',
                width=8,
                relief='solid',
                bd=1
            ).grid(row=i//5, column=i%5, padx=2, pady=2, sticky='ew')
        
        # Configurar columnas para que se expandan
        for i in range(5):
            datos_frame.grid_columnconfigure(i, weight=1)
        
        # Botones para calcular medidas
        botones_frame = tk.Frame(actividad_frame)
        botones_frame.pack(pady=(0, 15))
        
        medidas = [
            "Calcular Media",
            "Calcular Mediana",
            "Calcular Moda",
            "Calcular Cuartiles"
        ]
        
        for medida in medidas:
            tk.Button(
                botones_frame,
                text=medida,
                font=('Arial', 9),
                bg='#3b82f6',
                fg='white',
                command=lambda m=medida: self.calcular_medida_tendencia_central(m, presiones)
            ).pack(side='left', padx=5)
        
        # Área de retroalimentación para la actividad
        self.feedback_area_medidas = tk.Text(
            actividad_frame,
            height=8,
            width=80,
            font=('Arial', 9),
            bg='#f9fafb',
            fg='#374151',
            state='disabled'
        )
        self.feedback_area_medidas.pack(pady=15, padx=15, fill='x')
        
        # Botón para limpiar retroalimentación
        tk.Button(
            actividad_frame,
            text="Limpiar Resultados",
            font=('Arial', 10),
            bg='#6b7280',
            fg='white',
            command=self.limpiar_retroalimentacion_medidas
        ).pack(pady=(0, 15))
    
    def calcular_medida_tendencia_central(self, medida, datos):
        """Calcula una medida de tendencia central para el conjunto de datos"""
        # Habilitar área de texto para escribir
        self.feedback_area_medidas.config(state='normal')
        
        # Ordenar datos para cálculos
        datos_ordenados = sorted(datos)
        n = len(datos)
        
        # Calcular según la medida solicitada
        if medida == "Calcular Media":
            media = sum(datos) / n
            feedback = f"✓ Media Aritmética: {media:.2f} mmHg\n"
            feedback += f"   Fórmula: Σx/n = {sum(datos)}/{n} = {media:.2f}\n"
            
        elif medida == "Calcular Mediana":
            if n % 2 == 0:
                mediana = (datos_ordenados[n//2 - 1] + datos_ordenados[n//2]) / 2
                feedback = f"✓ Mediana: {mediana:.1f} mmHg\n"
                feedback += f"   Datos ordenados: {datos_ordenados}\n"
                feedback += f"   Posiciones centrales: {n//2 - 1} y {n//2}\n"
            else:
                mediana = datos_ordenados[n//2]
                feedback = f"✓ Mediana: {mediana} mmHg\n"
                feedback += f"   Datos ordenados: {datos_ordenados}\n"
                feedback += f"   Posición central: {n//2}\n"
                
        elif medida == "Calcular Moda":
            from collections import Counter
            frecuencias = Counter(datos)
            moda_valores = [valor for valor, freq in frecuencias.items() if freq == max(frecuencias.values())]
            if len(moda_valores) == 1:
                feedback = f"✓ Moda: {moda_valores[0]} mmHg\n"
            else:
                feedback = f"✓ Moda: {', '.join(map(str, moda_valores))} mmHg (multimodal)\n"
            feedback += f"   Frecuencias: {dict(frecuencias)}\n"
            
        elif medida == "Calcular Cuartiles":
            q1_pos = (n + 1) * 0.25
            q2_pos = (n + 1) * 0.50
            q3_pos = (n + 1) * 0.75
            
            q1 = datos_ordenados[int(q1_pos) - 1] if q1_pos.is_integer() else \
                 datos_ordenados[int(q1_pos) - 1] + (q1_pos - int(q1_pos)) * (datos_ordenados[int(q1_pos)] - datos_ordenados[int(q1_pos) - 1])
            q2 = datos_ordenados[int(q2_pos) - 1] if q2_pos.is_integer() else \
                 datos_ordenados[int(q2_pos) - 1] + (q2_pos - int(q2_pos)) * (datos_ordenados[int(q2_pos)] - datos_ordenados[int(q2_pos) - 1])
            q3 = datos_ordenados[int(q3_pos) - 1] if q3_pos.is_integer() else \
                 datos_ordenados[int(q3_pos) - 1] + (q3_pos - int(q3_pos)) * (datos_ordenados[int(q3_pos)] - datos_ordenados[int(q3_pos) - 1])
            
            feedback = f"✓ Cuartiles:\n"
            feedback += f"   Q1 (25%): {q1:.1f} mmHg\n"
            feedback += f"   Q2 (50%): {q2:.1f} mmHg (Mediana)\n"
            feedback += f"   Q3 (75%): {q3:.1f} mmHg\n"
            feedback += f"   Rango Intercuartílico: {q3 - q1:.1f} mmHg\n"
            feedback += f"   Datos ordenados: {datos_ordenados}\n"
        
        self.feedback_area_medidas.insert('end', feedback + "\n")
        
        # Deshabilitar área de texto
        self.feedback_area_medidas.config(state='disabled')
        
        # Hacer scroll hacia abajo
        self.feedback_area_medidas.see('end')
    
    def limpiar_retroalimentacion_medidas(self):
        """Limpia el área de retroalimentación de medidas de tendencia central"""
        self.feedback_area_medidas.config(state='normal')
        self.feedback_area_medidas.delete(1.0, 'end')
        self.feedback_area_medidas.config(state='disabled')
    
    # ============================
    # OVA 5: Dispersión y Variabilidad Clínica
    # ============================
    def ejecutar_ova_dispersion_variabilidad(self):
        """Ejecuta la OVA de Dispersión y variabilidad clínica en la misma pantalla"""
        try:
            # Limpiar la pantalla actual
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Configurar la pantalla para mostrar el contenido de la OVA
            self.root.title("OVA 5: Dispersión y Variabilidad Clínica")
            self.root.configure(bg='#f8f9fa')
            
            # Crear interfaz de la OVA en la misma pantalla
            self.mostrar_ova_dispersion_variabilidad_en_pantalla()
            
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Error al cargar la OVA:\n{str(e)}"
            )
    
    def mostrar_ova_dispersion_variabilidad_en_pantalla(self):
        """Muestra el contenido de la OVA de Dispersión y Variabilidad en la pantalla principal"""
        
        # Header de la OVA
        header_ova = tk.Frame(self.root, bg='#f59e0b', height=120)
        header_ova.pack(fill='x', pady=(0, 20))
        header_ova.pack_propagate(False)
        
        # Título principal de la OVA
        titulo_ova = tk.Label(
            header_ova,
            text="OVA 5: Dispersión y Variabilidad Clínica",
            font=('Arial', 24, 'bold'),
            bg='#f59e0b',
            fg='white'
        )
        titulo_ova.pack(pady=30)
        
        # Subtítulo
        subtitulo_ova = tk.Label(
            header_ova,
            text="Universidad Antonio Nariño - Estadística Descriptiva para Ciencias de la Salud",
            font=('Arial', 12),
            bg='#f59e0b',
            fg='#fef3c7'
        )
        subtitulo_ova.pack()
        
        # Frame principal con scrollbar
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de la OVA
        self.crear_contenido_ova_dispersion_variabilidad(scrollable_frame)
        
        # Configurar scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Botón para volver al menú principal
        btn_volver = tk.Button(
            self.root,
            text="Volver al Menú Principal",
            font=('Arial', 12, 'bold'),
            bg='#28a745',
            fg='white',
            width=20,
            height=2,
            command=self.volver_al_menu_principal
        )
        btn_volver.pack(pady=20)
    
    def crear_contenido_ova_dispersion_variabilidad(self, parent_frame):
        """Crea el contenido de la OVA de Dispersión y Variabilidad en la pantalla principal"""
        
        # Sección 1: Introducción a la Dispersión
        intro_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        intro_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            intro_frame,
            text="1. ¿Qué es la Dispersión en Estadística?",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#f59e0b'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            intro_frame,
            text="La dispersión mide qué tan esparcidos están los datos alrededor de la tendencia central. Es crucial para entender la variabilidad en estudios clínicos y la precisión de las mediciones.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Caso clínico
        caso_frame = tk.Frame(intro_frame, bg='#fef3c7', relief='sunken', bd=1)
        caso_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            caso_frame,
            text="Caso Clínico: Variabilidad en Mediciones de Presión Arterial",
            font=('Arial', 12, 'bold'),
            bg='#fef3c7',
            fg='#d97706'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            caso_frame,
            text="Un estudio compara la variabilidad de presión arterial entre dos grupos de pacientes: uno con tratamiento estándar y otro con nuevo protocolo.",
            font=('Arial', 10),
            bg='#fef3c7',
            fg='#d97706',
            wraplength=750,
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 2: Medidas de Dispersión
        medidas_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        medidas_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            medidas_frame,
            text="2. Principales Medidas de Dispersión",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#dc2626'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Rango
        rango_frame = tk.Frame(medidas_frame, bg='#fee2e2', relief='sunken', bd=1)
        rango_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            rango_frame,
            text="Rango:",
            font=('Arial', 12, 'bold'),
            bg='#fee2e2',
            fg='#dc2626'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            rango_frame,
            text="• Diferencia entre el valor máximo y mínimo\n• R = Xmax - Xmin\n• Sensible a valores extremos (outliers)\n• Fácil de calcular pero limitado",
            font=('Arial', 10),
            bg='#fee2e2',
            fg='#dc2626',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Varianza
        varianza_frame = tk.Frame(medidas_frame, bg='#dbeafe', relief='sunken', bd=1)
        varianza_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            varianza_frame,
            text="Varianza:",
            font=('Arial', 12, 'bold'),
            bg='#dbeafe',
            fg='#1e40af'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            varianza_frame,
            text="• Promedio de las desviaciones al cuadrado de la media\n• s² = Σ(x - x̄)² / (n-1)\n• Siempre positiva\n• Unidades al cuadrado",
            font=('Arial', 10),
            bg='#dbeafe',
            fg='#1e40af',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Desviación estándar
        desv_frame = tk.Frame(medidas_frame, bg='#d1fae5', relief='sunken', bd=1)
        desv_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            desv_frame,
            text="Desviación Estándar:",
            font=('Arial', 12, 'bold'),
            bg='#d1fae5',
            fg='#047857'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            desv_frame,
            text="• Raíz cuadrada de la varianza\n• s = √s²\n• Mismas unidades que los datos originales\n• Interpretación más intuitiva",
            font=('Arial', 10),
            bg='#d1fae5',
            fg='#047857',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 3: Coeficiente de Variación
        cv_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        cv_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            cv_frame,
            text="3. Coeficiente de Variación (CV)",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#7c3aed'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            cv_frame,
            text="El CV permite comparar la variabilidad relativa entre diferentes variables o grupos, independientemente de sus unidades de medida.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        cv_info_frame = tk.Frame(cv_frame, bg='#ede9fe', relief='sunken', bd=1)
        cv_info_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            cv_info_frame,
            text="Fórmula: CV = (s / x̄) × 100%",
            font=('Arial', 12, 'bold'),
            bg='#ede9fe',
            fg='#5b21b6'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            cv_info_frame,
            text="• CV < 15%: Baja variabilidad\n• CV 15-30%: Variabilidad moderada\n• CV > 30%: Alta variabilidad\n• Útil para comparar grupos con diferentes escalas",
            font=('Arial', 10),
            bg='#ede9fe',
            fg='#5b21b6',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 4: Actividad Interactiva
        actividad_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        actividad_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            actividad_frame,
            text="4. Actividad: Calcular Medidas de Dispersión",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#1e40af'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            actividad_frame,
            text="Calcula las medidas de dispersión para el siguiente conjunto de datos de presión arterial sistólica (mmHg):",
            font=('Arial', 12),
            bg='white',
            fg='#374151'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Dataset de presión arterial
        dataset_frame = tk.Frame(actividad_frame, bg='#f3f4f6', relief='sunken', bd=1)
        dataset_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Datos de presión arterial
        presiones = [120, 135, 118, 142, 125, 130, 128, 140, 115, 132, 138, 122, 136, 129, 134]
        
        # Crear encabezado
        tk.Label(
            dataset_frame,
            text="Presión Arterial Sistólica (mmHg)",
            font=('Arial', 10, 'bold'),
            bg='#d1d5db',
            fg='#374151'
        ).pack(pady=10, padx=10)
        
        # Mostrar datos en filas
        datos_frame = tk.Frame(dataset_frame, bg='#f3f4f6')
        datos_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        for i, presion in enumerate(presiones):
            bg_color = '#f9fafb' if i % 2 == 0 else '#ffffff'
            tk.Label(
                datos_frame,
                text=str(presion),
                font=('Arial', 9),
                bg=bg_color,
                fg='#374151',
                width=8,
                relief='solid',
                bd=1
            ).grid(row=i//5, column=i%5, padx=2, pady=2, sticky='ew')
        
        # Configurar columnas para que se expandan
        for i in range(5):
            datos_frame.grid_columnconfigure(i, weight=1)
        
        # Botones para calcular medidas
        botones_frame = tk.Frame(actividad_frame)
        botones_frame.pack(pady=(0, 15))
        
        medidas = [
            "Calcular Rango",
            "Calcular Varianza",
            "Calcular Desv. Estándar",
            "Calcular CV"
        ]
        
        for medida in medidas:
            tk.Button(
                botones_frame,
                text=medida,
                font=('Arial', 9),
                bg='#3b82f6',
                fg='white',
                command=lambda m=medida: self.calcular_medida_dispersion(m, presiones)
            ).pack(side='left', padx=5)
        
        # Área de retroalimentación para la actividad
        self.feedback_area_dispersion = tk.Text(
            actividad_frame,
            height=8,
            width=80,
            font=('Arial', 9),
            bg='#f9fafb',
            fg='#374151',
            state='disabled'
        )
        self.feedback_area_dispersion.pack(pady=15, padx=15, fill='x')
        
        # Botón para limpiar retroalimentación
        tk.Button(
            actividad_frame,
            text="Limpiar Resultados",
            font=('Arial', 10),
            bg='#6b7280',
            fg='white',
            command=self.limpiar_retroalimentacion_dispersion
        ).pack(pady=(0, 15))
    
    def calcular_medida_dispersion(self, medida, datos):
        """Calcula una medida de dispersión para el conjunto de datos"""
        # Habilitar área de texto para escribir
        self.feedback_area_dispersion.config(state='normal')
        
        # Calcular media para los cálculos
        media = sum(datos) / len(datos)
        n = len(datos)
        
        # Calcular según la medida solicitada
        if medida == "Calcular Rango":
            rango = max(datos) - min(datos)
            feedback = f"✓ Rango: {rango} mmHg\n"
            feedback += f"   Fórmula: R = Xmax - Xmin = {max(datos)} - {min(datos)} = {rango}\n"
            feedback += f"   Datos ordenados: {sorted(datos)}\n"
            
        elif medida == "Calcular Varianza":
            # Varianza muestral (n-1 en denominador)
            suma_cuadrados = sum((x - media) ** 2 for x in datos)
            varianza = suma_cuadrados / (n - 1)
            feedback = f"✓ Varianza: {varianza:.2f} mmHg²\n"
            feedback += f"   Fórmula: s² = Σ(x - x̄)² / (n-1)\n"
            feedback += f"   Media (x̄): {media:.2f}\n"
            feedback += f"   Suma de cuadrados: {suma_cuadrados:.2f}\n"
            feedback += f"   Varianza: {suma_cuadrados:.2f} / {n-1} = {varianza:.2f}\n"
            
        elif medida == "Calcular Desv. Estándar":
            # Desviación estándar
            suma_cuadrados = sum((x - media) ** 2 for x in datos)
            varianza = suma_cuadrados / (n - 1)
            desv_est = varianza ** 0.5
            feedback = f"✓ Desviación Estándar: {desv_est:.2f} mmHg\n"
            feedback += f"   Fórmula: s = √s² = √{varianza:.2f} = {desv_est:.2f}\n"
            feedback += f"   Interpretación: Los datos se desvían en promedio {desv_est:.2f} mmHg de la media\n"
            
        elif medida == "Calcular CV":
            # Coeficiente de variación
            suma_cuadrados = sum((x - media) ** 2 for x in datos)
            varianza = suma_cuadrados / (n - 1)
            desv_est = varianza ** 0.5
            cv = (desv_est / media) * 100
            feedback = f"✓ Coeficiente de Variación: {cv:.2f}%\n"
            feedback += f"   Fórmula: CV = (s / x̄) × 100% = ({desv_est:.2f} / {media:.2f}) × 100% = {cv:.2f}%\n"
            if cv < 15:
                feedback += f"   Interpretación: Baja variabilidad (CV < 15%)\n"
            elif cv < 30:
                feedback += f"   Interpretación: Variabilidad moderada (15% ≤ CV < 30%)\n"
            else:
                feedback += f"   Interpretación: Alta variabilidad (CV ≥ 30%)\n"
        
        self.feedback_area_dispersion.insert('end', feedback + "\n")
        
        # Deshabilitar área de texto
        self.feedback_area_dispersion.config(state='disabled')
        
        # Hacer scroll hacia abajo
        self.feedback_area_dispersion.see('end')
    
    def limpiar_retroalimentacion_dispersion(self):
        """Limpia el área de retroalimentación de medidas de dispersión"""
        self.feedback_area_dispersion.config(state='normal')
        self.feedback_area_dispersion.delete(1.0, 'end')
        self.feedback_area_dispersion.config(state='disabled')
    
    # ============================
    # OVA 6: Asimetría, Curtosis y Normalidad Práctica
    # ============================
    def ejecutar_ova_asimetria_curtosis(self):
        """Ejecuta la OVA de Asimetría, curtosis y normalidad práctica en la misma pantalla"""
        try:
            # Limpiar la pantalla actual
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Configurar la pantalla para mostrar el contenido de la OVA
            self.root.title("OVA 6: Asimetría, Curtosis y Normalidad Práctica")
            self.root.configure(bg='#f8f9fa')
            
            # Crear interfaz de la OVA en la misma pantalla
            self.mostrar_ova_asimetria_curtosis_en_pantalla()
            
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Error al cargar la OVA:\n{str(e)}"
            )
    
    def mostrar_ova_asimetria_curtosis_en_pantalla(self):
        """Muestra el contenido de la OVA de Asimetría, Curtosis y Normalidad en la pantalla principal"""
        
        # Header de la OVA
        header_ova = tk.Frame(self.root, bg='#ec4899', height=120)
        header_ova.pack(fill='x', pady=(0, 20))
        header_ova.pack_propagate(False)
        
        # Título principal de la OVA
        titulo_ova = tk.Label(
            header_ova,
            text="OVA 6: Asimetría, Curtosis y Normalidad Práctica",
            font=('Arial', 24, 'bold'),
            bg='#ec4899',
            fg='white'
        )
        titulo_ova.pack(pady=30)
        
        # Subtítulo
        subtitulo_ova = tk.Label(
            header_ova,
            text="Universidad Antonio Nariño - Estadística Descriptiva para Ciencias de la Salud",
            font=('Arial', 12),
            bg='#ec4899',
            fg='#fce7f3'
        )
        subtitulo_ova.pack()
        
        # Frame principal con scrollbar
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de la OVA
        self.crear_contenido_ova_asimetria_curtosis(scrollable_frame)
        
        # Configurar scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Botón para volver al menú principal
        btn_volver = tk.Button(
            self.root,
            text="Volver al Menú Principal",
            font=('Arial', 12, 'bold'),
            bg='#28a745',
            fg='white',
            width=20,
            height=2,
            command=self.volver_al_menu_principal
        )
        btn_volver.pack(pady=20)
    
    def crear_contenido_ova_asimetria_curtosis(self, parent_frame):
        """Crea el contenido de la OVA de Asimetría, Curtosis y Normalidad en la pantalla principal"""
        
        # Sección 1: Introducción a la Asimetría
        intro_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        intro_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            intro_frame,
            text="1. ¿Qué es la Asimetría en Estadística?",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#ec4899'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            intro_frame,
            text="La asimetría mide el grado de desviación de una distribución respecto a su simetría. Es crucial para entender la forma de los datos y determinar si se aproximan a una distribución normal.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Caso clínico
        caso_frame = tk.Frame(intro_frame, bg='#fce7f3', relief='sunken', bd=1)
        caso_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            caso_frame,
            text="Caso Clínico: Distribución de Edades en Pacientes con Diabetes",
            font=('Arial', 12, 'bold'),
            bg='#fce7f3',
            fg='#be185d'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            caso_frame,
            text="Un estudio analiza la distribución de edades en pacientes diabéticos para determinar si la muestra es representativa de la población general.",
            font=('Arial', 10),
            bg='#fce7f3',
            fg='#be185d',
            wraplength=750,
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 2: Tipos de Asimetría
        asimetria_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        asimetria_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            asimetria_frame,
            text="2. Tipos de Asimetría y su Interpretación",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#dc2626'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Asimetría positiva
        pos_frame = tk.Frame(asimetria_frame, bg='#fee2e2', relief='sunken', bd=1)
        pos_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            pos_frame,
            text="Asimetría Positiva (Derecha):",
            font=('Arial', 12, 'bold'),
            bg='#fee2e2',
            fg='#dc2626'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            pos_frame,
            text="• Cola larga hacia la derecha\n• Media > Mediana > Moda\n• Coeficiente de asimetría > 0\n• Ejemplo: Distribución de ingresos, edades en enfermedades crónicas",
            font=('Arial', 10),
            bg='#fee2e2',
            fg='#dc2626',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Asimetría negativa
        neg_frame = tk.Frame(asimetria_frame, bg='#dbeafe', relief='sunken', bd=1)
        neg_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            neg_frame,
            text="Asimetría Negativa (Izquierda):",
            font=('Arial', 12, 'bold'),
            bg='#dbeafe',
            fg='#1e40af'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            neg_frame,
            text="• Cola larga hacia la izquierda\n• Media < Mediana < Moda\n• Coeficiente de asimetría < 0\n• Ejemplo: Distribución de calificaciones, tiempo de supervivencia",
            font=('Arial', 10),
            bg='#dbeafe',
            fg='#1e40af',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Simetría
        sim_frame = tk.Frame(asimetria_frame, bg='#d1fae5', relief='sunken', bd=1)
        sim_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            sim_frame,
            text="Simetría Perfecta:",
            font=('Arial', 12, 'bold'),
            bg='#d1fae5',
            fg='#047857'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            sim_frame,
            text="• Distribución balanceada\n• Media = Mediana = Moda\n• Coeficiente de asimetría ≈ 0\n• Ejemplo: Distribución normal estándar",
            font=('Arial', 10),
            bg='#d1fae5',
            fg='#047857',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 3: Curtosis
        curtosis_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        curtosis_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            curtosis_frame,
            text="3. ¿Qué es la Curtosis?",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#7c3aed'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            curtosis_frame,
            text="La curtosis mide qué tan 'puntiaguda' o 'plana' es una distribución comparada con la distribución normal. Indica la concentración de datos alrededor de la media.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Tipos de curtosis
        tipos_curtosis_frame = tk.Frame(curtosis_frame, bg='#ede9fe', relief='sunken', bd=1)
        tipos_curtosis_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            tipos_curtosis_frame,
            text="Tipos de Curtosis:",
            font=('Arial', 12, 'bold'),
            bg='#ede9fe',
            fg='#5b21b6'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            tipos_curtosis_frame,
            text="• Leptocúrtica (K > 3): Distribución más puntiaguda que la normal\n• Mesocúrtica (K = 3): Distribución normal estándar\n• Platicúrtica (K < 3): Distribución más plana que la normal",
            font=('Arial', 10),
            bg='#ede9fe',
            fg='#5b21b6',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 4: Pruebas de Normalidad
        normalidad_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        normalidad_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            normalidad_frame,
            text="4. Pruebas de Normalidad Prácticas",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#059669'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            normalidad_frame,
            text="Existen varios métodos para evaluar si los datos siguen una distribución normal. Algunos son gráficos y otros son pruebas estadísticas formales.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Métodos de evaluación
        metodos_frame = tk.Frame(normalidad_frame, bg='#d1fae5', relief='sunken', bd=1)
        metodos_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            metodos_frame,
            text="Métodos de Evaluación de Normalidad:",
            font=('Arial', 12, 'bold'),
            bg='#d1fae5',
            fg='#047857'
        ).pack(pady=10, padx=10, anchor='w')
        
        metodos_lista = [
            "• Histograma: Visualizar la forma de la distribución",
            "• Q-Q Plot: Comparar cuantiles con la distribución normal",
            "• Prueba de Shapiro-Wilk: Para muestras pequeñas (< 50)",
            "• Prueba de Kolmogorov-Smirnov: Para muestras grandes",
            "• Prueba de Anderson-Darling: Alternativa robusta"
        ]
        
        for metodo in metodos_lista:
            tk.Label(
                metodos_frame,
                text=metodo,
                font=('Arial', 10),
                bg='#d1fae5',
                fg='#047857',
                justify='left'
            ).pack(pady=2, padx=10, anchor='w')
        
        # Sección 5: Actividad Interactiva
        actividad_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        actividad_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            actividad_frame,
            text="5. Actividad: Evaluar Asimetría y Curtosis",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#1e40af'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            actividad_frame,
            text="Analiza el siguiente conjunto de datos y determina su asimetría y curtosis:",
            font=('Arial', 12),
            bg='white',
            fg='#374151'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Dataset de ejemplo
        dataset_frame = tk.Frame(actividad_frame, bg='#f3f4f6', relief='sunken', bd=1)
        dataset_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Datos de ejemplo (distribución asimétrica positiva)
        datos_ejemplo = [25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52, 55, 58, 60, 62, 65, 68, 70, 72, 75, 78, 80, 82, 85]
        
        # Crear encabezado
        tk.Label(
            dataset_frame,
            text="Edades de Pacientes (años) - n=25",
            font=('Arial', 10, 'bold'),
            bg='#d1d5db',
            fg='#374151'
        ).pack(pady=10, padx=10)
        
        # Mostrar datos en filas
        datos_frame = tk.Frame(dataset_frame, bg='#f3f4f6')
        datos_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        for i, dato in enumerate(datos_ejemplo):
            bg_color = '#f9fafb' if i % 2 == 0 else '#ffffff'
            tk.Label(
                datos_frame,
                text=str(dato),
                font=('Arial', 9),
                bg=bg_color,
                fg='#374151',
                width=6,
                relief='solid',
                bd=1
            ).grid(row=i//5, column=i%5, padx=1, pady=1, sticky='ew')
        
        # Configurar columnas para que se expandan
        for i in range(5):
            datos_frame.grid_columnconfigure(i, weight=1)
        
        # Botones para analizar
        botones_frame = tk.Frame(actividad_frame)
        botones_frame.pack(pady=(0, 15))
        
        analisis = [
            "Analizar Asimetría",
            "Analizar Curtosis",
            "Evaluar Normalidad",
            "Mostrar Estadísticas"
        ]
        
        for analisis_item in analisis:
            tk.Button(
                botones_frame,
                text=analisis_item,
                font=('Arial', 9),
                bg='#3b82f6',
                fg='white',
                command=lambda a=analisis_item: self.analizar_distribucion(a, datos_ejemplo)
            ).pack(side='left', padx=5)
        
        # Área de retroalimentación para la actividad
        self.feedback_area_asimetria = tk.Text(
            actividad_frame,
            height=10,
            width=80,
            font=('Arial', 9),
            bg='#f9fafb',
            fg='#374151',
            state='disabled'
        )
        self.feedback_area_asimetria.pack(pady=15, padx=15, fill='x')
        
        # Botón para limpiar retroalimentación
        tk.Button(
            actividad_frame,
            text="Limpiar Análisis",
            font=('Arial', 10),
            bg='#6b7280',
            fg='white',
            command=self.limpiar_retroalimentacion_asimetria
        ).pack(pady=(0, 15))
    
    def analizar_distribucion(self, tipo_analisis, datos):
        """Analiza la distribución de los datos según el tipo solicitado"""
        # Habilitar área de texto para escribir
        self.feedback_area_asimetria.config(state='normal')
        
        # Calcular estadísticas básicas
        n = len(datos)
        media = sum(datos) / n
        datos_ordenados = sorted(datos)
        
        # Calcular mediana
        if n % 2 == 0:
            mediana = (datos_ordenados[n//2 - 1] + datos_ordenados[n//2]) / 2
        else:
            mediana = datos_ordenados[n//2]
        
        # Calcular moda
        from collections import Counter
        frecuencias = Counter(datos)
        moda = max(frecuencias, key=frecuencias.get)
        
        # Calcular según el tipo de análisis
        if tipo_analisis == "Analizar Asimetría":
            # Coeficiente de asimetría de Pearson
            suma_cubos = sum((x - media) ** 3 for x in datos)
            varianza = sum((x - media) ** 2 for x in datos) / (n - 1)
            desv_est = varianza ** 0.5
            
            if desv_est > 0:
                asimetria = (suma_cubos / n) / (desv_est ** 3)
            else:
                asimetria = 0
            
            feedback = f"✓ Análisis de Asimetría:\n"
            feedback += f"   Media: {media:.2f}\n"
            feedback += f"   Mediana: {mediana:.2f}\n"
            feedback += f"   Moda: {moda}\n"
            feedback += f"   Coeficiente de Asimetría: {asimetria:.3f}\n\n"
            
            if asimetria > 0.5:
                feedback += f"   Interpretación: Asimetría POSITIVA (derecha)\n"
                feedback += f"   • Cola larga hacia la derecha\n"
                feedback += f"   • Media > Mediana > Moda\n"
                feedback += f"   • Distribución sesgada hacia valores altos\n"
            elif asimetria < -0.5:
                feedback += f"   Interpretación: Asimetría NEGATIVA (izquierda)\n"
                feedback += f"   • Cola larga hacia la izquierda\n"
                feedback += f"   • Media < Mediana < Moda\n"
                feedback += f"   • Distribución sesgada hacia valores bajos\n"
            else:
                feedback += f"   Interpretación: Distribución APROXIMADAMENTE SIMÉTRICA\n"
                feedback += f"   • Media ≈ Mediana ≈ Moda\n"
                feedback += f"   • Forma balanceada\n"
            
        elif tipo_analisis == "Analizar Curtosis":
            # Coeficiente de curtosis
            suma_cuartos = sum((x - media) ** 4 for x in datos)
            varianza = sum((x - media) ** 2 for x in datos) / (n - 1)
            desv_est = varianza ** 0.5
            
            if desv_est > 0:
                curtosis = (suma_cuartos / n) / (desv_est ** 4)
            else:
                curtosis = 0
            
            feedback = f"✓ Análisis de Curtosis:\n"
            feedback += f"   Coeficiente de Curtosis: {curtosis:.3f}\n"
            feedback += f"   Curtosis Normal: 3.000\n\n"
            
            if curtosis > 3.5:
                feedback += f"   Interpretación: LEPTOCÚRTICA\n"
                feedback += f"   • Distribución más puntiaguda que la normal\n"
                feedback += f"   • Datos concentrados alrededor de la media\n"
                feedback += f"   • Colas más delgadas\n"
            elif curtosis < 2.5:
                feedback += f"   Interpretación: PLATICÚRTICA\n"
                feedback += f"   • Distribución más plana que la normal\n"
                feedback += f"   • Datos más dispersos\n"
                feedback += f"   • Colas más gruesas\n"
            else:
                feedback += f"   Interpretación: MESOCÚRTICA\n"
                feedback += f"   • Distribución similar a la normal\n"
                feedback += f"   • Forma estándar\n"
            
        elif tipo_analisis == "Evaluar Normalidad":
            # Prueba simple de normalidad basada en regla empírica
            varianza = sum((x - media) ** 2 for x in datos) / (n - 1)
            desv_est = varianza ** 0.5
            
            # Contar datos dentro de 1, 2 y 3 desviaciones estándar
            dentro_1sd = sum(1 for x in datos if abs(x - media) <= desv_est)
            dentro_2sd = sum(1 for x in datos if abs(x - media) <= 2*desv_est)
            dentro_3sd = sum(1 for x in datos if abs(x - media) <= 3*desv_est)
            
            pct_1sd = (dentro_1sd / n) * 100
            pct_2sd = (dentro_2sd / n) * 100
            pct_3sd = (dentro_3sd / n) * 100
            
            feedback = f"✓ Evaluación de Normalidad (Regla Empírica):\n"
            feedback += f"   Media: {media:.2f}\n"
            feedback += f"   Desv. Estándar: {desv_est:.2f}\n\n"
            feedback += f"   Datos dentro de ±1 SD: {dentro_1sd}/{n} ({pct_1sd:.1f}%)\n"
            feedback += f"   Datos dentro de ±2 SD: {dentro_2sd}/{n} ({pct_2sd:.1f}%)\n"
            feedback += f"   Datos dentro de ±3 SD: {dentro_3sd}/{n} ({pct_3sd:.1f}%)\n\n"
            
            # Evaluar normalidad
            normal_1sd = 68.27
            normal_2sd = 95.45
            normal_3sd = 99.73
            
            if (abs(pct_1sd - normal_1sd) < 10 and 
                abs(pct_2sd - normal_2sd) < 10 and 
                abs(pct_3sd - normal_3sd) < 10):
                feedback += f"   CONCLUSIÓN: Los datos siguen APROXIMADAMENTE una distribución NORMAL\n"
                feedback += f"   • Cumple la regla empírica (68-95-99.7%)\n"
                feedback += f"   • Apropiado para pruebas paramétricas\n"
            else:
                feedback += f"   CONCLUSIÓN: Los datos NO siguen una distribución normal\n"
                feedback += f"   • No cumple la regla empírica\n"
                feedback += f"   • Considerar pruebas no paramétricas\n"
            
        elif tipo_analisis == "Mostrar Estadísticas":
            # Estadísticas descriptivas completas
            varianza = sum((x - media) ** 2 for x in datos) / (n - 1)
            desv_est = varianza ** 0.5
            rango = max(datos) - min(datos)
            
            feedback = f"✓ Estadísticas Descriptivas Completas:\n"
            feedback += f"   Tamaño de muestra (n): {n}\n"
            feedback += f"   Mínimo: {min(datos)}\n"
            feedback += f"   Máximo: {max(datos)}\n"
            feedback += f"   Rango: {rango}\n"
            feedback += f"   Media: {media:.2f}\n"
            feedback += f"   Mediana: {mediana:.2f}\n"
            feedback += f"   Moda: {moda}\n"
            feedback += f"   Varianza: {varianza:.2f}\n"
            feedback += f"   Desv. Estándar: {desv_est:.2f}\n"
            feedback += f"   Coeficiente de Variación: {(desv_est/media)*100:.2f}%\n"
        
        self.feedback_area_asimetria.insert('end', feedback + "\n")
        
        # Deshabilitar área de texto
        self.feedback_area_asimetria.config(state='disabled')
        
        # Hacer scroll hacia abajo
        self.feedback_area_asimetria.see('end')
    
    def limpiar_retroalimentacion_asimetria(self):
        """Limpia el área de retroalimentación de análisis de asimetría y curtosis"""
        self.feedback_area_asimetria.config(state='normal')
        self.feedback_area_asimetria.delete(1.0, 'end')
        self.feedback_area_asimetria.config(state='disabled')
    
    # ============================
    # OVA 7: Visualización para Salud I - Gráficos Categóricos
    # ============================
    def ejecutar_ova_visualizacion_categoricos(self):
        """Ejecuta la OVA de Visualización para salud I: gráficos categóricos en la misma pantalla"""
        try:
            # Limpiar la pantalla actual
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Configurar la pantalla para mostrar el contenido de la OVA
            self.root.title("OVA 7: Visualización para Salud I - Gráficos Categóricos")
            self.root.configure(bg='#f8f9fa')
            
            # Crear interfaz de la OVA en la misma pantalla
            self.mostrar_ova_visualizacion_categoricos_en_pantalla()
            
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Error al cargar la OVA:\n{str(e)}"
            )
    
    def mostrar_ova_visualizacion_categoricos_en_pantalla(self):
        """Muestra el contenido de la OVA de Visualización para Salud I en la pantalla principal"""
        
        # Header de la OVA
        header_ova = tk.Frame(self.root, bg='#10b981', height=120)
        header_ova.pack(fill='x', pady=(0, 20))
        header_ova.pack_propagate(False)
        
        # Título principal de la OVA
        titulo_ova = tk.Label(
            header_ova,
            text="OVA 7: Visualización para Salud I - Gráficos Categóricos",
            font=('Arial', 24, 'bold'),
            bg='#10b981',
            fg='white'
        )
        titulo_ova.pack(pady=30)
        
        # Subtítulo
        subtitulo_ova = tk.Label(
            header_ova,
            text="Universidad Antonio Nariño - Estadística Descriptiva para Ciencias de la Salud",
            font=('Arial', 12),
            bg='#10b981',
            fg='#d1fae5'
        )
        subtitulo_ova.pack()
        
        # Frame principal con scrollbar
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de la OVA
        self.crear_contenido_ova_visualizacion_categoricos(scrollable_frame)
        
        # Configurar scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Botón para volver al menú principal
        btn_volver = tk.Button(
            self.root,
            text="Volver al Menú Principal",
            font=('Arial', 12, 'bold'),
            bg='#28a745',
            fg='white',
            width=20,
            height=2,
            command=self.volver_al_menu_principal
        )
        btn_volver.pack(pady=20)
    
    def crear_contenido_ova_visualizacion_categoricos(self, parent_frame):
        """Crea el contenido de la OVA de Visualización para Salud I en la pantalla principal"""
        
        # Sección 1: Introducción a la Visualización en Salud
        intro_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        intro_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            intro_frame,
            text="1. Importancia de la Visualización en Ciencias de la Salud",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#10b981'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            intro_frame,
            text="La visualización de datos es fundamental en salud pública y epidemiología. Los gráficos permiten comunicar hallazgos complejos de manera clara y efectiva a diferentes audiencias.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Caso clínico
        caso_frame = tk.Frame(intro_frame, bg='#d1fae5', relief='sunken', bd=1)
        caso_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            caso_frame,
            text="Caso Clínico: Epidemia de COVID-19 en una Región",
            font=('Arial', 12, 'bold'),
            bg='#d1fae5',
            fg='#047857'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            caso_frame,
            text="Un equipo de salud pública necesita comunicar la distribución de casos por grupo de edad, género y comorbilidades a autoridades locales y población general.",
            font=('Arial', 10),
            bg='#d1fae5',
            fg='#047857',
            wraplength=750,
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 2: Tipos de Gráficos Categóricos
        graficos_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        graficos_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            graficos_frame,
            text="2. Principales Gráficos Categóricos en Salud",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#dc2626'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Gráfico de barras
        barras_frame = tk.Frame(graficos_frame, bg='#fee2e2', relief='sunken', bd=1)
        barras_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            barras_frame,
            text="Gráfico de Barras:",
            font=('Arial', 12, 'bold'),
            bg='#fee2e2',
            fg='#dc2626'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            barras_frame,
            text="• Ideal para comparar frecuencias entre categorías\n• Barras verticales u horizontales\n• Fácil interpretación para audiencias generales\n• Ejemplo: Distribución de diagnósticos por especialidad médica",
            font=('Arial', 10),
            bg='#fee2e2',
            fg='#dc2626',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Gráfico circular
        circular_frame = tk.Frame(graficos_frame, bg='#dbeafe', relief='sunken', bd=1)
        circular_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            circular_frame,
            text="Gráfico Circular (Pie Chart):",
            font=('Arial', 12, 'bold'),
            bg='#dbeafe',
            fg='#1e40af'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            circular_frame,
            text="• Muestra proporciones de un todo\n• Útil para composición de muestras\n• Limitado a pocas categorías (máximo 5-6)\n• Ejemplo: Distribución de tipos de cáncer por localización",
            font=('Arial', 10),
            bg='#dbeafe',
            fg='#1e40af',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Gráfico de líneas
        lineas_frame = tk.Frame(graficos_frame, bg='#fef3c7', relief='sunken', bd=1)
        lineas_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            lineas_frame,
            text="Gráfico de Líneas:",
            font=('Arial', 12, 'bold'),
            bg='#fef3c7',
            fg='#d97706'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            lineas_frame,
            text="• Ideal para mostrar tendencias temporales\n• Conecta puntos de datos secuenciales\n• Útil para series de tiempo epidemiológicas\n• Ejemplo: Evolución de casos de influenza por semana",
            font=('Arial', 10),
            bg='#fef3c7',
            fg='#d97706',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 3: Principios de Visualización Efectiva
        principios_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        principios_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            principios_frame,
            text="3. Principios de Visualización Efectiva en Salud",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#7c3aed'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            principios_frame,
            text="Una visualización efectiva debe ser clara, precisa y accesible para diferentes audiencias, desde profesionales de la salud hasta el público general.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Lista de principios
        principios_lista = [
            "• Simplicidad: Un gráfico debe transmitir una idea principal",
            "• Precisión: Los datos deben representarse sin distorsión",
            "• Accesibilidad: Colores y etiquetas comprensibles para todos",
            "• Contexto: Incluir títulos, fuentes y escalas apropiadas",
            "• Consistencia: Mantener convenciones en toda la presentación"
        ]
        
        principios_info_frame = tk.Frame(principios_frame, bg='#ede9fe', relief='sunken', bd=1)
        principios_info_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        for principio in principios_lista:
            tk.Label(
                principios_info_frame,
                text=principio,
                font=('Arial', 10),
                bg='#ede9fe',
                fg='#5b21b6',
                justify='left'
            ).pack(pady=2, padx=10, anchor='w')
        
        # Sección 4: Dataset de Ejemplo
        dataset_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        dataset_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            dataset_frame,
            text="4. Dataset de Ejemplo: Distribución de Pacientes por Especialidad",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#059669'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Datos de ejemplo
        especialidades = {
            "Cardiología": 45,
            "Neurología": 32,
            "Oncología": 28,
            "Pediatría": 67,
            "Ginecología": 53,
            "Traumatología": 41,
            "Dermatología": 38,
            "Psiquiatría": 29
        }
        
        # Crear tabla de datos
        tabla_frame = tk.Frame(dataset_frame, bg='#f3f4f6', relief='sunken', bd=1)
        tabla_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        headers = ["Especialidad", "Número de Pacientes", "Porcentaje"]
        for i, header in enumerate(headers):
            tk.Label(
                tabla_frame,
                text=header,
                font=('Arial', 10, 'bold'),
                bg='#d1d5db',
                fg='#374151',
                width=20
            ).grid(row=0, column=i, padx=2, pady=2, sticky='ew')
        
        total_pacientes = sum(especialidades.values())
        for row_idx, (esp, num) in enumerate(especialidades.items(), 1):
            porcentaje = (num / total_pacientes) * 100
            bg_color = '#f9fafb' if row_idx % 2 == 0 else '#ffffff'
            
            tk.Label(tabla_frame, text=esp, font=('Arial', 10), bg=bg_color, fg='#374151', width=20).grid(row=row_idx, column=0, padx=2, pady=1, sticky='ew')
            tk.Label(tabla_frame, text=str(num), font=('Arial', 10), bg=bg_color, fg='#374151', width=20).grid(row=row_idx, column=1, padx=2, pady=1, sticky='ew')
            tk.Label(tabla_frame, text=f"{porcentaje:.1f}%", font=('Arial', 10), bg=bg_color, fg='#374151', width=20).grid(row=row_idx, column=2, padx=2, pady=1, sticky='ew')
        
        for i in range(3):
            tabla_frame.grid_columnconfigure(i, weight=1)
        
        # Sección 5: Actividad Interactiva
        actividad_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        actividad_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            actividad_frame,
            text="5. Actividad: Crear Visualizaciones Categóricas",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#1e40af'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            actividad_frame,
            text="Utiliza el dataset anterior para crear diferentes tipos de visualizaciones:",
            font=('Arial', 12),
            bg='white',
            fg='#374151'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Botones para crear visualizaciones
        botones_frame = tk.Frame(actividad_frame)
        botones_frame.pack(pady=(0, 15))
        
        visualizaciones = [
            "Gráfico de Barras",
            "Gráfico Circular",
            "Gráfico Horizontal",
            "Análisis Comparativo"
        ]
        
        for viz in visualizaciones:
            tk.Button(
                botones_frame,
                text=viz,
                font=('Arial', 9),
                bg='#3b82f6',
                fg='white',
                command=lambda v=viz: self.crear_visualizacion_categorica(v, especialidades)
            ).pack(side='left', padx=5)
        
        # Área de visualización
        viz_frame = tk.Frame(actividad_frame, bg='#f9fafb', relief='sunken', bd=1)
        viz_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Canvas para dibujar gráficos simples
        self.canvas_viz = tk.Canvas(viz_frame, bg='white', height=300, width=700)
        self.canvas_viz.pack(pady=10, padx=10)
        
        # Área de retroalimentación
        self.feedback_area_viz = tk.Text(
            actividad_frame,
            height=6,
            width=80,
            font=('Arial', 9),
            bg='#f9fafb',
            fg='#374151',
            state='disabled'
        )
        self.feedback_area_viz.pack(pady=15, padx=15, fill='x')
        
        # Botón para limpiar
        tk.Button(
            actividad_frame,
            text="Limpiar Visualización",
            font=('Arial', 10),
            bg='#6b7280',
            fg='white',
            command=self.limpiar_visualizacion
        ).pack(pady=(0, 15))
    
    def crear_visualizacion_categorica(self, tipo, datos):
        """Crea una visualización categórica según el tipo solicitado"""
        # Limpiar canvas
        self.canvas_viz.delete("all")
        
        # Habilitar área de texto para escribir
        self.feedback_area_viz.config(state='normal')
        self.feedback_area_viz.delete(1.0, 'end')
        
        # Obtener datos ordenados
        datos_ordenados = sorted(datos.items(), key=lambda x: x[1], reverse=True)
        especialidades = [item[0] for item in datos_ordenados]
        valores = [item[1] for item in datos_ordenados]
        total = sum(valores)
        
        # Configurar dimensiones del canvas
        canvas_width = 700
        canvas_height = 300
        margin = 50
        
        if tipo == "Gráfico de Barras":
            # Crear gráfico de barras vertical
            bar_width = (canvas_width - 2*margin) / len(especialidades)
            max_valor = max(valores)
            
            # Dibujar ejes
            self.canvas_viz.create_line(margin, canvas_height-margin, canvas_width-margin, canvas_height-margin, width=2)  # Eje X
            self.canvas_viz.create_line(margin, margin, margin, canvas_height-margin, width=2)  # Eje Y
            
            # Dibujar barras
            for i, (esp, valor) in enumerate(datos_ordenados):
                x1 = margin + i * bar_width + 5
                x2 = margin + (i+1) * bar_width - 5
                y1 = canvas_height - margin
                y2 = canvas_height - margin - (valor / max_valor) * (canvas_height - 2*margin)
                
                # Color alternado para las barras
                color = '#3b82f6' if i % 2 == 0 else '#10b981'
                self.canvas_viz.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                
                # Etiqueta del valor
                self.canvas_viz.create_text((x1+x2)/2, y2-10, text=str(valor), font=('Arial', 8, 'bold'))
                
                # Etiqueta de la especialidad (rotada)
                self.canvas_viz.create_text((x1+x2)/2, canvas_height-margin+15, text=esp[:8], font=('Arial', 7), angle=45)
            
            feedback = f"✓ Gráfico de Barras Vertical creado\n"
            feedback += f"   • {len(especialidades)} especialidades mostradas\n"
            feedback += f"   • Cardiología tiene la mayor cantidad: {max(valores)} pacientes\n"
            feedback += f"   • Total de pacientes: {total}\n"
            
        elif tipo == "Gráfico Circular":
            # Crear gráfico circular simple
            center_x = canvas_width // 2
            center_y = canvas_height // 2
            radius = min(center_x, center_y) - margin
            
            # Colores para las secciones
            colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16', '#f97316']
            
            # Dibujar secciones del círculo
            current_angle = 0
            for i, (esp, valor) in enumerate(datos_ordenados):
                angle = (valor / total) * 360
                end_angle = current_angle + angle
                
                # Convertir ángulos a coordenadas
                start_x = center_x + radius * 0.7 * (current_angle / 360) * 2 * 3.14159
                start_y = center_y - radius * 0.7 * (current_angle / 360) * 2 * 3.14159
                end_x = center_x + radius * 0.7 * (end_angle / 360) * 2 * 3.14159
                end_y = center_y - radius * 0.7 * (end_angle / 360) * 2 * 3.14159
                
                # Dibujar arco (simplificado como línea)
                color = colors[i % len(colors)]
                self.canvas_viz.create_line(center_x, center_y, start_x, start_y, fill=color, width=2)
                self.canvas_viz.create_line(center_x, center_y, end_x, end_y, fill=color, width=2)
                
                # Etiqueta de porcentaje
                mid_angle = current_angle + angle/2
                label_x = center_x + (radius * 0.5) * (mid_angle / 360) * 2 * 3.14159
                label_y = center_y - (radius * 0.5) * (mid_angle / 360) * 2 * 3.14159
                porcentaje = (valor / total) * 100
                self.canvas_viz.create_text(label_x, label_y, text=f"{porcentaje:.1f}%", font=('Arial', 8, 'bold'))
                
                current_angle = end_angle
            
            # Círculo central
            self.canvas_viz.create_oval(center_x-10, center_y-10, center_x+10, center_y+10, fill='white', outline='black')
            
            feedback = f"✓ Gráfico Circular creado\n"
            feedback += f"   • {len(especialidades)} secciones representando especialidades\n"
            feedback += f"   • Pediatría representa el mayor porcentaje: {(max(valores)/total)*100:.1f}%\n"
            feedback += f"   • Distribución proporcional por especialidad\n"
            
        elif tipo == "Gráfico Horizontal":
            # Crear gráfico de barras horizontal
            bar_height = (canvas_height - 2*margin) / len(especialidades)
            max_valor = max(valores)
            
            # Dibujar ejes
            self.canvas_viz.create_line(margin, margin, margin, canvas_height-margin, width=2)  # Eje Y
            self.canvas_viz.create_line(margin, canvas_height-margin, canvas_width-margin, canvas_height-margin, width=2)  # Eje X
            
            # Dibujar barras horizontales
            for i, (esp, valor) in enumerate(datos_ordenados):
                y1 = margin + i * bar_height + 5
                y2 = margin + (i+1) * bar_height - 5
                x1 = margin
                x2 = margin + (valor / max_valor) * (canvas_width - 2*margin)
                
                # Color alternado para las barras
                color = '#8b5cf6' if i % 2 == 0 else '#06b6d4'
                self.canvas_viz.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                
                # Etiqueta del valor
                self.canvas_viz.create_text(x2+10, (y1+y2)/2, text=str(valor), font=('Arial', 8, 'bold'))
                
                # Etiqueta de la especialidad
                self.canvas_viz.create_text(margin-5, (y1+y2)/2, text=esp[:12], font=('Arial', 8), anchor='e')
            
            feedback = f"✓ Gráfico de Barras Horizontal creado\n"
            feedback += f"   • {len(especialidades)} especialidades ordenadas por número de pacientes\n"
            feedback += f"   • Fácil comparación entre categorías\n"
            feedback += f"   • Etiquetas de especialidades legibles\n"
            
        elif tipo == "Análisis Comparativo":
            # Crear análisis comparativo con múltiples métricas
            self.canvas_viz.create_text(canvas_width//2, 30, text="ANÁLISIS COMPARATIVO", font=('Arial', 14, 'bold'))
            
            # Top 3 especialidades
            top3 = datos_ordenados[:3]
            y_start = 80
            
            for i, (esp, valor) in enumerate(top3):
                y_pos = y_start + i * 50
                color = ['#ef4444', '#f59e0b', '#10b981'][i]
                
                # Rango y especialidad
                self.canvas_viz.create_text(100, y_pos, text=f"{i+1}°", font=('Arial', 12, 'bold'), fill=color)
                self.canvas_viz.create_text(150, y_pos, text=esp, font=('Arial', 10, 'bold'))
                
                # Valor y porcentaje
                porcentaje = (valor / total) * 100
                self.canvas_viz.create_text(400, y_pos, text=f"{valor} pacientes", font=('Arial', 10))
                self.canvas_viz.create_text(500, y_pos, text=f"({porcentaje:.1f}%)", font=('Arial', 10))
                
                # Barra de progreso
                bar_width = (valor / max(valores)) * 200
                self.canvas_viz.create_rectangle(600, y_pos-8, 600+bar_width, y_pos+8, fill=color, outline='black')
            
            # Estadísticas generales
            y_stats = y_start + 200
            self.canvas_viz.create_text(100, y_stats, text="ESTADÍSTICAS:", font=('Arial', 12, 'bold'))
            self.canvas_viz.create_text(100, y_stats+25, text=f"Total de pacientes: {total}", font=('Arial', 10))
            self.canvas_viz.create_text(100, y_stats+45, text=f"Promedio por especialidad: {total/len(especialidades):.1f}", font=('Arial', 10))
            self.canvas_viz.create_text(100, y_stats+65, text=f"Especialidad con más pacientes: {max(datos_ordenados, key=lambda x: x[1])[0]}", font=('Arial', 10))
            
            feedback = f"✓ Análisis Comparativo creado\n"
            feedback += f"   • Top 3 especialidades por número de pacientes\n"
            feedback += f"   • Estadísticas generales del dataset\n"
            feedback += f"   • Comparación visual con barras de progreso\n"
        
        self.feedback_area_viz.insert('end', feedback + "\n")
        
        # Deshabilitar área de texto
        self.feedback_area_viz.config(state='disabled')
    
    def limpiar_visualizacion(self):
        """Limpia el canvas de visualización y el área de retroalimentación"""
        self.canvas_viz.delete("all")
        self.feedback_area_viz.config(state='normal')
        self.feedback_area_viz.delete(1.0, 'end')
        self.feedback_area_viz.config(state='disabled')
    
    # ============================
    # OVA 8: Visualización para Salud II - Gráficos Numéricos
    # ============================
    def ejecutar_ova_visualizacion_numerica(self):
        """Ejecuta la OVA de Visualización para salud II: gráficos numéricos en la misma pantalla"""
        try:
            # Limpiar la pantalla actual
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Configurar la pantalla para mostrar el contenido de la OVA
            self.root.title("OVA 8: Visualización para Salud II - Gráficos Numéricos")
            self.root.configure(bg='#f8f9fa')
            
            # Crear interfaz de la OVA en la misma pantalla
            self.mostrar_ova_visualizacion_numerica_en_pantalla()
            
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Error al cargar la OVA:\n{str(e)}"
            )
    
    def mostrar_ova_visualizacion_numerica_en_pantalla(self):
        """Muestra el contenido de la OVA de Visualización para Salud II en la pantalla principal"""
        
        # Header de la OVA
        header_ova = tk.Frame(self.root, bg='#8b5cf6', height=120)
        header_ova.pack(fill='x', pady=(0, 20))
        header_ova.pack_propagate(False)
        
        # Título principal de la OVA
        titulo_ova = tk.Label(
            header_ova,
            text="OVA 8: Visualización para Salud II - Gráficos Numéricos",
            font=('Arial', 24, 'bold'),
            bg='#8b5cf6',
            fg='white'
        )
        titulo_ova.pack(pady=30)
        
        # Subtítulo
        subtitulo_ova = tk.Label(
            header_ova,
            text="Universidad Antonio Nariño - Estadística Descriptiva para Ciencias de la Salud",
            font=('Arial', 12),
            bg='#8b5cf6',
            fg='#c4b5fd'
        )
        subtitulo_ova.pack()
        
        # Frame principal con scrollbar
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de la OVA
        self.crear_contenido_ova_visualizacion_numerica(scrollable_frame)
        
        # Configurar scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Botón para volver al menú principal
        btn_volver = tk.Button(
            self.root,
            text="Volver al Menú Principal",
            font=('Arial', 12, 'bold'),
            bg='#28a745',
            fg='white',
            width=20,
            height=2,
            command=self.volver_al_menu_principal
        )
        btn_volver.pack(pady=20)
    
    def crear_contenido_ova_visualizacion_numerica(self, parent_frame):
        """Crea el contenido de la OVA de Visualización para Salud II en la pantalla principal"""
        
        # Sección 1: Introducción a Gráficos Numéricos en Salud
        intro_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        intro_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            intro_frame,
            text="1. Gráficos Numéricos en Ciencias de la Salud",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#8b5cf6'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            intro_frame,
            text="Los gráficos numéricos son fundamentales para analizar variables continuas, distribuciones y relaciones entre variables en estudios clínicos y epidemiológicos.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Caso clínico
        caso_frame = tk.Frame(intro_frame, bg='#ede9fe', relief='sunken', bd=1)
        caso_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            caso_frame,
            text="Caso Clínico: Estudio de Presión Arterial y Edad",
            font=('Arial', 12, 'bold'),
            bg='#ede9fe',
            fg='#5b21b6'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            caso_frame,
            text="Un cardiólogo investiga la relación entre la edad de los pacientes y su presión arterial sistólica para identificar patrones y factores de riesgo.",
            font=('Arial', 10),
            bg='#ede9fe',
            fg='#5b21b6',
            wraplength=750,
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 2: Tipos de Gráficos Numéricos
        graficos_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        graficos_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            graficos_frame,
            text="2. Principales Gráficos Numéricos en Salud",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#dc2626'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Histograma
        histograma_frame = tk.Frame(graficos_frame, bg='#fee2e2', relief='sunken', bd=1)
        histograma_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            histograma_frame,
            text="Histograma:",
            font=('Arial', 12, 'bold'),
            bg='#fee2e2',
            fg='#dc2626'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            histograma_frame,
            text="• Muestra la distribución de frecuencias de una variable continua\n• Barras adyacentes sin espacios\n• Útil para identificar forma de distribución (normal, asimétrica)\n• Ejemplo: Distribución de presión arterial en una población",
            font=('Arial', 10),
            bg='#fee2e2',
            fg='#dc2626',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Gráfico de dispersión
        dispersion_frame = tk.Frame(graficos_frame, bg='#dbeafe', relief='sunken', bd=1)
        dispersion_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(
            dispersion_frame,
            text="Gráfico de Dispersión (Scatter Plot):",
            font=('Arial', 12, 'bold'),
            bg='#dbeafe',
            fg='#1e40af'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            dispersion_frame,
            text="• Muestra la relación entre dos variables numéricas\n• Cada punto representa una observación\n• Útil para identificar correlaciones y patrones\n• Ejemplo: Relación entre edad y presión arterial",
            font=('Arial', 10),
            bg='#dbeafe',
            fg='#1e40af',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Gráfico de cajas
        cajas_frame = tk.Frame(graficos_frame, bg='#d1fae5', relief='sunken', bd=1)
        cajas_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(
            cajas_frame,
            text="Gráfico de Cajas (Box Plot):",
            font=('Arial', 12, 'bold'),
            bg='#d1fae5',
            fg='#047857'
        ).pack(pady=10, padx=10, anchor='w')
        
        tk.Label(
            cajas_frame,
            text="• Muestra la distribución y valores atípicos\n• Incluye mediana, cuartiles y rango\n• Ideal para comparar grupos\n• Ejemplo: Comparar presión arterial entre grupos de edad",
            font=('Arial', 10),
            bg='#d1fae5',
            fg='#047857',
            justify='left'
        ).pack(pady=(0, 10), padx=10, anchor='w')
        
        # Sección 3: Interpretación de Gráficos Numéricos
        interpretacion_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        interpretacion_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            interpretacion_frame,
            text="3. Interpretación de Gráficos Numéricos en Salud",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#7c3aed'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            interpretacion_frame,
            text="La interpretación correcta de gráficos numéricos es crucial para extraer conclusiones válidas en investigación clínica.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Elementos de interpretación
        elementos_lista = [
            "• Forma de la distribución: Normal, asimétrica, bimodal",
            "• Centro de los datos: Media, mediana, moda",
            "• Dispersión: Rango, desviación estándar, cuartiles",
            "• Valores atípicos: Puntos que se desvían significativamente",
            "• Relaciones: Correlación, tendencias, patrones"
        ]
        
        elementos_info_frame = tk.Frame(interpretacion_frame, bg='#ede9fe', relief='sunken', bd=1)
        elementos_info_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        for elemento in elementos_lista:
            tk.Label(
                elementos_info_frame,
                text=elemento,
                font=('Arial', 10),
                bg='#ede9fe',
                fg='#5b21b6',
                justify='left'
            ).pack(pady=2, padx=10, anchor='w')
        
        # Sección 4: Dataset de Ejemplo
        dataset_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        dataset_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            dataset_frame,
            text="4. Dataset de Ejemplo: Presión Arterial y Edad",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#059669'
        ).pack(pady=15, padx=15, anchor='w')
        
        # Datos de ejemplo (edad, presión arterial)
        datos_ejemplo = [
            (25, 120), (30, 125), (35, 128), (40, 132), (45, 135),
            (50, 140), (55, 145), (60, 150), (65, 155), (70, 160),
            (75, 165), (80, 170), (85, 175), (90, 180), (95, 185)
        ]
        
        # Crear tabla de datos
        tabla_frame = tk.Frame(dataset_frame, bg='#f3f4f6', relief='sunken', bd=1)
        tabla_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        headers = ["Edad (años)", "Presión Sistólica (mmHg)"]
        for i, header in enumerate(headers):
            tk.Label(
                tabla_frame,
                text=header,
                font=('Arial', 10, 'bold'),
                bg='#d1d5db',
                fg='#374151',
                width=25
            ).grid(row=0, column=i, padx=2, pady=2, sticky='ew')
        
        for row_idx, (edad, presion) in enumerate(datos_ejemplo, 1):
            bg_color = '#f9fafb' if row_idx % 2 == 0 else '#ffffff'
            tk.Label(tabla_frame, text=str(edad), font=('Arial', 10), bg=bg_color, fg='#374151', width=25).grid(row=row_idx, column=0, padx=2, pady=1, sticky='ew')
            tk.Label(tabla_frame, text=str(presion), font=('Arial', 10), bg=bg_color, fg='#374151', width=25).grid(row=row_idx, column=1, padx=2, pady=1, sticky='ew')
        
        for i in range(2):
            tabla_frame.grid_columnconfigure(i, weight=1)
        
        # Sección 5: Actividad Interactiva
        actividad_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        actividad_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            actividad_frame,
            text="5. Actividad: Crear Gráficos Numéricos",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#1e40af'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            actividad_frame,
            text="Utiliza el dataset anterior para crear diferentes tipos de gráficos numéricos:",
            font=('Arial', 12),
            bg='white',
            fg='#374151'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Botones para crear gráficos
        botones_frame = tk.Frame(actividad_frame)
        botones_frame.pack(pady=(0, 15))
        
        graficos = [
            "Histograma",
            "Gráfico de Dispersión",
            "Gráfico de Cajas",
            "Análisis Estadístico"
        ]
        
        for grafico in graficos:
            tk.Button(
                botones_frame,
                text=grafico,
                font=('Arial', 9),
                bg='#3b82f6',
                fg='white',
                command=lambda g=grafico: self.crear_grafico_numerico(g, datos_ejemplo)
            ).pack(side='left', padx=5)
        
        # Área de visualización
        viz_frame = tk.Frame(actividad_frame, bg='#f9fafb', relief='sunken', bd=1)
        viz_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Canvas para dibujar gráficos
        self.canvas_numerico = tk.Canvas(viz_frame, bg='white', height=350, width=700)
        self.canvas_numerico.pack(pady=10, padx=10)
        
        # Área de retroalimentación
        self.feedback_area_numerico = tk.Text(
            actividad_frame,
            height=8,
            width=80,
            font=('Arial', 9),
            bg='#f9fafb',
            fg='#374151',
            state='disabled'
        )
        self.feedback_area_numerico.pack(pady=15, padx=15, fill='x')
        
        # Botón para limpiar
        tk.Button(
            actividad_frame,
            text="Limpiar Gráfico",
            font=('Arial', 10),
            bg='#6b7280',
            fg='white',
            command=self.limpiar_grafico_numerico
        ).pack(pady=(0, 15))
    
    def crear_grafico_numerico(self, tipo, datos):
        """Crea un gráfico numérico según el tipo solicitado"""
        # Limpiar canvas
        self.canvas_numerico.delete("all")
        
        # Habilitar área de texto para escribir
        self.feedback_area_numerico.config(state='normal')
        self.feedback_area_numerico.delete(1.0, 'end')
        
        # Extraer variables
        edades = [d[0] for d in datos]
        presiones = [d[1] for d in datos]
        
        # Configurar dimensiones del canvas
        canvas_width = 700
        canvas_height = 350
        margin = 60
        
        if tipo == "Histograma":
            # Crear histograma de presión arterial
            # Definir rangos (bins)
            min_presion = min(presiones)
            max_presion = max(presiones)
            num_bins = 6
            bin_width = (max_presion - min_presion) / num_bins
            
            # Contar frecuencias por bin
            frecuencias = [0] * num_bins
            for presion in presiones:
                bin_index = min(int((presion - min_presion) / bin_width), num_bins - 1)
                frecuencias[bin_index] += 1
            
            # Dibujar ejes
            self.canvas_numerico.create_line(margin, canvas_height-margin, canvas_width-margin, canvas_height-margin, width=2)  # Eje X
            self.canvas_numerico.create_line(margin, margin, margin, canvas_height-margin, width=2)  # Eje Y
            
            # Etiquetas de ejes
            self.canvas_numerico.create_text(canvas_width//2, canvas_height-margin+20, text="Presión Arterial Sistólica (mmHg)", font=('Arial', 10, 'bold'))
            self.canvas_numerico.create_text(margin-20, canvas_height//2, text="Frecuencia", font=('Arial', 10, 'bold'), angle=90)
            
            # Dibujar barras del histograma
            max_freq = max(frecuencias)
            bar_width = (canvas_width - 2*margin) / num_bins
            
            for i, freq in enumerate(frecuencias):
                if freq > 0:
                    x1 = margin + i * bar_width + 2
                    x2 = margin + (i+1) * bar_width - 2
                    y1 = canvas_height - margin
                    y2 = canvas_height - margin - (freq / max_freq) * (canvas_height - 2*margin)
                    
                    # Color alternado para las barras
                    color = '#8b5cf6' if i % 2 == 0 else '#06b6d4'
                    self.canvas_numerico.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                    
                    # Etiqueta del valor
                    self.canvas_numerico.create_text((x1+x2)/2, y2-10, text=str(freq), font=('Arial', 8, 'bold'))
                    
                    # Etiqueta del rango
                    bin_start = min_presion + i * bin_width
                    bin_end = min_presion + (i+1) * bin_width
                    self.canvas_numerico.create_text((x1+x2)/2, canvas_height-margin+15, text=f"{bin_start:.0f}-{bin_end:.0f}", font=('Arial', 7))
            
            feedback = f"✓ Histograma de Presión Arterial creado\n"
            feedback += f"   • {num_bins} rangos (bins) de presión arterial\n"
            feedback += f"   • Rango total: {min_presion}-{max_presion} mmHg\n"
            feedback += f"   • Frecuencia máxima: {max_freq} pacientes\n"
            feedback += f"   • Distribución: {len([f for f in frecuencias if f > 0])} rangos con datos\n"
            
        elif tipo == "Gráfico de Dispersión":
            # Crear gráfico de dispersión edad vs presión arterial
            # Escalar datos al canvas
            min_edad = min(edades)
            max_edad = max(edades)
            min_presion = min(presiones)
            max_presion = max(presiones)
            
            # Dibujar ejes
            self.canvas_numerico.create_line(margin, canvas_height-margin, canvas_width-margin, canvas_height-margin, width=2)  # Eje X
            self.canvas_numerico.create_line(margin, margin, margin, canvas_height-margin, width=2)  # Eje Y
            
            # Etiquetas de ejes
            self.canvas_numerico.create_text(canvas_width//2, canvas_height-margin+20, text="Edad (años)", font=('Arial', 10, 'bold'))
            self.canvas_numerico.create_text(margin-20, canvas_height//2, text="Presión Arterial (mmHg)", font=('Arial', 10, 'bold'), angle=90)
            
            # Dibujar puntos de dispersión
            for edad, presion in datos:
                # Escalar coordenadas
                x = margin + (edad - min_edad) / (max_edad - min_edad) * (canvas_width - 2*margin)
                y = canvas_height - margin - (presion - min_presion) / (max_presion - min_presion) * (canvas_height - 2*margin)
                
                # Punto con etiqueta
                self.canvas_numerico.create_oval(x-3, y-3, x+3, y+3, fill='#ef4444', outline='black')
                self.canvas_numerico.create_text(x+8, y-8, text=f"({edad},{presion})", font=('Arial', 6))
            
            # Línea de tendencia (simplificada)
            # Calcular pendiente promedio
            if len(datos) > 1:
                x_coords = []
                y_coords = []
                for edad, presion in datos:
                    x = margin + (edad - min_edad) / (max_edad - min_edad) * (canvas_width - 2*margin)
                    y = canvas_height - margin - (presion - min_presion) / (max_presion - min_presion) * (canvas_height - 2*margin)
                    x_coords.append(x)
                    y_coords.append(y)
                
                # Dibujar línea de tendencia
                self.canvas_numerico.create_line(x_coords[0], y_coords[0], x_coords[-1], y_coords[-1], fill='#3b82f6', width=2, dash=(5,5))
                self.canvas_numerico.create_text(x_coords[-1]+20, y_coords[-1], text="Tendencia", font=('Arial', 8), fill='#3b82f6')
            
            feedback = f"✓ Gráfico de Dispersión creado\n"
            feedback += f"   • {len(datos)} puntos de datos (edad vs presión arterial)\n"
            feedback += f"   • Rango de edad: {min_edad}-{max_edad} años\n"
            feedback += f"   • Rango de presión: {min_presion}-{max_presion} mmHg\n"
            feedback += f"   • Línea de tendencia: Presión arterial aumenta con la edad\n"
            
        elif tipo == "Gráfico de Cajas":
            # Crear gráfico de cajas para presión arterial
            # Calcular estadísticas
            presiones_ordenadas = sorted(presiones)
            n = len(presiones_ordenadas)
            q1_pos = (n + 1) * 0.25
            q2_pos = (n + 1) * 0.50
            q3_pos = (n + 1) * 0.75
            
            q1 = presiones_ordenadas[int(q1_pos) - 1] if q1_pos.is_integer() else \
                 presiones_ordenadas[int(q1_pos) - 1] + (q1_pos - int(q1_pos)) * (presiones_ordenadas[int(q1_pos)] - presiones_ordenadas[int(q1_pos) - 1])
            q2 = presiones_ordenadas[int(q2_pos) - 1] if q2_pos.is_integer() else \
                 presiones_ordenadas[int(q2_pos) - 1] + (q2_pos - int(q2_pos)) * (presiones_ordenadas[int(q2_pos)] - presiones_ordenadas[int(q2_pos) - 1])
            q3 = presiones_ordenadas[int(q3_pos) - 1] if q3_pos.is_integer() else \
                 presiones_ordenadas[int(q3_pos) - 1] + (q3_pos - int(q3_pos)) * (presiones_ordenadas[int(q3_pos)] - presiones_ordenadas[int(q3_pos) - 1])
            
            iqr = q3 - q1
            limite_inferior = q1 - 1.5 * iqr
            limite_superior = q3 + 1.5 * iqr
            
            # Escalar al canvas
            min_presion = min(presiones)
            max_presion = max(presiones)
            rango = max_presion - min_presion
            
            # Dibujar ejes
            self.canvas_numerico.create_line(margin, canvas_height-margin, canvas_width-margin, canvas_height-margin, width=2)  # Eje X
            self.canvas_numerico.create_line(margin, margin, margin, canvas_height-margin, width=2)  # Eje Y
            
            # Etiqueta del eje Y
            self.canvas_numerico.create_text(margin-20, canvas_height//2, text="Presión Arterial (mmHg)", font=('Arial', 10, 'bold'), angle=90)
            
            # Posición central del gráfico de cajas
            box_center_x = canvas_width // 2
            box_width = 100
            
            # Escalar valores
            def escalar(valor):
                return canvas_height - margin - (valor - min_presion) / rango * (canvas_height - 2*margin)
            
            # Dibujar bigotes
            bigote_inferior = escalar(max(limite_inferior, min_presion))
            bigote_superior = escalar(min(limite_superior, max_presion))
            q1_y = escalar(q1)
            q2_y = escalar(q2)
            q3_y = escalar(q3)
            
            # Línea horizontal del bigote inferior
            self.canvas_numerico.create_line(box_center_x - box_width//2, bigote_inferior, box_center_x + box_width//2, bigote_inferior, width=2)
            # Línea vertical del bigote inferior
            self.canvas_numerico.create_line(box_center_x, bigote_inferior, box_center_x, q1_y, width=2)
            
            # Línea horizontal del bigote superior
            self.canvas_numerico.create_line(box_center_x - box_width//2, bigote_superior, box_center_x + box_width//2, bigote_superior, width=2)
            # Línea vertical del bigote superior
            self.canvas_numerico.create_line(box_center_x, bigote_superior, box_center_x, q3_y, width=2)
            
            # Caja principal
            self.canvas_numerico.create_rectangle(box_center_x - box_width//2, q1_y, box_center_x + box_width//2, q3_y, fill='#10b981', outline='black', width=2)
            
            # Línea de la mediana
            self.canvas_numerico.create_line(box_center_x - box_width//2, q2_y, box_center_x + box_width//2, q2_y, fill='white', width=3)
            
            # Etiquetas de valores
            self.canvas_numerico.create_text(box_center_x, bigote_inferior-10, text=f"{max(limite_inferior, min_presion):.0f}", font=('Arial', 8))
            self.canvas_numerico.create_text(box_center_x, q1_y-10, text=f"Q1: {q1:.0f}", font=('Arial', 8))
            self.canvas_numerico.create_text(box_center_x, q2_y-10, text=f"Q2: {q2:.0f}", font=('Arial', 8))
            self.canvas_numerico.create_text(box_center_x, q3_y-10, text=f"Q3: {q3:.0f}", font=('Arial', 8))
            self.canvas_numerico.create_text(box_center_x, bigote_superior-10, text=f"{min(limite_superior, max_presion):.0f}", font=('Arial', 8))
            
            # Título
            self.canvas_numerico.create_text(box_center_x, margin-10, text="Gráfico de Cajas - Presión Arterial", font=('Arial', 12, 'bold'))
            
            feedback = f"✓ Gráfico de Cajas creado\n"
            feedback += f"   • Q1 (25%): {q1:.1f} mmHg\n"
            feedback += f"   • Q2/Mediana (50%): {q2:.1f} mmHg\n"
            feedback += f"   • Q3 (75%): {q3:.1f} mmHg\n"
            feedback += f"   • Rango Intercuartílico: {iqr:.1f} mmHg\n"
            feedback += f"   • Límites de bigotes: {limite_inferior:.1f} - {limite_superior:.1f} mmHg\n"
            
        elif tipo == "Análisis Estadístico":
            # Crear análisis estadístico completo
            # Calcular estadísticas
            media_edad = sum(edades) / len(edades)
            media_presion = sum(presiones) / len(presiones)
            
            # Varianza y desviación estándar
            varianza_edad = sum((x - media_edad) ** 2 for x in edades) / (len(edades) - 1)
            desv_est_edad = varianza_edad ** 0.5
            varianza_presion = sum((x - media_presion) ** 2 for x in presiones) / (len(presiones) - 1)
            desv_est_presion = varianza_presion ** 0.5
            
            # Correlación
            n = len(datos)
            suma_productos = sum((edades[i] - media_edad) * (presiones[i] - media_presion) for i in range(n))
            correlacion = suma_productos / ((n-1) * desv_est_edad * desv_est_presion)
            
            # Dibujar análisis
            self.canvas_numerico.create_text(canvas_width//2, 30, text="ANÁLISIS ESTADÍSTICO COMPLETO", font=('Arial', 14, 'bold'))
            
            # Estadísticas de edad
            y_start = 70
            self.canvas_numerico.create_text(100, y_start, text="ESTADÍSTICAS DE EDAD:", font=('Arial', 12, 'bold'), fill='#1e40af')
            self.canvas_numerico.create_text(100, y_start+25, text=f"Media: {media_edad:.1f} años", font=('Arial', 10))
            self.canvas_numerico.create_text(100, y_start+45, text=f"Desv. Estándar: {desv_est_edad:.1f} años", font=('Arial', 10))
            self.canvas_numerico.create_text(100, y_start+65, text=f"Rango: {min(edades)} - {max(edades)} años", font=('Arial', 10))
            
            # Estadísticas de presión arterial
            y_start += 100
            self.canvas_numerico.create_text(100, y_start, text="ESTADÍSTICAS DE PRESIÓN ARTERIAL:", font=('Arial', 12, 'bold'), fill='#dc2626')
            self.canvas_numerico.create_text(100, y_start+25, text=f"Media: {media_presion:.1f} mmHg", font=('Arial', 10))
            self.canvas_numerico.create_text(100, y_start+45, text=f"Desv. Estándar: {desv_est_presion:.1f} mmHg", font=('Arial', 10))
            self.canvas_numerico.create_text(100, y_start+65, text=f"Rango: {min(presiones)} - {max(presiones)} mmHg", font=('Arial', 10))
            
            # Correlación
            y_start += 100
            self.canvas_numerico.create_text(100, y_start, text="ANÁLISIS DE CORRELACIÓN:", font=('Arial', 12, 'bold'), fill='#059669')
            self.canvas_numerico.create_text(100, y_start+25, text=f"Coeficiente de Correlación: {correlacion:.3f}", font=('Arial', 10))
            
            # Interpretación de correlación
            if correlacion > 0.7:
                interpretacion = "Correlación POSITIVA FUERTE"
            elif correlacion > 0.3:
                interpretacion = "Correlación POSITIVA MODERADA"
            elif correlacion > 0:
                interpretacion = "Correlación POSITIVA DÉBIL"
            elif correlacion < -0.7:
                interpretacion = "Correlación NEGATIVA FUERTE"
            elif correlacion < -0.3:
                interpretacion = "Correlación NEGATIVA MODERADA"
            elif correlacion < 0:
                interpretacion = "Correlación NEGATIVA DÉBIL"
            else:
                interpretacion = "Sin correlación lineal"
            
            self.canvas_numerico.create_text(100, y_start+45, text=f"Interpretación: {interpretacion}", font=('Arial', 10))
            self.canvas_numerico.create_text(100, y_start+65, text="La presión arterial tiende a aumentar con la edad", font=('Arial', 10))
            
            feedback = f"✓ Análisis Estadístico Completo creado\n"
            feedback += f"   • Media de edad: {media_edad:.1f} años\n"
            feedback += f"   • Media de presión arterial: {media_presion:.1f} mmHg\n"
            feedback += f"   • Coeficiente de correlación: {correlacion:.3f}\n"
            feedback += f"   • Interpretación: {interpretacion}\n"
            feedback += f"   • Conclusión: Existe una relación positiva entre edad y presión arterial\n"
        
        self.feedback_area_numerico.insert('end', feedback + "\n")
        
        # Deshabilitar área de texto
        self.feedback_area_numerico.config(state='disabled')
    
    def limpiar_grafico_numerico(self):
        """Limpia el canvas de gráficos numéricos y el área de retroalimentación"""
        self.canvas_numerico.delete("all")
        self.feedback_area_numerico.config(state='normal')
        self.feedback_area_numerico.delete(1.0, 'end')
        self.feedback_area_numerico.config(state='disabled')

    # ============================
    # OVA 3: Tablas de Frecuencias
    # ============================
    def ejecutar_ova_tablas_frecuencias(self):
        """Ejecuta la OVA de Tablas de frecuencias y resúmenes categóricos en la misma pantalla"""
        try:
            # Limpiar la pantalla actual
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Configurar la pantalla para mostrar el contenido de la OVA
            self.root.title("OVA 3: Tablas de Frecuencias y Resúmenes Categóricos")
            self.root.configure(bg='#f8f9fa')
            
            # Crear interfaz de la OVA en la misma pantalla
            self.mostrar_ova_tablas_frecuencias_en_pantalla()
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Error al cargar la OVA:\n{str(e)}"
            )

    def mostrar_ova_tablas_frecuencias_en_pantalla(self):
        """Muestra el contenido de la OVA de Tablas de frecuencias en la pantalla principal"""
        
        # Header de la OVA
        header_ova = tk.Frame(self.root, bg='#0ea5e9', height=120)
        header_ova.pack(fill='x', pady=(0, 20))
        header_ova.pack_propagate(False)
        
        # Título principal de la OVA
        titulo_ova = tk.Label(
            header_ova,
            text="OVA 3: Tablas de Frecuencias y Resúmenes Categóricos",
            font=('Arial', 24, 'bold'),
            bg='#0ea5e9',
            fg='white'
        )
        titulo_ova.pack(pady=30)
        
        # Subtítulo
        subtitulo_ova = tk.Label(
            header_ova,
            text="Universidad Antonio Nariño - Estadística Descriptiva para Ciencias de la Salud",
            font=('Arial', 12),
            bg='#0ea5e9',
            fg='#cffafe'
        )
        subtitulo_ova.pack()
        
        # Frame principal con scrollbar
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido de la OVA
        self.crear_contenido_ova_tablas_frecuencias(scrollable_frame)
        
        # Configurar scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Botón para volver al menú principal
        btn_volver = tk.Button(
            self.root,
            text="Volver al Menú Principal",
            font=('Arial', 12, 'bold'),
            bg='#28a745',
            fg='white',
            width=20,
            height=2,
            command=self.volver_al_menu_principal
        )
        btn_volver.pack(pady=20)

    def crear_contenido_ova_tablas_frecuencias(self, parent_frame):
        """Crea el contenido de la OVA de Tablas de Frecuencias en la pantalla principal"""
        
        # Sección 1: Introducción
        intro_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        intro_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            intro_frame,
            text="1. Tablas de Frecuencias y Resúmenes Categóricos",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#0ea5e9'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            intro_frame,
            text="Las tablas de frecuencias permiten resumir variables cualitativas y discretas mostrando conteos y proporciones por categoría.",
            font=('Arial', 11),
            bg='white',
            fg='#374151',
            wraplength=800,
            justify='left'
        ).pack(pady=(0, 15), padx=15, anchor='w')
        
        # Sección 2: Dataset Categórico
        dataset_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        dataset_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            dataset_frame,
            text="2. Dataset de Ejemplo (Estado de Control)",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#0284c7'
        ).pack(pady=15, padx=15, anchor='w')
        
        categorias = [
            "Óptimo", "Adecuado", "Inadecuado", "Adecuado", "Óptimo",
            "Inadecuado", "Adecuado", "Óptimo", "Inadecuado", "Adecuado",
            "Óptimo", "Óptimo", "Inadecuado", "Adecuado", "Adecuado"
        ]
        
        # Construir tabla de frecuencias
        from collections import Counter
        conteos = Counter(categorias)
        total = len(categorias)
        
        tabla_frame = tk.Frame(dataset_frame, bg='#f3f4f6', relief='sunken', bd=1)
        tabla_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        headers = ["Categoría", "Frecuencia", "Porcentaje"]
        for i, header in enumerate(headers):
            tk.Label(
                tabla_frame,
                text=header,
                font=('Arial', 10, 'bold'),
                bg='#d1d5db',
                fg='#374151',
                width=18
            ).grid(row=0, column=i, padx=2, pady=2, sticky='ew')
        
        for row_idx, (cat, freq) in enumerate(conteos.items(), 1):
            porcentaje = (freq / total) * 100
            tk.Label(tabla_frame, text=cat, font=('Arial', 10), bg='#ffffff', fg='#374151', width=18).grid(row=row_idx, column=0, padx=2, pady=1, sticky='ew')
            tk.Label(tabla_frame, text=str(freq), font=('Arial', 10), bg='#ffffff', fg='#374151', width=18).grid(row=row_idx, column=1, padx=2, pady=1, sticky='ew')
            tk.Label(tabla_frame, text=f"{porcentaje:.1f}%", font=('Arial', 10), bg='#ffffff', fg='#374151', width=18).grid(row=row_idx, column=2, padx=2, pady=1, sticky='ew')
        
        for i in range(3):
            tabla_frame.grid_columnconfigure(i, weight=1)
        
        # Sección 3: Actividad Interactiva
        actividad_frame = tk.Frame(parent_frame, bg='white', relief='raised', bd=2)
        actividad_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            actividad_frame,
            text="3. Actividad: Construye tu propia tabla de frecuencias",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#0ea5e9'
        ).pack(pady=15, padx=15, anchor='w')
        
        tk.Label(
            actividad_frame,
            text="Ingresa valores categóricos separados por comas (ej: Óptimo,Adecuado,Inadecuado)",
            font=('Arial', 11),
            bg='white',
            fg='#374151'
        ).pack(pady=(0, 10), padx=15, anchor='w')
        
        entrada = tk.Entry(actividad_frame, font=('Arial', 11))
        entrada.pack(padx=15, fill='x')
        
        resultado = tk.Text(actividad_frame, height=8, width=80, font=('Arial', 9), bg='#f9fafb', fg='#374151', state='disabled')
        resultado.pack(pady=10, padx=15, fill='x')
        
        def construir_tabla_desde_entrada():
            texto = entrada.get().strip()
            if not texto:
                return
            categorias_usuario = [x.strip() for x in texto.split(',') if x.strip()]
            if not categorias_usuario:
                return
            conteos_u = Counter(categorias_usuario)
            total_u = len(categorias_usuario)
            lineas = ["Categoría\tFrecuencia\tPorcentaje"]
            for cat, freq in conteos_u.items():
                lineas.append(f"{cat}\t{freq}\t{(freq/total_u)*100:.1f}%")
            resultado.config(state='normal')
            resultado.delete(1.0, 'end')
            resultado.insert('end', "\n".join(lineas))
            resultado.config(state='disabled')
            resultado.see('end')
        
        tk.Button(
            actividad_frame,
            text="Construir Tabla",
            font=('Arial', 10),
            bg='#3b82f6',
            fg='white',
            command=construir_tabla_desde_entrada
        ).pack(pady=(5, 15))
    
    def funcion_analisis(self):
        """Función del botón Análisis de Datos"""
        messagebox.showinfo("Análisis", "Función de Análisis de Datos activada")
    
    def funcion_graficos(self):
        """Función del botón Gráficos"""
        messagebox.showinfo("Gráficos", "Función de Gráficos activada")
    
    def funcion_reportes(self):
        """Función del botón Reportes"""
        messagebox.showinfo("Reportes", "Función de Reportes activada")
    
    def funcion_configuracion(self):
        """Función del botón Configuración"""
        messagebox.showinfo("Configuración", "Función de Configuración activada")

def main():
    """Función principal"""
    root = tk.Tk()
    app = AplicacionEstadistica(root)
    root.mainloop()

if __name__ == "__main__":
    main()
