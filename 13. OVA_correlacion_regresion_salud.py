
import flet as ft
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
import json

class OVAApp:
    def __init__(self):
        self.current_section = "intro"
        self.current_quiz_question = 0
        self.quiz_answers = [None] * 10
        self.progress = 0
        
        # Datos para casos de estudio
        self.case_data = {
            "imc_pa": {
                "x": [22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41],
                "y": [110, 115, 125, 130, 140, 145, 155, 160, 170, 175, 112, 118, 128, 135, 142, 148, 158, 165, 172, 178],
                "labels": ["IMC (kg/m²)", "Presión Arterial (mmHg)"]
            },
            "edad_cvf": {
                "x": [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 28, 33, 38, 43, 48, 53, 58, 63, 68, 72],
                "y": [4.8, 4.6, 4.4, 4.2, 4.0, 3.8, 3.6, 3.4, 3.2, 3.0, 4.7, 4.5, 4.3, 4.1, 3.9, 3.7, 3.5, 3.3, 3.1, 2.9],
                "labels": ["Edad (años)", "CVF (litros)"]
            },
            "dosis_tiempo": {
                "x": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105],
                "y": [11.5, 10.8, 10.1, 9.4, 8.7, 8.0, 7.3, 6.6, 5.9, 5.2, 11.2, 10.5, 9.8, 9.1, 8.4, 7.7, 7.0, 6.3, 5.6, 4.9],
                "labels": ["Dosis (mg)", "Tiempo Recuperación (horas)"]
            },
            "sueno_cognitivo": {
                "x": [4, 5, 6, 7, 8, 9, 10, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 5.2, 6.2, 7.2, 8.2, 9.2],
                "y": [65, 72, 78, 85, 92, 98, 105, 68, 75, 81, 88, 95, 101, 73, 79, 86, 93, 99],
                "labels": ["Horas de Sueño", "Puntuación Cognitiva"]
            }
        }
        
        # Preguntas del quiz
        self.quiz_questions = [
            {
                "question": "¿Cuál es el rango de valores que puede tomar el coeficiente de correlación de Pearson?",
                "options": ["0 a 1", "-1 a 1", "0 a 100", "-100 a 100"],
                "correct": 1,
                "explanation": "El coeficiente de correlación de Pearson (r) siempre está entre -1 y 1, donde -1 indica correlación negativa perfecta, 0 indica ausencia de correlación lineal, y 1 indica correlación positiva perfecta."
            },
            {
                "question": "Si r = -0.85, ¿cómo clasificarías esta correlación?",
                "options": ["Débil negativa", "Moderada negativa", "Fuerte negativa", "Perfecta negativa"],
                "correct": 2,
                "explanation": "Una correlación de -0.85 se considera fuerte negativa, ya que |r| > 0.7. El signo negativo indica que cuando una variable aumenta, la otra tiende a disminuir."
            },
            {
                "question": "En la ecuación Y = 120 + 3.5X, ¿qué representa el valor 3.5?",
                "options": ["El intercepto", "La pendiente", "El coeficiente de correlación", "El error estándar"],
                "correct": 1,
                "explanation": "En la ecuación de regresión Y = a + bX, el valor 3.5 es la pendiente (b), que indica el cambio esperado en Y por cada unidad de aumento en X."
            },
            {
                "question": "¿Qué significa que R² = 0.64 en un análisis de regresión?",
                "options": ["64% de los datos son correctos", "La correlación es 0.64", "64% de la variabilidad en Y se explica por X", "El error es del 64%"],
                "correct": 2,
                "explanation": "R² (coeficiente de determinación) indica qué porcentaje de la variabilidad en la variable dependiente (Y) es explicada por la variable independiente (X). R² = 0.64 significa que el 64% de la variabilidad se explica por el modelo."
            },
            {
                "question": "¿Cuál es la principal diferencia entre correlación y causalidad?",
                "options": ["No hay diferencia", "La correlación implica causalidad", "La causalidad implica correlación, pero no viceversa", "Son conceptos opuestos"],
                "correct": 2,
                "explanation": "La causalidad implica que una variable causa cambios en otra, lo que generalmente resulta en correlación. Sin embargo, la correlación no implica causalidad, ya que puede deberse a variables confusoras o coincidencias."
            },
            {
                "question": "En un estudio médico, ¿cuál sería la interpretación más apropiada de r = 0.92 entre dosis de medicamento y mejoría clínica?",
                "options": ["El medicamento no es efectivo", "Hay una relación muy fuerte y positiva", "La dosis es incorrecta", "Los datos están mal calculados"],
                "correct": 1,
                "explanation": "r = 0.92 indica una correlación muy fuerte y positiva, sugiriendo que a mayor dosis del medicamento, mayor es la mejoría clínica observada."
            },
            {
                "question": "¿Qué supuesto es fundamental para aplicar regresión lineal simple?",
                "options": ["Los datos deben ser categóricos", "La relación debe ser lineal", "Debe haber más de 1000 observaciones", "Las variables deben ser independientes del tiempo"],
                "correct": 1,
                "explanation": "Uno de los supuestos fundamentales de la regresión lineal simple es que la relación entre las variables X e Y sea aproximadamente lineal."
            },
            {
                "question": "Si el valor p de una correlación es 0.03, ¿qué puedes concluir?",
                "options": ["La correlación no es significativa", "La correlación es significativa al nivel 0.05", "Los datos están incorrectos", "Se necesitan más datos"],
                "correct": 1,
                "explanation": "Un valor p = 0.03 < 0.05 indica que la correlación es estadísticamente significativa al nivel de significancia del 5%, lo que significa que es poco probable que la correlación observada se deba al azar."
            },
            {
                "question": "En investigación epidemiológica, ¿para qué se usa principalmente el análisis de correlación?",
                "options": ["Para establecer causalidad", "Para identificar asociaciones entre variables", "Para calcular prevalencias", "Para determinar incidencias"],
                "correct": 1,
                "explanation": "En epidemiología, el análisis de correlación se usa principalmente para identificar asociaciones entre variables (como factores de riesgo y enfermedades), no para establecer causalidad directa."
            },
            {
                "question": "¿Cuál es la mejor práctica al interpretar resultados de regresión en contextos clínicos?",
                "options": ["Considerar solo la significancia estadística", "Evaluar tanto significancia estadística como clínica", "Ignorar los intervalos de confianza", "Usar solo el coeficiente de correlación"],
                "correct": 1,
                "explanation": "En contextos clínicos es fundamental evaluar tanto la significancia estadística (si el efecto es real) como la significancia clínica (si el efecto es relevante para la práctica médica)."
            }
        ]

    def main(self, page: ft.Page):
        page.title = "OVA 13: Correlación y Regresión Lineal en Investigación en Salud"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.scroll = ft.ScrollMode.AUTO
        
        # Variables de la interfaz
        self.page = page
        self.progress_bar = ft.ProgressBar(width=400, color="blue", bgcolor="#eeeeee")
        self.progress_text = ft.Text("0%", size=12)
        self.content_area = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("OVA 13: Correlación y Regresión Lineal", 
                           size=28, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text("Estadística Descriptiva para Ciencias de la Salud", 
                           size=16, color="white")
                ], expand=True),
                ft.Column([
                    ft.Text("Modelo Pedagógico C(H)ANGE", size=12, color="white"),
                    ft.Text("Universidad Antonio Nariño", size=12, weight=ft.FontWeight.BOLD, color="white")
                ])
            ]),
            bgcolor=ft.colors.BLUE_700,
            padding=20,
            border=ft.border.only(bottom=ft.BorderSide(4, ft.colors.BLUE_500))
        )
        
        # Progress bar
        progress_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Progreso del Aprendizaje", size=12),
                    self.progress_text
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar
            ]),
            padding=10,
            bgcolor="white"
        )
        
        # Navigation
        nav_buttons = [
            ft.ElevatedButton("Introducción", on_click=lambda _: self.show_section("intro"), 
                            bgcolor=ft.colors.BLUE_500, color="white"),
            ft.ElevatedButton("Marco Teórico", on_click=lambda _: self.show_section("teoria")),
            ft.ElevatedButton("Casos de Estudio", on_click=lambda _: self.show_section("casos")),
            ft.ElevatedButton("Simulador", on_click=lambda _: self.show_section("simulador")),
            ft.ElevatedButton("Actividades", on_click=lambda _: self.show_section("actividades")),
            ft.ElevatedButton("Evaluación", on_click=lambda _: self.show_section("evaluacion")),
            ft.ElevatedButton("Recursos", on_click=lambda _: self.show_section("recursos"))
        ]
        
        navigation = ft.Container(
            content=ft.Row(nav_buttons, scroll=ft.ScrollMode.AUTO),
            padding=10,
            bgcolor="white"
        )
        
        # Main layout
        page.add(
            ft.Column([
                header,
                progress_container,
                navigation,
                ft.Container(
                    content=self.content_area,
                    padding=20,
                    expand=True
                )
            ], expand=True)
        )
        
        # Show initial section
        self.show_section("intro")
        self.update_progress()

    def show_section(self, section_id):
        self.current_section = section_id
        self.content_area.controls.clear()
        
        if section_id == "intro":
            self.show_intro()
        elif section_id == "teoria":
            self.show_teoria()
        elif section_id == "casos":
            self.show_casos()
        elif section_id == "simulador":
            self.show_simulador()
        elif section_id == "actividades":
            self.show_actividades()
        elif section_id == "evaluacion":
            self.show_evaluacion()
        elif section_id == "recursos":
            self.show_recursos()
        
        self.update_progress()
        self.page.update()

    def update_progress(self):
        sections = ["intro", "teoria", "casos", "simulador", "actividades", "evaluacion", "recursos"]
        current_index = sections.index(self.current_section)
        progress = ((current_index + 1) / len(sections))
        
        self.progress_bar.value = progress
        self.progress_text.value = f"{int(progress * 100)}%"

    def show_intro(self):
        intro_content = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.ANALYTICS, size=60, color=ft.colors.BLUE_500),
                        ft.Text("Análisis de Correlación y Regresión Lineal", 
                               size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text("Aplicaciones en Investigación en Salud", 
                               size=18, text_align=ft.TextAlign.CENTER),
                        
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("¿Por qué es importante?", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Text("• Identificar relaciones entre variables de salud"),
                                    ft.Text("• Predecir resultados clínicos"),
                                    ft.Text("• Fundamentar decisiones basadas en evidencia"),
                                    ft.Text("• Interpretar estudios epidemiológicos")
                                ]),
                                bgcolor=ft.colors.BLUE_50,
                                padding=15,
                                border_radius=10,
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Modelo C(H)ANGE", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Text("Combinatoria: Análisis de variables múltiples"),
                                    ft.Text("Álgebra: Ecuaciones de regresión"),
                                    ft.Text("Números: Coeficientes estadísticos"),
                                    ft.Text("Geometría: Visualización gráfica"),
                                    ft.Text("Estadística: Análisis inferencial")
                                ]),
                                bgcolor=ft.colors.GREEN_50,
                                padding=15,
                                border_radius=10,
                                expand=True
                            )
                        ]),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Objetivos de Aprendizaje", size=18, weight=ft.FontWeight.BOLD),
                                ft.Row([
                                    ft.Column([
                                        ft.Text("Al finalizar esta OVA, podrás:", weight=ft.FontWeight.BOLD),
                                        ft.Text("✓ Calcular e interpretar coeficientes de correlación"),
                                        ft.Text("✓ Construir modelos de regresión lineal simple"),
                                        ft.Text("✓ Evaluar la significancia estadística"),
                                        ft.Text("✓ Distinguir correlación de causalidad")
                                    ], expand=True),
                                    ft.Column([
                                        ft.Text("Aplicaciones en Salud:", weight=ft.FontWeight.BOLD),
                                        ft.Text("✓ Análisis de factores de riesgo"),
                                        ft.Text("✓ Predicción de resultados clínicos"),
                                        ft.Text("✓ Evaluación de tratamientos"),
                                        ft.Text("✓ Investigación epidemiológica")
                                    ], expand=True)
                                ])
                            ]),
                            bgcolor=ft.colors.PURPLE_50,
                            padding=15,
                            border_radius=10
                        ),
                        
                        ft.ElevatedButton(
                            "Comenzar Aprendizaje →",
                            on_click=lambda _: self.show_section("teoria"),
                            bgcolor=ft.colors.BLUE_500,
                            color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
                    bgcolor="white",
                    padding=30,
                    border_radius=15,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.colors.GREY_300)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        
        self.content_area.controls.append(intro_content)

    def show_teoria(self):
        teoria_content = ft.Column([
            ft.Text("Marco Teórico", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            
            ft.Row([
                # Correlación
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.TRENDING_UP, color=ft.colors.BLUE_600),
                            ft.Text("Correlación", size=20, weight=ft.FontWeight.BOLD)
                        ]),
                        ft.Text("La correlación mide la fuerza y dirección de la relación lineal entre dos variables cuantitativas."),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Coeficiente de Correlación de Pearson (r)", weight=ft.FontWeight.BOLD),
                                ft.Text("r = Σ(xi - x̄)(yi - ȳ) / √[Σ(xi - x̄)² Σ(yi - ȳ)²]", 
                                       style=ft.TextStyle(font_family="monospace"))
                            ]),
                            bgcolor=ft.colors.BLUE_50,
                            padding=10,
                            border_radius=5
                        ),
                        
                        ft.Column([
                            ft.Text("r = 1: Correlación positiva perfecta"),
                            ft.Text("0.7 ≤ |r| < 1: Correlación fuerte"),
                            ft.Text("0.3 ≤ |r| < 0.7: Correlación moderada"),
                            ft.Text("0 < |r| < 0.3: Correlación débil"),
                            ft.Text("r = 0: Sin correlación lineal")
                        ])
                    ], spacing=10),
                    bgcolor="white",
                    padding=15,
                    border_radius=10,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.GREY_300),
                    expand=True
                ),
                
                # Regresión
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.SHOW_CHART, color=ft.colors.GREEN_600),
                            ft.Text("Regresión Lineal Simple", size=20, weight=ft.FontWeight.BOLD)
                        ]),
                        ft.Text("Permite predecir el valor de una variable dependiente (Y) a partir de una variable independiente (X)."),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Ecuación de Regresión", weight=ft.FontWeight.BOLD),
                                ft.Text("Ŷ = a + bX", style=ft.TextStyle(font_family="monospace")),
                                ft.Text("a: Intercepto (valor de Y cuando X = 0)"),
                                ft.Text("b: Pendiente (cambio en Y por unidad de X)")
                            ]),
                            bgcolor=ft.colors.GREEN_50,
                            padding=10,
                            border_radius=5
                        ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Cálculo de Parámetros", weight=ft.FontWeight.BOLD),
                                ft.Text("b = Σ(xi - x̄)(yi - ȳ) / Σ(xi - x̄)²", 
                                       style=ft.TextStyle(font_family="monospace")),
                                ft.Text("a = ȳ - bx̄", 
                                       style=ft.TextStyle(font_family="monospace"))
                            ]),
                            bgcolor=ft.colors.GREEN_50,
                            padding=10,
                            border_radius=5
                        )
                    ], spacing=10),
                    bgcolor="white",
                    padding=15,
                    border_radius=10,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.GREY_300),
                    expand=True
                )
            ], spacing=20),
            
            # Interpretación en Salud
            ft.Container(
                content=ft.Column([
                    ft.Text("Interpretación en Contextos de Salud", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.icons.WARNING, color=ft.colors.RED_600, size=40),
                                ft.Text("¡Cuidado!", weight=ft.FontWeight.BOLD),
                                ft.Text("Correlación NO implica causalidad. Una relación estadística no establece causa-efecto.", text_align=ft.TextAlign.CENTER)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.RED_50,
                            padding=15,
                            border_radius=10,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.icons.LIGHTBULB, color=ft.colors.YELLOW_600, size=40),
                                ft.Text("Significancia Clínica", weight=ft.FontWeight.BOLD),
                                ft.Text("Evalúa si la diferencia estadística es relevante en la práctica clínica.", text_align=ft.TextAlign.CENTER)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.YELLOW_50,
                            padding=15,
                            border_radius=10,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.BLUE_600, size=40),
                                ft.Text("Validación", weight=ft.FontWeight.BOLD),
                                ft.Text("Verifica supuestos: linealidad, normalidad, homocedasticidad e independencia.", text_align=ft.TextAlign.CENTER)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.BLUE_50,
                            padding=15,
                            border_radius=10,
                            expand=True
                        )
                    ], spacing=15)
                ]),
                bgcolor="white",
                padding=20,
                border_radius=15,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.colors.GREY_300)
            ),
            
            ft.ElevatedButton(
                "Ver Casos de Estudio →",
                on_click=lambda _: self.show_section("casos"),
                bgcolor=ft.colors.GREEN_500,
                color="white"
            )
        ], spacing=20)
        
        self.content_area.controls.append(teoria_content)

    def show_casos(self):
        casos_content = ft.Column([
            ft.Text("Casos de Estudio Interactivos", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            
            ft.Row([
                # Caso 1: IMC y Presión Arterial
                self.create_case_card(
                    "Caso 1: IMC y Presión Arterial",
                    "Estudio con 50 pacientes para analizar la relación entre el Índice de Masa Corporal (IMC) y la presión arterial sistólica.",
                    "imc_pa",
                    "0.78",
                    "0.61",
                    "PA = 85.2 + 2.1 × IMC",
                    "Por cada unidad de aumento en el IMC, la presión arterial sistólica aumenta aproximadamente 2.1 mmHg.",
                    ft.colors.RED_500
                ),
                
                # Caso 2: Edad y Capacidad Pulmonar
                self.create_case_card(
                    "Caso 2: Edad y Capacidad Pulmonar",
                    "Análisis de la relación entre edad y capacidad vital forzada (CVF) en 45 individuos sanos.",
                    "edad_cvf",
                    "-0.72",
                    "0.52",
                    "CVF = 5.8 - 0.03 × Edad",
                    "Por cada año de edad, la capacidad vital forzada disminuye aproximadamente 0.03 litros.",
                    ft.colors.BLUE_500
                )
            ], spacing=20),
            
            ft.Row([
                # Caso 3: Dosis y Tiempo de Recuperación
                self.create_case_card(
                    "Caso 3: Dosis y Recuperación",
                    "Estudio farmacológico: relación entre dosis de analgésico (mg) y tiempo de recuperación (horas) en 40 pacientes.",
                    "dosis_tiempo",
                    "-0.85",
                    "0.72",
                    "Tiempo = 12.5 - 0.08 × Dosis",
                    "Por cada mg adicional de medicamento, el tiempo de recuperación disminuye 0.08 horas.",
                    ft.colors.GREEN_500
                ),
                
                # Caso 4: Sueño y Rendimiento Cognitivo
                self.create_case_card(
                    "Caso 4: Sueño y Cognición",
                    "Investigación sobre la relación entre horas de sueño y puntuación en test cognitivo en 35 estudiantes de medicina.",
                    "sueno_cognitivo",
                    "0.68",
                    "0.46",
                    "Puntuación = 45 + 6.2 × Horas_Sueño",
                    "Por cada hora adicional de sueño, la puntuación cognitiva aumenta 6.2 puntos.",
                    ft.colors.PURPLE_500
                )
            ], spacing=20),
            
            ft.ElevatedButton(
                "Usar Simulador Interactivo →",
                on_click=lambda _: self.show_section("simulador"),
                bgcolor=ft.colors.PURPLE_500,
                color="white"
            )
        ], spacing=20)
        
        self.content_area.controls.append(casos_content)

    def create_case_card(self, title, description, case_key, correlation, r2, equation, interpretation, color):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.FAVORITE, color=color),
                    ft.Text(title, size=16, weight=ft.FontWeight.BOLD)
                ]),
                ft.Text(description),
                
                # Placeholder para gráfico
                ft.Container(
                    content=ft.Text("📊 Gráfico de Dispersión", text_align=ft.TextAlign.CENTER),
                    height=150,
                    bgcolor=ft.colors.GREY_100,
                    border_radius=5
                ),
                
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text(correlation, size=20, weight=ft.FontWeight.BOLD, color=color),
                            ft.Text("Correlación", size=12)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=f"{color}20",
                        padding=10,
                        border_radius=5,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text(r2, size=20, weight=ft.FontWeight.BOLD, color=color),
                            ft.Text("R² (Varianza explicada)", size=12)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=f"{color}20",
                        padding=10,
                        border_radius=5,
                        expand=True
                    )
                ], spacing=10),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ecuación de Regresión:", weight=ft.FontWeight.BOLD),
                        ft.Text(equation, style=ft.TextStyle(font_family="monospace")),
                        ft.Text(interpretation, size=12)
                    ]),
                    bgcolor=f"{color}20",
                    padding=10,
                    border_radius=5
                ),
                
                ft.ElevatedButton(
                    "Ver Análisis Detallado",
                    bgcolor=color,
                    color="white",
                    on_click=lambda _, k=case_key: self.show_case_details(k)
                )
            ], spacing=10),
            bgcolor="white",
            padding=15,
            border_radius=10,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.GREY_300),
            expand=True
        )

    def show_case_details(self, case_key):
        # Aquí se mostraría un diálogo con detalles del caso
        details = {
            "imc_pa": "• Correlación fuerte positiva (r = 0.78)\n• El IMC explica el 61% de la variabilidad en la PA\n• Relación estadísticamente significativa (p < 0.001)\n• Importante para prevención cardiovascular",
            "edad_cvf": "• Correlación fuerte negativa (r = -0.72)\n• La edad explica el 52% de la variabilidad en CVF\n• Declino esperado con el envejecimiento\n• Útil para establecer valores de referencia",
            "dosis_tiempo": "• Correlación fuerte negativa (r = -0.85)\n• La dosis explica el 72% de la variabilidad\n• Relación dosis-respuesta clara\n• Importante para optimización terapéutica",
            "sueno_cognitivo": "• Correlación moderada-fuerte positiva (r = 0.68)\n• El sueño explica el 46% de la variabilidad\n• Importancia del descanso en el rendimiento\n• Relevante para bienestar estudiantil"
        }
        
        dlg = ft.AlertDialog(
            title=ft.Text("Interpretación Clínica"),
            content=ft.Text(details.get(case_key, "Detalles no disponibles")),
            actions=[ft.TextButton("Cerrar", on_click=lambda _: self.close_dialog())]
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()

    def show_simulador(self):
        # Variables del simulador
        self.sim_data_x = ft.TextField(
            label="Datos X (separados por comas)",
            value="20, 25, 30, 35, 40, 22, 28, 33, 38, 42",
            multiline=True,
            max_lines=3
        )
        self.sim_data_y = ft.TextField(
            label="Datos Y (separados por comas)",
            value="110, 125, 135, 145, 155, 115, 130, 138, 148, 158",
            multiline=True,
            max_lines=3
        )
        self.sim_corr_result = ft.Text("-", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600)
        self.sim_r2_result = ft.Text("-", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_600)
        self.sim_equation = ft.Text("Y = a + bX", style=ft.TextStyle(font_family="monospace"))
        self.sim_interpretation = ft.Text("Ingresa datos y calcula la correlación para ver la interpretación.")
        self.sim_predict_input = ft.TextField(label="Valor X", width=100)
        self.sim_predict_result = ft.Text("")
        
        simulador_content = ft.Column([
            ft.Text("Simulador Interactivo", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            
            ft.Row([
                # Panel de Control
                ft.Container(
                    content=ft.Column([
                        ft.Text("Panel de Control", size=18, weight=ft.FontWeight.BOLD),
                        
                        ft.Dropdown(
                            label="Conjunto de Datos",
                            options=[
                                ft.dropdown.Option("custom", "Datos Personalizados"),
                                ft.dropdown.Option("imc_pa", "IMC vs Presión Arterial"),
                                ft.dropdown.Option("edad_cvf", "Edad vs Capacidad Pulmonar"),
                                ft.dropdown.Option("dosis_tiempo", "Dosis vs Tiempo Recuperación"),
                                ft.dropdown.Option("sueno_cognitivo", "Sueño vs Rendimiento Cognitivo")
                            ],
                            value="custom",
                            on_change=self.update_simulation_data
                        ),
                        
                        self.sim_data_x,
                        self.sim_data_y,
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "Calcular Correlación",
                                bgcolor=ft.colors.BLUE_500,
                                color="white",
                                on_click=self.calculate_correlation,
                                expand=True
                            ),
                            ft.ElevatedButton(
                                "Regresión Lineal",
                                bgcolor=ft.colors.GREEN_500,
                                color="white",
                                on_click=self.calculate_regression,
                                expand=True
                            )
                        ], spacing=10),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Predictor", weight=ft.FontWeight.BOLD),
                                ft.Row([
                                    self.sim_predict_input,
                                    ft.ElevatedButton(
                                        "Predecir Y",
                                        bgcolor=ft.colors.PURPLE_500,
                                        color="white",
                                        on_click=self.make_prediction
                                    )
                                ], spacing=10),
                                self.sim_predict_result
                            ]),
                            bgcolor=ft.colors.GREY_50,
                            padding=10,
                            border_radius=5
                        )
                    ], spacing=15),
                    bgcolor="white",
                    padding=15,
                    border_radius=10,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.GREY_300),
                    expand=True
                ),
                
                # Visualización y Resultados
                ft.Container(
                    content=ft.Column([
                        ft.Text("Visualización y Resultados", size=18, weight=ft.FontWeight.BOLD),
                        
                        # Placeholder para gráfico
                        ft.Container(
                            content=ft.Text("📊 Gráfico de Correlación y Regresión", text_align=ft.TextAlign.CENTER),
                            height=200,
                            bgcolor=ft.colors.GREY_100,
                            border_radius=5
                        ),
                        
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    self.sim_corr_result,
                                    ft.Text("Correlación (r)", size=12)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                bgcolor=ft.colors.BLUE_50,
                                padding=10,
                                border_radius=5,
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column([
                                    self.sim_r2_result,
                                    ft.Text("R² (Determinación)", size=12)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                bgcolor=ft.colors.GREEN_50,
                                padding=10,
                                border_radius=5,
                                expand=True
                            )
                        ], spacing=10),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Ecuación de Regresión:", weight=ft.FontWeight.BOLD),
                                self.sim_equation
                            ]),
                            bgcolor=ft.colors.PURPLE_50,
                            padding=10,
                            border_radius=5
                        ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Interpretación:", weight=ft.FontWeight.BOLD),
                                self.sim_interpretation
                            ]),
                            bgcolor=ft.colors.YELLOW_50,
                            padding=10,
                            border_radius=5
                        )
                    ], spacing=15),
                    bgcolor="white",
                    padding=15,
                    border_radius=10,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.GREY_300),
                    expand=True
                )
            ], spacing=20),
            
            ft.ElevatedButton(
                "Realizar Actividades Prácticas →",
                on_click=lambda _: self.show_section("actividades"),
                bgcolor=ft.colors.INDIGO_500,
                color="white"
            )
        ], spacing=20)
        
        self.content_area.controls.append(simulador_content)

    def update_simulation_data(self, e):
        if e.control.value != "custom":
            data = self.case_data[e.control.value]
            self.sim_data_x.value = ", ".join(map(str, data["x"]))
            self.sim_data_y.value = ", ".join(map(str, data["y"]))
            self.page.update()

    def parse_data(self, data_string):
        try:
            return [float(x.strip()) for x in data_string.split(",") if x.strip()]
        except:
            return []

    def pearson_correlation(self, x, y):
        if len(x) != len(y) or len(x) < 2:
            return 0
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi * xi for xi in x)
        sum_y2 = sum(yi * yi for yi in y)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y))
        
        return numerator / denominator if denominator != 0 else 0

    def linear_regression(self, x, y):
        if len(x) != len(y) or len(x) < 2:
            return {"slope": 0, "intercept": 0}
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi * xi for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n
        
        return {"slope": slope, "intercept": intercept}

    def calculate_correlation(self, e):
        x_data = self.parse_data(self.sim_data_x.value)
        y_data = self.parse_data(self.sim_data_y.value)
        
        if len(x_data) != len(y_data) or len(x_data) < 2:
            self.show_error("Los datos X e Y deben tener la misma cantidad de valores y al menos 2 puntos.")
            return
        
        correlation = self.pearson_correlation(x_data, y_data)
        r2 = correlation * correlation
        
        self.sim_corr_result.value = f"{correlation:.3f}"
        self.sim_r2_result.value = f"{r2:.3f}"
        
        self.update_interpretation(correlation, r2)
        self.page.update()

    def calculate_regression(self, e):
        x_data = self.parse_data(self.sim_data_x.value)
        y_data = self.parse_data(self.sim_data_y.value)
        
        if len(x_data) != len(y_data) or len(x_data) < 2:
            self.show_error("Los datos X e Y deben tener la misma cantidad de valores y al menos 2 puntos.")
            return
        
        regression = self.linear_regression(x_data, y_data)
        correlation = self.pearson_correlation(x_data, y_data)
        r2 = correlation * correlation
        
        self.sim_corr_result.value = f"{correlation:.3f}"
        self.sim_r2_result.value = f"{r2:.3f}"
        self.sim_equation.value = f"Y = {regression['intercept']:.2f} + {regression['slope']:.2f}X"
        
        self.update_interpretation(correlation, r2, regression)
        self.page.update()

    def update_interpretation(self, correlation, r2, regression=None):
        abs_corr = abs(correlation)
        if abs_corr >= 0.9:
            strength = "muy fuerte"
        elif abs_corr >= 0.7:
            strength = "fuerte"
        elif abs_corr >= 0.5:
            strength = "moderada"
        elif abs_corr >= 0.3:
            strength = "débil"
        else:
            strength = "muy débil o inexistente"
        
        direction = "positiva" if correlation > 0 else "negativa"
        
        interpretation = f"Correlación: {strength} {direction} (r = {correlation:.3f})\n"
        interpretation += f"Varianza explicada: {r2*100:.1f}% de la variabilidad en Y se explica por X"
        
        if regression:
            change = "aumenta" if regression["slope"] > 0 else "disminuye"
            interpretation += f"\nPendiente: Por cada unidad de aumento en X, Y {change} {abs(regression['slope']):.3f} unidades"
        
        self.sim_interpretation.value = interpretation

    def make_prediction(self, e):
        try:
            x_value = float(self.sim_predict_input.value)
            equation_text = self.sim_equation.value
            
            if equation_text == "Y = a + bX":
                self.show_error("Primero calcula la regresión lineal.")
                return
            
            # Extraer coeficientes de la ecuación
            import re
            match = re.search(r'Y = ([-\d.]+) \+ ([-\d.]+)X', equation_text)
            if match:
                intercept = float(match.group(1))
                slope = float(match.group(2))
                prediction = intercept + slope * x_value
                
                self.sim_predict_result.value = f"Para X = {x_value}, Y predicho = {prediction:.2f}"
                self.page.update()
        except ValueError:
            self.show_error("Por favor, ingresa un valor numérico válido.")

    def show_error(self, message):
        dlg = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda _: self.close_dialog())]
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def show_actividades(self):
        actividades_content = ft.Column([
            ft.Text("Actividades Prácticas", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            
            # Actividad 1
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text("1", size=20, weight=ft.FontWeight.BOLD, color="white"),
                            bgcolor=ft.colors.BLUE_500,
                            width=40,
                            height=40,
                            border_radius=20,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Análisis de Datos Reales", size=20, weight=ft.FontWeight.BOLD)
                    ]),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Contexto Clínico:", weight=ft.FontWeight.BOLD),
                            ft.Text("Un estudio evaluó la relación entre el nivel de colesterol total (mg/dL) y la edad (años) en 20 pacientes:"),
                            ft.Text("Edad: 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 28, 33, 38, 43, 48, 53, 58, 63, 68, 72"),
                            ft.Text("Colesterol: 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 185, 195, 205, 215, 225, 235, 245, 255, 265, 275")
                        ]),
                        bgcolor=ft.colors.BLUE_50,
                        padding=15,
                        border_radius=10
                    ),
                    
                    ft.TextField(label="1. Calcula el coeficiente de correlación:", hint_text="Ej: 0.85"),
                    ft.TextField(label="2. ¿Cuál es la ecuación de regresión? (formato: Y = a + bX)", hint_text="Ej: Y = 120 + 2.1X"),
                    ft.TextField(label="3. Interpreta el resultado clínicamente:", multiline=True, max_lines=3),
                    
                    ft.ElevatedButton(
                        "Verificar Respuestas",
                        bgcolor=ft.colors.BLUE_500,
                        color="white",
                        on_click=lambda _: self.check_activity_1()
                    )
                ], spacing=15),
                bgcolor="white",
                padding=20,
                border_radius=15,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.colors.GREY_300)
            ),
            
            # Actividad 2
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text("2", size=20, weight=ft.FontWeight.BOLD, color="white"),
                            bgcolor=ft.colors.GREEN_500,
                            width=40,
                            height=40,
                            border_radius=20,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Interpretación de Estudios", size=20, weight=ft.FontWeight.BOLD)
                    ]),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Caso de Estudio:", weight=ft.FontWeight.BOLD),
                            ft.Text("Un investigador reporta los siguientes resultados sobre la relación entre horas de ejercicio semanal y niveles de glucosa en sangre:"),
                            ft.Text("• Correlación (r): -0.65"),
                            ft.Text("• R² (coeficiente de determinación): 0.42"),
                            ft.Text("• Ecuación: Glucosa = 140 - 3.2 × Horas_Ejercicio"),
                            ft.Text("• Valor p: 0.003"),
                            ft.Text("• Tamaño de muestra: n = 80")
                        ]),
                        bgcolor=ft.colors.GREEN_50,
                        padding=15,
                        border_radius=10
                    ),
                    
                    ft.Dropdown(
                        label="1. ¿Cómo clasificarías la fuerza de esta correlación?",
                        options=[
                            ft.dropdown.Option("debil", "Débil"),
                            ft.dropdown.Option("moderada", "Moderada"),
                            ft.dropdown.Option("fuerte", "Fuerte"),
                            ft.dropdown.Option("perfecta", "Perfecta")
                        ]
                    ),
                    ft.TextField(label="2. ¿Qué porcentaje de la variabilidad en glucosa explica el ejercicio?", hint_text="Porcentaje"),
                    ft.TextField(label="3. Si una persona hace 5 horas de ejercicio semanal, ¿cuál sería su nivel de glucosa predicho?", hint_text="mg/dL"),
                    ft.TextField(label="4. ¿Es estadísticamente significativa esta relación? ¿Por qué?", multiline=True, max_lines=2),
                    
                    ft.ElevatedButton(
                        "Verificar Respuestas",
                        bgcolor=ft.colors.GREEN_500,
                        color="white",
                        on_click=lambda _: self.check_activity_2()
                    )
                ], spacing=15),
                bgcolor="white",
                padding=20,
                border_radius=15,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.colors.GREY_300)
            ),
            
            ft.ElevatedButton(
                "Realizar Evaluación Final →",
                on_click=lambda _: self.show_section("evaluacion"),
                bgcolor=ft.colors.RED_500,
                color="white"
            )
        ], spacing=20)
        
        self.content_area.controls.append(actividades_content)

    def check_activity_1(self):
        # Implementar verificación de actividad 1
        dlg = ft.AlertDialog(
            title=ft.Text("Retroalimentación Actividad 1"),
            content=ft.Text("Respuestas esperadas:\n1. Correlación ≈ 0.99\n2. Ecuación ≈ Y = 100 + 2.5X\n3. Interpretación sobre la relación positiva fuerte entre edad y colesterol."),
            actions=[ft.TextButton("OK", on_click=lambda _: self.close_dialog())]
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def check_activity_2(self):
        # Implementar verificación de actividad 2
        dlg = ft.AlertDialog(
            title=ft.Text("Retroalimentación Actividad 2"),
            content=ft.Text("Respuestas esperadas:\n1. Moderada-fuerte\n2. 42%\n3. 124 mg/dL\n4. Sí, porque p = 0.003 < 0.05"),
            actions=[ft.TextButton("OK", on_click=lambda _: self.close_dialog())]
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def show_evaluacion(self):
        self.current_quiz_question = 0
        self.quiz_answers = [None] * len(self.quiz_questions)
        
        self.quiz_container = ft.Column()
        self.quiz_navigation = ft.Row([
            ft.ElevatedButton("← Anterior", on_click=self.previous_question, disabled=True),
            ft.ElevatedButton("Siguiente →", on_click=self.next_question)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        
        evaluacion_content = ft.Column([
            ft.Text("Evaluación Final", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.QUIZ, size=60, color=ft.colors.RED_500),
                    ft.Text("Quiz de Evaluación", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("10 preguntas sobre correlación y regresión lineal"),
                    ft.Text(f"Pregunta {self.current_quiz_question + 1} de {len(self.quiz_questions)}")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20
            ),
            
            self.quiz_container,
            self.quiz_navigation,
            
            ft.ElevatedButton(
                "Ver Recursos Adicionales →",
                on_click=lambda _: self.show_section("recursos"),
                bgcolor=ft.colors.TEAL_500,
                color="white"
            )
        ], spacing=20)
        
        self.content_area.controls.append(evaluacion_content)
        self.show_quiz_question()

    def show_quiz_question(self):
        question = self.quiz_questions[self.current_quiz_question]
        
        self.quiz_container.controls.clear()
        self.quiz_container.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(question["question"], size=16, weight=ft.FontWeight.BOLD),
                    ft.RadioGroup(
                        content=ft.Column([
                            ft.Radio(value=i, label=option) 
                            for i, option in enumerate(question["options"])
                        ]),
                        value=self.quiz_answers[self.current_quiz_question],
                        on_change=self.on_quiz_answer_change
                    )
                ]),
                bgcolor="white",
                padding=20,
                border_radius=10,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.GREY_300)
            )
        )
        
        # Update navigation buttons
        self.quiz_navigation.controls[0].disabled = self.current_quiz_question == 0
        
        if self.current_quiz_question == len(self.quiz_questions) - 1:
            self.quiz_navigation.controls[1].text = "Finalizar Quiz"
            self.quiz_navigation.controls[1].on_click = self.submit_quiz
        else:
            self.quiz_navigation.controls[1].text = "Siguiente →"
            self.quiz_navigation.controls[1].on_click = self.next_question
        
        self.page.update()

    def on_quiz_answer_change(self, e):
        self.quiz_answers[self.current_quiz_question] = int(e.control.value)

    def next_question(self, e):
        if self.current_quiz_question < len(self.quiz_questions) - 1:
            self.current_quiz_question += 1
            self.show_quiz_question()

    def previous_question(self, e):
        if self.current_quiz_question > 0:
            self.current_quiz_question -= 1
            self.show_quiz_question()

    def submit_quiz(self, e):
        score = sum(1 for i, answer in enumerate(self.quiz_answers) 
                   if answer == self.quiz_questions[i]["correct"])
        percentage = (score / len(self.quiz_questions)) * 100
        
        if percentage >= 80:
            performance = "Excelente"
            color = ft.colors.GREEN_600
        elif percentage >= 60:
            performance = "Bueno"
            color = ft.colors.YELLOW_600
        else:
            performance = "Necesita mejorar"
            color = ft.colors.RED_600
        
        results_content = ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text(f"{score}/{len(self.quiz_questions)}", size=40, weight=ft.FontWeight.BOLD, color=color),
                    ft.Text(f"{percentage:.1f}% - {performance}", size=20, color=color),
                    ft.Text("Has completado la evaluación")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20
            ),
            
            ft.ElevatedButton(
                "Generar Certificado",
                bgcolor=ft.colors.ORANGE_500,
                color="white",
                on_click=self.generate_certificate
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.quiz_container.controls.clear()
        self.quiz_container.controls.append(results_content)
        self.quiz_navigation.controls.clear()
        self.page.update()

    def generate_certificate(self, e):
        dlg = ft.AlertDialog(
            title=ft.Text("¡Felicitaciones!"),
            content=ft.Text("Has completado exitosamente la OVA 13: Análisis de Correlación y Regresión Lineal en Investigación en Salud. Tu certificado ha sido generado."),
            actions=[ft.TextButton("Cerrar", on_click=lambda _: self.close_dialog())]
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def show_recursos(self):
        recursos_content = ft.Column([
            ft.Text("Recursos Adicionales", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            
            ft.Row([
                # Herramientas de Software
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.COMPUTER, color=ft.colors.BLUE_600),
                            ft.Text("Herramientas de Software", size=16, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        ft.Column([
                            self.create_resource_item("R Statistical Software", "Software libre para análisis estadístico", "cor(x, y), lm(y ~ x)", ft.colors.BLUE_500),
                            self.create_resource_item("Python (SciPy/Pandas)", "Librerías para análisis de datos", "scipy.stats.pearsonr()", ft.colors.GREEN_500),
                            self.create_resource_item("SPSS", "Software estadístico comercial", "CORRELATIONS, REGRESSION", ft.colors.PURPLE_500),
                            self.create_resource_item("Excel", "Funciones básicas de correlación", "=CORREL(), =LINEST()", ft.colors.ORANGE_500)
                        ])
                    ], spacing=10),
                    bgcolor="white",
                    padding=15,
                    border_radius=10,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.GREY_300),
                    expand=True
                ),
                
                # Estudios de Referencia
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.BOOK, color=ft.colors.GREEN_600),
                            ft.Text("Estudios de Referencia", size=16, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        ft.Column([
                            self.create_study_item("Framingham Heart Study", "Estudio longitudinal sobre factores de riesgo cardiovascular", "Epidemiología", ft.colors.GREEN_500),
                            self.create_study_item("Nurses' Health Study", "Investigación sobre salud femenina y factores de riesgo", "Cohorte", ft.colors.BLUE_500),
                            self.create_study_item("NHANES", "Encuesta Nacional de Salud y Nutrición (EE.UU.)", "Transversal", ft.colors.PURPLE_500)
                        ])
                    ], spacing=10),
                    bgcolor="white",
                    padding=15,
                    border_radius=10,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.GREY_300),
                    expand=True
                ),
                
                # Bibliografía
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.LIBRARY_BOOKS, color=ft.colors.PURPLE_600),
                            ft.Text("Bibliografía Recomendada", size=16, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        ft.Column([
                            self.create_bibliography_item("Bioestadística Médica", "Dawson, B. & Trapp, R. (2005)", "Manual Moderno", ft.colors.PURPLE_500),
                            self.create_bibliography_item("Epidemiología Clínica", "Fletcher, R. & Fletcher, S. (2007)", "Lippincott Williams & Wilkins", ft.colors.INDIGO_500),
                            self.create_bibliography_item("Statistics in Medicine", "Altman, D. (1991)", "Chapman & Hall", ft.colors.PINK_500),
                            self.create_bibliography_item("Regression Analysis", "Montgomery, D. et al. (2012)", "Wiley", ft.colors.TEAL_500)
                        ])
                    ], spacing=10),
                    bgcolor="white",
                    padding=15,
                    border_radius=10,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color=ft.colors.GREY_300),
                    expand=True
                )
            ], spacing=20),
            
            # Enlaces Útiles
            ft.Container(
                content=ft.Column([
                    ft.Text("Enlaces Útiles", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Row([
                        self.create_link_item("PubMed", "Base de datos de literatura médica", ft.icons.PUBLIC, ft.colors.RED_500),
                        self.create_link_item("Cochrane Library", "Revisiones sistemáticas", ft.icons.ANALYTICS, ft.colors.BLUE_500),
                        self.create_link_item("WHO", "Organización Mundial de la Salud", ft.icons.HEALTH_AND_SAFETY, ft.colors.GREEN_500),
                        self.create_link_item("CDC", "Centros para el Control de Enfermedades", ft.icons.SCIENCE, ft.colors.PURPLE_500)
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                ]),
                bgcolor="white",
                padding=20,
                border_radius=15,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.colors.GREY_300)
            ),
            
            # Certificado de Finalización
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.EMOJI_EVENTS, size=60, color=ft.colors.YELLOW_600),
                    ft.Text("¡Felicitaciones!", size=24, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text("Has completado exitosamente la OVA 13: Análisis de Correlación y Regresión Lineal en Investigación en Salud", 
                           color="white", text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton(
                        "Generar Certificado",
                        bgcolor="white",
                        color=ft.colors.ORANGE_600,
                        on_click=self.generate_certificate
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                bgcolor=ft.colors.ORANGE_500,
                padding=30,
                border_radius=15,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.colors.GREY_300)
            )
        ], spacing=20)
        
        self.content_area.controls.append(recursos_content)

    def create_resource_item(self, title, description, code, color):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, weight=ft.FontWeight.BOLD),
                ft.Text(description, size=12),
                ft.Container(
                    content=ft.Text(code, style=ft.TextStyle(font_family="monospace")),
                    bgcolor=ft.colors.GREY_100,
                    padding=5,
                    border_radius=3
                )
            ]),
            border=ft.border.only(left=ft.BorderSide(4, color)),
            padding=ft.padding.only(left=10)
        )

    def create_study_item(self, title, description, type_study, color):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, weight=ft.FontWeight.BOLD),
                ft.Text(description, size=12),
                ft.Container(
                    content=ft.Text(type_study, size=10, color="white"),
                    bgcolor=color,
                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    border_radius=10
                )
            ]),
            bgcolor=f"{color}20",
            padding=10,
            border_radius=5
        )

    def create_bibliography_item(self, title, author, publisher, color):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, weight=ft.FontWeight.BOLD),
                ft.Text(author),
                ft.Text(publisher, size=10, color=ft.colors.GREY_600)
            ]),
            border=ft.border.only(left=ft.BorderSide(4, color)),
            padding=ft.padding.only(left=10)
        )

    def create_link_item(self, title, description, icon, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=color, size=40),
                ft.Text(title, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(description, size=12, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=150,
            padding=15
        )

def main(page: ft.Page):
    app = OVAApp()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)
