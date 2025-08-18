
import flet as ft
import math
import statistics
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import io
import base64

class StatCalculator:
    @staticmethod
    def calculate_stats(data):
        if not data:
            return None
        
        n = len(data)
        mean = statistics.mean(data)
        variance = statistics.variance(data) if n > 1 else 0
        std_dev = statistics.stdev(data) if n > 1 else 0
        data_range = max(data) - min(data)
        cv = (std_dev / mean) * 100 if mean != 0 else 0
        
        return {
            'n': n,
            'mean': mean,
            'variance': variance,
            'std_dev': std_dev,
            'range': data_range,
            'cv': cv
        }
    
    @staticmethod
    def get_interpretation(cv):
        if cv < 10:
            return "Variabilidad baja - Datos muy consistentes"
        elif cv < 20:
            return "Variabilidad moderada - Datos relativamente consistentes"
        elif cv < 30:
            return "Variabilidad alta - Considerar factores que causan dispersión"
        else:
            return "Variabilidad muy alta - Requiere investigación adicional"

class QuizManager:
    def __init__(self):
        self.questions = [
            {
                "question": "¿Cuál es la principal ventaja del coeficiente de variación sobre la desviación estándar?",
                "options": [
                    "Es más fácil de calcular",
                    "Permite comparar variabilidades entre diferentes escalas de medición",
                    "Siempre es menor que la desviación estándar",
                    "No se ve afectado por valores extremos"
                ],
                "correct": 1,
                "explanation": "El coeficiente de variación es una medida relativa que permite comparar la variabilidad entre conjuntos de datos con diferentes unidades o escalas."
            },
            {
                "question": "En un estudio clínico, se encontró que la presión arterial sistólica tiene una media de 120 mmHg y una desviación estándar de 15 mmHg. ¿Qué porcentaje aproximado de pacientes tendrá valores entre 105 y 135 mmHg?",
                "options": [
                    "50%",
                    "68%",
                    "95%",
                    "99.7%"
                ],
                "correct": 1,
                "explanation": "Según la regla empírica (68-95-99.7), aproximadamente 68% de los datos se encuentran dentro de una desviación estándar de la media."
            },
            {
                "question": "¿Cuál de las siguientes situaciones clínicas requiere MENOR variabilidad?",
                "options": [
                    "Niveles de glucosa en ayunas en diabéticos",
                    "Frecuencia cardíaca durante ejercicio",
                    "Dosificación de medicamentos críticos",
                    "Tiempo de respuesta inmunológica"
                ],
                "correct": 2,
                "explanation": "La dosificación de medicamentos críticos requiere la menor variabilidad posible para garantizar eficacia y seguridad del tratamiento."
            },
            {
                "question": "Si dos grupos de pacientes tienen la misma media pero diferentes desviaciones estándar, ¿qué implica esto clínicamente?",
                "options": [
                    "Los tratamientos son igualmente efectivos",
                    "Un grupo tiene mayor variabilidad en la respuesta al tratamiento",
                    "Los grupos son idénticos estadísticamente",
                    "No hay diferencia clínica significativa"
                ],
                "correct": 1,
                "explanation": "Diferentes desviaciones estándar indican diferentes niveles de variabilidad, lo que puede reflejar diferencias en la respuesta al tratamiento o en las características de los pacientes."
            },
            {
                "question": "¿Cuál es la interpretación correcta de un coeficiente de variación del 25% en mediciones de laboratorio?",
                "options": [
                    "Variabilidad muy baja, excelente precisión",
                    "Variabilidad moderada, aceptable para la mayoría de aplicaciones",
                    "Variabilidad alta, requiere investigación adicional",
                    "Variabilidad extrema, datos no confiables"
                ],
                "correct": 2,
                "explanation": "Un CV del 25% indica alta variabilidad que podría requerir investigación adicional para determinar las causas y mejorar la precisión."
            }
        ]
        
        self.current_question = 0
        self.score = 0
        self.user_answers = []

class OVAApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "OVA: Dispersión y Variabilidad Clínica"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.window_width = 1200
        self.page.window_height = 800
        
        self.current_section = "intro"
        self.quiz_manager = QuizManager()
        
        # Colores del tema
        self.primary_color = ft.colors.BLUE_600
        self.secondary_color = ft.colors.PURPLE_500
        self.success_color = ft.colors.GREEN_500
        self.warning_color = ft.colors.ORANGE_500
        self.error_color = ft.colors.RED_500
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        self.header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "📊 Dispersión y Variabilidad Clínica",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.WHITE
                ),
                ft.Text(
                    "Objeto Virtual de Aprendizaje - Estadística Descriptiva para Ciencias de la Salud",
                    size=16,
                    color=ft.colors.WHITE70
                ),
                ft.Row([
                    ft.Container(
                        content=ft.Text("🎯 Modelo C(H)ANGE", size=12),
                        bgcolor=ft.colors.WHITE24,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=20
                    ),
                    ft.Container(
                        content=ft.Text("🤖 IA Integrada", size=12),
                        bgcolor=ft.colors.WHITE24,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=20
                    ),
                    ft.Container(
                        content=ft.Text("🏥 Casos Clínicos", size=12),
                        bgcolor=ft.colors.WHITE24,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=20
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            gradient=ft.LinearGradient([
                ft.colors.BLUE_600,
                ft.colors.PURPLE_600
            ]),
            padding=30,
            alignment=ft.alignment.center
        )
        
        # Navigation
        self.nav_bar = ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    "Introducción",
                    on_click=lambda _: self.show_section("intro"),
                    style=self.get_nav_button_style("intro")
                ),
                ft.ElevatedButton(
                    "Conceptos",
                    on_click=lambda _: self.show_section("conceptos"),
                    style=self.get_nav_button_style("conceptos")
                ),
                ft.ElevatedButton(
                    "Simulador",
                    on_click=lambda _: self.show_section("simulador"),
                    style=self.get_nav_button_style("simulador")
                ),
                ft.ElevatedButton(
                    "Casos Clínicos",
                    on_click=lambda _: self.show_section("casos"),
                    style=self.get_nav_button_style("casos")
                ),
                ft.ElevatedButton(
                    "Evaluación",
                    on_click=lambda _: self.show_section("evaluacion"),
                    style=self.get_nav_button_style("evaluacion")
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.colors.WHITE,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.colors.BLACK12
            )
        )
        
        # Content area
        self.content_area = ft.Container(
            content=self.create_intro_section(),
            padding=20,
            expand=True
        )
        
        # Main layout
        self.page.add(
            ft.Column([
                self.header,
                self.nav_bar,
                self.content_area
            ], expand=True, spacing=0)
        )
    
    def get_nav_button_style(self, section):
        if self.current_section == section:
            return ft.ButtonStyle(
                bgcolor=self.primary_color,
                color=ft.colors.WHITE
            )
        else:
            return ft.ButtonStyle(
                bgcolor=ft.colors.WHITE,
                color=self.primary_color
            )
    
    def show_section(self, section):
        self.current_section = section
        
        # Update navigation buttons
        for control in self.nav_bar.content.controls:
            if isinstance(control, ft.ElevatedButton):
                control.style = self.get_nav_button_style(section)
        
        # Update content
        if section == "intro":
            self.content_area.content = self.create_intro_section()
        elif section == "conceptos":
            self.content_area.content = self.create_conceptos_section()
        elif section == "simulador":
            self.content_area.content = self.create_simulador_section()
        elif section == "casos":
            self.content_area.content = self.create_casos_section()
        elif section == "evaluacion":
            self.content_area.content = self.create_evaluacion_section()
        
        self.page.update()
    
    def create_intro_section(self):
        return ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "🎯 Objetivos de Aprendizaje",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREY_800
                        ),
                        ft.Row([
                            ft.Column([
                                ft.Row([
                                    ft.Text("✓", color=self.success_color, size=20),
                                    ft.Text("Comprender los conceptos fundamentales de dispersión y variabilidad en datos clínicos", expand=True)
                                ]),
                                ft.Row([
                                    ft.Text("✓", color=self.success_color, size=20),
                                    ft.Text("Calcular e interpretar medidas de dispersión en contextos de salud", expand=True)
                                ]),
                                ft.Row([
                                    ft.Text("✓", color=self.success_color, size=20),
                                    ft.Text("Aplicar el pensamiento estadístico en la toma de decisiones clínicas", expand=True)
                                ]),
                                ft.Row([
                                    ft.Text("✓", color=self.success_color, size=20),
                                    ft.Text("Evaluar la significancia clínica de la variabilidad en parámetros de salud", expand=True)
                                ])
                            ], expand=True),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(
                                        "💡 ¿Por qué es importante?",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=self.primary_color
                                    ),
                                    ft.Text(
                                        "En ciencias de la salud, la variabilidad no es solo un concepto estadístico, sino una realidad clínica fundamental que afecta:"
                                    ),
                                    ft.Text("• Diagnósticos precisos"),
                                    ft.Text("• Dosificación de medicamentos"),
                                    ft.Text("• Evaluación de tratamientos"),
                                    ft.Text("• Monitoreo de pacientes"),
                                    ft.Text("• Investigación biomédica")
                                ]),
                                bgcolor=ft.colors.BLUE_50,
                                padding=20,
                                border_radius=10,
                                expand=True
                            )
                        ])
                    ]),
                    padding=30
                )
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "🚀 Metodología C(H)ANGE",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE
                        ),
                        ft.Row([
                            self.create_change_card("🔢", "Combinatoria", "Análisis de variaciones"),
                            self.create_change_card("📐", "Álgebra", "Fórmulas estadísticas"),
                            self.create_change_card("🔢", "Números", "Cálculos precisos"),
                            self.create_change_card("📊", "Geometría", "Visualización gráfica"),
                            self.create_change_card("📈", "Estadística", "Análisis de datos")
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                    ]),
                    padding=30
                ),
                gradient=ft.LinearGradient([
                    self.secondary_color,
                    ft.colors.PINK_500
                ])
            )
        ], scroll=ft.ScrollMode.AUTO)
    
    def create_change_card(self, icon, title, subtitle):
        return ft.Container(
            content=ft.Column([
                ft.Text(icon, size=24),
                ft.Text(title, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text(subtitle, size=12, color=ft.colors.WHITE70)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.colors.WHITE24,
            padding=15,
            border_radius=10,
            width=150
        )
    
    def create_conceptos_section(self):
        # Input field for data
        self.data_input = ft.TextField(
            label="Ingrese datos (separados por comas)",
            multiline=True,
            min_lines=3,
            value="120, 125, 118, 130, 122, 135, 128",
            expand=True
        )
        
        # Results container
        self.stats_results = ft.Container(
            visible=False
        )
        
        # Sliders for distribution
        self.mean_slider = ft.Slider(
            min=50, max=150, value=100,
            label="Media: {value}",
            on_change=self.update_distribution
        )
        
        self.std_slider = ft.Slider(
            min=5, max=30, value=15,
            label="Desviación Estándar: {value}",
            on_change=self.update_distribution
        )
        
        self.clinical_interpretation = ft.Text(
            "Ajuste los parámetros para ver cómo cambia la distribución.",
            color=ft.colors.GREY_700
        )
        
        return ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "📚 Conceptos Fundamentales",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREY_800
                        ),
                        ft.Row([
                            ft.Column([
                                self.create_concept_card(
                                    "🎯 Rango",
                                    "Diferencia entre el valor máximo y mínimo de un conjunto de datos.",
                                    "Rango = Valor máximo - Valor mínimo",
                                    "Ejemplo clínico: Rango de presión arterial sistólica en un grupo de pacientes.",
                                    ft.colors.BLUE_500
                                ),
                                self.create_concept_card(
                                    "📊 Varianza",
                                    "Promedio de las desviaciones cuadráticas respecto a la media.",
                                    "σ² = Σ(xi - μ)² / N",
                                    "Aplicación: Variabilidad en niveles de glucosa en sangre.",
                                    ft.colors.GREEN_500
                                ),
                                self.create_concept_card(
                                    "📈 Desviación Estándar",
                                    "Raíz cuadrada de la varianza, expresada en las mismas unidades que los datos.",
                                    "σ = √(σ²)",
                                    "Interpretación: Aproximadamente 68% de los datos están dentro de ±1σ de la media.",
                                    ft.colors.PURPLE_500
                                ),
                                self.create_concept_card(
                                    "🎲 Coeficiente de Variación",
                                    "Medida relativa de dispersión, útil para comparar variabilidades.",
                                    "CV = (σ / μ) × 100%",
                                    "Ventaja: Permite comparar variabilidades entre diferentes escalas de medición.",
                                    ft.colors.ORANGE_500
                                )
                            ], expand=True),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(
                                        "🧮 Calculadora Interactiva",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.GREY_800
                                    ),
                                    self.data_input,
                                    ft.ElevatedButton(
                                        "Calcular Medidas de Dispersión",
                                        on_click=self.calculate_statistics,
                                        style=ft.ButtonStyle(
                                            bgcolor=self.primary_color,
                                            color=ft.colors.WHITE
                                        )
                                    ),
                                    self.stats_results
                                ]),
                                bgcolor=ft.colors.GREY_50,
                                padding=20,
                                border_radius=10,
                                width=400
                            )
                        ])
                    ]),
                    padding=30
                )
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "📊 Visualización Interactiva",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREY_800
                        ),
                        ft.Row([
                            ft.Container(
                                content=ft.Text("Aquí iría el gráfico de distribución", 
                                               text_align=ft.TextAlign.CENTER),
                                bgcolor=ft.colors.GREY_100,
                                padding=20,
                                border_radius=10,
                                width=400,
                                height=300,
                                alignment=ft.alignment.center
                            ),
                            ft.Column([
                                ft.Text("Controles de Simulación", 
                                        weight=ft.FontWeight.BOLD),
                                ft.Text("Media (μ):"),
                                self.mean_slider,
                                ft.Text("Desviación Estándar (σ):"),
                                self.std_slider,
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Interpretación Clínica:",
                                               weight=ft.FontWeight.BOLD,
                                               color=self.primary_color),
                                        self.clinical_interpretation
                                    ]),
                                    bgcolor=ft.colors.BLUE_50,
                                    padding=15,
                                    border_radius=10
                                )
                            ], expand=True)
                        ])
                    ]),
                    padding=30
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
    
    def create_concept_card(self, title, description, formula, example, color):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(description, color=ft.colors.GREY_700),
                ft.Container(
                    content=ft.Text(formula, color=color, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.colors.with_opacity(0.1, color),
                    padding=10,
                    border_radius=5
                ),
                ft.Text(example, size=12, color=ft.colors.GREY_600, italic=True)
            ]),
            border=ft.border.only(left=ft.BorderSide(4, color)),
            padding=ft.padding.only(left=20, top=10, bottom=10, right=10),
            margin=ft.margin.only(bottom=20)
        )
    
    def calculate_statistics(self, e):
        try:
            data_str = self.data_input.value
            data = [float(x.strip()) for x in data_str.split(',') if x.strip()]
            
            if not data:
                self.show_error("Por favor, ingrese datos válidos separados por comas.")
                return
            
            stats = StatCalculator.calculate_stats(data)
            interpretation = StatCalculator.get_interpretation(stats['cv'])
            
            self.stats_results.content = ft.Column([
                ft.Text("Resultados:", weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Container(
                        content=ft.Text(f"Media: {stats['mean']:.2f}"),
                        bgcolor=ft.colors.BLUE_50,
                        padding=10,
                        border_radius=5,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Text(f"Rango: {stats['range']:.2f}"),
                        bgcolor=ft.colors.GREEN_50,
                        padding=10,
                        border_radius=5,
                        expand=True
                    )
                ]),
                ft.Row([
                    ft.Container(
                        content=ft.Text(f"Varianza: {stats['variance']:.2f}"),
                        bgcolor=ft.colors.PURPLE_50,
                        padding=10,
                        border_radius=5,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Text(f"Desv. Estándar: {stats['std_dev']:.2f}"),
                        bgcolor=ft.colors.ORANGE_50,
                        padding=10,
                        border_radius=5,
                        expand=True
                    )
                ]),
                ft.Container(
                    content=ft.Text(f"Coef. Variación: {stats['cv']:.2f}%"),
                    bgcolor=ft.colors.RED_50,
                    padding=10,
                    border_radius=5
                ),
                ft.Container(
                    content=ft.Text(f"Interpretación: {interpretation}"),
                    bgcolor=ft.colors.YELLOW_50,
                    padding=10,
                    border_radius=5
                )
            ])
            self.stats_results.visible = True
            self.page.update()
            
        except ValueError:
            self.show_error("Error: Por favor, ingrese solo números separados por comas.")
    
    def update_distribution(self, e):
        mean = self.mean_slider.value
        std = self.std_slider.value
        cv = (std / mean) * 100
        
        if cv < 10:
            interpretation = "Excelente control clínico. La baja variabilidad indica estabilidad en el parámetro medido."
        elif cv < 20:
            interpretation = "Control clínico aceptable. Variabilidad dentro de rangos normales para la mayoría de parámetros."
        else:
            interpretation = "Alta variabilidad. Considerar factores que puedan estar afectando la estabilidad del parámetro."
        
        self.clinical_interpretation.value = interpretation
        self.page.update()
    
    def create_simulador_section(self):
        return ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "🔬 Simulador Clínico Avanzado",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREY_800
                        ),
                        ft.Row([
                            ft.ElevatedButton(
                                content=ft.Column([
                                    ft.Text("🫀", size=32),
                                    ft.Text("Presión Arterial", weight=ft.FontWeight.BOLD),
                                    ft.Text("Análisis de variabilidad en hipertensión", size=12)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                on_click=lambda _: self.load_scenario("presion"),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.RED_100,
                                    color=ft.colors.RED_800,
                                    padding=20
                                ),
                                width=200,
                                height=120
                            ),
                            ft.ElevatedButton(
                                content=ft.Column([
                                    ft.Text("🩸", size=32),
                                    ft.Text("Glucemia", weight=ft.FontWeight.BOLD),
                                    ft.Text("Control glucémico en diabetes", size=12)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                on_click=lambda _: self.load_scenario("glucosa"),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.BLUE_100,
                                    color=ft.colors.BLUE_800,
                                    padding=20
                                ),
                                width=200,
                                height=120
                            ),
                            ft.ElevatedButton(
                                content=ft.Column([
                                    ft.Text("💓", size=32),
                                    ft.Text("Frecuencia Cardíaca", weight=ft.FontWeight.BOLD),
                                    ft.Text("Variabilidad del ritmo cardíaco", size=12)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                on_click=lambda _: self.load_scenario("frecuencia"),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.GREEN_100,
                                    color=ft.colors.GREEN_800,
                                    padding=20
                                ),
                                width=200,
                                height=120
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("🎯", size=48, text_align=ft.TextAlign.CENTER),
                                ft.Text(
                                    "Selecciona un Escenario Clínico",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    "Elige uno de los escenarios arriba para comenzar la simulación interactiva.",
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.GREY_50,
                            padding=40,
                            border_radius=10,
                            alignment=ft.alignment.center,
                            height=200
                        )
                    ]),
                    padding=30
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
    
    def load_scenario(self, scenario_type):
        scenarios = {
            "presion": {
                "title": "🫀 Simulador de Presión Arterial",
                "description": "Analiza la variabilidad en mediciones de presión arterial y su impacto clínico.",
                "data": [142, 138, 145, 140, 148, 135, 143, 139, 146, 141],
                "unit": "mmHg",
                "normal_range": "120-140",
                "color": ft.colors.RED_500
            },
            "glucosa": {
                "title": "🩸 Simulador de Glucemia",
                "description": "Evalúa el control glucémico y la variabilidad en pacientes diabéticos.",
                "data": [95, 110, 88, 125, 102, 118, 92, 135, 98, 115],
                "unit": "mg/dL",
                "normal_range": "70-100",
                "color": ft.colors.BLUE_500
            },
            "frecuencia": {
                "title": "💓 Simulador de Frecuencia Cardíaca",
                "description": "Monitorea la variabilidad del ritmo cardíaco en diferentes condiciones.",
                "data": [72, 68, 75, 70, 78, 65, 73, 69, 76, 71],
                "unit": "lpm",
                "normal_range": "60-80",
                "color": ft.colors.GREEN_500
            }
        }
        
        scenario = scenarios.get(scenario_type)
        if not scenario:
            return
        
        stats = StatCalculator.calculate_stats(scenario["data"])
        interpretation = self.get_scenario_interpretation(scenario_type, stats['cv'], stats['mean'])
        recommendations = self.get_scenario_recommendations(scenario_type, stats['cv'])
        
        # Update the simulator content
        simulator_content = ft.Column([
            ft.Text(scenario["title"], size=20, weight=ft.FontWeight.BOLD),
            ft.Text(scenario["description"]),
            ft.Row([
                ft.Column([
                    ft.Text("📊 Datos de Simulación", weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text(f"Mediciones: {', '.join(map(str, scenario['data']))} {scenario['unit']}"),
                        bgcolor=ft.colors.GREY_50,
                        padding=15,
                        border_radius=5
                    ),
                    ft.Container(
                        content=ft.Text(f"Media: {stats['mean']:.1f} {scenario['unit']}"),
                        bgcolor=ft.colors.BLUE_50,
                        padding=10,
                        border_radius=5
                    ),
                    ft.Container(
                        content=ft.Text(f"Desviación Estándar: {stats['std_dev']:.1f} {scenario['unit']}"),
                        bgcolor=ft.colors.GREEN_50,
                        padding=10,
                        border_radius=5
                    ),
                    ft.Container(
                        content=ft.Text(f"Coeficiente de Variación: {stats['cv']:.1f}%"),
                        bgcolor=ft.colors.PURPLE_50,
                        padding=10,
                        border_radius=5
                    ),
                    ft.Container(
                        content=ft.Text(f"Rango Normal: {scenario['normal_range']} {scenario['unit']}"),
                        bgcolor=ft.colors.YELLOW_50,
                        padding=10,
                        border_radius=5
                    )
                ], expand=True),
                ft.Column([
                    ft.Text("🎯 Interpretación Clínica", weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Análisis de Variabilidad:", weight=ft.FontWeight.BOLD),
                            ft.Text(interpretation, size=12)
                        ]),
                        bgcolor=ft.colors.with_opacity(0.1, scenario["color"]),
                        border=ft.border.only(left=ft.BorderSide(4, scenario["color"])),
                        padding=15,
                        border_radius=5
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Recomendaciones:", weight=ft.FontWeight.BOLD),
                            *[ft.Text(f"• {rec}", size=12) for rec in recommendations]
                        ]),
                        bgcolor=ft.colors.GREY_50,
                        padding=15,
                        border_radius=5
                    ),
                    ft.ElevatedButton(
                        "🔄 Generar Nuevos Datos",
                        on_click=lambda _: self.generate_new_data(scenario_type),
                        style=ft.ButtonStyle(
                            bgcolor=scenario["color"],
                            color=ft.colors.WHITE
                        )
                    )
                ], expand=True)
            ])
        ])
        
        # Find and update the simulator section
        for card in self.content_area.content.controls:
            if isinstance(card, ft.Card):
                container = card.content
                if isinstance(container, ft.Container):
                    column = container.content
                    if isinstance(column, ft.Column) and len(column.controls) > 2:
                        # Replace the placeholder content
                        column.controls[2] = ft.Container(
                            content=simulator_content,
                            bgcolor=ft.colors.WHITE,
                            padding=20,
                            border_radius=10
                        )
                        break
        
        self.page.update()
    
    def get_scenario_interpretation(self, scenario_type, cv, mean):
        interpretations = {
            "presion": "Excelente control de la presión arterial con baja variabilidad." if cv < 5 else 
                      "Control aceptable, pero considerar optimización del tratamiento." if cv < 10 else
                      "Alta variabilidad que requiere evaluación del régimen terapéutico.",
            "glucosa": "Buen control glucémico con variabilidad aceptable." if cv < 15 else
                      "Control moderado, revisar adherencia al tratamiento." if cv < 25 else
                      "Control deficiente con alta variabilidad glucémica.",
            "frecuencia": "Ritmo cardíaco estable con variabilidad normal." if cv < 8 else
                         "Variabilidad moderada, monitorear condiciones del paciente." if cv < 15 else
                         "Alta variabilidad que puede indicar arritmias o estrés."
        }
        return interpretations.get(scenario_type, "Interpretación no disponible")
    
    def get_scenario_recommendations(self, scenario_type, cv):
        recommendations = {
            "presion": ["Revisar adherencia a medicación antihipertensiva", "Evaluar factores de estrés", "Considerar monitoreo ambulatorio"] if cv > 10 else
                      ["Mantener régimen actual", "Monitoreo periódico", "Reforzar hábitos saludables"],
            "glucosa": ["Revisar técnica de medición", "Evaluar adherencia a dieta y medicación", "Considerar ajuste terapéutico"] if cv > 20 else
                      ["Continuar plan actual", "Monitoreo regular", "Mantener estilo de vida"],
            "frecuencia": ["Evaluar causas de variabilidad", "Considerar Holter 24h", "Revisar medicación cardíaca"] if cv > 12 else
                         ["Monitoreo rutinario", "Mantener actividad física", "Control de factores de riesgo"]
        }
        return recommendations.get(scenario_type, ["Recomendaciones no disponibles"])
    
    def generate_new_data(self, scenario_type):
        self.show_info("🤖 Función de IA: Generando nuevos datos simulados basados en patrones clínicos reales...")
        # Simulate AI data generation
        import time
        time.sleep(1)
        self.load_scenario(scenario_type)
    
    def create_casos_section(self):
        return ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "🏥 Casos Clínicos Reales",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREY_800
                        ),
                        self.create_caso_clinico(
                            "Caso 1: Control de Hipertensión",
                            "Cardiología",
                            "Un paciente de 55 años con hipertensión arterial ha sido monitoreado durante 2 semanas. Se registraron las siguientes mediciones de presión arterial sistólica (mmHg):",
                            [142, 138, 145, 140, 148, 135, 143, 139, 146, 141, 144, 137, 149, 136, 147],
                            "La baja variabilidad (CV = 3.2%) sugiere un control estable de la presión arterial, pero los valores se mantienen elevados.",
                            "Considerar ajuste de medicación antihipertensiva para reducir la media sin aumentar la variabilidad.",
                            ft.colors.RED_100,
                            ft.colors.RED_800
                        ),
                        self.create_caso_clinico(
                            "Caso 2: Monitoreo Glucémico",
                            "Endocrinología",
                            "Paciente diabético tipo 2 con mediciones de glucosa preprandial durante 10 días (mg/dL):",
                            [95, 110, 88, 125, 102, 118, 92, 135, 98, 115, 105, 128, 85, 122, 108],
                            "Alta variabilidad glucémica (CV > 14%) indica control subóptimo del diabetes.",
                            "Revisar adherencia al tratamiento y considerar ajustes en la terapia para reducir variabilidad.",
                            ft.colors.BLUE_100,
                            ft.colors.BLUE_800
                        )
                    ]),
                    padding=30
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
    
    def create_caso_clinico(self, titulo, especialidad, contexto, datos, interpretacion, decision, bg_color, text_color):
        stats = StatCalculator.calculate_stats(datos)
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD, expand=True),
                    ft.Container(
                        content=ft.Text(especialidad, size=12),
                        bgcolor=bg_color,
                        color=text_color,
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=20
                    )
                ]),
                ft.Row([
                    ft.Column([
                        ft.Text("📋 Contexto Clínico", weight=ft.FontWeight.BOLD),
                        ft.Text(contexto),
                        ft.Container(
                            content=ft.Text(f"Datos: {', '.join(map(str, datos))}"),
                            bgcolor=ft.colors.GREY_50,
                            padding=15,
                            border_radius=5
                        ),
                        ft.Container(
                            content=ft.Text(f"Media: {stats['mean']:.1f}"),
                            bgcolor=ft.colors.BLUE_50,
                            padding=10,
                            border_radius=5
                        ),
                        ft.Container(
                            content=ft.Text(f"Desviación Estándar: {stats['std_dev']:.1f}"),
                            bgcolor=ft.colors.GREEN_50,
                            padding=10,
                            border_radius=5
                        ),
                        ft.Container(
                            content=ft.Text(f"Coeficiente de Variación: {stats['cv']:.1f}%"),
                            bgcolor=ft.colors.PURPLE_50,
                            padding=10,
                            border_radius=5
                        )
                    ], expand=True),
                    ft.Column([
                        ft.Text("🎯 Análisis Clínico", weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Interpretación:", weight=ft.FontWeight.BOLD),
                                ft.Text(interpretacion, size=12)
                            ]),
                            bgcolor=ft.colors.YELLOW_50,
                            border=ft.border.only(left=ft.BorderSide(4, ft.colors.YELLOW_400)),
                            padding=15,
                            border_radius=5
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Decisión Clínica:", weight=ft.FontWeight.BOLD),
                                ft.Text(decision, size=12)
                            ]),
                            bgcolor=ft.colors.RED_50,
                            border=ft.border.only(left=ft.BorderSide(4, ft.colors.RED_400)),
                            padding=15,
                            border_radius=5
                        ),
                        ft.ElevatedButton(
                            "Ver Análisis Detallado",
                            style=ft.ButtonStyle(
                                bgcolor=self.primary_color,
                                color=ft.colors.WHITE
                            )
                        )
                    ], expand=True)
                ])
            ]),
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10,
            padding=20,
            margin=ft.margin.only(bottom=20)
        )
    
    def create_evaluacion_section(self):
        self.quiz_manager = QuizManager()  # Reset quiz
        
        return ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "📝 Evaluación Interactiva",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREY_800
                        ),
                        self.create_quiz_interface()
                    ]),
                    padding=30
                )
            )
        ], scroll=ft.ScrollMode.AUTO)
    
    def create_quiz_interface(self):
        self.quiz_progress = ft.ProgressBar(
            value=0.2,
            bgcolor=ft.colors.GREY_200,
            color=self.primary_color
        )
        
        self.quiz_question_text = ft.Text(
            self.quiz_manager.questions[0]["question"],
            size=16,
            weight=ft.FontWeight.BOLD
        )
        
        self.quiz_options = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value=str(i), label=option)
                for i, option in enumerate(self.quiz_manager.questions[0]["options"])
            ])
        )
        
        self.quiz_feedback = ft.Container(visible=False)
        
        self.quiz_prev_btn = ft.ElevatedButton(
            "← Anterior",
            on_click=self.previous_question,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.GREY_500,
                color=ft.colors.WHITE
            )
        )
        
        self.quiz_next_btn = ft.ElevatedButton(
            "Siguiente →",
            on_click=self.next_question,
            style=ft.ButtonStyle(
                bgcolor=self.primary_color,
                color=ft.colors.WHITE
            )
        )
        
        return ft.Column([
            ft.Row([
                ft.Text(f"Pregunta {self.quiz_manager.current_question + 1} de {len(self.quiz_manager.questions)}",
                       size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(f"Puntuación: {self.quiz_manager.score}/{len(self.quiz_manager.questions)}",
                                   color=self.primary_color, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.colors.BLUE_100,
                    padding=ft.padding.symmetric(horizontal=15, vertical=8),
                    border_radius=20
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.quiz_progress,
            ft.Container(
                content=ft.Column([
                    self.quiz_question_text,
                    self.quiz_options
                ]),
                bgcolor=ft.colors.BLUE_50,
                padding=20,
                border_radius=10,
                margin=ft.margin.symmetric(vertical=20)
            ),
            self.quiz_feedback,
            ft.Row([
                self.quiz_prev_btn,
                self.quiz_next_btn
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ])
    
    def next_question(self, e):
        if not self.quiz_options.value:
            self.show_error("Por favor, selecciona una respuesta antes de continuar.")
            return
        
        selected_answer = int(self.quiz_options.value)
        question = self.quiz_manager.questions[self.quiz_manager.current_question]
        is_correct = selected_answer == question["correct"]
        
        self.quiz_manager.user_answers.append({
            "question_index": self.quiz_manager.current_question,
            "selected_answer": selected_answer,
            "correct": is_correct
        })
        
        if is_correct:
            self.quiz_manager.score += 1
        
        # Show feedback
        self.show_quiz_feedback(question, selected_answer, is_correct)
        
        # Update UI after delay
        def update_after_delay():
            if self.quiz_manager.current_question < len(self.quiz_manager.questions) - 1:
                self.quiz_manager.current_question += 1
                self.load_quiz_question()
            else:
                self.show_quiz_results()
        
        # Simulate delay for feedback
        self.page.run_task(lambda: [
            __import__('time').sleep(2),
            update_after_delay()
        ])
    
    def previous_question(self, e):
        if self.quiz_manager.current_question > 0:
            self.quiz_manager.current_question -= 1
            # Remove last answer
            if self.quiz_manager.user_answers:
                last_answer = self.quiz_manager.user_answers.pop()
                if last_answer["correct"]:
                    self.quiz_manager.score -= 1
            self.load_quiz_question()
    
    def load_quiz_question(self):
        question = self.quiz_manager.questions[self.quiz_manager.current_question]
        
        self.quiz_question_text.value = question["question"]
        self.quiz_options.content = ft.Column([
            ft.Radio(value=str(i), label=option)
            for i, option in enumerate(question["options"])
        ])
        self.quiz_options.value = None
        
        # Update progress
        progress = (self.quiz_manager.current_question + 1) / len(self.quiz_manager.questions)
        self.quiz_progress.value = progress
        
        # Update buttons
        self.quiz_prev_btn.disabled = self.quiz_manager.current_question == 0
        self.quiz_next_btn.text = "Finalizar" if self.quiz_manager.current_question == len(self.quiz_manager.questions) - 1 else "Siguiente →"
        
        # Hide feedback
        self.quiz_feedback.visible = False
        
        self.page.update()
    
    def show_quiz_feedback(self, question, selected_answer, is_correct):
        icon = "✅" if is_correct else "❌"
        title = "¡Correcto!" if is_correct else "Incorrecto"
        bg_color = ft.colors.GREEN_50 if is_correct else ft.colors.RED_50
        border_color = ft.colors.GREEN_400 if is_correct else ft.colors.RED_400
        
        feedback_content = ft.Column([
            ft.Row([
                ft.Text(icon, size=20),
                ft.Column([
                    ft.Text(title, weight=ft.FontWeight.BOLD),
                    ft.Text(question["explanation"], size=12),
                    ft.Text(f"Respuesta correcta: {question['options'][question['correct']]}", 
                           size=12, weight=ft.FontWeight.BOLD) if not is_correct else ft.Container()
                ], expand=True)
            ])
        ])
        
        self.quiz_feedback.content = ft.Container(
            content=feedback_content,
            bgcolor=bg_color,
            border=ft.border.only(left=ft.BorderSide(4, border_color)),
            padding=15,
            border_radius=5
        )
        self.quiz_feedback.visible = True
        self.page.update()
    
    def show_quiz_results(self):
        percentage = (self.quiz_manager.score / len(self.quiz_manager.questions)) * 100
        
        if percentage >= 80:
            message = "¡Excelente dominio de los conceptos!"
        elif percentage >= 60:
            message = "Buen trabajo, pero puedes mejorar."
        else:
            message = "Necesitas repasar los conceptos fundamentales."
        
        results_content = ft.Column([
            ft.Text("🎉", size=48, text_align=ft.TextAlign.CENTER),
            ft.Text("¡Evaluación Completada!", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Container(
                content=ft.Column([
                    ft.Text(f"{self.quiz_manager.score}/{len(self.quiz_manager.questions)}", 
                           size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text(message, size=16, color=ft.colors.WHITE)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                gradient=ft.LinearGradient([ft.colors.GREEN_400, ft.colors.BLUE_500]),
                padding=30,
                border_radius=10,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Análisis Detallado:", weight=ft.FontWeight.BOLD),
                    *[ft.Container(
                        content=ft.Row([
                            ft.Text(f"Pregunta {i+1}", weight=ft.FontWeight.BOLD),
                            ft.Text("✅ Correcta" if answer["correct"] else "❌ Incorrecta",
                                   color=ft.colors.GREEN_600 if answer["correct"] else ft.colors.RED_600)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=ft.colors.GREEN_50 if answer["correct"] else ft.colors.RED_50,
                        padding=10,
                        border_radius=5,
                        margin=ft.margin.only(bottom=5)
                    ) for i, answer in enumerate(self.quiz_manager.user_answers)],
                    ft.Container(
                        content=ft.Text(f"Porcentaje de aciertos: {percentage:.1f}%", 
                                       color=self.primary_color, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.colors.BLUE_50,
                        padding=15,
                        border_radius=5
                    )
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=20,
                border_radius=10
            ),
            ft.ElevatedButton(
                "Reiniciar Evaluación",
                on_click=self.restart_quiz,
                style=ft.ButtonStyle(
                    bgcolor=self.primary_color,
                    color=ft.colors.WHITE
                )
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Replace quiz interface with results
        for card in self.content_area.content.controls:
            if isinstance(card, ft.Card):
                container = card.content
                if isinstance(container, ft.Container):
                    column = container.content
                    if isinstance(column, ft.Column) and len(column.controls) > 1:
                        column.controls[1] = results_content
                        break
        
        self.page.update()
    
    def restart_quiz(self, e):
        self.quiz_manager = QuizManager()
        self.show_section("evaluacion")
    
    def show_error(self, message):
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=self.error_color
            )
        )
    
    def show_info(self, message):
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=self.primary_color
            )
        )

def main(page: ft.Page):
    app = OVAApp(page)

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
