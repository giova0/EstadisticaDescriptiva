
import flet as ft
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import pandas as pd
import io
import base64
from datetime import datetime
import json

class OVAInequidadesSalud:
    def __init__(self):
        self.current_section = "intro"
        self.completed_steps = 0
        self.quiz_score = 0
        self.current_scenario = None
        self.section_progress = {
            "intro": False,
            "objectives": False,
            "theory": False,
            "practice": False,
            "evaluation": False,
            "resources": False
        }
        self.sections = ["intro", "objectives", "theory", "practice", "evaluation", "resources"]
        self.checklist_items = [False] * 5
        self.quiz_answers = {}
        
        # Datos de escenarios
        self.scenarios = {
            "maternal": {
                "title": "Mortalidad Materna por Departamentos",
                "data": [
                    {"departamento": "Chocó", "tasa": 155.2, "poblacion": 534000, "nivel": "Bajo"},
                    {"departamento": "La Guajira", "tasa": 142.8, "poblacion": 957000, "nivel": "Bajo"},
                    {"departamento": "Bogotá", "tasa": 28.5, "poblacion": 7800000, "nivel": "Alto"},
                    {"departamento": "Antioquia", "tasa": 45.3, "poblacion": 6600000, "nivel": "Medio"},
                    {"departamento": "Valle", "tasa": 38.7, "poblacion": 4600000, "nivel": "Alto"}
                ]
            },
            "diabetes": {
                "title": "Prevalencia de Diabetes por Nivel Socioeconómico",
                "data": [
                    {"estrato": "Estrato 1", "prevalencia": 12.8, "poblacion": 2500000, "nivel": "Bajo"},
                    {"estrato": "Estrato 2", "prevalencia": 10.5, "poblacion": 3200000, "nivel": "Bajo"},
                    {"estrato": "Estrato 3", "prevalencia": 8.2, "poblacion": 2800000, "nivel": "Medio"},
                    {"estrato": "Estrato 4", "prevalencia": 6.1, "poblacion": 1500000, "nivel": "Alto"},
                    {"estrato": "Estrato 5-6", "prevalencia": 4.3, "poblacion": 800000, "nivel": "Alto"}
                ]
            },
            "vaccination": {
                "title": "Cobertura Vacunal por Área",
                "data": [
                    {"area": "Rural Disperso", "cobertura": 68.5, "poblacion": 1200000, "tipo": "Rural"},
                    {"area": "Rural Nucleado", "cobertura": 78.2, "poblacion": 2100000, "tipo": "Rural"},
                    {"area": "Urbano Pequeño", "cobertura": 85.7, "poblacion": 3500000, "tipo": "Urbano"},
                    {"area": "Urbano Grande", "cobertura": 92.3, "poblacion": 15200000, "tipo": "Urbano"}
                ]
            }
        }

    def main(self, page: ft.Page):
        page.title = "OVA: Visualización de Inequidades en Salud"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.scroll = ft.ScrollMode.AUTO
        page.window_width = 1200
        page.window_height = 800
        
        # Variables de la página
        self.page = page
        
        # Crear componentes principales
        self.create_header()
        self.create_progress_bar()
        self.create_navigation()
        self.create_sections()
        
        # Layout principal
        main_content = ft.Column([
            self.header,
            self.progress_container,
            self.navigation,
            self.content_container
        ], spacing=0)
        
        page.add(main_content)
        self.show_section("intro")

    def create_header(self):
        self.header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.TRENDING_UP, size=30, color=ft.Colors.WHITE),
                        ft.Text("Visualización de Inequidades en Salud", 
                               size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                    ]),
                    ft.Text("Objeto Virtual de Aprendizaje - Modelo C(H)ANGE + IA", 
                           size=14, color=ft.Colors.WHITE70)
                ], expand=True),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Duración estimada", size=12, color=ft.Colors.WHITE70),
                        ft.Text("2-4 horas", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.WHITE24,
                    padding=10,
                    border_radius=8
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.BLUE_700,
            padding=20,
            height=100
        )

    def create_progress_bar(self):
        self.progress_text = ft.Text("0% completado", size=12, color=ft.Colors.GREY_600)
        self.progress_bar = ft.ProgressBar(value=0, color=ft.Colors.BLUE_600, height=8)
        
        self.progress_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Progreso del OVA", size=12, color=ft.Colors.GREY_600),
                    self.progress_text
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar
            ], spacing=5),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor=ft.Colors.WHITE
        )

    def create_navigation(self):
        nav_buttons = []
        nav_items = [
            ("intro", "Introducción", ft.Icons.PLAY_CIRCLE),
            ("objectives", "Objetivos", ft.Icons.TRACK_CHANGES),
            ("theory", "Microlección", ft.Icons.BOOK),
            ("practice", "Práctica", ft.Icons.COMPUTER),
            ("evaluation", "Evaluación", ft.Icons.ASSIGNMENT_TURNED_IN),
            ("resources", "Recursos", ft.Icons.DOWNLOAD)
        ]
        
        for section_id, title, icon in nav_items:
            btn = ft.ElevatedButton(
                text=title,
                icon=icon,
                on_click=lambda e, s=section_id: self.show_section(s),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_100 if section_id == "intro" else ft.Colors.GREY_100,
                    color=ft.Colors.BLUE_700 if section_id == "intro" else ft.Colors.GREY_700
                )
            )
            nav_buttons.append(btn)
        
        self.nav_buttons = nav_buttons
        self.navigation = ft.Container(
            content=ft.Row(nav_buttons, scroll=ft.ScrollMode.AUTO),
            padding=10,
            bgcolor=ft.Colors.WHITE
        )

    def create_sections(self):
        self.content_container = ft.Container(
            content=ft.Column([]),
            padding=20,
            bgcolor=ft.Colors.GREY_50,
            expand=True
        )

    def show_section(self, section_id):
        self.current_section = section_id
        self.section_progress[section_id] = True
        self.update_progress()
        self.update_navigation_style(section_id)
        
        # Limpiar contenido actual
        self.content_container.content.controls.clear()
        
        # Mostrar sección correspondiente
        if section_id == "intro":
            self.show_intro_section()
        elif section_id == "objectives":
            self.show_objectives_section()
        elif section_id == "theory":
            self.show_theory_section()
        elif section_id == "practice":
            self.show_practice_section()
        elif section_id == "evaluation":
            self.show_evaluation_section()
        elif section_id == "resources":
            self.show_resources_section()
        
        self.page.update()

    def update_progress(self):
        completed = sum(1 for v in self.section_progress.values() if v)
        percentage = completed / len(self.sections)
        self.progress_bar.value = percentage
        self.progress_text.value = f"{int(percentage * 100)}% completado"

    def update_navigation_style(self, active_section):
        for i, (section_id, _, _) in enumerate([
            ("intro", "Introducción", ft.Icons.PLAY_CIRCLE),
            ("objectives", "Objetivos", ft.Icons.TRACK_CHANGES),
            ("theory", "Microlección", ft.Icons.BOOK),
            ("practice", "Práctica", ft.Icons.COMPUTER),
            ("evaluation", "Evaluación", ft.Icons.ASSIGNMENT_TURNED_IN),
            ("resources", "Recursos", ft.Icons.DOWNLOAD)
        ]):
            if section_id == active_section:
                self.nav_buttons[i].style.bgcolor = ft.Colors.BLUE_100
                self.nav_buttons[i].style.color = ft.Colors.BLUE_700
            else:
                self.nav_buttons[i].style.bgcolor = ft.Colors.GREY_100
                self.nav_buttons[i].style.color = ft.Colors.GREY_700

    def show_intro_section(self):
        # Selector de área de interés
        self.interest_dropdown = ft.Dropdown(
            label="Selecciona tu área de interés",
            options=[
                ft.dropdown.Option("maternal", "Salud Materna"),
                ft.dropdown.Option("chronic", "Enfermedades Crónicas"),
                ft.dropdown.Option("mental", "Salud Mental"),
                ft.dropdown.Option("infectious", "Enfermedades Infecciosas"),
                ft.dropdown.Option("nutrition", "Nutrición")
            ],
            on_change=self.update_ai_recommendation
        )
        
        self.ai_recommendation = ft.Container(
            content=ft.Column([
                ft.Text("💡 Recomendación IA:", weight=ft.FontWeight.BOLD, size=12),
                ft.Text("Para maximizar tu aprendizaje, te sugiero comenzar identificando un problema de inequidad en salud de tu región.", size=12)
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=15,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        
        content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO, size=30, color=ft.Colors.BLUE_600),
                    ft.Text("Introducción", size=28, weight=ft.FontWeight.BOLD)
                ]),
                ft.Row([
                    ft.Column([
                        ft.Text("¿Qué son las inequidades en salud?", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Las inequidades en salud son diferencias sistemáticas, evitables e injustas en los resultados de salud entre diferentes grupos poblacionales. Estas diferencias están determinadas por factores sociales, económicos, geográficos y demográficos.",
                            size=14
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.AMBER_600),
                                    ft.Text("Modelo C(H)ANGE en acción", weight=ft.FontWeight.BOLD)
                                ]),
                                ft.Text(
                                    "Integraremos Combinatoria (patrones), Álgebra (relaciones), Números (indicadores), Geometría (mapas) y Estadística (análisis) para comprender las inequidades.",
                                    size=12
                                )
                            ]),
                            bgcolor=ft.Colors.AMBER_50,
                            padding=15,
                            border_radius=8,
                            border=ft.border.all(2, ft.Colors.AMBER_400)
                        )
                    ], expand=True),
                    ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.SMART_TOY, color=ft.Colors.PURPLE_600),
                            ft.Text("Asistente IA Integrado", weight=ft.FontWeight.BOLD)
                        ]),
                        self.ai_recommendation,
                        self.interest_dropdown
                    ], expand=True)
                ], spacing=20),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Continuar a Objetivos",
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda e: self.show_section("objectives"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
                )
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        
        self.content_container.content.controls.append(content)

    def update_ai_recommendation(self, e):
        recommendations = {
            "maternal": "Para salud materna, enfócate en inequidades por nivel socioeconómico y acceso geográfico a servicios especializados.",
            "chronic": "En enfermedades crónicas, analiza diferencias por edad, sexo y determinantes sociales como educación e ingresos.",
            "mental": "Para salud mental, considera inequidades por género, edad y estigma social en diferentes poblaciones.",
            "infectious": "En enfermedades infecciosas, examina patrones por densidad poblacional, condiciones de vivienda y acceso a servicios.",
            "nutrition": "Para nutrición, analiza inequidades por nivel socioeconómico, área geográfica y disponibilidad de alimentos."
        }
        
        if e.control.value and e.control.value in recommendations:
            self.ai_recommendation.content.controls[1].value = recommendations[e.control.value]
            self.page.update()

    def show_objectives_section(self):
        change_components = [
            ("C - Combinatoria", "Identificar patrones de inequidad en diferentes combinaciones de variables demográficas", ft.Colors.RED_400),
            ("Á - Álgebra", "Establecer relaciones matemáticas entre determinantes sociales y resultados de salud", ft.Colors.BLUE_400),
            ("N - Números", "Calcular e interpretar indicadores de inequidad (razones, diferencias, índices)", ft.Colors.GREEN_400),
            ("G - Geometría", "Utilizar representaciones espaciales y mapas para mostrar distribuciones geográficas", ft.Colors.PURPLE_400),
            ("E - Estadística", "Aplicar métodos descriptivos para cuantificar y comunicar inequidades", ft.Colors.ORANGE_400)
        ]
        
        change_cards = []
        for title, description, color in change_components:
            card = ft.Container(
                content=ft.Column([
                    ft.Text(title, weight=ft.FontWeight.BOLD, color=color),
                    ft.Text(description, size=12)
                ]),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=8,
                border=ft.border.all(2, color)
            )
            change_cards.append(card)
        
        content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TRACK_CHANGES, size=30, color=ft.Colors.GREEN_600),
                    ft.Text("Objetivos de Aprendizaje", size=28, weight=ft.FontWeight.BOLD)
                ]),
                ft.Row([
                    ft.Column([
                        ft.Text("Objetivo Principal", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Text(
                                "Describir brechas en salud por sexo, edad, territorio y determinantes sociales de la salud (SDOH) mediante visualizaciones efectivas y análisis estadístico descriptivo.",
                                size=14, weight=ft.FontWeight.W_500
                            ),
                            bgcolor=ft.Colors.BLUE_50,
                            padding=20,
                            border_radius=8
                        ),
                        ft.Text("Al finalizar podrás:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Column([
                            ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500), 
                                   ft.Text("Identificar y clasificar diferentes tipos de inequidades en salud", size=12)]),
                            ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500), 
                                   ft.Text("Calcular razones de tasas y diferencias absolutas entre grupos", size=12)]),
                            ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500), 
                                   ft.Text("Crear mapas y heatmaps para visualizar inequidades territoriales", size=12)]),
                            ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500), 
                                   ft.Text("Interpretar visualizaciones desde una perspectiva de salud pública", size=12)])
                        ])
                    ], expand=True),
                    ft.Column([
                        ft.Text("Competencias C(H)ANGE", size=18, weight=ft.FontWeight.BOLD),
                        ft.Column(change_cards, spacing=10)
                    ], expand=True)
                ], spacing=20),
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Iniciar Microlección",
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda e: self.show_section("theory"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
                )
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        
        self.content_container.content.controls.append(content)

    def show_theory_section(self):
        # Campos para la calculadora
        self.rate_privileged = ft.TextField(label="Tasa Grupo Privilegiado (por 100,000)", 
                                          hint_text="Ej: 50", on_change=self.calculate_inequality)
        self.pop_privileged = ft.TextField(label="Población Grupo Privilegiado", 
                                         hint_text="Ej: 100000", on_change=self.calculate_inequality)
        self.rate_disadvantaged = ft.TextField(label="Tasa Grupo Desfavorecido (por 100,000)", 
                                             hint_text="Ej: 120", on_change=self.calculate_inequality)
        self.pop_disadvantaged = ft.TextField(label="Población Grupo Desfavorecido", 
                                            hint_text="Ej: 80000", on_change=self.calculate_inequality)
        
        self.inequality_results = ft.Container(visible=False)
        
        # Crear gráfico de tendencias
        trend_chart = self.create_trend_chart()
        
        content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.BOOK, size=30, color=ft.Colors.PURPLE_600),
                    ft.Text("Microlección Interactiva", size=28, weight=ft.FontWeight.BOLD)
                ]),
                
                ft.Text("1. Conceptos Fundamentales", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.create_concept_card("Equidad vs Igualdad", "Diferencias conceptuales clave", ft.Icons.BALANCE, ft.Colors.BLUE_600),
                    self.create_concept_card("Determinantes Sociales", "Factores que influyen en la salud", ft.Icons.NETWORK_NODE, ft.Colors.GREEN_600),
                    self.create_concept_card("Indicadores de Inequidad", "Métricas para medir brechas", ft.Icons.BAR_CHART, ft.Colors.PURPLE_600)
                ], spacing=10),
                
                ft.Text("2. Tipos de Visualización para Inequidades", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Gráficos de Tendencias", weight=ft.FontWeight.BOLD),
                            trend_chart,
                            ft.Text("Evolución temporal de inequidades por grupos", size=12)
                        ]),
                        bgcolor=ft.Colors.WHITE,
                        padding=15,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Mapas de Calor", weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Text("Simulación de Mapa de Inequidades", 
                                               text_align=ft.TextAlign.CENTER),
                                height=200,
                                bgcolor=ft.Colors.GRADIENT,
                                border_radius=8
                            ),
                            ft.Text("Distribución geográfica de indicadores de salud", size=12)
                        ]),
                        bgcolor=ft.Colors.WHITE,
                        padding=15,
                        border_radius=8,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        expand=True
                    )
                ], spacing=10),
                
                ft.Text("3. Calculadora de Indicadores de Inequidad", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Column([
                                ft.Text("Datos del Grupo Privilegiado", weight=ft.FontWeight.BOLD),
                                self.rate_privileged,
                                self.pop_privileged
                            ], expand=True),
                            ft.Column([
                                ft.Text("Datos del Grupo Desfavorecido", weight=ft.FontWeight.BOLD),
                                self.rate_disadvantaged,
                                self.pop_disadvantaged
                            ], expand=True)
                        ], spacing=20),
                        self.inequality_results
                    ]),
                    bgcolor=ft.Colors.GREY_50,
                    padding=20,
                    border_radius=8
                ),
                
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Ir a Práctica Guiada",
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda e: self.show_section("practice"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE)
                )
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        
        self.content_container.content.controls.append(content)

    def create_concept_card(self, title, description, icon, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=40, color=color),
                ft.Text(title, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(description, size=12, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=8,
            border=ft.border.all(1, color),
            expand=True,
            on_click=lambda e, t=title: self.show_concept_detail(t)
        )

    def show_concept_detail(self, concept_title):
        # Aquí se podría mostrar un diálogo con más detalles del concepto
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Mostrando detalles de: {concept_title}")))

    def create_trend_chart(self):
        # Crear gráfico simple con matplotlib
        fig, ax = plt.subplots(figsize=(6, 4))
        years = ['2018', '2019', '2020', '2021', '2022']
        privileged = [45, 42, 40, 38, 35]
        disadvantaged = [95, 92, 88, 85, 82]
        
        ax.plot(years, privileged, label='Grupo Privilegiado', color='green', marker='o')
        ax.plot(years, disadvantaged, label='Grupo Desfavorecido', color='red', marker='o')
        ax.set_ylabel('Tasa por 100,000')
        ax.set_title('Tendencias de Inequidad')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Convertir a imagen
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return ft.Image(src_base64=base64.b64encode(buf.getvalue()).decode(), height=200)

    def calculate_inequality(self, e):
        try:
            rate_priv = float(self.rate_privileged.value) if self.rate_privileged.value else 0
            rate_disadv = float(self.rate_disadvantaged.value) if self.rate_disadvantaged.value else 0
            pop_priv = float(self.pop_privileged.value) if self.pop_privileged.value else 0
            pop_disadv = float(self.pop_disadvantaged.value) if self.pop_disadvantaged.value else 0
            
            if all([rate_priv, rate_disadv, pop_priv, pop_disadv]):
                rate_ratio = rate_disadv / rate_priv
                rate_difference = rate_disadv - rate_priv
                total_rate = ((rate_priv * pop_priv) + (rate_disadv * pop_disadv)) / (pop_priv + pop_disadv)
                attributable_fraction = (rate_difference / total_rate) * 100
                
                self.inequality_results.content = ft.Column([
                    ft.Text("Resultados del Análisis", weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Razón de Tasas", size=12),
                                ft.Text(f"{rate_ratio:.2f}", size=18, weight=ft.FontWeight.BOLD)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.BLUE_50,
                            padding=15,
                            border_radius=8,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Diferencia de Tasas", size=12),
                                ft.Text(f"{rate_difference:.1f}", size=18, weight=ft.FontWeight.BOLD)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.GREEN_50,
                            padding=15,
                            border_radius=8,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Fracción Atribuible", size=12),
                                ft.Text(f"{attributable_fraction:.1f}%", size=18, weight=ft.FontWeight.BOLD)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.PURPLE_50,
                            padding=15,
                            border_radius=8,
                            expand=True
                        )
                    ], spacing=10),
                    ft.Container(
                        content=ft.Text(f"Interpretación: El grupo desfavorecido tiene {rate_ratio:.1f} veces más riesgo que el grupo privilegiado.", 
                                       size=12),
                        bgcolor=ft.Colors.YELLOW_50,
                        padding=10,
                        border_radius=8
                    )
                ])
                self.inequality_results.visible = True
                self.page.update()
        except:
            pass

    def show_practice_section(self):
        self.scenario_title = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
        self.data_table_container = ft.Container(visible=False)
        self.ai_analysis_container = ft.Container(visible=False)
        self.visualization_container = ft.Container(visible=False)
        self.guided_steps_container = ft.Container(visible=False)
        
        content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.COMPUTER, size=30, color=ft.Colors.ORANGE_600),
                    ft.Text("Práctica Guiada con Dataset", size=28, weight=ft.FontWeight.BOLD)
                ]),
                
                ft.Text("Selecciona un Escenario de Práctica", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.create_scenario_button("maternal", "Mortalidad Materna", "Por departamentos en Colombia", ft.Icons.CHILD_CARE, ft.Colors.PINK_600),
                    self.create_scenario_button("diabetes", "Diabetes Tipo 2", "Por nivel socioeconómico", ft.Icons.FAVORITE, ft.Colors.RED_600),
                    self.create_scenario_button("vaccination", "Cobertura Vacunal", "Por área urbana/rural", ft.Icons.VACCINES, ft.Colors.GREEN_600)
                ], spacing=10),
                
                ft.Column([
                    ft.Text("Dataset: ", size=16, weight=ft.FontWeight.BOLD),
                    self.scenario_title,
                    self.data_table_container,
                    self.ai_analysis_container,
                    self.visualization_container,
                    self.guided_steps_container
                ]),
                
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Ir a Evaluación",
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda e: self.show_section("evaluation"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE)
                )
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        
        self.content_container.content.controls.append(content)

    def create_scenario_button(self, scenario_id, title, description, icon, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=40, color=color),
                ft.Text(title, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(description, size=12, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=8,
            border=ft.border.all(2, ft.Colors.GREY_300),
            expand=True,
            on_click=lambda e, s=scenario_id: self.load_scenario(s)
        )

    def load_scenario(self, scenario_type):
        self.current_scenario = scenario_type
        scenario = self.scenarios[scenario_type]
        self.scenario_title.value = scenario["title"]
        
        # Crear tabla de datos
        headers = list(scenario["data"][0].keys())
        rows = []
        for item in scenario["data"]:
            row = ft.DataRow(cells=[ft.DataCell(ft.Text(str(item[header]))) for header in headers])
            rows.append(row)
        
        data_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(header.capitalize())) for header in headers],
            rows=rows
        )
        
        self.data_table_container.content = ft.Column([
            ft.Row([
                ft.Text("Vista de Datos", weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.ElevatedButton("Análisis IA", icon=ft.Icons.SMART_TOY, on_click=self.analyze_data),
                    ft.ElevatedButton("Visualizar", icon=ft.Icons.BAR_CHART, on_click=self.create_visualization)
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(content=data_table, bgcolor=ft.Colors.GREY_50, padding=10, border_radius=8)
        ])
        self.data_table_container.visible = True
        
        # Crear pasos guiados
        self.create_guided_steps()
        
        self.page.update()

    def analyze_data(self, e):
        insights = {
            "maternal": [
                "Se observa una inequidad significativa en mortalidad materna entre departamentos",
                "Chocó presenta una tasa 5.4 veces mayor que Bogotá",
                "Los departamentos con menor desarrollo socioeconómico muestran las tasas más altas"
            ],
            "diabetes": [
                "Existe un gradiente socioeconómico claro en la prevalencia de diabetes",
                "Los estratos más bajos tienen 3 veces más prevalencia que los estratos altos",
                "Se evidencia la influencia de determinantes sociales en enfermedades crónicas"
            ],
            "vaccination": [
                "Las áreas rurales presentan menor cobertura vacunal",
                "La brecha entre rural disperso y urbano grande es de 23.8 puntos porcentuales",
                "Se observa un patrón de inequidad por acceso geográfico a servicios"
            ]
        }
        
        insight_list = insights.get(self.current_scenario, [])
        insight_controls = []
        for insight in insight_list:
            insight_controls.append(
                ft.Row([
                    ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.YELLOW_600),
                    ft.Text(insight, size=12, expand=True)
                ])
            )
        
        self.ai_analysis_container.content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SMART_TOY, color=ft.Colors.BLUE_600),
                    ft.Text("Análisis Automático IA", weight=ft.FontWeight.BOLD)
                ]),
                ft.Column(insight_controls)
            ]),
            bgcolor=ft.Colors.BLUE_50,
            padding=15,
            border_radius=8
        )
        self.ai_analysis_container.visible = True
        self.page.update()

    def create_visualization(self, e):
        if not self.current_scenario:
            return
        
        # Crear gráficos basados en el escenario
        if self.current_scenario == "maternal":
            main_chart = self.create_maternal_chart()
            inequality_chart = self.create_inequality_chart()
        else:
            main_chart = ft.Text("Gráfico no disponible en esta demo")
            inequality_chart = ft.Text("Análisis no disponible en esta demo")
        
        self.visualization_container.content = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Gráfico Principal", weight=ft.FontWeight.BOLD),
                    main_chart
                ]),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=8,
                border=ft.border.all(1, ft.Colors.GREY_300),
                expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Análisis de Inequidad", weight=ft.FontWeight.BOLD),
                    inequality_chart
                ]),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=8,
                border=ft.border.all(1, ft.Colors.GREY_300),
                expand=True
            )
        ], spacing=10)
        self.visualization_container.visible = True
        self.page.update()

    def create_maternal_chart(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        departments = ['Chocó', 'La Guajira', 'Antioquia', 'Valle', 'Bogotá']
        rates = [155.2, 142.8, 45.3, 38.7, 28.5]
        colors = ['red', 'orange', 'yellow', 'lightgreen', 'cyan']
        
        bars = ax.bar(departments, rates, color=colors)
        ax.set_ylabel('Tasa de Mortalidad Materna')
        ax.set_title('Mortalidad Materna por Departamento')
        ax.tick_params(axis='x', rotation=45)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return ft.Image(src_base64=base64.b64encode(buf.getvalue()).decode(), height=200)

    def create_inequality_chart(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        departments = ['Bogotá', 'Valle', 'Antioquia', 'La Guajira', 'Chocó']
        ratios = [1.0, 1.36, 1.59, 5.01, 5.44]
        
        ax.plot(departments, ratios, marker='o', color='red', linewidth=2, markersize=8)
        ax.fill_between(departments, ratios, alpha=0.3, color='red')
        ax.set_ylabel('Razón de Tasas vs Bogotá')
        ax.set_title('Inequidad Relativa')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return ft.Image(src_base64=base64.b64encode(buf.getvalue()).decode(), height=200)

    def create_guided_steps(self):
        steps = [
            ("Exploración de Datos", "Examina las variables y identifica patrones iniciales"),
            ("Cálculo de Indicadores", "Calcula razones de tasas y diferencias absolutas"),
            ("Creación de Visualizaciones", "Diseña gráficos efectivos para mostrar inequidades"),
            ("Interpretación y Recomendaciones", "Analiza resultados y propone intervenciones")
        ]
        
        step_controls = []
        for i, (title, description) in enumerate(steps, 1):
            step_control = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(f"Paso {i}: {title}", weight=ft.FontWeight.BOLD),
                        ft.Text(description, size=12)
                    ], expand=True),
                    ft.ElevatedButton("Completar", on_click=lambda e, step=i: self.complete_step(step))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=ft.Colors.GREY_50,
                padding=15,
                border_radius=8,
                border=ft.border.all(2, ft.Colors.GREY_300)
            )
            step_controls.append(step_control)
        
        self.guided_steps_container.content = ft.Column([
            ft.Text("Pasos Guiados", size=16, weight=ft.FontWeight.BOLD),
            ft.Column(step_controls, spacing=10)
        ])
        self.guided_steps_container.visible = True

    def complete_step(self, step_number):
        self.completed_steps += 1
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Paso {step_number} completado!")))
        
        if self.completed_steps == 4:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("¡Excelente! Has completado todos los pasos.")))

    def show_evaluation_section(self):
        # Preguntas del quiz
        questions = [
            {
                "question": "¿Cuál es la principal diferencia entre equidad e igualdad en salud?",
                "options": [
                    "Ambos conceptos son idénticos",
                    "La equidad busca dar lo mismo a todos, la igualdad considera las necesidades específicas",
                    "La igualdad busca dar lo mismo a todos, la equidad considera las necesidades específicas",
                    "No hay diferencia práctica entre ambos conceptos"
                ],
                "correct": 2
            },
            {
                "question": "Si el grupo A tiene una tasa de mortalidad de 50 por 100,000 y el grupo B tiene 100 por 100,000, ¿cuál es la razón de tasas?",
                "options": ["0.5", "2.0", "50", "150"],
                "correct": 1
            },
            {
                "question": "¿Cuál es el tipo de gráfico más apropiado para mostrar inequidades geográficas en salud?",
                "options": ["Gráfico de barras", "Gráfico circular", "Mapa de calor (heatmap)", "Diagrama de dispersión"],
                "correct": 2
            },
            {
                "question": "Una razón de tasas de 2.5 entre grupos desfavorecidos y privilegiados indica que:",
                "options": [
                    "El grupo desfavorecido tiene 2.5 veces menos riesgo",
                    "El grupo desfavorecido tiene 2.5 veces más riesgo",
                    "No hay diferencia significativa entre grupos",
                    "Los datos son insuficientes para interpretar"
                ],
                "correct": 1
            }
        ]
        
        self.quiz_controls = []
        for i, q in enumerate(questions):
            question_control = ft.Container(
                content=ft.Column([
                    ft.Text(f"Pregunta {i+1}: {q['question']}", weight=ft.FontWeight.BOLD),
                    ft.RadioGroup(
                        content=ft.Column([
                            ft.Radio(value=j, label=option) for j, option in enumerate(q['options'])
                        ]),
                        on_change=lambda e, qi=i: self.update_quiz_answer(qi, e.control.value)
                    )
                ]),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=8,
                border=ft.border.all(1, ft.Colors.GREY_300)
            )
            self.quiz_controls.append(question_control)
        
        self.quiz_results_container = ft.Container(visible=False)
        
        content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ASSIGNMENT_TURNED_IN, size=30, color=ft.Colors.RED_600),
                    ft.Text("Evaluación Automatizada", size=28, weight=ft.FontWeight.BOLD)
                ]),
                
                ft.Container(
                    content=ft.Text("Responde las siguientes preguntas basadas en lo aprendido. Recibirás retroalimentación inmediata.", 
                                   size=14),
                    bgcolor=ft.Colors.BLUE_50,
                    padding=15,
                    border_radius=8
                ),
                
                ft.Column(self.quiz_controls, spacing=15),
                
                ft.ElevatedButton(
                    "Enviar Respuestas",
                    icon=ft.Icons.CHECK,
                    on_click=self.submit_quiz,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE)
                ),
                
                self.quiz_results_container,
                
                ft.Container(height=20),
                ft.ElevatedButton(
                    "Ver Recursos",
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda e: self.show_section("resources"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_600, color=ft.Colors.WHITE)
                )
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        
        self.content_container.content.controls.append(content)

    def update_quiz_answer(self, question_index, answer):
        self.quiz_answers[question_index] = int(answer) if answer is not None else None

    def submit_quiz(self, e):
        correct_answers = [2, 1, 2, 1]  # Respuestas correctas
        score = 0
        results = []
        
        for i, correct in enumerate(correct_answers):
            user_answer = self.quiz_answers.get(i)
            is_correct = user_answer == correct
            if is_correct:
                score += 1
            results.append(is_correct)
        
        self.quiz_score = score
        percentage = (score / len(correct_answers)) * 100
        
        result_controls = []
        for i, is_correct in enumerate(results):
            result_controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE if is_correct else ft.Icons.CANCEL, 
                               color=ft.Colors.GREEN_600 if is_correct else ft.Colors.RED_600),
                        ft.Text(f"Pregunta {i+1}: {'Correcta' if is_correct else 'Incorrecta'}", 
                               weight=ft.FontWeight.BOLD)
                    ]),
                    bgcolor=ft.Colors.GREEN_50 if is_correct else ft.Colors.RED_50,
                    padding=10,
                    border_radius=8,
                    border=ft.border.all(1, ft.Colors.GREEN_200 if is_correct else ft.Colors.RED_200)
                )
            )
        
        self.quiz_results_container.content = ft.Container(
            content=ft.Column([
                ft.Text("Resultados de la Evaluación", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Column([
                        ft.Text(f"{score}/{len(correct_answers)} ({percentage:.0f}%)", 
                               size=24, weight=ft.FontWeight.BOLD, 
                               color=ft.Colors.GREEN_600 if percentage >= 70 else ft.Colors.RED_600),
                        ft.Text("¡Excelente trabajo!" if percentage >= 70 else "Necesitas repasar algunos conceptos")
                    ], expand=True),
                    ft.Text("🎉" if percentage >= 70 else "📚", size=40)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Column(result_controls, spacing=5)
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        self.quiz_results_container.visible = True
        self.page.update()

    def show_resources_section(self):
        # Checklist items
        checklist_controls = []
        checklist_items = [
            "Identifiqué correctamente los tipos de inequidad",
            "Calculé razones de tasas y diferencias absolutas",
            "Creé visualizaciones apropiadas",
            "Interpreté resultados en contexto clínico",
            "Propuse recomendaciones de salud pública"
        ]
        
        for i, item in enumerate(checklist_items):
            checkbox = ft.Checkbox(
                label=item,
                value=self.checklist_items[i],
                on_change=lambda e, idx=i: self.update_checklist(idx, e.control.value)
            )
            checklist_controls.append(checkbox)
        
        self.checklist_progress = ft.Text("Progreso: 0/5 completado", size=12)
        
        # Recursos descargables
        resources = [
            ("Guía de Indicadores de Inequidad", ft.Icons.PICTURE_AS_PDF, ft.Colors.RED_600),
            ("Plantilla de Análisis de Inequidades", ft.Icons.TABLE_CHART, ft.Colors.GREEN_600),
            ("Scripts R para Visualización", ft.Icons.CODE, ft.Colors.PURPLE_600),
            ("Datasets de Práctica", ft.Icons.DATABASE, ft.Colors.BLUE_600)
        ]
        
        resource_controls = []
        for title, icon, color in resources:
            resource_control = ft.Container(
                content=ft.Row([
                    ft.Row([
                        ft.Icon(icon, color=color),
                        ft.Text(title)
                    ], expand=True),
                    ft.IconButton(ft.Icons.DOWNLOAD, on_click=lambda e, t=title: self.download_resource(t))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=ft.Colors.GREY_50,
                padding=10,
                border_radius=8
            )
            resource_controls.append(resource_control)
        
        content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.DOWNLOAD, size=30, color=ft.Colors.INDIGO_600),
                    ft.Text("Recursos y Transferencia", size=28, weight=ft.FontWeight.BOLD)
                ]),
                
                ft.Row([
                    ft.Column([
                        ft.Text("Materiales Descargables", size=18, weight=ft.FontWeight.BOLD),
                        ft.Column(resource_controls, spacing=10)
                    ], expand=True),
                    ft.Column([
                        ft.Text("Checklist de Verificación", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Column([
                                ft.Column(checklist_controls),
                                self.checklist_progress
                            ]),
                            bgcolor=ft.Colors.GREEN_50,
                            padding=15,
                            border_radius=8
                        )
                    ], expand=True)
                ], spacing=20),
                
                ft.Text("Actividad de Transferencia", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Miniinforme: Análisis de Inequidades en tu Contexto", weight=ft.FontWeight.BOLD),
                        ft.Text("Aplica lo aprendido creando un breve informe sobre inequidades en salud en tu región o área de interés."),
                        ft.TextField(label="1. Problema de salud identificado:", multiline=True, min_lines=2),
                        ft.TextField(label="2. Grupos comparados:", multiline=True, min_lines=2),
                        ft.TextField(label="3. Indicadores calculados:", multiline=True, min_lines=2),
                        ft.TextField(label="4. Recomendaciones:", multiline=True, min_lines=3),
                        ft.ElevatedButton("Generar Informe", icon=ft.Icons.DESCRIPTION, on_click=self.generate_report)
                    ]),
                    bgcolor=ft.Colors.BLUE_50,
                    padding=20,
                    border_radius=8
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.EMOJI_EVENTS, size=40, color=ft.Colors.WHITE),
                        ft.Text("¡Felicitaciones!", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("Has completado exitosamente el OVA de Visualización de Inequidades en Salud", 
                               color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton(
                            "Descargar Certificado",
                            icon=ft.Icons.DOWNLOAD,
                            on_click=self.generate_certificate,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.WHITE, color=ft.Colors.ORANGE_600)
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.ORANGE_600,
                    padding=30,
                    border_radius=12
                )
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        
        self.content_container.content.controls.append(content)

    def update_checklist(self, index, value):
        self.checklist_items[index] = value
        completed = sum(self.checklist_items)
        self.checklist_progress.value = f"Progreso: {completed}/5 completado"
        if completed == 5:
            self.checklist_progress.value = "¡Completado! 5/5"
            self.checklist_progress.color = ft.Colors.GREEN_600
        self.page.update()

    def download_resource(self, resource_title):
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Descargando: {resource_title}")))

    def generate_report(self, e):
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Generando informe personalizado...")))

    def generate_certificate(self, e):
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text("¡Felicitaciones! Generando certificado de finalización...")))

def main(page: ft.Page):
    app = OVAInequidadesSalud()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)
