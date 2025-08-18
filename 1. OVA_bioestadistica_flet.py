
import flet as ft
import random
import csv
import io
import base64
from datetime import datetime
import os

class OVABioestadistica:
    def __init__(self):
        self.current_section = 0
        self.progress = 0
        self.classification_score = 0
        self.classification_total = 0
        self.simulator_score = {"correct": 0, "incorrect": 0}
        self.current_sim_variable = 0
        self.quiz_score = 0
        
        # Variables para el simulador
        self.health_variables = [
            {"name": "Presión arterial sistólica (mmHg)", "desc": "Medición de la presión máxima en las arterias", "type": "cuantitativa", "subtype": "continua", "scale": "razón"},
            {"name": "Grado de dolor (1-10)", "desc": "Escala subjetiva de intensidad del dolor", "type": "cualitativa", "subtype": "ordinal", "scale": "ordinal"},
            {"name": "Tipo de sangre (A, B, AB, O)", "desc": "Clasificación del grupo sanguíneo", "type": "cualitativa", "subtype": "nominal", "scale": "nominal"},
            {"name": "Número de embarazos", "desc": "Cantidad de embarazos previos", "type": "cuantitativa", "subtype": "discreta", "scale": "razón"},
            {"name": "Estadio del cáncer (I, II, III, IV)", "desc": "Clasificación de la extensión del cáncer", "type": "cualitativa", "subtype": "ordinal", "scale": "ordinal"},
            {"name": "Peso corporal (kg)", "desc": "Masa corporal en kilogramos", "type": "cuantitativa", "subtype": "continua", "scale": "razón"},
            {"name": "Estado civil", "desc": "Situación legal matrimonial", "type": "cualitativa", "subtype": "nominal", "scale": "nominal"},
            {"name": "Nivel de educación", "desc": "Grado académico alcanzado", "type": "cualitativa", "subtype": "ordinal", "scale": "ordinal"},
            {"name": "Frecuencia cardíaca (lpm)", "desc": "Latidos por minuto", "type": "cuantitativa", "subtype": "discreta", "scale": "razón"},
            {"name": "Temperatura corporal (°C)", "desc": "Temperatura en grados Celsius", "type": "cuantitativa", "subtype": "continua", "scale": "intervalo"}
        ]
        
        # Preguntas del quiz
        self.quiz_questions = [
            {
                "question": "En un estudio sobre hipertensión arterial, se registra la variable 'grado de hipertensión' con las categorías: Normal, Prehipertensión, Hipertensión Grado 1, Hipertensión Grado 2. ¿Cómo clasificarías esta variable?",
                "options": ["Cualitativa nominal", "Cualitativa ordinal", "Cuantitativa discreta", "Cuantitativa continua"],
                "correct": 1,
                "explanation": "Es cualitativa ordinal porque las categorías tienen un orden natural de severidad."
            },
            {
                "question": "Para la variable 'peso corporal en kilogramos', ¿cuál sería el estadístico de tendencia central más apropiado?",
                "options": ["Moda", "Mediana", "Media aritmética", "Percentil 75"],
                "correct": 2,
                "explanation": "Para variables cuantitativas continuas con distribución normal, la media es el estadístico más apropiado."
            },
            {
                "question": "¿Cuál de las siguientes afirmaciones sobre las escalas de medición es INCORRECTA?",
                "options": [
                    "La escala nominal solo permite clasificación",
                    "La escala ordinal tiene orden pero no distancias iguales", 
                    "La escala de razón permite calcular razones y proporciones",
                    "La temperatura en Celsius es una escala de razón"
                ],
                "correct": 3,
                "explanation": "La temperatura en Celsius es una escala de intervalo, no de razón, porque no tiene cero absoluto."
            }
        ]

    def main(self, page: ft.Page):
        page.title = "OVA 1: Bioestadística Esencial para Salud"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1200
        page.window_height = 800
        page.window_resizable = True
        page.scroll = ft.ScrollMode.AUTO
        
        # Colores del tema
        self.primary_color = ft.colors.BLUE_900
        self.secondary_color = ft.colors.BLUE_100
        self.success_color = ft.colors.GREEN_600
        self.warning_color = ft.colors.ORANGE_600
        self.error_color = ft.colors.RED_600
        
        # Referencias a controles
        self.progress_bar = ft.ProgressBar(width=400, color=self.success_color, value=0)
        self.progress_text = ft.Text("0%", color=ft.colors.WHITE)
        self.content_area = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Text("OVA 1: Bioestadística Esencial para Salud", 
                       size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Universidad Antonio Nariño - Estadística Descriptiva para Ciencias de la Salud",
                       size=14, color=ft.colors.BLUE_200),
                ft.Row([
                    ft.Text("Progreso:", color=ft.colors.WHITE),
                    self.progress_text
                ]),
                self.progress_bar
            ]),
            bgcolor=self.primary_color,
            padding=20
        )
        
        # Navigation
        self.nav_buttons = []
        nav_items = ["Introducción", "Objetivos", "Teoría", "Práctica", "Evaluación", "Recursos"]
        
        for i, item in enumerate(nav_items):
            btn = ft.ElevatedButton(
                text=item,
                on_click=lambda e, idx=i: self.show_section(idx),
                bgcolor=self.secondary_color if i == 0 else ft.colors.WHITE,
                color=self.primary_color if i == 0 else ft.colors.BLACK
            )
            self.nav_buttons.append(btn)
        
        navigation = ft.Container(
            content=ft.Row(self.nav_buttons, scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.colors.WHITE,
            padding=10
        )
        
        # Layout principal
        page.add(
            ft.Column([
                header,
                navigation,
                ft.Container(
                    content=self.content_area,
                    expand=True,
                    padding=20
                )
            ], expand=True)
        )
        
        # Mostrar primera sección
        self.show_section(0)
        page.update()

    def show_section(self, section_idx):
        self.current_section = section_idx
        self.update_progress()
        self.update_navigation()
        
        # Limpiar contenido
        self.content_area.controls.clear()
        
        # Mostrar sección correspondiente
        if section_idx == 0:
            self.show_introduction()
        elif section_idx == 1:
            self.show_objectives()
        elif section_idx == 2:
            self.show_theory()
        elif section_idx == 3:
            self.show_practice()
        elif section_idx == 4:
            self.show_evaluation()
        elif section_idx == 5:
            self.show_resources()
        
        self.content_area.update()

    def update_progress(self):
        progress = ((self.current_section + 1) / 6) * 100
        self.progress_bar.value = progress / 100
        self.progress_text.value = f"{int(progress)}%"
        self.progress_bar.update()
        self.progress_text.update()

    def update_navigation(self):
        for i, btn in enumerate(self.nav_buttons):
            if i == self.current_section:
                btn.bgcolor = self.secondary_color
                btn.color = self.primary_color
            else:
                btn.bgcolor = ft.colors.WHITE
                btn.color = ft.colors.BLACK
            btn.update()

    def show_introduction(self):
        intro_answer = ft.Container(
            content=ft.Text(
                "Variables a considerar: edad (cuantitativa), sexo (cualitativa nominal), "
                "nivel de glucosa (cuantitativa), adherencia al tratamiento (cualitativa ordinal), "
                "tiempo de diagnóstico (cuantitativa), etc.",
                color=ft.colors.GREEN_800
            ),
            bgcolor=ft.colors.GREEN_50,
            padding=10,
            border_radius=5,
            visible=False
        )
        
        def reveal_answer(e):
            intro_answer.visible = True
            e.control.visible = False
            self.content_area.update()
        
        content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text("1", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=self.secondary_color,
                            width=30, height=30,
                            border_radius=15,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Introducción a la Bioestadística", size=24, weight=ft.FontWeight.BOLD)
                    ]),
                    
                    ft.Row([
                        ft.Column([
                            ft.Text("¿Por qué es importante?", size=18, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            ft.Text(
                                "La bioestadística es el lenguaje fundamental para generar, interpretar y validar "
                                "el conocimiento científico en las ciencias de la salud. Es crucial para la toma "
                                "de decisiones clínicas, epidemiológicas y de investigación."
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "Dato importante: El 80% de los errores en investigación médica se deben "
                                    "a una incorrecta identificación y manejo de variables.",
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.ORANGE_800
                                ),
                                bgcolor=ft.colors.ORANGE_50,
                                padding=10,
                                border_radius=5,
                                border=ft.border.left(4, ft.colors.ORANGE_400)
                            )
                        ], expand=True),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Caso Clínico Introductorio", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_800),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Escenario: Un hospital quiere evaluar la efectividad de un nuevo protocolo de atención para pacientes con diabetes tipo 2.", weight=ft.FontWeight.BOLD),
                                        ft.Text("Pregunta: ¿Qué variables necesitamos identificar y cómo las clasificamos?"),
                                        ft.ElevatedButton(
                                            "Ver respuesta",
                                            on_click=reveal_answer,
                                            bgcolor=self.primary_color,
                                            color=ft.colors.WHITE
                                        ),
                                        intro_answer
                                    ]),
                                    bgcolor=ft.colors.WHITE,
                                    padding=10,
                                    border_radius=5
                                )
                            ]),
                            bgcolor=ft.colors.INDIGO_50,
                            padding=15,
                            border_radius=10,
                            expand=True
                        )
                    ]),
                    
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Continuar a Objetivos →",
                            on_click=lambda e: self.show_section(1),
                            bgcolor=self.primary_color,
                            color=ft.colors.WHITE
                        ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(top=20)
                    )
                ]),
                padding=20
            )
        )
        
        self.content_area.controls.append(content)

    def show_objectives(self):
        content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text("2", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.colors.GREEN_600,
                            width=30, height=30,
                            border_radius=15,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Objetivos de Aprendizaje", size=24, weight=ft.FontWeight.BOLD)
                    ]),
                    
                    ft.Row([
                        ft.Column([
                            ft.Text("Objetivo General", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                            ft.Container(
                                content=ft.Text(
                                    "Reconocer tipos de variables, escalas de medición y su impacto en la selección "
                                    "de métodos estadísticos apropiados para el análisis de datos en ciencias de la salud.",
                                    weight=ft.FontWeight.W_500,
                                    color=ft.colors.GREEN_800
                                ),
                                bgcolor=ft.colors.GREEN_50,
                                padding=15,
                                border_radius=5,
                                border=ft.border.all(1, ft.colors.GREEN_200)
                            )
                        ], expand=True),
                        
                        ft.Column([
                            ft.Text("Objetivos Específicos", size=18, weight=ft.FontWeight.BOLD, color=self.primary_color),
                            ft.Column([
                                ft.Row([
                                    ft.Container(
                                        content=ft.Text("1", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
                                        bgcolor=self.secondary_color,
                                        width=20, height=20,
                                        border_radius=10,
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Text("Identificar y clasificar variables según su naturaleza y escala de medición", expand=True)
                                ]),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Text("2", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
                                        bgcolor=self.secondary_color,
                                        width=20, height=20,
                                        border_radius=10,
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Text("Reconocer errores comunes en la clasificación de variables", expand=True)
                                ]),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Text("3", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
                                        bgcolor=self.secondary_color,
                                        width=20, height=20,
                                        border_radius=10,
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Text("Seleccionar estadísticos y gráficos apropiados según el tipo de variable", expand=True)
                                ]),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Text("4", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
                                        bgcolor=self.secondary_color,
                                        width=20, height=20,
                                        border_radius=10,
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Text("Aplicar estos conceptos en contextos clínicos y epidemiológicos", expand=True)
                                ])
                            ])
                        ], expand=True)
                    ]),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Tiempo Estimado", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_800),
                            ft.Row([
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("10", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_600),
                                        ft.Text("min Introducción", size=12, color=ft.colors.GREY_600)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    bgcolor=ft.colors.WHITE,
                                    padding=10,
                                    border_radius=5,
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("30", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_600),
                                        ft.Text("min Teoría", size=12, color=ft.colors.GREY_600)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    bgcolor=ft.colors.WHITE,
                                    padding=10,
                                    border_radius=5,
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("60", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_600),
                                        ft.Text("min Práctica", size=12, color=ft.colors.GREY_600)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    bgcolor=ft.colors.WHITE,
                                    padding=10,
                                    border_radius=5,
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("20", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_600),
                                        ft.Text("min Evaluación", size=12, color=ft.colors.GREY_600)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    bgcolor=ft.colors.WHITE,
                                    padding=10,
                                    border_radius=5,
                                    expand=True
                                )
                            ])
                        ]),
                        bgcolor=ft.colors.INDIGO_50,
                        padding=15,
                        border_radius=10,
                        margin=ft.margin.only(top=20)
                    ),
                    
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Comenzar Teoría →",
                            on_click=lambda e: self.show_section(2),
                            bgcolor=ft.colors.GREEN_600,
                            color=ft.colors.WHITE
                        ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(top=20)
                    )
                ]),
                padding=20
            )
        )
        
        self.content_area.controls.append(content)

    def show_theory(self):
        # Variables para el simulador de clasificación
        self.current_variable_text = ft.Text("Edad del paciente", size=16, weight=ft.FontWeight.BOLD)
        self.classification_feedback = ft.Container(visible=False)
        self.classification_score_text = ft.Text("0/0")
        
        def classify_variable(classification):
            variables = [
                {"name": "Edad del paciente", "correct": "cuantitativa"},
                {"name": "Sexo (M/F)", "correct": "cualitativa"},
                {"name": "Grado de dolor", "correct": "cualitativa"},
                {"name": "Presión arterial", "correct": "cuantitativa"},
                {"name": "Tipo de cáncer", "correct": "cualitativa"}
            ]
            
            current_var = variables[self.classification_total % len(variables)]
            self.classification_total += 1
            
            if classification == current_var["correct"]:
                self.classification_score += 1
                self.classification_feedback.content = ft.Container(
                    content=ft.Text(f"✓ ¡Correcto! {current_var['name']} es una variable {classification}.", 
                                   color=ft.colors.GREEN_700),
                    bgcolor=ft.colors.GREEN_100,
                    padding=10,
                    border_radius=5,
                    border=ft.border.all(1, ft.colors.GREEN_400)
                )
            else:
                self.classification_feedback.content = ft.Container(
                    content=ft.Text(f"✗ Incorrecto. {current_var['name']} es una variable {current_var['correct']}.", 
                                   color=ft.colors.RED_700),
                    bgcolor=ft.colors.RED_100,
                    padding=10,
                    border_radius=5,
                    border=ft.border.all(1, ft.colors.RED_400)
                )
            
            self.classification_feedback.visible = True
            self.classification_score_text.value = f"{self.classification_score}/{self.classification_total}"
            
            # Cambiar a la siguiente variable después de 2 segundos
            def change_variable():
                next_var = variables[self.classification_total % len(variables)]
                self.current_variable_text.value = next_var["name"]
                self.classification_feedback.visible = False
                self.current_variable_text.update()
                self.classification_feedback.update()
            
            # Simular delay
            import threading
            timer = threading.Timer(2.0, change_variable)
            timer.start()
            
            self.classification_feedback.update()
            self.classification_score_text.update()
        
        # Tabs para teoría
        theory_tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Variables",
                    content=ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text("Clasificación de Variables", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Variables Cualitativas", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                        ft.Text("Expresan cualidades o atributos"),
                                        ft.Text("• Nominales: Sin orden (sexo, grupo sanguíneo)", size=12),
                                        ft.Text("• Ordinales: Con orden (grado de dolor, estadio del cáncer)", size=12)
                                    ]),
                                    bgcolor=ft.colors.BLUE_50,
                                    padding=10,
                                    border_radius=5,
                                    border=ft.border.all(1, ft.colors.BLUE_200)
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Variables Cuantitativas", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                                        ft.Text("Expresan cantidades numéricas"),
                                        ft.Text("• Discretas: Valores enteros (número de hijos, episodios)", size=12),
                                        ft.Text("• Continuas: Cualquier valor (peso, presión arterial)", size=12)
                                    ]),
                                    bgcolor=ft.colors.GREEN_50,
                                    padding=10,
                                    border_radius=5,
                                    border=ft.border.all(1, ft.colors.GREEN_200)
                                )
                            ], expand=True),
                            
                            ft.Column([
                                ft.Text("Simulador Interactivo", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Clasifica la siguiente variable:"),
                                        ft.Container(
                                            content=self.current_variable_text,
                                            bgcolor=ft.colors.WHITE,
                                            padding=10,
                                            border_radius=5,
                                            alignment=ft.alignment.center
                                        ),
                                        ft.Row([
                                            ft.ElevatedButton(
                                                "Cualitativa",
                                                on_click=lambda e: classify_variable("cualitativa"),
                                                bgcolor=ft.colors.BLUE_500,
                                                color=ft.colors.WHITE
                                            ),
                                            ft.ElevatedButton(
                                                "Cuantitativa",
                                                on_click=lambda e: classify_variable("cuantitativa"),
                                                bgcolor=ft.colors.GREEN_500,
                                                color=ft.colors.WHITE
                                            )
                                        ]),
                                        self.classification_feedback,
                                        ft.Row([
                                            ft.Text("Puntuación: "),
                                            self.classification_score_text
                                        ])
                                    ]),
                                    bgcolor=ft.colors.GREY_50,
                                    padding=15,
                                    border_radius=5
                                )
                            ], expand=True)
                        ]),
                        padding=20
                    )
                ),
                
                ft.Tab(
                    text="Escalas",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Escalas de Medición", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                            ft.Row([
                                ft.Column([
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Escala Nominal", weight=ft.FontWeight.BOLD, color=ft.colors.RED_800),
                                            ft.Text("Solo clasificación, sin orden", size=12),
                                            ft.Container(
                                                content=ft.Text("Ejemplo: Tipo de sangre (A, B, AB, O)", size=12),
                                                bgcolor=ft.colors.WHITE,
                                                padding=5,
                                                border_radius=3
                                            )
                                        ]),
                                        bgcolor=ft.colors.RED_50,
                                        padding=10,
                                        border_radius=5,
                                        border=ft.border.all(1, ft.colors.RED_200)
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Escala Ordinal", weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_800),
                                            ft.Text("Clasificación con orden, sin distancias iguales", size=12),
                                            ft.Container(
                                                content=ft.Text("Ejemplo: Dolor (leve, moderado, severo)", size=12),
                                                bgcolor=ft.colors.WHITE,
                                                padding=5,
                                                border_radius=3
                                            )
                                        ]),
                                        bgcolor=ft.colors.ORANGE_50,
                                        padding=10,
                                        border_radius=5,
                                        border=ft.border.all(1, ft.colors.ORANGE_200)
                                    )
                                ], expand=True),
                                
                                ft.Column([
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Escala de Intervalo", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                            ft.Text("Orden y distancias iguales, sin cero absoluto", size=12),
                                            ft.Container(
                                                content=ft.Text("Ejemplo: Temperatura en °C", size=12),
                                                bgcolor=ft.colors.WHITE,
                                                padding=5,
                                                border_radius=3
                                            )
                                        ]),
                                        bgcolor=ft.colors.BLUE_50,
                                        padding=10,
                                        border_radius=5,
                                        border=ft.border.all(1, ft.colors.BLUE_200)
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Escala de Razón", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                                            ft.Text("Orden, distancias iguales y cero absoluto", size=12),
                                            ft.Container(
                                                content=ft.Text("Ejemplo: Peso, altura, presión arterial", size=12),
                                                bgcolor=ft.colors.WHITE,
                                                padding=5,
                                                border_radius=3
                                            )
                                        ]),
                                        bgcolor=ft.colors.GREEN_50,
                                        padding=10,
                                        border_radius=5,
                                        border=ft.border.all(1, ft.colors.GREEN_200)
                                    )
                                ], expand=True)
                            ])
                        ]),
                        padding=20
                    )
                ),
                
                ft.Tab(
                    text="Ejemplos",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Ejemplos en Ciencias de la Salud", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                            ft.Row([
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Cardiología", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                        ft.Container(
                                            content=ft.Text("Presión arterial: Cuantitativa continua (razón)", size=12),
                                            bgcolor=ft.colors.WHITE,
                                            padding=5,
                                            border_radius=3
                                        ),
                                        ft.Container(
                                            content=ft.Text("Clase funcional NYHA: Cualitativa ordinal", size=12),
                                            bgcolor=ft.colors.WHITE,
                                            padding=5,
                                            border_radius=3
                                        ),
                                        ft.Container(
                                            content=ft.Text("Tipo de arritmia: Cualitativa nominal", size=12),
                                            bgcolor=ft.colors.WHITE,
                                            padding=5,
                                            border_radius=3
                                        )
                                    ]),
                                    bgcolor=ft.colors.BLUE_50,
                                    padding=15,
                                    border_radius=10,
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Oncología", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                                        ft.Container(
                                            content=ft.Text("Estadio TNM: Cualitativa ordinal", size=12),
                                            bgcolor=ft.colors.WHITE,
                                            padding=5,
                                            border_radius=3
                                        ),
                                        ft.Container(
                                            content=ft.Text("Tamaño del tumor: Cuantitativa continua", size=12),
                                            bgcolor=ft.colors.WHITE,
                                            padding=5,
                                            border_radius=3
                                        ),
                                        ft.Container(
                                            content=ft.Text("Tipo histológico: Cualitativa nominal", size=12),
                                            bgcolor=ft.colors.WHITE,
                                            padding=5,
                                            border_radius=3
                                        )
                                    ]),
                                    bgcolor=ft.colors.GREEN_50,
                                    padding=15,
                                    border_radius=10,
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Epidemiología", weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                                        ft.Container(
                                            content=ft.Text("Incidencia: Cuantitativa continua", size=12),
                                            bgcolor=ft.colors.WHITE,
                                            padding=5,
                                            border_radius=3
                                        ),
                                        ft.Container(
                                            content=ft.Text("Nivel socioeconómico: Cualitativa ordinal", size=12),
                                            bgcolor=ft.colors.WHITE,
                                            padding=5,
                                            border_radius=3
                                        ),
                                        ft.Container(
                                            content=ft.Text("Región geográfica: Cualitativa nominal", size=12),
                                            bgcolor=ft.colors.WHITE,
                                            padding=5,
                                            border_radius=3
                                        )
                                    ]),
                                    bgcolor=ft.colors.PURPLE_50,
                                    padding=15,
                                    border_radius=10,
                                    expand=True
                                )
                            ])
                        ]),
                        padding=20
                    )
                ),
                
                ft.Tab(
                    text="Errores Comunes",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Errores Comunes y Cómo Evitarlos", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("⚠️ Error 1: Confundir Ordinal con Cuantitativa", weight=ft.FontWeight.BOLD, color=ft.colors.RED_800),
                                    ft.Row([
                                        ft.Column([
                                            ft.Text("Incorrecto:", weight=ft.FontWeight.BOLD, color=ft.colors.RED_700),
                                            ft.Container(
                                                content=ft.Text("Tratar 'grado de dolor (1-10)' como cuantitativa y calcular la media.", size=12),
                                                bgcolor=ft.colors.WHITE,
                                                padding=5,
                                                border_radius=3
                                            )
                                        ], expand=True),
                                        ft.Column([
                                            ft.Text("Correcto:", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700),
                                            ft.Container(
                                                content=ft.Text("Es ordinal. Usar mediana y percentiles para resumir.", size=12),
                                                bgcolor=ft.colors.WHITE,
                                                padding=5,
                                                border_radius=3
                                            )
                                        ], expand=True)
                                    ])
                                ]),
                                bgcolor=ft.colors.RED_50,
                                padding=15,
                                border_radius=5,
                                border=ft.border.all(1, ft.colors.RED_200)
                            )
                        ]),
                        padding=20
                    )
                )
            ]
        )
        
        content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text("3", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.colors.PURPLE_600,
                            width=30, height=30,
                            border_radius=15,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Microlección: Tipos de Variables y Escalas", size=24, weight=ft.FontWeight.BOLD)
                    ]),
                    theory_tabs,
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Ir a Práctica Guiada →",
                            on_click=lambda e: self.show_section(3),
                            bgcolor=ft.colors.PURPLE_600,
                            color=ft.colors.WHITE
                        ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(top=20)
                    )
                ]),
                padding=20
            )
        )
        
        self.content_area.controls.append(content)

    def show_practice(self):
        # Simulador de variables
        self.sim_variable_name = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_800)
        self.sim_variable_desc = ft.Text("", size=12, color=ft.colors.INDIGO_600)
        self.sim_feedback = ft.Container(visible=False)
        self.sim_correct_text = ft.Text("0", color=ft.colors.GREEN_600, weight=ft.FontWeight.BOLD)
        self.sim_incorrect_text = ft.Text("0", color=ft.colors.RED_600, weight=ft.FontWeight.BOLD)
        self.sim_percentage_text = ft.Text("0%", color=ft.colors.INDIGO_600, weight=ft.FontWeight.BOLD)
        self.sim_history = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)
        
        self.subtype_question = ft.Container(visible=False)
        self.scale_question = ft.Container(visible=False)
        
        def simulator_answer(step, answer):
            current_var = self.health_variables[self.current_sim_variable]
            is_correct = False
            
            if step == "type":
                is_correct = answer == current_var["type"]
                if is_correct:
                    self.show_subtype_question(current_var["type"])
            elif step == "subtype":
                is_correct = answer == current_var["subtype"]
                if is_correct:
                    self.show_scale_question()
            elif step == "scale":
                is_correct = answer == current_var["scale"]
                self.complete_simulator_question(is_correct)
            
            self.show_simulator_feedback(step, is_correct, current_var)
        
        def next_simulator_variable():
            self.current_sim_variable = (self.current_sim_variable + 1) % len(self.health_variables)
            variable = self.health_variables[self.current_sim_variable]
            
            self.sim_variable_name.value = variable["name"]
            self.sim_variable_desc.value = variable["desc"]
            
            # Reset form
            self.subtype_question.visible = False
            self.scale_question.visible = False
            self.sim_feedback.visible = False
            
            self.sim_variable_name.update()
            self.sim_variable_desc.update()
            self.subtype_question.update()
            self.scale_question.update()
            self.sim_feedback.update()
        
        # Inicializar primera variable
        next_simulator_variable()
        
        practice_tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Caso 1: Diabetes",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Caso Clínico 1: Estudio de Diabetes Tipo 2", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                    ft.Text("Un hospital universitario está realizando un estudio para evaluar el control glucémico en pacientes con diabetes tipo 2. Se recolectaron los siguientes datos de 200 pacientes:")
                                ]),
                                bgcolor=ft.colors.BLUE_50,
                                padding=15,
                                border_radius=10
                            ),
                            ft.Text("Dataset Simulado", weight=ft.FontWeight.BOLD),
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("ID")),
                                    ft.DataColumn(ft.Text("Edad")),
                                    ft.DataColumn(ft.Text("Sexo")),
                                    ft.DataColumn(ft.Text("HbA1c (%)")),
                                    ft.DataColumn(ft.Text("Control")),
                                    ft.DataColumn(ft.Text("Comorbilidades"))
                                ],
                                rows=[
                                    ft.DataRow(cells=[
                                        ft.DataCell(ft.Text("001")),
                                        ft.DataCell(ft.Text("65")),
                                        ft.DataCell(ft.Text("M")),
                                        ft.DataCell(ft.Text("7.2")),
                                        ft.DataCell(ft.Text("Adecuado")),
                                        ft.DataCell(ft.Text("2"))
                                    ]),
                                    ft.DataRow(cells=[
                                        ft.DataCell(ft.Text("002")),
                                        ft.DataCell(ft.Text("58")),
                                        ft.DataCell(ft.Text("F")),
                                        ft.DataCell(ft.Text("9.1")),
                                        ft.DataCell(ft.Text("Inadecuado")),
                                        ft.DataCell(ft.Text("1"))
                                    ]),
                                    ft.DataRow(cells=[
                                        ft.DataCell(ft.Text("003")),
                                        ft.DataCell(ft.Text("72")),
                                        ft.DataCell(ft.Text("F")),
                                        ft.DataCell(ft.Text("6.8")),
                                        ft.DataCell(ft.Text("Óptimo")),
                                        ft.DataCell(ft.Text("0"))
                                    ])
                                ]
                            )
                        ]),
                        padding=20
                    )
                ),
                
                ft.Tab(
                    text="Simulador",
                    content=ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text("Variable a Clasificar", weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_800),
                                ft.Container(
                                    content=ft.Column([
                                        self.sim_variable_name,
                                        self.sim_variable_desc
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    bgcolor=ft.colors.INDIGO_50,
                                    padding=15,
                                    border_radius=10
                                ),
                                
                                ft.Column([
                                    ft.Text("1. Tipo de variable:", weight=ft.FontWeight.W_500),
                                    ft.Row([
                                        ft.ElevatedButton(
                                            "Cualitativa",
                                            on_click=lambda e: simulator_answer("type", "cualitativa"),
                                            bgcolor=ft.colors.BLUE_500,
                                            color=ft.colors.WHITE
                                        ),
                                        ft.ElevatedButton(
                                            "Cuantitativa",
                                            on_click=lambda e: simulator_answer("type", "cuantitativa"),
                                            bgcolor=ft.colors.GREEN_500,
                                            color=ft.colors.WHITE
                                        )
                                    ])
                                ]),
                                
                                self.subtype_question,
                                self.scale_question,
                                self.sim_feedback,
                                
                                ft.ElevatedButton(
                                    "Siguiente Variable",
                                    on_click=lambda e: next_simulator_variable(),
                                    bgcolor=ft.colors.INDIGO_600,
                                    color=ft.colors.WHITE
                                )
                            ], expand=True),
                            
                            ft.Column([
                                ft.Text("Puntuación y Progreso", weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_800),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Row([ft.Text("Correctas:"), self.sim_correct_text]),
                                        ft.Row([ft.Text("Incorrectas:"), self.sim_incorrect_text]),
                                        ft.Row([ft.Text("Porcentaje:"), self.sim_percentage_text])
                                    ]),
                                    bgcolor=ft.colors.INDIGO_50,
                                    padding=10,
                                    border_radius=5
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Historial de Variables:", weight=ft.FontWeight.W_500),
                                        self.sim_history
                                    ]),
                                    bgcolor=ft.colors.GREY_50,
                                    padding=10,
                                    border_radius=5
                                )
                            ], expand=True)
                        ]),
                        padding=20
                    )
                )
            ]
        )
        
        content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text("4", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=self.warning_color,
                            width=30, height=30,
                            border_radius=15,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Práctica Guiada con Casos Clínicos", size=24, weight=ft.FontWeight.BOLD)
                    ]),
                    practice_tabs,
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Ir a Evaluación →",
                            on_click=lambda e: self.show_section(4),
                            bgcolor=self.warning_color,
                            color=ft.colors.WHITE
                        ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(top=20)
                    )
                ]),
                padding=20
            )
        )
        
        self.content_area.controls.append(content)

    def show_subtype_question(self, var_type):
        if var_type == "cualitativa":
            options = [
                ft.ElevatedButton(
                    "Nominal",
                    on_click=lambda e: self.simulator_answer("subtype", "nominal"),
                    bgcolor=ft.colors.BLUE_500,
                    color=ft.colors.WHITE
                ),
                ft.ElevatedButton(
                    "Ordinal",
                    on_click=lambda e: self.simulator_answer("subtype", "ordinal"),
                    bgcolor=ft.colors.GREEN_500,
                    color=ft.colors.WHITE
                )
            ]
        else:
            options = [
                ft.ElevatedButton(
                    "Discreta",
                    on_click=lambda e: self.simulator_answer("subtype", "discreta"),
                    bgcolor=ft.colors.BLUE_500,
                    color=ft.colors.WHITE
                ),
                ft.ElevatedButton(
                    "Continua",
                    on_click=lambda e: self.simulator_answer("subtype", "continua"),
                    bgcolor=ft.colors.GREEN_500,
                    color=ft.colors.WHITE
                )
            ]
        
        self.subtype_question.content = ft.Column([
            ft.Text("2. Subtipo:", weight=ft.FontWeight.W_500),
            ft.Row(options)
        ])
        self.subtype_question.visible = True
        self.subtype_question.update()

    def show_scale_question(self):
        options = [
            ft.ElevatedButton(
                "Nominal",
                on_click=lambda e: self.simulator_answer("scale", "nominal"),
                bgcolor=ft.colors.RED_500,
                color=ft.colors.WHITE
            ),
            ft.ElevatedButton(
                "Ordinal",
                on_click=lambda e: self.simulator_answer("scale", "ordinal"),
                bgcolor=ft.colors.ORANGE_500,
                color=ft.colors.WHITE
            ),
            ft.ElevatedButton(
                "Intervalo",
                on_click=lambda e: self.simulator_answer("scale", "intervalo"),
                bgcolor=ft.colors.BLUE_500,
                color=ft.colors.WHITE
            ),
            ft.ElevatedButton(
                "Razón",
                on_click=lambda e: self.simulator_answer("scale", "razón"),
                bgcolor=ft.colors.GREEN_500,
                color=ft.colors.WHITE
            )
        ]
        
        self.scale_question.content = ft.Column([
            ft.Text("3. Escala de medición:", weight=ft.FontWeight.W_500),
            ft.Row(options[:2]),
            ft.Row(options[2:])
        ])
        self.scale_question.visible = True
        self.scale_question.update()

    def simulator_answer(self, step, answer):
        current_var = self.health_variables[self.current_sim_variable]
        is_correct = False
        
        if step == "type":
            is_correct = answer == current_var["type"]
            if is_correct:
                self.show_subtype_question(current_var["type"])
        elif step == "subtype":
            is_correct = answer == current_var["subtype"]
            if is_correct:
                self.show_scale_question()
        elif step == "scale":
            is_correct = answer == current_var["scale"]
            self.complete_simulator_question(is_correct)
        
        self.show_simulator_feedback(step, is_correct, current_var)

    def show_simulator_feedback(self, step, is_correct, variable):
        if is_correct:
            self.sim_feedback.content = ft.Container(
                content=ft.Text("✓ ¡Correcto!", color=ft.colors.GREEN_700),
                bgcolor=ft.colors.GREEN_100,
                padding=10,
                border_radius=5,
                border=ft.border.all(1, ft.colors.GREEN_400)
            )
        else:
            correct_answer = ""
            if step == "type":
                correct_answer = variable["type"]
            elif step == "subtype":
                correct_answer = variable["subtype"]
            elif step == "scale":
                correct_answer = variable["scale"]
            
            self.sim_feedback.content = ft.Container(
                content=ft.Text(f"✗ Incorrecto. La respuesta correcta es: {correct_answer}", color=ft.colors.RED_700),
                bgcolor=ft.colors.RED_100,
                padding=10,
                border_radius=5,
                border=ft.border.all(1, ft.colors.RED_400)
            )
        
        self.sim_feedback.visible = True
        self.sim_feedback.update()

    def complete_simulator_question(self, is_correct):
        if is_correct:
            self.simulator_score["correct"] += 1
        else:
            self.simulator_score["incorrect"] += 1
        
        self.update_simulator_score()
        self.add_to_simulator_history(is_correct)

    def update_simulator_score(self):
        self.sim_correct_text.value = str(self.simulator_score["correct"])
        self.sim_incorrect_text.value = str(self.simulator_score["incorrect"])
        
        total = self.simulator_score["correct"] + self.simulator_score["incorrect"]
        percentage = int((self.simulator_score["correct"] / total) * 100) if total > 0 else 0
        self.sim_percentage_text.value = f"{percentage}%"
        
        self.sim_correct_text.update()
        self.sim_incorrect_text.update()
        self.sim_percentage_text.update()

    def add_to_simulator_history(self, is_correct):
        variable = self.health_variables[self.current_sim_variable]
        icon = "✓" if is_correct else "✗"
        color = ft.colors.GREEN_600 if is_correct else ft.colors.RED_600
        
        entry = ft.Text(f"{icon} {variable['name']}", size=10, color=color)
        self.sim_history.controls.append(entry)
        self.sim_history.update()

    def show_evaluation(self):
        # Variables para el quiz
        self.quiz_answers = [None] * len(self.quiz_questions)
        self.quiz_feedback_containers = []
        
        def check_quiz_answers():
            score = 0
            for i, question in enumerate(self.quiz_questions):
                if self.quiz_answers[i] is not None:
                    is_correct = self.quiz_answers[i] == question["correct"]
                    if is_correct:
                        score += 1
                        self.quiz_feedback_containers[i].content = ft.Container(
                            content=ft.Text(f"✓ ¡Correcto! {question['explanation']}", color=ft.colors.GREEN_700),
                            bgcolor=ft.colors.GREEN_100,
                            padding=10,
                            border_radius=5,
                            border=ft.border.all(1, ft.colors.GREEN_400)
                        )
                    else:
                        self.quiz_feedback_containers[i].content = ft.Container(
                            content=ft.Text(f"✗ Incorrecto. {question['explanation']}", color=ft.colors.RED_700),
                            bgcolor=ft.colors.RED_100,
                            padding=10,
                            border_radius=5,
                            border=ft.border.all(1, ft.colors.RED_400)
                        )
                    
                    self.quiz_feedback_containers[i].visible = True
                    self.quiz_feedback_containers[i].update()
            
            self.show_quiz_results(score, len(self.quiz_questions))
        
        # Crear preguntas del quiz
        quiz_questions_ui = []
        for i, question in enumerate(self.quiz_questions):
            feedback_container = ft.Container(visible=False)
            self.quiz_feedback_containers.append(feedback_container)
            
            radio_group = ft.RadioGroup(
                content=ft.Column([
                    ft.Radio(value=j, label=option) for j, option in enumerate(question["options"])
                ]),
                on_change=lambda e, idx=i: self.set_quiz_answer(idx, int(e.control.value))
            )
            
            question_ui = ft.Container(
                content=ft.Column([
                    ft.Text(f"Pregunta {i+1} de {len(self.quiz_questions)}", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(question["question"]),
                    radio_group,
                    feedback_container
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=15,
                border_radius=10,
                margin=ft.margin.only(bottom=10)
            )
            quiz_questions_ui.append(question_ui)
        
        self.quiz_results_container = ft.Container(visible=False)
        
        content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text("5", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=self.error_color,
                            width=30, height=30,
                            border_radius=15,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Evaluación Automatizada", size=24, weight=ft.FontWeight.BOLD)
                    ]),
                    
                    ft.Container(
                        content=ft.Text(
                            "Instrucciones: Completa las siguientes preguntas para evaluar tu comprensión. "
                            "Tendrás retroalimentación inmediata y podrás ver tu puntuación final.",
                            color=ft.colors.ORANGE_800
                        ),
                        bgcolor=ft.colors.ORANGE_50,
                        padding=10,
                        border_radius=5,
                        border=ft.border.all(1, ft.colors.ORANGE_200)
                    ),
                    
                    ft.Column(quiz_questions_ui),
                    
                    ft.Row([
                        ft.ElevatedButton(
                            "Verificar Respuestas",
                            on_click=lambda e: check_quiz_answers(),
                            bgcolor=self.error_color,
                            color=ft.colors.WHITE
                        ),
                        ft.ElevatedButton(
                            "Ver Recursos →",
                            on_click=lambda e: self.show_section(5),
                            bgcolor=ft.colors.GREY_600,
                            color=ft.colors.WHITE
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                    self.quiz_results_container
                ]),
                padding=20
            )
        )
        
        self.content_area.controls.append(content)

    def set_quiz_answer(self, question_idx, answer_idx):
        self.quiz_answers[question_idx] = answer_idx

    def show_quiz_results(self, score, total):
        percentage = int((score / total) * 100)
        
        if percentage >= 80:
            message = "¡Excelente! Has demostrado un dominio sólido de los conceptos."
            color_scheme = (ft.colors.GREEN_100, ft.colors.GREEN_400, ft.colors.GREEN_700)
        elif percentage >= 60:
            message = "Buen trabajo. Revisa los conceptos donde tuviste dificultades."
            color_scheme = (ft.colors.YELLOW_100, ft.colors.YELLOW_400, ft.colors.YELLOW_700)
        else:
            message = "Necesitas repasar los conceptos. Te recomendamos revisar la teoría."
            color_scheme = (ft.colors.RED_100, ft.colors.RED_400, ft.colors.RED_700)
        
        self.quiz_results_container.content = ft.Container(
            content=ft.Column([
                ft.Text("Resultados del Quiz", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(f"Puntuación: {score}/{total} ({percentage}%)"),
                ft.Text(message)
            ]),
            bgcolor=color_scheme[0],
            padding=15,
            border_radius=5,
            border=ft.border.all(1, color_scheme[1])
        )
        self.quiz_results_container.visible = True
        self.quiz_results_container.update()
        
        self.quiz_score = score

    def show_resources(self):
        def download_template(template_type):
            content = ""
            filename = ""
            
            if template_type == "variables":
                content = "Variable,Tipo,Subtipo,Escala,Estadístico Recomendado,Gráfico Recomendado\n"
                content += "Edad,Cuantitativa,Continua,Razón,Media y DE,Histograma\n"
                content += "Sexo,Cualitativa,Nominal,Nominal,Moda y frecuencias,Barras\n"
                filename = "plantilla_variables.csv"
            elif template_type == "checklist":
                content = """CHECKLIST DE CLASIFICACIÓN DE VARIABLES

□ ¿La variable expresa una cualidad o una cantidad?
□ Si es cualitativa: ¿existe orden natural entre categorías?
□ Si es cuantitativa: ¿los valores son enteros o pueden ser decimales?
□ ¿Cuál es la escala de medición más apropiada?
□ ¿El estadístico seleccionado es apropiado para esta escala?
□ ¿El gráfico elegido representa adecuadamente los datos?
□ ¿La interpretación considera el contexto clínico?"""
                filename = "checklist_variables.txt"
            elif template_type == "dataset":
                content = "ID,Edad,Sexo,Peso,Altura,Presion_Sistolica,Diabetes,Grado_HTA\n"
                for i in range(1, 51):
                    edad = random.randint(30, 70)
                    sexo = random.choice(['M', 'F'])
                    peso = random.randint(60, 100)
                    altura = round(random.uniform(1.5, 1.9), 2)
                    presion = random.randint(110, 170)
                    diabetes = random.choice(['Si', 'No'])
                    grado = random.choice(['Normal', 'Prehipertension', 'Grado 1', 'Grado 2'])
                    
                    content += f"{i},{edad},{sexo},{peso},{altura},{presion},{diabetes},{grado}\n"
                filename = "dataset_practica.csv"
            
            # Crear archivo y guardarlo
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Mostrar diálogo de confirmación
                def close_dialog(e):
                    dialog.open = False
                    self.content_area.page.update()
                
                dialog = ft.AlertDialog(
                    title=ft.Text("Descarga Completada"),
                    content=ft.Text(f"El archivo {filename} se ha guardado exitosamente."),
                    actions=[ft.TextButton("OK", on_click=close_dialog)]
                )
                
                self.content_area.page.dialog = dialog
                dialog.open = True
                self.content_area.page.update()
                
            except Exception as e:
                print(f"Error al guardar archivo: {e}")
        
        def generate_certificate():
            # Crear certificado simple
            certificate_text = f"""
CERTIFICADO DE COMPLETACIÓN

OVA 1: Bioestadística Esencial para Salud

Estudiante de Ciencias de la Salud

Ha completado exitosamente el módulo de
clasificación de variables y escalas de medición

Fecha: {datetime.now().strftime('%d/%m/%Y')}

Universidad Antonio Nariño
"""
            
            try:
                with open("certificado_ova1.txt", 'w', encoding='utf-8') as f:
                    f.write(certificate_text)
                
                def close_dialog(e):
                    dialog.open = False
                    self.content_area.page.update()
                
                dialog = ft.AlertDialog(
                    title=ft.Text("Certificado Generado"),
                    content=ft.Text("El certificado se ha guardado como certificado_ova1.txt"),
                    actions=[ft.TextButton("OK", on_click=close_dialog)]
                )
                
                self.content_area.page.dialog = dialog
                dialog.open = True
                self.content_area.page.update()
                
            except Exception as e:
                print(f"Error al generar certificado: {e}")
        
        def restart_ova():
            def confirm_restart(e):
                if e.control.text == "Sí":
                    # Reiniciar variables
                    self.current_section = 0
                    self.progress = 0
                    self.classification_score = 0
                    self.classification_total = 0
                    self.simulator_score = {"correct": 0, "incorrect": 0}
                    self.current_sim_variable = 0
                    self.quiz_score = 0
                    
                    # Mostrar primera sección
                    self.show_section(0)
                
                dialog.open = False
                self.content_area.page.update()
            
            dialog = ft.AlertDialog(
                title=ft.Text("Reiniciar OVA"),
                content=ft.Text("¿Estás seguro de que quieres reiniciar la OVA? Se perderá todo el progreso."),
                actions=[
                    ft.TextButton("Sí", on_click=confirm_restart),
                    ft.TextButton("No", on_click=confirm_restart)
                ]
            )
            
            self.content_area.page.dialog = dialog
            dialog.open = True
            self.content_area.page.update()
        
        content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text("6", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.colors.GREY_600,
                            width=30, height=30,
                            border_radius=15,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Recursos Descargables y Material de Apoyo", size=24, weight=ft.FontWeight.BOLD)
                    ]),
                    
                    ft.Row([
                        ft.Column([
                            ft.Text("Material Descargable", size=18, weight=ft.FontWeight.BOLD),
                            
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text("📊", size=20),
                                        ft.Text("Plantilla de Clasificación de Variables", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800)
                                    ]),
                                    ft.Text("Tabla estructurada para clasificar variables en estudios de salud", size=12, color=ft.colors.BLUE_700),
                                    ft.ElevatedButton(
                                        "Descargar CSV",
                                        on_click=lambda e: download_template("variables"),
                                        bgcolor=ft.colors.BLUE_600,
                                        color=ft.colors.WHITE
                                    )
                                ]),
                                bgcolor=ft.colors.BLUE_50,
                                padding=10,
                                border_radius=5,
                                border=ft.border.all(1, ft.colors.BLUE_200),
                                margin=ft.margin.only(bottom=10)
                            ),
                            
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text("📋", size=20),
                                        ft.Text("Checklist de Verificación", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800)
                                    ]),
                                    ft.Text("Lista de verificación para clasificación correcta de variables", size=12, color=ft.colors.GREEN_700),
                                    ft.ElevatedButton(
                                        "Descargar TXT",
                                        on_click=lambda e: download_template("checklist"),
                                        bgcolor=ft.colors.GREEN_600,
                                        color=ft.colors.WHITE
                                    )
                                ]),
                                bgcolor=ft.colors.GREEN_50,
                                padding=10,
                                border_radius=5,
                                border=ft.border.all(1, ft.colors.GREEN_200),
                                margin=ft.margin.only(bottom=10)
                            ),
                            
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text("🗂️", size=20),
                                        ft.Text("Dataset de Práctica", weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_800)
                                    ]),
                                    ft.Text("Datos simulados de pacientes para practicar clasificación", size=12, color=ft.colors.ORANGE_700),
                                    ft.ElevatedButton(
                                        "Descargar CSV",
                                        on_click=lambda e: download_template("dataset"),
                                        bgcolor=ft.colors.ORANGE_600,
                                        color=ft.colors.WHITE
                                    )
                                ]),
                                bgcolor=ft.colors.ORANGE_50,
                                padding=10,
                                border_radius=5,
                                border=ft.border.all(1, ft.colors.ORANGE_200)
                            )
                        ], expand=True),
                        
                        ft.Column([
                            ft.Text("Referencias y Enlaces", size=18, weight=ft.FontWeight.BOLD),
                            
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Lecturas Recomendadas", weight=ft.FontWeight.BOLD),
                                    ft.Text("• Hulley, S. B. (2013). Designing Clinical Research. 4th ed.", size=12),
                                    ft.Text("• Kirkwood, B. R. & Sterne, J. A. (2003). Essential Medical Statistics.", size=12),
                                    ft.Text("• Altman, D. G. (1991). Practical Statistics for Medical Research.", size=12)
                                ]),
                                bgcolor=ft.colors.GREY_50,
                                padding=10,
                                border_radius=5,
                                margin=ft.margin.only(bottom=10)
                            ),
                            
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Software Recomendado", weight=ft.FontWeight.BOLD),
                                    ft.Text("• R/RStudio: Análisis estadístico avanzado", size=12),
                                    ft.Text("• PSPP: Alternativa libre a SPSS", size=12),
                                    ft.Text("• Excel: Análisis básico y visualización", size=12),
                                    ft.Text("• Jamovi: Interfaz gráfica para R", size=12)
                                ]),
                                bgcolor=ft.colors.GREY_50,
                                padding=10,
                                border_radius=5
                            ),
                            
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Actividad de Transferencia", weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_800),
                                    ft.Text("Completa un miniinforme clasificando variables de un estudio real en tu área de interés.", size=12, color=ft.colors.INDIGO_700),
                                    ft.Column([
                                        ft.Checkbox(label="Seleccionar un artículo científico reciente", value=False),
                                        ft.Checkbox(label="Identificar todas las variables del estudio", value=False),
                                        ft.Checkbox(label="Clasificar cada variable usando la plantilla", value=False),
                                        ft.Checkbox(label="Justificar la elección de estadísticos y gráficos", value=False),
                                        ft.Checkbox(label="Redactar un párrafo de interpretación clínica", value=False)
                                    ])
                                ]),
                                bgcolor=ft.colors.INDIGO_50,
                                padding=15,
                                border_radius=10,
                                margin=ft.margin.only(top=15)
                            )
                        ], expand=True)
                    ]),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("¡Felicitaciones!", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                            ft.Text(
                                "Has completado exitosamente la OVA 1: Bioestadística Esencial para Salud. "
                                "Ahora tienes las bases para identificar y clasificar variables correctamente en estudios de ciencias de la salud.",
                                color=ft.colors.GREEN_700
                            ),
                            ft.Row([
                                ft.ElevatedButton(
                                    "Generar Certificado",
                                    on_click=lambda e: generate_certificate(),
                                    bgcolor=ft.colors.GREEN_600,
                                    color=ft.colors.WHITE
                                ),
                                ft.ElevatedButton(
                                    "Reiniciar OVA",
                                    on_click=lambda e: restart_ova(),
                                    bgcolor=ft.colors.GREY_600,
                                    color=ft.colors.WHITE
                                )
                            ])
                        ]),
                        bgcolor=ft.colors.GREEN_50,
                        padding=15,
                        border_radius=10,
                        border=ft.border.all(1, ft.colors.GREEN_200),
                        margin=ft.margin.only(top=20)
                    )
                ]),
                padding=20
            )
        )
        
        self.content_area.controls.append(content)

def main(page: ft.Page):
    app = OVABioestadistica()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)
