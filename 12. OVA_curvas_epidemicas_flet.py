
import flet as ft
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import math
import random
import io
import base64
from PIL import Image

class OVAEpidemicCurves:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "OVA 12: Curvas Epidémicas y Series de Tiempo"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.window_resizable = True
        
        # Variables de estado
        self.current_tab = 0
        self.progress = 0
        self.evaluation_score = 0
        self.simulation_data = {}
        self.case_data = {}
        
        # Generar datos simulados
        self.generate_sample_data()
        
        # Crear la interfaz
        self.create_ui()
    
    def generate_sample_data(self):
        """Generar datos simulados para los casos de estudio"""
        # COVID-19 Colombia
        covid_data = []
        cases = 1
        for i in range(300):
            if i < 50:
                cases = max(1, cases * (1 + random.random() * 0.15))
            elif i < 120:
                cases = cases * (1 + (random.random() - 0.5) * 0.1)
            elif i < 180:
                cases = cases * (1 + random.random() * 0.08)
            else:
                cases = cases * (0.95 + random.random() * 0.1)
            covid_data.append(max(0, int(cases + random.random() * cases * 0.2)))
        
        # Dengue Bogotá
        dengue_data = []
        for i in range(52):
            seasonal = math.sin((i / 52) * 2 * math.pi) * 50 + 60
            noise = (random.random() - 0.5) * 20
            dengue_data.append(max(0, int(seasonal + noise)))
        
        # Influenza Estacional
        influenza_data = []
        for i in range(104):
            seasonal = math.cos((i / 52) * 2 * math.pi) * 30 + 40
            noise = (random.random() - 0.5) * 15
            influenza_data.append(max(0, int(seasonal + noise)))
        
        self.case_data = {
            'covid': covid_data[:100],
            'dengue': dengue_data,
            'influenza': influenza_data[:52]
        }
    
    def create_chart_image(self, data, title="Gráfico", xlabel="Tiempo", ylabel="Casos"):
        """Crear imagen de gráfico usando matplotlib"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(range(len(data)), data, linewidth=2, color='#3B82F6')
        ax.fill_between(range(len(data)), data, alpha=0.3, color='#3B82F6')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        
        # Convertir a imagen base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{image_base64}"
    
    def create_ui(self):
        """Crear la interfaz de usuario principal"""
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("OVA 12: Curvas Epidémicas y Series de Tiempo", 
                           size=24, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800),
                    ft.Text("Modelo Pedagógico C(H)ANGE con Inteligencia Artificial", 
                           size=16, color=ft.colors.GREY_600)
                ], expand=True),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Duración: 3 horas", size=12, color=ft.colors.BLUE_800),
                        ft.Text("Modalidad: Interactiva", size=12, color=ft.colors.BLUE_800)
                    ]),
                    bgcolor=ft.colors.BLUE_100,
                    padding=10,
                    border_radius=8
                )
            ]),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border=ft.border.only(bottom=ft.border.BorderSide(4, ft.colors.BLUE_500))
        )
        
        # Barra de progreso
        self.progress_bar = ft.ProgressBar(value=0, color=ft.colors.BLUE_500, height=4)
        self.progress_text = ft.Text("0%", size=12, color=ft.colors.GREY_600)
        
        progress_container = ft.Container(
            content=ft.Row([
                ft.Text("Progreso:", size=12, color=ft.colors.GREY_600),
                ft.Container(self.progress_bar, expand=True, margin=ft.margin.symmetric(horizontal=10)),
                self.progress_text
            ]),
            bgcolor=ft.colors.WHITE,
            padding=10
        )
        
        # Pestañas de navegación
        self.tabs = ft.Tabs(
            selected_index=0,
            on_change=self.on_tab_change,
            tabs=[
                ft.Tab(text="Introducción", icon=ft.icons.PLAY_CIRCLE),
                ft.Tab(text="Fundamentos C(H)ANGE", icon=ft.icons.BOOK),
                ft.Tab(text="Simulador IA", icon=ft.icons.SHOW_CHART),
                ft.Tab(text="Práctica Guiada", icon=ft.icons.SCIENCE),
                ft.Tab(text="Laboratorio IA", icon=ft.icons.SMART_TOY),
                ft.Tab(text="Evaluación", icon=ft.icons.ASSIGNMENT_TURNED_IN),
                ft.Tab(text="Recursos", icon=ft.icons.DOWNLOAD)
            ]
        )
        
        # Contenido de las pestañas
        self.tab_content = ft.Container(
            content=self.create_intro_tab(),
            expand=True,
            padding=20
        )
        
        # Layout principal
        main_layout = ft.Column([
            header,
            progress_container,
            self.tabs,
            self.tab_content
        ], expand=True)
        
        self.page.add(main_layout)
        self.update_progress()
    
    def on_tab_change(self, e):
        """Manejar cambio de pestaña"""
        self.current_tab = e.control.selected_index
        
        # Actualizar contenido según la pestaña
        if self.current_tab == 0:
            self.tab_content.content = self.create_intro_tab()
        elif self.current_tab == 1:
            self.tab_content.content = self.create_theory_tab()
        elif self.current_tab == 2:
            self.tab_content.content = self.create_simulator_tab()
        elif self.current_tab == 3:
            self.tab_content.content = self.create_practice_tab()
        elif self.current_tab == 4:
            self.tab_content.content = self.create_lab_tab()
        elif self.current_tab == 5:
            self.tab_content.content = self.create_evaluation_tab()
        elif self.current_tab == 6:
            self.tab_content.content = self.create_resources_tab()
        
        self.update_progress()
        self.page.update()
    
    def update_progress(self):
        """Actualizar barra de progreso"""
        self.progress = (self.current_tab + 1) / 7
        self.progress_bar.value = self.progress
        self.progress_text.value = f"{int(self.progress * 100)}%"
    
    def create_intro_tab(self):
        """Crear pestaña de introducción"""
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.TIMELINE, size=60, color=ft.colors.BLUE_600)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text("Bienvenido al Análisis de Curvas Epidémicas", 
                           size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text("Aprende a construir, interpretar y analizar curvas epidémicas utilizando el modelo pedagógico C(H)ANGE e inteligencia artificial para la toma de decisiones en salud pública.",
                           size=16, text_align=ft.TextAlign.CENTER, color=ft.colors.GREY_600),
                    
                    ft.Row([
                        # Objetivos
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.icons.TARGET_OUTLINED, color=ft.colors.BLUE_600),
                                    ft.Text("Objetivos de Aprendizaje", size=18, weight=ft.FontWeight.BOLD)
                                ]),
                                ft.Column([
                                    self.create_objective_item("Construir e interpretar curvas epidémicas"),
                                    self.create_objective_item("Identificar patrones temporales y tendencias"),
                                    self.create_objective_item("Aplicar herramientas de IA para análisis predictivo"),
                                    self.create_objective_item("Integrar conceptos del modelo C(H)ANGE")
                                ])
                            ]),
                            bgcolor=ft.colors.BLUE_50,
                            padding=20,
                            border_radius=10,
                            expand=True
                        ),
                        
                        # Competencias
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.icons.SETTINGS, color=ft.colors.GREEN_600),
                                    ft.Text("Competencias a Desarrollar", size=18, weight=ft.FontWeight.BOLD)
                                ]),
                                ft.Column([
                                    self.create_competency_item("Pensamiento estadístico aplicado", ft.colors.PURPLE_500),
                                    self.create_competency_item("Visualización efectiva de datos", ft.colors.BLUE_500),
                                    self.create_competency_item("Interpretación clínica de patrones", ft.colors.YELLOW_600),
                                    self.create_competency_item("Comunicación de hallazgos", ft.colors.RED_500)
                                ])
                            ]),
                            bgcolor=ft.colors.GREEN_50,
                            padding=20,
                            border_radius=10,
                            expand=True
                        )
                    ], spacing=20),
                    
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.INFO, color=ft.colors.YELLOW_600),
                            ft.Column([
                                ft.Text("Contexto Epidemiológico", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW_800),
                                ft.Text("Las curvas epidémicas son herramientas fundamentales para entender la dinámica de transmisión de enfermedades, identificar brotes, evaluar intervenciones y predecir tendencias futuras.",
                                       color=ft.colors.YELLOW_700)
                            ], expand=True)
                        ]),
                        bgcolor=ft.colors.YELLOW_50,
                        padding=15,
                        border_radius=8,
                        border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400))
                    ),
                    
                    ft.ElevatedButton(
                        "Comenzar Módulo",
                        icon=ft.icons.ARROW_FORWARD,
                        on_click=lambda _: self.next_tab(),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.BLUE_600,
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=15)
                        )
                    )
                ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.colors.WHITE,
                padding=30,
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.GREY_300)
            )
        ], scroll=ft.ScrollMode.AUTO)
    
    def create_objective_item(self, text):
        """Crear item de objetivo"""
        return ft.Row([
            ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN_500, size=16),
            ft.Text(text, size=14, expand=True)
        ])
    
    def create_competency_item(self, text, color):
        """Crear item de competencia"""
        return ft.Row([
            ft.Icon(ft.icons.PSYCHOLOGY, color=color, size=16),
            ft.Text(text, size=14, expand=True)
        ])
    
    def create_theory_tab(self):
        """Crear pestaña de fundamentos teóricos"""
        return ft.Column([
            ft.Text("Fundamentos del Modelo C(H)ANGE", size=24, weight=ft.FontWeight.BOLD),
            
            # Componentes C(H)ANGE
            ft.Row([
                self.create_change_component("C", "Combinatoria", "Análisis de combinaciones de factores", 
                                           ["Rutas de transmisión", "Grupos poblacionales", "Factores de riesgo"], 
                                           ft.colors.RED_500),
                self.create_change_component("H", "Álgebra", "Modelos matemáticos epidémicos", 
                                           ["Ecuaciones diferenciales", "Modelos SIR/SEIR", "Funciones exponenciales"], 
                                           ft.colors.BLUE_500),
                self.create_change_component("A", "Números", "Cálculos estadísticos clave", 
                                           ["Tasas de incidencia", "Número reproductivo", "Intervalos seriales"], 
                                           ft.colors.GREEN_500),
                self.create_change_component("N", "Geometría", "Visualización de patrones", 
                                           ["Curvas de crecimiento", "Distribución espacial", "Patrones geométricos"], 
                                           ft.colors.PURPLE_500),
                self.create_change_component("G", "Estadística", "Análisis de series temporales", 
                                           ["Tendencias temporales", "Estacionalidad", "Predicción estadística"], 
                                           ft.colors.ORANGE_500)
            ], wrap=True, spacing=10),
            
            # Conceptos fundamentales
            ft.Container(
                content=ft.Column([
                    ft.Text("Conceptos Fundamentales", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Column([
                            self.create_concept_card("Curva Epidémica", "Representación gráfica del número de casos en función del tiempo", ft.icons.SHOW_CHART, ft.colors.BLUE_600),
                            self.create_concept_card("Período de Incubación", "Tiempo entre exposición y aparición de síntomas", ft.icons.SCHEDULE, ft.colors.GREEN_600),
                            self.create_concept_card("Caso Índice", "Primer caso identificado en un brote", ft.icons.PERSON, ft.colors.PURPLE_600)
                        ], expand=True),
                        ft.Column([
                            self.create_concept_card("Número Reproductivo (R₀)", "Casos secundarios generados por un caso primario", ft.icons.TRENDING_UP, ft.colors.RED_600),
                            self.create_concept_card("Estacionalidad", "Patrón recurrente relacionado con factores temporales", ft.icons.CALENDAR_TODAY, ft.colors.ORANGE_600),
                            self.create_concept_card("Vigilancia Epidemiológica", "Sistema de recolección y análisis de datos", ft.icons.VISIBILITY, ft.colors.INDIGO_600)
                        ], expand=True)
                    ], spacing=20)
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=20,
                border_radius=10
            ),
            
            ft.ElevatedButton(
                "Ir al Simulador",
                icon=ft.icons.ARROW_FORWARD,
                on_click=lambda _: self.next_tab(),
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
    
    def create_change_component(self, letter, name, description, items, color):
        """Crear componente del modelo C(H)ANGE"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Text(letter, size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        bgcolor=color,
                        width=50,
                        height=50,
                        border_radius=25,
                        alignment=ft.alignment.center
                    ),
                    ft.Text(name, size=16, weight=ft.FontWeight.BOLD, expand=True)
                ]),
                ft.Text(description, size=12, color=ft.colors.GREY_700),
                ft.Column([ft.Text(f"• {item}", size=10, color=ft.colors.GREY_600) for item in items])
            ], spacing=5),
            bgcolor=ft.colors.WHITE,
            padding=15,
            border_radius=8,
            border=ft.border.all(1, color),
            width=220
        )
    
    def create_concept_card(self, title, description, icon, color):
        """Crear tarjeta de concepto"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, color=color, size=20),
                    ft.Text(title, size=14, weight=ft.FontWeight.BOLD, expand=True)
                ]),
                ft.Text(description, size=12, color=ft.colors.GREY_600)
            ]),
            bgcolor=ft.colors.WHITE,
            padding=15,
            border_radius=8,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_200)
        )
    
    def create_simulator_tab(self):
        """Crear pestaña del simulador"""
        # Controles del simulador
        self.outbreak_type = ft.Dropdown(
            label="Tipo de Brote",
            value="point",
            options=[
                ft.dropdown.Option("point", "Fuente puntual"),
                ft.dropdown.Option("continuous", "Fuente continua"),
                ft.dropdown.Option("propagated", "Propagación persona-persona"),
                ft.dropdown.Option("mixed", "Mixto")
            ],
            on_change=self.update_simulation
        )
        
        self.population_slider = ft.Slider(
            min=1000, max=100000, value=10000, divisions=99,
            label="Población: {value}",
            on_change=self.update_simulation
        )
        
        self.transmission_slider = ft.Slider(
            min=0.1, max=1.0, value=0.3, divisions=9,
            label="Transmisión: {value}",
            on_change=self.update_simulation
        )
        
        # Imagen del gráfico
        self.chart_image = ft.Image(
            src=self.create_chart_image([1, 2, 5, 8, 12, 15, 18, 20, 18, 15, 12, 8, 5, 2, 1], 
                                      "Curva Epidémica Simulada", "Días", "Casos"),
            width=600,
            height=400,
            fit=ft.ImageFit.CONTAIN
        )
        
        # Métricas
        self.peak_day = ft.Text("7", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600)
        self.peak_cases = ft.Text("20", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600)
        self.total_cases = ft.Text("141", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_600)
        self.r0_value = ft.Text("2.3", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_600)
        
        return ft.Column([
            ft.Text("Simulador Inteligente de Curvas Epidémicas", size=24, weight=ft.FontWeight.BOLD),
            
            ft.Row([
                # Panel de control
                ft.Container(
                    content=ft.Column([
                        ft.Text("Parámetros del Brote", size=18, weight=ft.FontWeight.BOLD),
                        self.outbreak_type,
                        ft.Text("Población Susceptible"),
                        self.population_slider,
                        ft.Text("Tasa de Transmisión"),
                        self.transmission_slider,
                        ft.ElevatedButton(
                            "Predicción IA",
                            icon=ft.icons.AUTO_AWESOME,
                            on_click=self.generate_ai_prediction,
                            style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE)
                        ),
                        ft.ElevatedButton(
                            "Reiniciar",
                            icon=ft.icons.REFRESH,
                            on_click=self.reset_simulation,
                            style=ft.ButtonStyle(bgcolor=ft.colors.GREY_600, color=ft.colors.WHITE)
                        )
                    ], spacing=15),
                    bgcolor=ft.colors.GREY_50,
                    padding=20,
                    border_radius=10,
                    width=300
                ),
                
                # Gráfico y métricas
                ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("Curva Epidémica Simulada", size=16, weight=ft.FontWeight.BOLD),
                                ft.IconButton(ft.icons.DOWNLOAD, tooltip="Exportar")
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            self.chart_image
                        ]),
                        bgcolor=ft.colors.WHITE,
                        padding=15,
                        border_radius=8,
                        border=ft.border.all(1, ft.colors.GREY_300)
                    ),
                    
                    # Métricas
                    ft.Row([
                        self.create_metric_card("Día Pico", self.peak_day, ft.colors.BLUE_50),
                        self.create_metric_card("Casos Pico", self.peak_cases, ft.colors.RED_50),
                        self.create_metric_card("Total Casos", self.total_cases, ft.colors.GREEN_50),
                        self.create_metric_card("R₀ Estimado", self.r0_value, ft.colors.PURPLE_50)
                    ], spacing=10)
                ], expand=True)
            ], spacing=20),
            
            ft.ElevatedButton(
                "Práctica Guiada",
                icon=ft.icons.ARROW_FORWARD,
                on_click=lambda _: self.next_tab(),
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
    
    def create_metric_card(self, title, value_widget, bgcolor):
        """Crear tarjeta de métrica"""
        return ft.Container(
            content=ft.Column([
                value_widget,
                ft.Text(title, size=12, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=bgcolor,
            padding=15,
            border_radius=8,
            width=120
        )
    
    def update_simulation(self, e=None):
        """Actualizar simulación"""
        # Generar nuevos datos basados en parámetros
        outbreak_type = self.outbreak_type.value
        population = int(self.population_slider.value)
        transmission = self.transmission_slider.value
        
        # Simular datos epidémicos
        data = self.generate_outbreak_data(outbreak_type, population, transmission)
        
        # Actualizar gráfico
        self.chart_image.src = self.create_chart_image(data, "Curva Epidémica Simulada", "Días", "Casos")
        
        # Calcular métricas
        peak_day = data.index(max(data))
        peak_cases = max(data)
        total_cases = sum(data)
        r0 = round(2.0 + random.random() * 2.0, 1)  # Simulado
        
        self.peak_day.value = str(peak_day)
        self.peak_cases.value = str(peak_cases)
        self.total_cases.value = str(total_cases)
        self.r0_value.value = str(r0)
        
        self.page.update()
    
    def generate_outbreak_data(self, outbreak_type, population, transmission):
        """Generar datos de brote según parámetros"""
        data = []
        initial_cases = 5
        
        for day in range(60):
            if outbreak_type == "point":
                # Fuente puntual
                cases = initial_cases * math.exp(-((day - 5) ** 2) / 20) if day < 20 else 0
            elif outbreak_type == "continuous":
                # Fuente continua
                cases = initial_cases * (1 + math.sin(day / 10) * 0.2)
            elif outbreak_type == "propagated":
                # Propagación persona-persona (SIR simplificado)
                if day == 0:
                    cases = initial_cases
                else:
                    prev_cases = data[-1] if data else initial_cases
                    cases = prev_cases * (1 + transmission * 0.1) * (1 - day / 100)
            else:  # mixed
                # Patrón mixto
                cases = initial_cases * (math.exp(-day / 30) + 0.5 * math.exp(-(day - 30) / 15))
            
            data.append(max(0, int(cases)))
        
        return data
    
    def generate_ai_prediction(self, e):
        """Generar predicción con IA"""
        # Mostrar diálogo de análisis IA
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Análisis Inteligente"),
            content=ft.Column([
                ft.Row([ft.ProgressRing(width=16, height=16), ft.Text("Analizando patrones...")]),
                ft.Text("🔍 Patrón Identificado: Transmisión comunitaria sostenida"),
                ft.Text("📈 Tendencia: Crecimiento exponencial seguido de estabilización"),
                ft.Text("⚠️ Alerta: R₀ sugiere necesidad de medidas de control"),
                ft.Text("🎯 Recomendación: Vigilancia intensificada próximos 14 días"),
                ft.Text("📊 Confianza: 87% basado en patrones históricos")
            ], height=200, scroll=ft.ScrollMode.AUTO),
            actions=[ft.TextButton("Cerrar", on_click=close_dialog)]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def reset_simulation(self, e):
        """Reiniciar simulación"""
        self.outbreak_type.value = "point"
        self.population_slider.value = 10000
        self.transmission_slider.value = 0.3
        self.update_simulation()
    
    def create_practice_tab(self):
        """Crear pestaña de práctica guiada"""
        # Botones de casos
        case_buttons = ft.Row([
            ft.ElevatedButton("Caso 1: COVID-19 Colombia", 
                            on_click=lambda _: self.load_case(1),
                            style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)),
            ft.ElevatedButton("Caso 2: Dengue Bogotá", 
                            on_click=lambda _: self.load_case(2),
                            style=ft.ButtonStyle(bgcolor=ft.colors.GREY_600, color=ft.colors.WHITE)),
            ft.ElevatedButton("Caso 3: Influenza Estacional", 
                            on_click=lambda _: self.load_case(3),
                            style=ft.ButtonStyle(bgcolor=ft.colors.GREY_600, color=ft.colors.WHITE))
        ])
        
        # Gráfico del caso
        self.case_chart = ft.Image(
            src=self.create_chart_image(self.case_data['covid'], "COVID-19 Colombia - Primera Ola", "Días", "Casos"),
            width=500,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )
        
        # Ejercicios interactivos
        self.pattern_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="point", label="Fuente puntual (brote común)"),
                ft.Radio(value="continuous", label="Fuente continua"),
                ft.Radio(value="propagated", label="Propagación persona a persona"),
                ft.Radio(value="mixed", label="Patrón mixto")
            ])
        )
        
        self.r0_input = ft.TextField(label="R₀ estimado", width=100, keyboard_type=ft.KeyboardType.NUMBER)
        
        self.interpretation_text = ft.TextField(
            label="Interpretación y recomendaciones",
            multiline=True,
            min_lines=3,
            max_lines=5
        )
        
        return ft.Column([
            ft.Text("Práctica Guiada: Casos Reales", size=24, weight=ft.FontWeight.BOLD),
            
            case_buttons,
            
            # Caso de estudio
            ft.Container(
                content=ft.Column([
                    ft.Text("Caso 1: Análisis COVID-19 en Colombia (2020-2021)", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Column([
                            ft.Text("Contexto Epidemiológico", size=14, weight=ft.FontWeight.BOLD),
                            ft.Text("Análisis de la primera ola de COVID-19 en Colombia, desde marzo 2020 hasta febrero 2021.", size=12),
                            ft.Text("• Primer caso: 6 de marzo de 2020", size=12),
                            ft.Text("• Pico principal: Agosto 2020", size=12),
                            ft.Text("• Población afectada: 50+ millones", size=12),
                            ft.Text("• Medidas: Cuarentenas, distanciamiento", size=12)
                        ], expand=True),
                        ft.Container(
                            content=self.case_chart,
                            bgcolor=ft.colors.WHITE,
                            padding=10,
                            border_radius=8,
                            border=ft.border.all(1, ft.colors.GREY_300)
                        )
                    ])
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=20,
                border_radius=10
            ),
            
            # Ejercicios
            ft.Container(
                content=ft.Column([
                    ft.Text("Ejercicios Interactivos", size=18, weight=ft.FontWeight.BOLD),
                    
                    # Ejercicio 1
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Ejercicio 1: Identificación de Patrones", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                            ft.Text("¿Qué tipo de patrón de transmisión observas?", color=ft.colors.BLUE_700),
                            self.pattern_radio,
                            ft.ElevatedButton("Verificar Respuesta", on_click=self.check_pattern_answer)
                        ]),
                        bgcolor=ft.colors.BLUE_50,
                        padding=15,
                        border_radius=8
                    ),
                    
                    # Ejercicio 2
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Ejercicio 2: Cálculo de Métricas", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                            ft.Text("Calcula el R₀ aproximado para el período inicial:", color=ft.colors.GREEN_700),
                            ft.Row([
                                self.r0_input,
                                ft.ElevatedButton("Verificar", on_click=self.check_r0_answer)
                            ]),
                        ]),
                        bgcolor=ft.colors.GREEN_50,
                        padding=15,
                        border_radius=8
                    ),
                    
                    # Ejercicio 3
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Ejercicio 3: Interpretación Clínica", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                            ft.Text("¿Qué medidas de salud pública recomendarías?", color=ft.colors.PURPLE_700),
                            self.interpretation_text,
                            ft.ElevatedButton("Evaluar Respuesta", on_click=self.check_interpretation_answer)
                        ]),
                        bgcolor=ft.colors.PURPLE_50,
                        padding=15,
                        border_radius=8
                    )
                ], spacing=15),
                bgcolor=ft.colors.WHITE,
                padding=20,
                border_radius=10,
                border=ft.border.all(1, ft.colors.GREY_300)
            ),
            
            ft.ElevatedButton(
                "Laboratorio IA",
                icon=ft.icons.ARROW_FORWARD,
                on_click=lambda _: self.next_tab(),
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
    
    def load_case(self, case_number):
        """Cargar caso de estudio"""
        if case_number == 1:
            data = self.case_data['covid']
            title = "COVID-19 Colombia - Primera Ola"
        elif case_number == 2:
            data = self.case_data['dengue']
            title = "Dengue Bogotá - Patrón Estacional"
        else:
            data = self.case_data['influenza']
            title = "Influenza Estacional - 2 Años"
        
        self.case_chart.src = self.create_chart_image(data, title, "Tiempo", "Casos")
        self.page.update()
    
    def check_pattern_answer(self, e):
        """Verificar respuesta de patrón"""
        if self.pattern_radio.value == "propagated":
            self.show_feedback("¡Correcto! El patrón muestra múltiples ondas características de transmisión persona a persona.", True)
        else:
            self.show_feedback("Incorrecto. Observa las múltiples ondas que sugieren generaciones sucesivas de transmisión.", False)
    
    def check_r0_answer(self, e):
        """Verificar respuesta de R₀"""
        try:
            r0_val = float(self.r0_input.value)
            if 2.0 <= r0_val <= 3.5:
                self.show_feedback("¡Excelente! Tu estimación está en el rango esperado para este tipo de brote.", True)
            else:
                self.show_feedback("Revisa tu cálculo. Para COVID-19, R₀ típicamente está entre 2.0 y 3.5.", False)
        except:
            self.show_feedback("Por favor ingresa un valor numérico válido.", False)
    
    def check_interpretation_answer(self, e):
        """Verificar respuesta de interpretación"""
        if len(self.interpretation_text.value) > 50:
            self.show_feedback("Respuesta registrada. Considera: medidas de distanciamiento, testing, rastreo de contactos y comunicación de riesgo.", True)
        else:
            self.show_feedback("Desarrolla más tu respuesta. Incluye medidas específicas de salud pública.", False)
    
    def show_feedback(self, message, is_correct):
        """Mostrar retroalimentación"""
        color = ft.colors.GREEN_600 if is_correct else ft.colors.RED_600
        icon = ft.icons.CHECK_CIRCLE if is_correct else ft.icons.ERROR
        
        def close_snack(e):
            self.page.snack_bar.open = False
            self.page.update()
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(icon, color=color),
                ft.Text(message, expand=True)
            ]),
            action="Cerrar",
            action_color=color,
            on_action=close_snack
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def create_lab_tab(self):
        """Crear pestaña de laboratorio IA"""
        return ft.Column([
            ft.Text("Laboratorio de Inteligencia Artificial", size=24, weight=ft.FontWeight.BOLD),
            
            ft.Row([
                # Panel de carga de datos
                ft.Container(
                    content=ft.Column([
                        ft.Text("Carga de Datos", size=18, weight=ft.FontWeight.BOLD),
                        ft.Dropdown(
                            label="Seleccionar Dataset",
                            options=[
                                ft.dropdown.Option("covid_colombia", "COVID-19 Colombia"),
                                ft.dropdown.Option("dengue_bogota", "Dengue Bogotá"),
                                ft.dropdown.Option("influenza", "Influenza Estacional"),
                                ft.dropdown.Option("custom", "Datos Personalizados")
                            ]
                        ),
                        ft.ElevatedButton("Procesar Datos", icon=ft.icons.SETTINGS),
                        
                        ft.Divider(),
                        ft.Text("Configuración de IA", size=16, weight=ft.FontWeight.BOLD),
                        ft.Dropdown(
                            label="Algoritmo",
                            value="arima",
                            options=[
                                ft.dropdown.Option("arima", "ARIMA"),
                                ft.dropdown.Option("exponential", "Suavizado Exponencial"),
                                ft.dropdown.Option("polynomial", "Regresión Polinomial"),
                                ft.dropdown.Option("sir", "Modelo SIR")
                            ]
                        ),
                        ft.Slider(min=7, max=90, value=30, label="Días a predecir: {value}"),
                        ft.Slider(min=80, max=99, value=95, label="Confianza: {value}%")
                    ], spacing=10),
                    bgcolor=ft.colors.GREY_50,
                    padding=20,
                    border_radius=10,
                    width=300
                ),
                
                # Visualización
                ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("Análisis Predictivo", size=16, weight=ft.FontWeight.BOLD),
                                ft.Row([
                                    ft.ElevatedButton("Ejecutar", icon=ft.icons.PLAY_ARROW, 
                                                    on_click=self.run_prediction,
                                                    style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE)),
                                    ft.ElevatedButton("Exportar", icon=ft.icons.DOWNLOAD)
                                ])
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Image(
                                src=self.create_prediction_chart(),
                                width=500,
                                height=300,
                                fit=ft.ImageFit.CONTAIN
                            )
                        ]),
                        bgcolor=ft.colors.WHITE,
                        padding=15,
                        border_radius=8,
                        border=ft.border.all(1, ft.colors.GREY_300)
                    ),
                    
                    # Métricas de rendimiento
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("12.3", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600),
                                ft.Text("Error Absoluto Medio", size=10, text_align=ft.TextAlign.CENTER)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.BLUE_50,
                            padding=10,
                            border_radius=8,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("0.87", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_600),
                                ft.Text("R² (Bondad de Ajuste)", size=10, text_align=ft.TextAlign.CENTER)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.GREEN_50,
                            padding=10,
                            border_radius=8,
                            expand=True
                        )
                    ], spacing=10)
                ], expand=True)
            ], spacing=20),
            
            # Herramientas avanzadas
            ft.Container(
                content=ft.Column([
                    ft.Text("Herramientas Avanzadas", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.ElevatedButton("Detectar Brotes", icon=ft.icons.WARNING, 
                                        style=ft.ButtonStyle(bgcolor=ft.colors.RED_600, color=ft.colors.WHITE)),
                        ft.ElevatedButton("Análisis Estacional", icon=ft.icons.CALENDAR_TODAY,
                                        style=ft.ButtonStyle(bgcolor=ft.colors.ORANGE_600, color=ft.colors.WHITE)),
                        ft.ElevatedButton("Comparar Escenarios", icon=ft.icons.COMPARE,
                                        style=ft.ButtonStyle(bgcolor=ft.colors.PURPLE_600, color=ft.colors.WHITE))
                    ], spacing=10)
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=20,
                border_radius=10
            ),
            
            ft.ElevatedButton(
                "Evaluación Final",
                icon=ft.icons.ARROW_FORWARD,
                on_click=lambda _: self.next_tab(),
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
    
    def create_prediction_chart(self):
        """Crear gráfico de predicción"""
        # Datos históricos y predicción
        historical = [30 + 20 * math.sin(i/10) + random.random() * 10 for i in range(50)]
        prediction = [30 + 20 * math.sin((50+i)/10) + random.random() * 15 for i in range(30)]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Datos históricos
        ax.plot(range(50), historical, 'b-', linewidth=2, label='Datos Históricos')
        ax.fill_between(range(50), historical, alpha=0.3, color='blue')
        
        # Predicción
        pred_x = range(50, 80)
        ax.plot(pred_x, prediction, 'g--', linewidth=2, label='Predicción IA')
        ax.fill_between(pred_x, prediction, alpha=0.3, color='green')
        
        ax.set_title('Análisis Predictivo con IA', fontsize=14, fontweight='bold')
        ax.set_xlabel('Días')
        ax.set_ylabel('Casos')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Convertir a imagen
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{image_base64}"
    
    def run_prediction(self, e):
        """Ejecutar predicción IA"""
        # Mostrar interpretación automática
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Interpretación Automática"),
            content=ft.Column([
                ft.Text("Análisis Predictivo Completado:", weight=ft.FontWeight.BOLD),
                ft.Text("• El modelo ARIMA muestra buen ajuste con R² = 0.87"),
                ft.Text("• Se predice tendencia estable con variabilidad estacional"),
                ft.Text("• Intervalo de confianza del 95% indica incertidumbre moderada"),
                ft.Text("• Recomendación: Monitoreo continuo para validar predicciones")
            ], height=150),
            actions=[ft.TextButton("Cerrar", on_click=close_dialog)]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def create_evaluation_tab(self):
        """Crear pestaña de evaluación"""
        # Preguntas de evaluación
        self.q1_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="a", label="A) Brote de fuente puntual con período de incubación corto"),
                ft.Radio(value="b", label="B) Transmisión persona a persona con múltiples generaciones"),
                ft.Radio(value="c", label="C) Fuente continua con exposición prolongada"),
                ft.Radio(value="d", label="D) Patrón estacional con picos recurrentes")
            ])
        )
        
        self.q2_initial = ft.TextField(label="Casos iniciales", value="5", width=150)
        self.q2_second_gen = ft.TextField(label="Casos segunda generación", width=150)
        self.q2_justification = ft.TextField(label="Justificación", multiline=True, min_lines=2)
        
        # Dropdowns para C(H)ANGE
        change_options = [
            ft.dropdown.Option("", "Seleccionar..."),
            ft.dropdown.Option("routes", "Rutas de transmisión"),
            ft.dropdown.Option("equations", "Ecuaciones diferenciales"),
            ft.dropdown.Option("rates", "Tasas de incidencia"),
            ft.dropdown.Option("curves", "Formas de curvas"),
            ft.dropdown.Option("trends", "Análisis de tendencias")
        ]
        
        self.change_c = ft.Dropdown(label="Combinatoria", options=change_options, width=200)
        self.change_a = ft.Dropdown(label="Álgebra", options=change_options, width=200)
        self.change_n = ft.Dropdown(label="Números", options=change_options, width=200)
        self.change_g = ft.Dropdown(label="Geometría", options=change_options, width=200)
        self.change_e = ft.Dropdown(label="Estadística", options=change_options, width=200)
        
        self.q4_data = ft.TextField(label="1. Recolección de datos", multiline=True, min_lines=2)
        self.q4_curve = ft.TextField(label="2. Construcción de curva", multiline=True, min_lines=2)
        self.q4_interpretation = ft.TextField(label="3. Interpretación y control", multiline=True, min_lines=2)
        
        return ft.Column([
            ft.Text("Evaluación y Autoevaluación", size=24, weight=ft.FontWeight.BOLD),
            
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.INFO, color=ft.colors.BLUE_600),
                    ft.Column([
                        ft.Text("Instrucciones", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                        ft.Text("Completa las siguientes preguntas para evaluar tu comprensión.", color=ft.colors.BLUE_700)
                    ], expand=True)
                ]),
                bgcolor=ft.colors.BLUE_50,
                padding=15,
                border_radius=8,
                border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.BLUE_500))
            ),
            
            # Pregunta 1
            ft.Container(
                content=ft.Column([
                    ft.Text("Pregunta 1: Interpretación de Curvas (25 puntos)", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Observa la curva epidémica. ¿Cuál es la interpretación más probable?"),
                    ft.Image(
                        src=self.create_chart_image([1,1,2,3,5,8,13,21,34,55,45,35,28,22,18,15,12,10,8,6,5,4,3,2,2,1,1,1,0,0],
                                                  "Curva Epidémica para Análisis", "Días", "Casos"),
                        width=400,
                        height=200,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    self.q1_radio
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=15,
                border_radius=8
            ),
            
            # Pregunta 2
            ft.Container(
                content=ft.Column([
                    ft.Text("Pregunta 2: Cálculos Epidemiológicos (25 puntos)", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Con R₀=2.5 y período infeccioso de 10 días, ¿cuántos casos en segunda generación?"),
                    ft.Row([self.q2_initial, self.q2_second_gen]),
                    self.q2_justification
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=15,
                border_radius=8
            ),
            
            # Pregunta 3
            ft.Container(
                content=ft.Column([
                    ft.Text("Pregunta 3: Aplicación C(H)ANGE (25 puntos)", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Relaciona cada componente con un aspecto del análisis epidémico:"),
                    ft.Column([
                        ft.Row([ft.Text("Combinatoria:", width=100), self.change_c]),
                        ft.Row([ft.Text("Álgebra:", width=100), self.change_a]),
                        ft.Row([ft.Text("Números:", width=100), self.change_n]),
                        ft.Row([ft.Text("Geometría:", width=100), self.change_g]),
                        ft.Row([ft.Text("Estadística:", width=100), self.change_e])
                    ])
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=15,
                border_radius=8
            ),
            
            # Pregunta 4
            ft.Container(
                content=ft.Column([
                    ft.Text("Pregunta 4: Caso Práctico (25 puntos)", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Analiza un brote de gastroenteritis en comunidad rural:"),
                    self.q4_data,
                    self.q4_curve,
                    self.q4_interpretation
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=15,
                border_radius=8
            ),
            
            # Botones de evaluación
            ft.Row([
                ft.ElevatedButton(
                    "Enviar Evaluación",
                    icon=ft.icons.CHECK,
                    on_click=self.submit_evaluation,
                    style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE)
                ),
                ft.ElevatedButton(
                    "Reiniciar",
                    icon=ft.icons.REFRESH,
                    on_click=self.reset_evaluation,
                    style=ft.ButtonStyle(bgcolor=ft.colors.GREY_600, color=ft.colors.WHITE)
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            
            ft.ElevatedButton(
                "Recursos y Material",
                icon=ft.icons.ARROW_FORWARD,
                on_click=lambda _: self.next_tab(),
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
    
    def submit_evaluation(self, e):
        """Enviar evaluación"""
        score = 0
        
        # Pregunta 1
        if self.q1_radio.value == "b":
            score += 25
        
        # Pregunta 2
        try:
            second_gen = float(self.q2_second_gen.value)
            if 10 <= second_gen <= 15:
                score += 25
        except:
            pass
        
        # Pregunta 3 - C(H)ANGE
        correct_answers = {
            'change_c': 'routes',
            'change_a': 'equations',
            'change_n': 'rates', 
            'change_g': 'curves',
            'change_e': 'trends'
        }
        
        change_score = 0
        for widget_name, correct_value in correct_answers.items():
            widget = getattr(self, widget_name)
            if widget.value == correct_value:
                change_score += 5
        score += change_score
        
        # Pregunta 4
        text_fields = [self.q4_data, self.q4_curve, self.q4_interpretation]
        text_score = 0
        for field in text_fields:
            if len(field.value) > 50:
                text_score += 8.33
        score += int(text_score)
        
        self.evaluation_score = score
        self.show_evaluation_results()
    
    def show_evaluation_results(self):
        """Mostrar resultados de evaluación"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        def generate_certificate(e):
            if self.evaluation_score >= 70:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"¡Felicitaciones! Certificado generado con {self.evaluation_score}/100 puntos.")
                )
            else:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Se requiere mínimo 70 puntos. Tu puntuación: {self.evaluation_score}/100")
                )
            self.page.snack_bar.open = True
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Resultados de la Evaluación"),
            content=ft.Column([
                ft.Row([
                    ft.Text(str(int(self.evaluation_score)), size=36, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_600),
                    ft.Text("de 100 puntos", size=16)
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                ft.Text("Retroalimentación detallada:", weight=ft.FontWeight.BOLD),
                ft.Text(f"• Pregunta 1: {'✅ Correcta' if self.q1_radio.value == 'b' else '❌ Incorrecta'}"),
                ft.Text(f"• Pregunta 2: Cálculo R₀ evaluado"),
                ft.Text(f"• Pregunta 3: Modelo C(H)ANGE aplicado"),
                ft.Text(f"• Pregunta 4: Caso práctico desarrollado")
            ], height=300, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Generar Certificado", on_click=generate_certificate),
                ft.TextButton("Cerrar", on_click=close_dialog)
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def reset_evaluation(self, e):
        """Reiniciar evaluación"""
        self.q1_radio.value = None
        self.q2_second_gen.value = ""
        self.q2_justification.value = ""
        
        for dropdown in [self.change_c, self.change_a, self.change_n, self.change_g, self.change_e]:
            dropdown.value = ""
        
        for field in [self.q4_data, self.q4_curve, self.q4_interpretation]:
            field.value = ""
        
        self.page.update()
    
    def create_resources_tab(self):
        """Crear pestaña de recursos"""
        return ft.Column([
            ft.Text("Recursos y Material Descargable", size=24, weight=ft.FontWeight.BOLD),
            
            ft.Row([
                # Plantillas y herramientas
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.FILE_PRESENT, color=ft.colors.BLUE_600),
                            ft.Text("Plantillas y Herramientas", size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        self.create_resource_item("Plantilla de Curva Epidémica", "Excel con fórmulas automatizadas"),
                        self.create_resource_item("Calculadora R₀", "Herramienta interactiva"),
                        self.create_resource_item("Checklist de Análisis", "Lista de verificación PDF"),
                        self.create_resource_item("Código R para Análisis", "Scripts comentados")
                    ], spacing=10),
                    bgcolor=ft.colors.GREY_50,
                    padding=20,
                    border_radius=10,
                    expand=True
                ),
                
                # Datasets
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.DATABASE, color=ft.colors.GREEN_600),
                            ft.Text("Datasets de Práctica", size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        self.create_resource_item("COVID-19 Colombia 2020-2022", "Datos diarios anonimizados"),
                        self.create_resource_item("Dengue Bogotá 2015-2023", "Series temporales semanales"),
                        self.create_resource_item("Influenza Estacional", "Patrones históricos 10 años"),
                        self.create_resource_item("Brotes Simulados", "Diferentes patrones epidémicos")
                    ], spacing=10),
                    bgcolor=ft.colors.GREY_50,
                    padding=20,
                    border_radius=10,
                    expand=True
                )
            ], spacing=20),
            
            # Bibliografía
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.BOOK, color=ft.colors.PURPLE_600),
                        ft.Text("Bibliografía y Referencias", size=18, weight=ft.FontWeight.BOLD)
                    ]),
                    ft.Row([
                        ft.Column([
                            ft.Text("Textos Fundamentales", weight=ft.FontWeight.BOLD),
                            ft.Text("• Gordis, L. (2013). Epidemiología. 5ª edición.", size=12),
                            ft.Text("• Rothman, K.J. (2012). Epidemiology: An Introduction.", size=12),
                            ft.Text("• Anderson, R.M. & May, R.M. (1991). Infectious Diseases.", size=12)
                        ], expand=True),
                        ft.Column([
                            ft.Text("Recursos Digitales", weight=ft.FontWeight.BOLD),
                            ft.Text("• CDC - Epidemic Intelligence Service", size=12),
                            ft.Text("• WHO - Disease Outbreak News", size=12),
                            ft.Text("• R Epidemics Consortium (RECON)", size=12)
                        ], expand=True)
                    ])
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=20,
                border_radius=10
            ),
            
            # Certificación
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.SCHOOL, color=ft.colors.YELLOW_600),
                        ft.Text("Certificación de Competencias", size=18, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text("Al completar exitosamente este módulo OVA, habrás desarrollado competencias clave en análisis de curvas epidémicas y series de tiempo.",
                           text_align=ft.TextAlign.CENTER),
                    
                    ft.Row([
                        self.create_competency_card("Análisis Temporal", "Construcción e interpretación", ft.icons.SHOW_CHART, ft.colors.BLUE_600),
                        self.create_competency_card("Herramientas IA", "Aplicación en epidemiología", ft.icons.SMART_TOY, ft.colors.GREEN_600),
                        self.create_competency_card("Salud Pública", "Decisiones basadas en evidencia", ft.icons.HEALTH_AND_SAFETY, ft.colors.PURPLE_600)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    
                    ft.ElevatedButton(
                        "Completar Módulo OVA",
                        icon=ft.icons.SCHOOL,
                        on_click=self.complete_course,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.BLUE_600,
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=15)
                        )
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                bgcolor=ft.colors.BLUE_50,
                padding=30,
                border_radius=15
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
    
    def create_resource_item(self, title, description):
        """Crear item de recurso"""
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(title, weight=ft.FontWeight.BOLD),
                    ft.Text(description, size=12, color=ft.colors.GREY_600)
                ], expand=True),
                ft.IconButton(ft.icons.DOWNLOAD, tooltip="Descargar", on_click=lambda _: self.download_resource(title))
            ]),
            bgcolor=ft.colors.WHITE,
            padding=10,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
    
    def create_competency_card(self, title, description, icon, color):
        """Crear tarjeta de competencia"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=40, color=color),
                ft.Text(title, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(description, size=12, text_align=ft.TextAlign.CENTER, color=ft.colors.GREY_600)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=10,
            width=200
        )
    
    def download_resource(self, resource_name):
        """Simular descarga de recurso"""
        self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Descargando: {resource_name}"))
        self.page.snack_bar.open = True
        self.page.update()
    
    def complete_course(self, e):
        """Completar curso"""
        if self.evaluation_score >= 70:
            message = f"""¡Excelente trabajo! Has completado exitosamente el OVA 12.

Competencias desarrolladas:
✅ Análisis de curvas epidémicas
✅ Aplicación del modelo C(H)ANGE  
✅ Uso de herramientas de IA
✅ Interpretación clínica de patrones

¡Continúa con el siguiente módulo!"""
        else:
            message = "Para completar el módulo, debes obtener al menos 70 puntos en la evaluación."
        
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Módulo Completado"),
            content=ft.Text(message),
            actions=[ft.TextButton("Cerrar", on_click=close_dialog)]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def next_tab(self):
        """Ir a la siguiente pestaña"""
        if self.current_tab < 6:
            self.tabs.selected_index = self.current_tab + 1
            self.on_tab_change(type('obj', (object,), {'control': self.tabs}))

def main(page: ft.Page):
    app = OVAEpidemicCurves(page)

if __name__ == "__main__":
    ft.app(target=main)
