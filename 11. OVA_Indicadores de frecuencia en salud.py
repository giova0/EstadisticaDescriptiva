
import flet as ft
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import math
import random
from io import BytesIO
import base64

class OVAIndicadoresSalud:
    def __init__(self):
        self.current_section = "intro"
        self.progress = 0
        self.evaluation_answers = {}
        self.evaluation_score = 0
        
        # Datos para cálculos
        self.prev_cases = 150
        self.prev_population = 10000
        self.inc_cases = 75
        self.inc_population = 9850
        self.let_deaths = 15
        self.let_cases = 150
        
        # Datos de práctica
        self.practice_prev_cases = 2450
        self.practice_prev_pop = 1028736
        self.practice_inc_cases = 3890
        self.practice_inc_pop = 1026286
        self.practice_let_deaths = 89
        self.practice_let_cases = 6340
        
        # Datos del simulador
        self.sim_population = 10000
        self.sim_prevalence = 2.0
        self.sim_incidence = 1.0
        self.sim_lethality = 10.0

    def main(self, page: ft.Page):
        page.title = "OVA 11: Indicadores de Frecuencia en Salud"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.scroll = ft.ScrollMode.AUTO
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "OVA 11: Indicadores de Frecuencia en Salud",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.WHITE,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Modelo Pedagógico C(H)ANGE - Universidad Antonio Nariño",
                    size=16,
                    color=ft.colors.WHITE,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Row([
                    ft.Text("Combinatoria", color=ft.colors.WHITE, size=12),
                    ft.Text("Álgebra", color=ft.colors.WHITE, size=12),
                    ft.Text("Números", color=ft.colors.WHITE, size=12),
                    ft.Text("Geometría", color=ft.colors.WHITE, size=12),
                    ft.Text("Estadística", color=ft.colors.WHITE, size=12),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            gradient=ft.LinearGradient([ft.colors.BLUE_700, ft.colors.PURPLE_700]),
            padding=20,
            margin=ft.margin.only(bottom=10)
        )
        
        # Progress Bar
        self.progress_bar = ft.ProgressBar(value=0, color=ft.colors.BLUE_600, height=4)
        self.progress_text = ft.Text("0%", size=12, color=ft.colors.GREY_600)
        
        progress_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Progreso del Aprendizaje", size=12, color=ft.colors.GREY_600),
                    self.progress_text
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar
            ]),
            padding=10,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
        
        # Navigation
        self.nav_buttons = []
        nav_items = [
            ("intro", "Introducción"),
            ("theory", "Teoría Interactiva"),
            ("simulator", "Simulador"),
            ("practice", "Práctica Guiada"),
            ("evaluation", "Evaluación"),
            ("resources", "Recursos")
        ]
        
        nav_row = ft.Row([], scroll=ft.ScrollMode.AUTO, spacing=10)
        for section_id, title in nav_items:
            btn = ft.ElevatedButton(
                text=title,
                on_click=lambda e, s=section_id: self.show_section(s),
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE_100 if section_id == "intro" else ft.colors.GREY_100,
                    color=ft.colors.BLUE_800 if section_id == "intro" else ft.colors.BLACK
                )
            )
            self.nav_buttons.append(btn)
            nav_row.controls.append(btn)
        
        navigation = ft.Container(
            content=nav_row,
            padding=10,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
        
        # Content Container
        self.content_container = ft.Container(
            content=self.create_intro_section(),
            padding=20,
            expand=True
        )
        
        # Main Layout
        page.add(
            ft.Column([
                header,
                progress_container,
                navigation,
                self.content_container
            ], expand=True, spacing=0)
        )
        
        page.update()

    def show_section(self, section_id):
        self.current_section = section_id
        self.update_progress()
        self.update_navigation()
        
        if section_id == "intro":
            self.content_container.content = self.create_intro_section()
        elif section_id == "theory":
            self.content_container.content = self.create_theory_section()
        elif section_id == "simulator":
            self.content_container.content = self.create_simulator_section()
        elif section_id == "practice":
            self.content_container.content = self.create_practice_section()
        elif section_id == "evaluation":
            self.content_container.content = self.create_evaluation_section()
        elif section_id == "resources":
            self.content_container.content = self.create_resources_section()
        
        self.content_container.update()

    def update_progress(self):
        sections = ["intro", "theory", "simulator", "practice", "evaluation", "resources"]
        current_index = sections.index(self.current_section)
        self.progress = (current_index + 1) / len(sections)
        self.progress_bar.value = self.progress
        self.progress_text.value = f"{int(self.progress * 100)}%"
        self.progress_bar.update()
        self.progress_text.update()

    def update_navigation(self):
        sections = ["intro", "theory", "simulator", "practice", "evaluation", "resources"]
        for i, btn in enumerate(self.nav_buttons):
            if sections[i] == self.current_section:
                btn.style.bgcolor = ft.colors.BLUE_100
                btn.style.color = ft.colors.BLUE_800
            else:
                btn.style.bgcolor = ft.colors.GREY_100
                btn.style.color = ft.colors.BLACK
            btn.update()

    def create_intro_section(self):
        return ft.Container(
            content=ft.Column([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("🎯 Objetivos de Aprendizaje", size=24, weight=ft.FontWeight.BOLD),
                            ft.Row([
                                ft.Column([
                                    self.create_objective_item("1", "Calcular e interpretar prevalencia, incidencia y letalidad en contextos de salud pública"),
                                    self.create_objective_item("2", "Aplicar definiciones operativas correctas para numeradores y denominadores"),
                                    self.create_objective_item("3", "Realizar estandarización directa simple para comparaciones poblacionales"),
                                ], expand=True),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Modelo C(H)ANGE Integrado", size=16, weight=ft.FontWeight.BOLD),
                                        ft.Text("• Combinatoria: Selección de muestras y casos", size=12),
                                        ft.Text("• Álgebra: Fórmulas de indicadores", size=12),
                                        ft.Text("• Números: Proporciones y tasas", size=12),
                                        ft.Text("• Geometría: Visualizaciones gráficas", size=12),
                                        ft.Text("• Estadística: Interpretación epidemiológica", size=12),
                                    ]),
                                    bgcolor=ft.colors.BLUE_50,
                                    padding=15,
                                    border_radius=10,
                                    expand=True
                                )
                            ], spacing=20),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("💡 ¿Por qué son importantes estos indicadores?", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Text("Los indicadores de frecuencia son fundamentales para la toma de decisiones en salud pública, permitiendo evaluar la magnitud de problemas de salud, planificar recursos y evaluar intervenciones.", size=14)
                                ]),
                                bgcolor=ft.colors.YELLOW_50,
                                padding=15,
                                border_radius=10,
                                border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400))
                            ),
                            ft.ElevatedButton(
                                "Comenzar Aprendizaje Interactivo →",
                                on_click=lambda e: self.show_section("theory"),
                                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)
                            )
                        ], spacing=20),
                        padding=20
                    )
                )
            ], scroll=ft.ScrollMode.AUTO)
        )

    def create_objective_item(self, number, text):
        return ft.Row([
            ft.Container(
                content=ft.Text(number, color=ft.colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
                bgcolor=ft.colors.GREEN_500,
                width=24,
                height=24,
                border_radius=12,
                alignment=ft.alignment.center
            ),
            ft.Text(text, size=14, expand=True)
        ], spacing=10)

    def create_theory_section(self):
        # Campos de entrada para cálculos
        self.prev_cases_field = ft.TextField(
            label="Casos existentes",
            value=str(self.prev_cases),
            on_change=self.calculate_prevalence,
            width=200
        )
        self.prev_pop_field = ft.TextField(
            label="Población total",
            value=str(self.prev_population),
            on_change=self.calculate_prevalence,
            width=200
        )
        self.prevalence_result = ft.Text("1.50%", size=16, weight=ft.FontWeight.BOLD)
        
        self.inc_cases_field = ft.TextField(
            label="Casos nuevos",
            value=str(self.inc_cases),
            on_change=self.calculate_incidence,
            width=200
        )
        self.inc_pop_field = ft.TextField(
            label="Población en riesgo",
            value=str(self.inc_population),
            on_change=self.calculate_incidence,
            width=200
        )
        self.incidence_result = ft.Text("0.76%", size=16, weight=ft.FontWeight.BOLD)
        
        self.let_deaths_field = ft.TextField(
            label="Muertes",
            value=str(self.let_deaths),
            on_change=self.calculate_lethality,
            width=200
        )
        self.let_cases_field = ft.TextField(
            label="Total de casos",
            value=str(self.let_cases),
            on_change=self.calculate_lethality,
            width=200
        )
        self.lethality_result = ft.Text("10.0%", size=16, weight=ft.FontWeight.BOLD)
        
        # Retroalimentación IA
        self.ai_feedback = ft.Text(
            "¡Excelente! Has calculado correctamente los tres indicadores principales.",
            size=14,
            color=ft.colors.WHITE
        )
        
        return ft.Column([
            ft.Row([
                # Prevalencia
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("📊", size=24),
                                    bgcolor=ft.colors.RED_100,
                                    width=48,
                                    height=48,
                                    border_radius=8,
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("Prevalencia", size=18, weight=ft.FontWeight.BOLD)
                            ], spacing=10),
                            ft.Text("Proporción de individuos que tienen una enfermedad en un momento específico.", size=12),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Fórmula (Álgebra):", weight=ft.FontWeight.BOLD),
                                    ft.Container(
                                        content=ft.Text("P = (Casos existentes / Población total) × 100", 
                                                       size=12, text_align=ft.TextAlign.CENTER),
                                        bgcolor=ft.colors.WHITE,
                                        padding=10,
                                        border_radius=5,
                                        border=ft.border.all(1, ft.colors.GREY_400)
                                    )
                                ]),
                                bgcolor=ft.colors.RED_50,
                                padding=10,
                                border_radius=8
                            ),
                            self.prev_cases_field,
                            self.prev_pop_field,
                            ft.Container(
                                content=ft.Text(f"Prevalencia: {self.prevalence_result.value}", weight=ft.FontWeight.BOLD),
                                bgcolor=ft.colors.GREY_50,
                                padding=10,
                                border_radius=5
                            )
                        ], spacing=10),
                        padding=15
                    ),
                    expand=True
                ),
                
                # Incidencia
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("📈", size=24),
                                    bgcolor=ft.colors.BLUE_100,
                                    width=48,
                                    height=48,
                                    border_radius=8,
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("Incidencia", size=18, weight=ft.FontWeight.BOLD)
                            ], spacing=10),
                            ft.Text("Número de casos nuevos que se desarrollan en un período específico.", size=12),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Fórmula (Álgebra):", weight=ft.FontWeight.BOLD),
                                    ft.Container(
                                        content=ft.Text("I = (Casos nuevos / Población en riesgo) × 100", 
                                                       size=12, text_align=ft.TextAlign.CENTER),
                                        bgcolor=ft.colors.WHITE,
                                        padding=10,
                                        border_radius=5,
                                        border=ft.border.all(1, ft.colors.GREY_400)
                                    )
                                ]),
                                bgcolor=ft.colors.BLUE_50,
                                padding=10,
                                border_radius=8
                            ),
                            self.inc_cases_field,
                            self.inc_pop_field,
                            ft.Container(
                                content=ft.Text(f"Incidencia: {self.incidence_result.value}", weight=ft.FontWeight.BOLD),
                                bgcolor=ft.colors.GREY_50,
                                padding=10,
                                border_radius=5
                            )
                        ], spacing=10),
                        padding=15
                    ),
                    expand=True
                ),
                
                # Letalidad
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("⚠️", size=24),
                                    bgcolor=ft.colors.PURPLE_100,
                                    width=48,
                                    height=48,
                                    border_radius=8,
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("Letalidad", size=18, weight=ft.FontWeight.BOLD)
                            ], spacing=10),
                            ft.Text("Proporción de personas que mueren entre aquellas que tienen la enfermedad.", size=12),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Fórmula (Álgebra):", weight=ft.FontWeight.BOLD),
                                    ft.Container(
                                        content=ft.Text("L = (Muertes por enfermedad / Total de casos) × 100", 
                                                       size=12, text_align=ft.TextAlign.CENTER),
                                        bgcolor=ft.colors.WHITE,
                                        padding=10,
                                        border_radius=5,
                                        border=ft.border.all(1, ft.colors.GREY_400)
                                    )
                                ]),
                                bgcolor=ft.colors.PURPLE_50,
                                padding=10,
                                border_radius=8
                            ),
                            self.let_deaths_field,
                            self.let_cases_field,
                            ft.Container(
                                content=ft.Text(f"Letalidad: {self.lethality_result.value}", weight=ft.FontWeight.BOLD),
                                bgcolor=ft.colors.GREY_50,
                                padding=10,
                                border_radius=5
                            )
                        ], spacing=10),
                        padding=15
                    ),
                    expand=True
                )
            ], spacing=10),
            
            # Gráfico y retroalimentación
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("📊 Visualización Geométrica de Indicadores", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.Container(
                                content=ft.Text("Gráfico de barras aquí", text_align=ft.TextAlign.CENTER),
                                bgcolor=ft.colors.GREY_100,
                                width=400,
                                height=300,
                                border_radius=8,
                                alignment=ft.alignment.center
                            ),
                            ft.Column([
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Interpretación Clínica", weight=ft.FontWeight.BOLD, color=ft.colors.RED_800),
                                        ft.Text("La prevalencia del 1.5% indica que 15 de cada 1000 personas tienen la enfermedad actualmente.", 
                                               size=12, color=ft.colors.RED_700)
                                    ]),
                                    bgcolor=ft.colors.RED_50,
                                    padding=10,
                                    border_radius=8,
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Implicaciones de Salud Pública", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                        ft.Text("Una incidencia del 0.76% sugiere 7-8 casos nuevos por cada 1000 personas en riesgo.", 
                                               size=12, color=ft.colors.BLUE_700)
                                    ]),
                                    bgcolor=ft.colors.BLUE_50,
                                    padding=10,
                                    border_radius=8,
                                    expand=True
                                )
                            ], expand=True, spacing=10)
                        ], spacing=20)
                    ], spacing=15),
                    padding=20
                )
            ),
            
            # Retroalimentación IA
            ft.Container(
                content=ft.Column([
                    ft.Text("🤖 Retroalimentación Inteligente", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    self.ai_feedback
                ]),
                gradient=ft.LinearGradient([ft.colors.BLUE_400, ft.colors.CYAN_400]),
                padding=20,
                border_radius=10
            )
        ], spacing=15, scroll=ft.ScrollMode.AUTO)

    def calculate_prevalence(self, e):
        try:
            cases = float(self.prev_cases_field.value or 0)
            population = float(self.prev_pop_field.value or 1)
            prevalence = (cases / population) * 100
            self.prevalence_result.value = f"{prevalence:.2f}%"
            self.update_ai_feedback()
            self.prevalence_result.update()
        except:
            pass

    def calculate_incidence(self, e):
        try:
            cases = float(self.inc_cases_field.value or 0)
            population = float(self.inc_pop_field.value or 1)
            incidence = (cases / population) * 100
            self.incidence_result.value = f"{incidence:.2f}%"
            self.update_ai_feedback()
            self.incidence_result.update()
        except:
            pass

    def calculate_lethality(self, e):
        try:
            deaths = float(self.let_deaths_field.value or 0)
            cases = float(self.let_cases_field.value or 1)
            lethality = (deaths / cases) * 100
            self.lethality_result.value = f"{lethality:.1f}%"
            self.update_ai_feedback()
            self.lethality_result.update()
        except:
            pass

    def update_ai_feedback(self):
        try:
            prevalence = float(self.prevalence_result.value.replace('%', ''))
            incidence = float(self.incidence_result.value.replace('%', ''))
            lethality = float(self.lethality_result.value.replace('%', ''))
            
            feedback = "Análisis de IA: "
            
            if incidence > prevalence:
                feedback += "La incidencia supera la prevalencia, sugiriendo un brote activo o enfermedad de corta duración. "
            elif prevalence > incidence * 2:
                feedback += "La prevalencia es significativamente mayor que la incidencia, indicando una enfermedad crónica. "
            
            if lethality > 10:
                feedback += "La letalidad es alta, requiere atención médica especializada inmediata."
            elif lethality < 1:
                feedback += "La letalidad es baja, sugiere buen pronóstico con tratamiento adecuado."
            
            self.ai_feedback.value = feedback
            self.ai_feedback.update()
        except:
            pass

    def create_simulator_section(self):
        # Controles del simulador
        self.sim_pop_slider = ft.Slider(
            min=1000, max=100000, value=self.sim_population,
            divisions=99, label="{value}",
            on_change=self.update_simulation
        )
        self.sim_prev_slider = ft.Slider(
            min=0.1, max=10, value=self.sim_prevalence,
            divisions=99, label="{value}%",
            on_change=self.update_simulation
        )
        self.sim_inc_slider = ft.Slider(
            min=0.1, max=5, value=self.sim_incidence,
            divisions=49, label="{value}%",
            on_change=self.update_simulation
        )
        self.sim_let_slider = ft.Slider(
            min=1, max=50, value=self.sim_lethality,
            divisions=49, label="{value}%",
            on_change=self.update_simulation
        )
        
        # Resultados del simulador
        self.sim_prev_result = ft.Text("2.0%", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600)
        self.sim_inc_result = ft.Text("1.0%", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600)
        self.sim_let_result = ft.Text("10%", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_600)
        
        # Cálculos combinatorios
        self.combinations_result = ft.Text("C(10000,100) ≈ 10^139", size=12)
        
        return ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("🧪 Simulador de Poblaciones", size=24, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.Column([
                                ft.Text("Parámetros de Simulación", size=16, weight=ft.FontWeight.BOLD),
                                ft.Column([
                                    ft.Text("Tamaño de Población:", weight=ft.FontWeight.BOLD),
                                    self.sim_pop_slider,
                                    ft.Text("Tasa de Prevalencia Inicial (%):", weight=ft.FontWeight.BOLD),
                                    self.sim_prev_slider,
                                    ft.Text("Tasa de Incidencia Anual (%):", weight=ft.FontWeight.BOLD),
                                    self.sim_inc_slider,
                                    ft.Text("Tasa de Letalidad (%):", weight=ft.FontWeight.BOLD),
                                    self.sim_let_slider,
                                    ft.ElevatedButton(
                                        "🚀 Ejecutar Simulación",
                                        on_click=self.run_simulation,
                                        style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE)
                                    )
                                ], spacing=10),
                                
                                # Sección de Combinatoria
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("🔢 Cálculos Combinatorios", weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW_800),
                                        ft.Text("Formas de seleccionar 100 individuos de 10,000:", size=12),
                                        self.combinations_result
                                    ]),
                                    bgcolor=ft.colors.YELLOW_50,
                                    padding=10,
                                    border_radius=8
                                )
                            ], expand=True),
                            
                            ft.Column([
                                ft.Text("Resultados de la Simulación", size=16, weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=ft.Text("Gráfico circular aquí", text_align=ft.TextAlign.CENTER),
                                    bgcolor=ft.colors.GREY_100,
                                    width=400,
                                    height=300,
                                    border_radius=8,
                                    alignment=ft.alignment.center
                                ),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Column([
                                            self.sim_prev_result,
                                            ft.Text("Prevalencia", size=12, color=ft.colors.GREY_600)
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        bgcolor=ft.colors.RED_50,
                                        padding=10,
                                        border_radius=8,
                                        expand=True
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            self.sim_inc_result,
                                            ft.Text("Incidencia", size=12, color=ft.colors.GREY_600)
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        bgcolor=ft.colors.BLUE_50,
                                        padding=10,
                                        border_radius=8,
                                        expand=True
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            self.sim_let_result,
                                            ft.Text("Letalidad", size=12, color=ft.colors.GREY_600)
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        bgcolor=ft.colors.PURPLE_50,
                                        padding=10,
                                        border_radius=8,
                                        expand=True
                                    )
                                ], spacing=10)
                            ], expand=True)
                        ], spacing=20)
                    ], spacing=15),
                    padding=20
                )
            ),
            
            # Escenarios predefinidos
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("📋 Escenarios Epidemiológicos", size=16, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.ElevatedButton(
                                "COVID-19\nPandemia viral",
                                on_click=lambda e: self.load_scenario("covid"),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                            ),
                            ft.ElevatedButton(
                                "Diabetes Tipo 2\nEnfermedad crónica",
                                on_click=lambda e: self.load_scenario("diabetes"),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                            ),
                            ft.ElevatedButton(
                                "Cáncer de Pulmón\nEnfermedad oncológica",
                                on_click=lambda e: self.load_scenario("cancer"),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                    ]),
                    padding=20
                )
            )
        ], spacing=15, scroll=ft.ScrollMode.AUTO)

    def update_simulation(self, e):
        self.sim_population = int(self.sim_pop_slider.value)
        self.sim_prevalence = self.sim_prev_slider.value
        self.sim_incidence = self.sim_inc_slider.value
        self.sim_lethality = self.sim_let_slider.value
        
        # Actualizar cálculos combinatorios
        sample_size = min(100, int(self.sim_population * 0.01))
        if self.sim_population > 1000:
            exponent = int(math.log10(self.sim_population) * sample_size / 10)
            self.combinations_result.value = f"C({int(self.sim_population):,},{sample_size}) ≈ 10^{exponent}"
            self.combinations_result.update()

    def run_simulation(self, e):
        population = int(self.sim_population)
        prevalence = self.sim_prevalence
        incidence = self.sim_incidence
        lethality = self.sim_lethality
        
        # Simular datos
        existing_cases = int(population * prevalence / 100)
        new_cases = int((population - existing_cases) * incidence / 100)
        deaths = int((existing_cases + new_cases) * lethality / 100)
        
        # Calcular indicadores finales
        final_prevalence = ((existing_cases + new_cases - deaths) / population * 100)
        final_incidence = (new_cases / (population - existing_cases) * 100)
        final_lethality = (deaths / (existing_cases + new_cases) * 100) if (existing_cases + new_cases) > 0 else 0
        
        # Actualizar resultados
        self.sim_prev_result.value = f"{final_prevalence:.2f}%"
        self.sim_inc_result.value = f"{final_incidence:.2f}%"
        self.sim_let_result.value = f"{final_lethality:.1f}%"
        
        self.sim_prev_result.update()
        self.sim_inc_result.update()
        self.sim_let_result.update()

    def load_scenario(self, scenario):
        scenarios = {
            "covid": {"population": 50000, "prevalence": 3.2, "incidence": 1.8, "lethality": 2.1},
            "diabetes": {"population": 100000, "prevalence": 8.5, "incidence": 0.6, "lethality": 1.2},
            "cancer": {"population": 75000, "prevalence": 1.2, "incidence": 0.4, "lethality": 25.0}
        }
        
        if scenario in scenarios:
            data = scenarios[scenario]
            self.sim_pop_slider.value = data["population"]
            self.sim_prev_slider.value = data["prevalence"]
            self.sim_inc_slider.value = data["incidence"]
            self.sim_let_slider.value = data["lethality"]
            
            self.sim_pop_slider.update()
            self.sim_prev_slider.update()
            self.sim_inc_slider.update()
            self.sim_let_slider.update()
            
            self.update_simulation(None)
            self.run_simulation(None)

    def create_practice_section(self):
        # Campos de práctica
        self.practice_prev_cases_field = ft.TextField(
            label="Casos existentes al inicio",
            value=str(self.practice_prev_cases),
            on_change=self.calculate_practice_indicators,
            width=200
        )
        self.practice_prev_pop_field = ft.TextField(
            label="Población total",
            value=str(self.practice_prev_pop),
            on_change=self.calculate_practice_indicators,
            width=200
        )
        self.practice_prev_result = ft.Text("0.24%", weight=ft.FontWeight.BOLD)
        
        self.practice_inc_cases_field = ft.TextField(
            label="Casos nuevos",
            value=str(self.practice_inc_cases),
            on_change=self.calculate_practice_indicators,
            width=200
        )
        self.practice_inc_pop_field = ft.TextField(
            label="Población en riesgo",
            value=str(self.practice_inc_pop),
            on_change=self.calculate_practice_indicators,
            width=200
        )
        self.practice_inc_result = ft.Text("0.38%", weight=ft.FontWeight.BOLD)
        
        self.practice_let_deaths_field = ft.TextField(
            label="Muertes por dengue",
            value=str(self.practice_let_deaths),
            on_change=self.calculate_practice_indicators,
            width=200
        )
        self.practice_let_cases_field = ft.TextField(
            label="Total de casos",
            value=str(self.practice_let_cases),
            on_change=self.calculate_practice_indicators,
            width=200
        )
        self.practice_let_result = ft.Text("1.40%", weight=ft.FontWeight.BOLD)
        
        # Interpretaciones
        self.epidemiological_interpretation = ft.Text(
            "La incidencia (0.38%) es mayor que la prevalencia inicial (0.24%), indicando un brote activo de dengue en la población.",
            size=12
        )
        self.public_health_actions = ft.Text(
            "Se requieren medidas inmediatas de control vectorial y vigilancia epidemiológica intensificada.",
            size=12
        )
        
        return ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("👩‍⚕️ Práctica Guiada: Caso Clínico", size=24, weight=ft.FontWeight.BOLD),
                        
                        # Caso de estudio
                        ft.Container(
                            content=ft.Column([
                                ft.Text("📋 Caso: Brote de Dengue en Cartagena", size=16, weight=ft.FontWeight.BOLD),
                                ft.Text("Durante el año 2023, en la ciudad de Cartagena (población: 1,028,736 habitantes), se reportaron los siguientes datos sobre dengue:"),
                                ft.Column([
                                    ft.Text("• Casos existentes al inicio del año: 2,450"),
                                    ft.Text("• Casos nuevos durante el año: 3,890"),
                                    ft.Text("• Muertes por dengue: 89"),
                                    ft.Text("• Población susceptible: 1,026,286"),
                                ])
                            ]),
                            bgcolor=ft.colors.BLUE_50,
                            padding=15,
                            border_radius=10
                        ),
                        
                        ft.Row([
                            # Calculadora paso a paso
                            ft.Column([
                                ft.Text("🧮 Calculadora Paso a Paso", size=16, weight=ft.FontWeight.BOLD),
                                
                                # Paso 1: Prevalencia
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Paso 1: Calcular Prevalencia", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700),
                                        self.practice_prev_cases_field,
                                        self.practice_prev_pop_field,
                                        ft.Container(
                                            content=ft.Text(f"Prevalencia: {self.practice_prev_result.value}"),
                                            bgcolor=ft.colors.GREEN_50,
                                            padding=10,
                                            border_radius=5
                                        )
                                    ], spacing=10),
                                    border=ft.border.all(1, ft.colors.GREY_300),
                                    padding=15,
                                    border_radius=8
                                ),
                                
                                # Paso 2: Incidencia
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Paso 2: Calcular Incidencia", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
                                        self.practice_inc_cases_field,
                                        self.practice_inc_pop_field,
                                        ft.Container(
                                            content=ft.Text(f"Incidencia: {self.practice_inc_result.value}"),
                                            bgcolor=ft.colors.BLUE_50,
                                            padding=10,
                                            border_radius=5
                                        )
                                    ], spacing=10),
                                    border=ft.border.all(1, ft.colors.GREY_300),
                                    padding=15,
                                    border_radius=8
                                ),
                                
                                # Paso 3: Letalidad
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Paso 3: Calcular Letalidad", weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
                                        self.practice_let_deaths_field,
                                        self.practice_let_cases_field,
                                        ft.Container(
                                            content=ft.Text(f"Letalidad: {self.practice_let_result.value}"),
                                            bgcolor=ft.colors.PURPLE_50,
                                            padding=10,
                                            border_radius=5
                                        )
                                    ], spacing=10),
                                    border=ft.border.all(1, ft.colors.GREY_300),
                                    padding=15,
                                    border_radius=8
                                )
                            ], expand=True, spacing=15),
                            
                            # Visualización y interpretación
                            ft.Column([
                                ft.Text("📊 Visualización de Resultados", size=16, weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=ft.Text("Gráfico radar aquí", text_align=ft.TextAlign.CENTER),
                                    bgcolor=ft.colors.GREY_100,
                                    width=400,
                                    height=300,
                                    border_radius=8,
                                    alignment=ft.alignment.center
                                ),
                                
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("💡 Interpretación Epidemiológica", weight=ft.FontWeight.BOLD),
                                        self.epidemiological_interpretation
                                    ]),
                                    bgcolor=ft.colors.YELLOW_50,
                                    padding=10,
                                    border_radius=8,
                                    border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400))
                                ),
                                
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("⚠️ Implicaciones para Salud Pública", weight=ft.FontWeight.BOLD),
                                        self.public_health_actions
                                    ]),
                                    bgcolor=ft.colors.RED_50,
                                    padding=10,
                                    border_radius=8,
                                    border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.RED_400))
                                )
                            ], expand=True, spacing=15)
                        ], spacing=20)
                    ], spacing=20),
                    padding=20
                )
            ),
            
            # Estandarización directa
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("📈 Estandarización Directa Simple", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Comparemos las tasas de dengue entre Cartagena y Bogotá, ajustando por estructura de edad:"),
                        
                        ft.Row([
                            # Tabla de datos
                            ft.Column([
                                ft.Text("Datos por Grupos de Edad", weight=ft.FontWeight.BOLD),
                                ft.DataTable(
                                    columns=[
                                        ft.DataColumn(ft.Text("Edad")),
                                        ft.DataColumn(ft.Text("Cartagena")),
                                        ft.DataColumn(ft.Text("Bogotá")),
                                        ft.DataColumn(ft.Text("Población Estándar")),
                                    ],
                                    rows=[
                                        ft.DataRow(cells=[
                                            ft.DataCell(ft.Text("0-14")),
                                            ft.DataCell(ft.Text("4.2/1000")),
                                            ft.DataCell(ft.Text("2.1/1000")),
                                            ft.DataCell(ft.Text("25%")),
                                        ]),
                                        ft.DataRow(cells=[
                                            ft.DataCell(ft.Text("15-64")),
                                            ft.DataCell(ft.Text("3.8/1000")),
                                            ft.DataCell(ft.Text("1.9/1000")),
                                            ft.DataCell(ft.Text("65%")),
                                        ]),
                                        ft.DataRow(cells=[
                                            ft.DataCell(ft.Text("65+")),
                                            ft.DataCell(ft.Text("2.1/1000")),
                                            ft.DataCell(ft.Text("1.2/1000")),
                                            ft.DataCell(ft.Text("10%")),
                                        ]),
                                    ],
                                )
                            ], expand=True),
                            
                            # Cálculos
                            ft.Column([
                                ft.Text("Tasas Estandarizadas", weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Cartagena (estandarizada):", weight=ft.FontWeight.BOLD),
                                        ft.Text("(4.2×0.25) + (3.8×0.65) + (2.1×0.10) = 3.73/1000", size=12)
                                    ]),
                                    bgcolor=ft.colors.BLUE_50,
                                    padding=10,
                                    border_radius=8
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Bogotá (estandarizada):", weight=ft.FontWeight.BOLD),
                                        ft.Text("(2.1×0.25) + (1.9×0.65) + (1.2×0.10) = 1.88/1000", size=12)
                                    ]),
                                    bgcolor=ft.colors.GREEN_50,
                                    padding=10,
                                    border_radius=8
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Razón de tasas: 3.73/1.88 = 1.98", weight=ft.FontWeight.BOLD),
                                        ft.Text("Cartagena tiene el doble de riesgo que Bogotá", size=12)
                                    ]),
                                    bgcolor=ft.colors.YELLOW_50,
                                    padding=10,
                                    border_radius=8
                                )
                            ], expand=True, spacing=10)
                        ], spacing=20)
                    ], spacing=15),
                    padding=20
                )
            )
        ], spacing=15, scroll=ft.ScrollMode.AUTO)

    def calculate_practice_indicators(self, e):
        try:
            prev_cases = float(self.practice_prev_cases_field.value or 0)
            prev_pop = float(self.practice_prev_pop_field.value or 1)
            inc_cases = float(self.practice_inc_cases_field.value or 0)
            inc_pop = float(self.practice_inc_pop_field.value or 1)
            let_deaths = float(self.practice_let_deaths_field.value or 0)
            let_cases = float(self.practice_let_cases_field.value or 1)
            
            prevalence = (prev_cases / prev_pop * 100)
            incidence = (inc_cases / inc_pop * 100)
            lethality = (let_deaths / let_cases * 100)
            
            self.practice_prev_result.value = f"{prevalence:.2f}%"
            self.practice_inc_result.value = f"{incidence:.2f}%"
            self.practice_let_result.value = f"{lethality:.2f}%"
            
            # Actualizar interpretaciones
            if incidence > prevalence:
                self.epidemiological_interpretation.value = f"La incidencia ({incidence:.2f}%) supera la prevalencia ({prevalence:.2f}%), indicando un brote activo con rápida propagación."
                self.public_health_actions.value = "Se requiere implementación inmediata de medidas de control vectorial y vigilancia epidemiológica intensificada."
            else:
                self.epidemiological_interpretation.value = f"La prevalencia ({prevalence:.2f}%) es mayor que la incidencia ({incidence:.2f}%), sugiriendo una enfermedad endémica con casos acumulados."
                self.public_health_actions.value = "Se necesita mantener vigilancia continua y programas de prevención sostenidos."
            
            if lethality > 5:
                self.public_health_actions.value += " La alta letalidad requiere protocolos de atención médica especializada."
            
            self.practice_prev_result.update()
            self.practice_inc_result.update()
            self.practice_let_result.update()
            self.epidemiological_interpretation.update()
            self.public_health_actions.update()
        except:
            pass

    def create_evaluation_section(self):
        # Preguntas de evaluación
        self.q1_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="a", label="a) 1.5%"),
                ft.Radio(value="b", label="b) 15%"),
                ft.Radio(value="c", label="c) 0.15%"),
                ft.Radio(value="d", label="d) 7.5%"),
            ])
        )
        
        self.q2_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="a", label="a) La diabetes es una enfermedad de corta duración"),
                ft.Radio(value="b", label="b) La diabetes es una enfermedad crónica de larga duración"),
                ft.Radio(value="c", label="c) Hay un error en los datos"),
                ft.Radio(value="d", label="d) No se puede determinar"),
            ])
        )
        
        self.q3_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="a", label="a) 3%"),
                ft.Radio(value="b", label="b) 30%"),
                ft.Radio(value="c", label="c) 0.3%"),
                ft.Radio(value="d", label="d) 6%"),
            ])
        )
        
        self.q4_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="a", label="a) Para ajustar por diferencias en la estructura de edad"),
                ft.Radio(value="b", label="b) Para aumentar el tamaño de muestra"),
                ft.Radio(value="c", label="c) Para reducir errores de medición"),
                ft.Radio(value="d", label="d) Para simplificar los cálculos"),
            ])
        )
        
        # Contenedores de retroalimentación
        self.feedback_q1 = ft.Container(visible=False)
        self.feedback_q2 = ft.Container(visible=False)
        self.feedback_q3 = ft.Container(visible=False)
        self.feedback_q4 = ft.Container(visible=False)
        
        # Resultado final
        self.final_score_container = ft.Container(visible=False)
        
        return ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("📝 Evaluación Automatizada", size=24, weight=ft.FontWeight.BOLD),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Instrucciones", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                ft.Text("Responde las siguientes preguntas basadas en el caso de estudio. Recibirás retroalimentación inmediata.", color=ft.colors.BLUE_700)
                            ]),
                            bgcolor=ft.colors.BLUE_50,
                            padding=15,
                            border_radius=10
                        ),
                        
                        # Pregunta 1
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Pregunta 1: Cálculo de Prevalencia", weight=ft.FontWeight.BOLD),
                                ft.Text("En una población de 50,000 habitantes, se encontraron 750 casos existentes de hipertensión. ¿Cuál es la prevalencia?"),
                                self.q1_group,
                                self.feedback_q1
                            ], spacing=10),
                            border=ft.border.all(1, ft.colors.GREY_300),
                            padding=15,
                            border_radius=8
                        ),
                        
                        # Pregunta 2
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Pregunta 2: Interpretación de Incidencia", weight=ft.FontWeight.BOLD),
                                ft.Text("Si la incidencia anual de diabetes es 0.8% y la prevalencia es 2.5%, ¿qué puedes concluir?"),
                                self.q2_group,
                                self.feedback_q2
                            ], spacing=10),
                            border=ft.border.all(1, ft.colors.GREY_300),
                            padding=15,
                            border_radius=8
                        ),
                        
                        # Pregunta 3
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Pregunta 3: Cálculo de Letalidad", weight=ft.FontWeight.BOLD),
                                ft.Text("En un brote de COVID-19 con 2,000 casos confirmados y 60 muertes, ¿cuál es la tasa de letalidad?"),
                                self.q3_group,
                                self.feedback_q3
                            ], spacing=10),
                            border=ft.border.all(1, ft.colors.GREY_300),
                            padding=15,
                            border_radius=8
                        ),
                        
                        # Pregunta 4
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Pregunta 4: Estandarización", weight=ft.FontWeight.BOLD),
                                ft.Text("¿Por qué es importante la estandarización directa al comparar tasas entre poblaciones?"),
                                self.q4_group,
                                self.feedback_q4
                            ], spacing=10),
                            border=ft.border.all(1, ft.colors.GREY_300),
                            padding=15,
                            border_radius=8
                        ),
                        
                        ft.ElevatedButton(
                            "📊 Enviar Evaluación",
                            on_click=self.submit_evaluation,
                            style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE)
                        ),
                        
                        self.final_score_container
                        
                    ], spacing=20),
                    padding=20
                )
            )
        ], scroll=ft.ScrollMode.AUTO)

    def submit_evaluation(self, e):
        questions = [self.q1_group, self.q2_group, self.q3_group, self.q4_group]
        feedbacks = [self.feedback_q1, self.feedback_q2, self.feedback_q3, self.feedback_q4]
        correct_answers = ["a", "b", "a", "a"]
        explanations = {
            "q1": {"correct": "Prevalencia = (750/50,000) × 100 = 1.5%", 
                   "incorrect": "Recuerda: Prevalencia = (casos existentes/población total) × 100"},
            "q2": {"correct": "Una prevalencia mayor que la incidencia indica enfermedad crónica de larga duración.", 
                   "incorrect": "Cuando prevalencia > incidencia, sugiere enfermedad crónica."},
            "q3": {"correct": "Letalidad = (60/2,000) × 100 = 3%", 
                   "incorrect": "Recuerda: Letalidad = (muertes/total de casos) × 100"},
            "q4": {"correct": "La estandarización permite comparaciones justas entre poblaciones con diferentes estructuras.", 
                   "incorrect": "La estandarización ajusta por factores como edad que pueden confundir las comparaciones."}
        }
        
        score = 0
        
        for i, (question, feedback, correct) in enumerate(zip(questions, feedbacks, correct_answers)):
            selected = question.value
            question_key = f"q{i+1}"
            
            if selected:
                is_correct = selected == correct
                if is_correct:
                    score += 1
                    feedback.content = ft.Container(
                        content=ft.Text(f"✓ Correcto! {explanations[question_key]['correct']}", color=ft.colors.GREEN_800),
                        bgcolor=ft.colors.GREEN_100,
                        padding=10,
                        border_radius=8
                    )
                else:
                    feedback.content = ft.Container(
                        content=ft.Text(f"✗ Incorrecto. {explanations[question_key]['incorrect']}", color=ft.colors.RED_800),
                        bgcolor=ft.colors.RED_100,
                        padding=10,
                        border_radius=8
                    )
                feedback.visible = True
                feedback.update()
        
        # Mostrar puntuación final
        percentage = (score / len(questions)) * 100
        
        if percentage >= 80:
            score_color = ft.colors.GREEN_100
            score_text_color = ft.colors.GREEN_800
            feedback_text = "🎉 ¡Excelente! Has demostrado un dominio sólido de los indicadores de frecuencia."
        elif percentage >= 60:
            score_color = ft.colors.YELLOW_100
            score_text_color = ft.colors.YELLOW_800
            feedback_text = "👍 Buen trabajo. Revisa los conceptos donde tuviste dificultades."
        else:
            score_color = ft.colors.RED_100
            score_text_color = ft.colors.RED_800
            feedback_text = "📚 Te recomendamos revisar la teoría y practicar más con el simulador."
        
        self.final_score_container.content = ft.Container(
            content=ft.Column([
                ft.Text("🎯 Resultados de la Evaluación", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(f"{score}/{len(questions)}", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600, text_align=ft.TextAlign.CENTER),
                ft.Text(f"{percentage:.0f}%", size=16, color=ft.colors.GREY_600, text_align=ft.TextAlign.CENTER),
                ft.Container(
                    content=ft.Text(feedback_text, color=score_text_color, text_align=ft.TextAlign.CENTER),
                    bgcolor=score_color,
                    padding=15,
                    border_radius=8
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.colors.GREY_50,
            padding=20,
            border_radius=10
        )
        self.final_score_container.visible = True
        self.final_score_container.update()

    def create_resources_section(self):
        return ft.Column([
            ft.Row([
                # Recursos descargables
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("📚 Recursos Descargables", size=18, weight=ft.FontWeight.BOLD),
                            
                            self.create_resource_item(
                                "Plantilla de Cálculo de Indicadores",
                                "Hoja de cálculo con fórmulas predefinidas",
                                "template"
                            ),
                            self.create_resource_item(
                                "Guía de Interpretación Clínica",
                                "Manual con ejemplos prácticos",
                                "guide"
                            ),
                            self.create_resource_item(
                                "Base de Datos de Práctica",
                                "Datos simulados para ejercicios",
                                "database"
                            ),
                            self.create_resource_item(
                                "Checklist de Verificación",
                                "Lista para validar cálculos",
                                "checklist"
                            )
                        ], spacing=15),
                        padding=20
                    ),
                    expand=True
                ),
                
                # Referencias y enlaces
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("🔗 Referencias y Enlaces", size=18, weight=ft.FontWeight.BOLD),
                            
                            self.create_reference_item(
                                "OMS - Indicadores de Salud",
                                "Definiciones oficiales y estándares internacionales",
                                ft.colors.BLUE_500
                            ),
                            self.create_reference_item(
                                "INS Colombia",
                                "Protocolos de vigilancia epidemiológica",
                                ft.colors.GREEN_500
                            ),
                            self.create_reference_item(
                                "CDC - Epidemiología",
                                "Recursos educativos y casos de estudio",
                                ft.colors.PURPLE_500
                            ),
                            self.create_reference_item(
                                "Coursera - Bioestadística",
                                "Cursos complementarios en línea",
                                ft.colors.RED_500
                            ),
                            
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("📖 Bibliografía Recomendada", weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW_800),
                                    ft.Text("• Gordis, L. (2013). Epidemiología. 5ª edición.", size=12),
                                    ft.Text("• Rothman, K.J. (2012). Epidemiology: An Introduction.", size=12),
                                    ft.Text("• Szklo, M. & Nieto, F.J. (2019). Epidemiología Intermedia.", size=12),
                                ]),
                                bgcolor=ft.colors.YELLOW_50,
                                padding=15,
                                border_radius=10
                            )
                        ], spacing=15),
                        padding=20
                    ),
                    expand=True
                )
            ], spacing=15),
            
            # Actividad de transferencia
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("🎯 Actividad de Transferencia", size=18, weight=ft.FontWeight.BOLD),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Proyecto Final: Miniinforme Epidemiológico", size=16, weight=ft.FontWeight.BOLD),
                                ft.Text("Elabora un informe de 2-3 páginas analizando un problema de salud pública de tu región, calculando e interpretando los tres indicadores principales."),
                                
                                ft.Row([
                                    ft.Column([
                                        ft.Text("Estructura Sugerida:", weight=ft.FontWeight.BOLD),
                                        ft.Text("1. Introducción al problema de salud", size=12),
                                        ft.Text("2. Metodología y fuentes de datos", size=12),
                                        ft.Text("3. Cálculo de indicadores", size=12),
                                        ft.Text("4. Interpretación epidemiológica", size=12),
                                        ft.Text("5. Implicaciones para salud pública", size=12),
                                        ft.Text("6. Limitaciones y conclusiones", size=12),
                                    ], expand=True),
                                    
                                    ft.Column([
                                        ft.Text("Criterios de Evaluación:", weight=ft.FontWeight.BOLD),
                                        ft.Text("✓ Correcta aplicación de fórmulas", size=12),
                                        ft.Text("✓ Interpretación clínica adecuada", size=12),
                                        ft.Text("✓ Uso apropiado de visualizaciones", size=12),
                                        ft.Text("✓ Consideraciones éticas", size=12),
                                        ft.Text("✓ Reproducibilidad del análisis", size=12),
                                    ], expand=True)
                                ], spacing=20),
                                
                                ft.ElevatedButton(
                                    "🚀 Iniciar Proyecto",
                                    on_click=self.start_transfer_activity,
                                    style=ft.ButtonStyle(bgcolor=ft.colors.PURPLE_600, color=ft.colors.WHITE)
                                )
                            ], spacing=15),
                            gradient=ft.LinearGradient([ft.colors.PURPLE_50, ft.colors.PINK_50]),
                            padding=20,
                            border_radius=10
                        )
                    ], spacing=15),
                    padding=20
                )
            )
        ], spacing=15, scroll=ft.ScrollMode.AUTO)

    def create_resource_item(self, title, description, resource_type):
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(title, weight=ft.FontWeight.BOLD),
                    ft.Text(description, size=12, color=ft.colors.GREY_600)
                ], expand=True),
                ft.ElevatedButton(
                    "📥 Descargar",
                    on_click=lambda e, rt=resource_type: self.download_resource(rt),
                    style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            border=ft.border.all(1, ft.colors.GREY_300),
            padding=15,
            border_radius=8
        )

    def create_reference_item(self, title, description, color):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(description, size=12),
                ft.Text("→ Visitar sitio web", size=12, color=color)
            ]),
            bgcolor=ft.colors.with_opacity(0.1, color),
            padding=15,
            border_radius=8,
            border=ft.border.only(left=ft.border.BorderSide(4, color))
        )

    def download_resource(self, resource_type):
        resources = {
            "template": "plantilla_indicadores_salud.xlsx",
            "guide": "guia_interpretacion_clinica.pdf",
            "database": "base_datos_practica.csv",
            "checklist": "checklist_verificacion.pdf"
        }
        
        # Simular descarga
        print(f"Descargando: {resources[resource_type]}")
        # En una implementación real, aquí se iniciaría la descarga del archivo

    def start_transfer_activity(self, e):
        print("🎯 Proyecto de Transferencia Iniciado")
        print("Instrucciones enviadas.")
        print("Recuerda incluir:")
        print("• Cálculos correctos")
        print("• Interpretación epidemiológica")
        print("• Visualizaciones apropiadas")
        print("• Consideraciones éticas")

def main(page: ft.Page):
    app = OVAIndicadoresSalud()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)
