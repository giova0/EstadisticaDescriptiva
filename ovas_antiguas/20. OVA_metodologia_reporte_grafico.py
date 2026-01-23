
import flet as ft
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
import time
from datetime import datetime
import json

class OVAApp:
    def __init__(self):
        self.current_section = 1
        self.total_sections = 6
        self.start_time = datetime.now()
        self.quiz_score = 0
        self.progress_bar = None
        self.progress_text = None
        self.main_content = None
        self.page = None
        
        # Datos simulados para gráficos
        self.datasets = {
            'covid': {
                'title': "Casos COVID-19 por Edad",
                'data': [120, 89, 156, 203, 178, 145, 98],
                'labels': ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60+'],
                'problems': [
                    "Título genérico sin contexto temporal",
                    "Colores no accesibles para daltónicos",
                    "Falta unidad de medida en eje Y",
                    "No hay línea de referencia para promedio"
                ]
            },
            'diabetes': {
                'title': "Diabetes por Departamento",
                'data': [8.2, 12.1, 15.7, 9.8, 11.3, 14.2, 10.5],
                'labels': ['Bogotá', 'Antioquia', 'Valle', 'Atlántico', 'Santander', 'Cundinamarca', 'Bolívar'],
                'problems': [
                    "Escala Y no comienza en cero",
                    "Orden alfabético no es el más informativo",
                    "Falta especificar tipo de diabetes",
                    "No incluye intervalos de confianza"
                ]
            },
            'vaccination': {
                'title': "Cobertura de Vacunación",
                'data': [95, 87, 92, 78, 89, 94, 85],
                'labels': ['DPT', 'Polio', 'BCG', 'Hepatitis B', 'Rotavirus', 'Neumococo', 'Influenza'],
                'problems': [
                    "No especifica grupo etario",
                    "Falta meta de cobertura (95%)",
                    "Colores muy similares entre categorías",
                    "No indica período de reporte"
                ]
            }
        }
        
        self.selected_dataset = None
        self.chart_title_field = None
        self.color_palette_dropdown = None
        self.ai_feedback_container = None

    def main(self, page: ft.Page):
        self.page = page
        page.title = "OVA: Mini-metodología de Reporte Gráfico"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.scroll = ft.ScrollMode.AUTO
        
        # Configurar la página
        page.window_width = 1200
        page.window_height = 800
        page.window_resizable = True
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("OVA 1: Mini-metodología de Reporte Gráfico", 
                           size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Estadística Descriptiva para Ciencias de la Salud", 
                           size=18, color=ft.Colors.WHITE70)
                ], expand=True),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Duración estimada", size=12, color=ft.Colors.WHITE70),
                        ft.Text("2-4 horas", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                    padding=15,
                    border_radius=10
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            gradient=ft.LinearGradient([ft.Colors.BLUE_700, ft.Colors.PURPLE_700]),
            padding=20,
            height=120
        )
        
        # Progress Bar
        self.progress_bar = ft.ProgressBar(value=0, width=400, height=8, color=ft.Colors.BLUE_600)
        self.progress_text = ft.Text("0%", size=14, color=ft.Colors.GREY_600)
        
        progress_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Progreso del OVA", size=14, color=ft.Colors.GREY_600),
                    self.progress_text
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar
            ]),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300))
        )
        
        # Main content container
        self.main_content = ft.Column([], scroll=ft.ScrollMode.AUTO, expand=True)
        
        # Footer
        footer = ft.Container(
            content=ft.Column([
                ft.Text("Universidad Antonio Nariño - Proyecto de Investigación", 
                       size=16, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
                ft.Text('"Uso de la inteligencia artificial y el enfoque C(H)ANGE para fortalecer el pensamiento estadístico en estudiantes de Ciencias de la Salud"', 
                       size=12, color=ft.Colors.WHITE70, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.GREY_800,
            padding=20
        )
        
        # Layout principal
        page.add(
            ft.Column([
                header,
                progress_container,
                ft.Container(self.main_content, padding=20, expand=True),
                footer
            ], expand=True)
        )
        
        # Cargar primera sección
        self.load_section_1()
        self.update_progress()

    def update_progress(self):
        progress = (self.current_section / self.total_sections) * 100
        self.progress_bar.value = progress / 100
        self.progress_text.value = f"{int(progress)}%"
        self.page.update()

    def next_section(self, e=None):
        self.current_section += 1
        if self.current_section <= self.total_sections:
            self.main_content.controls.clear()
            if self.current_section == 1:
                self.load_section_1()
            elif self.current_section == 2:
                self.load_section_2()
            elif self.current_section == 3:
                self.load_section_3()
            elif self.current_section == 4:
                self.load_section_4()
            elif self.current_section == 5:
                self.load_section_5()
            elif self.current_section == 6:
                self.load_section_6()
            self.update_progress()
        else:
            self.show_completion()
        self.page.update()

    def load_section_1(self):
        """Sección 1: Introducción y Objetivos"""
        section = ft.Container(
            content=ft.Column([
                # Header de sección
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.TRENDING_UP, size=30, color=ft.Colors.BLUE_600),
                        bgcolor=ft.Colors.BLUE_100,
                        padding=15,
                        border_radius=50
                    ),
                    ft.Text("Introducción y Objetivos de Aprendizaje", 
                           size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                ], alignment=ft.MainAxisAlignment.START),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Contenido principal
                ft.Row([
                    # Columna izquierda
                    ft.Column([
                        ft.Text("¿Por qué es importante?", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                        ft.Text(
                            "En las ciencias de la salud, los gráficos no son solo herramientas de presentación, sino instrumentos críticos para la toma de decisiones clínicas y de salud pública. Una visualización mal diseñada puede llevar a interpretaciones erróneas con consecuencias directas en la atención al paciente.",
                            size=14, color=ft.Colors.GREY_600
                        ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Caso Real", weight=ft.FontWeight.BOLD, color=ft.Colors.RED_800),
                                ft.Text(
                                    "En 2020, múltiples gráficos sobre COVID-19 fueron malinterpretados debido a escalas inadecuadas, llevando a decisiones de política pública incorrectas.",
                                    size=12, color=ft.Colors.RED_700
                                )
                            ]),
                            bgcolor=ft.Colors.RED_50,
                            border=ft.border.only(left=ft.BorderSide(4, ft.Colors.RED_400)),
                            padding=15,
                            margin=ft.margin.only(top=15)
                        )
                    ], expand=True),
                    
                    ft.VerticalDivider(width=40, color=ft.Colors.TRANSPARENT),
                    
                    # Columna derecha
                    ft.Column([
                        ft.Text("Objetivos de Aprendizaje", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
                        ft.Column([
                            self.create_objective_item("Estandarizar la 'gramática' de figuras en ciencias de la salud"),
                            self.create_objective_item("Crear títulos informativos y leyendas claras"),
                            self.create_objective_item("Seleccionar escalas y colores accesibles"),
                            self.create_objective_item("Garantizar reproducibilidad en reportes gráficos")
                        ])
                    ], expand=True)
                ]),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Modelo C(H)ANGE
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.PSYCHOLOGY, color=ft.Colors.WHITE, size=24),
                            ft.Text("Enfoque Pedagógico C(H)ANGE", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                        ]),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.Row([
                            ft.Column([
                                ft.Text("C - Combinatoria:", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=12),
                                ft.Text("Selección óptima de tipos de gráficos según datos", color=ft.Colors.WHITE, size=11),
                                ft.Text("A - Álgebra:", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=12),
                                ft.Text("Transformaciones de escalas y ejes", color=ft.Colors.WHITE, size=11),
                            ], expand=True),
                            ft.Column([
                                ft.Text("N - Números:", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=12),
                                ft.Text("Interpretación numérica precisa", color=ft.Colors.WHITE, size=11),
                                ft.Text("G - Geometría:", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=12),
                                ft.Text("Diseño visual y proporciones", color=ft.Colors.WHITE, size=11),
                            ], expand=True),
                            ft.Column([
                                ft.Text("E - Estadística:", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=12),
                                ft.Text("Representación de datos estadísticos", color=ft.Colors.WHITE, size=11),
                                ft.Text("Salud:", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=12),
                                ft.Text("Contexto clínico y epidemiológico", color=ft.Colors.WHITE, size=11),
                            ], expand=True)
                        ])
                    ]),
                    gradient=ft.LinearGradient([ft.Colors.GREEN_600, ft.Colors.TEAL_600]),
                    padding=20,
                    border_radius=10
                ),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Botón continuar
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("Comenzar Microlección", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.WHITE)
                    ], tight=True),
                    bgcolor=ft.Colors.BLUE_600,
                    on_click=self.next_section,
                    height=50,
                    width=250
                )
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        self.main_content.controls.append(section)

    def create_objective_item(self, text):
        return ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500, size=20),
            ft.Text(text, size=14, expand=True)
        ], alignment=ft.MainAxisAlignment.START)

    def load_section_2(self):
        """Sección 2: Microlección Interactiva"""
        section = ft.Container(
            content=ft.Column([
                # Header
                ft.Row([
                    ft.Icon(ft.Icons.SCIENCE, size=30, color=ft.Colors.BLUE_600),
                    ft.Text("Microlección: Gramática de Gráficos en Salud", 
                           size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                ]),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Asistente IA
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.SMART_TOY, color=ft.Colors.WHITE, size=30),
                            ft.Text("Asistente IA: Dr. GraphIA", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                        ]),
                        ft.Text(
                            "¡Hola! Soy tu asistente de inteligencia artificial especializado en visualización de datos de salud. Te ayudaré a analizar gráficos y sugerir mejoras en tiempo real.",
                            color=ft.Colors.WHITE, size=14
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Consejo inicial: Recuerda que en salud, la claridad puede salvar vidas. Cada elemento visual debe tener un propósito clínico claro.",
                                color=ft.Colors.WHITE, size=12, weight=ft.FontWeight.BOLD
                            ),
                            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                            padding=10,
                            border_radius=5
                        )
                    ]),
                    gradient=ft.LinearGradient([ft.Colors.INDIGO_600, ft.Colors.PURPLE_600]),
                    padding=20,
                    border_radius=10
                ),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Contenido principal
                ft.Row([
                    # Pilares
                    ft.Column([
                        ft.Text("Los 5 Pilares de un Gráfico Médico", size=20, weight=ft.FontWeight.W_600),
                        ft.Column([
                            self.create_pillar_card(1, "Título Informativo", "Debe responder: ¿Qué?, ¿Quién?, ¿Cuándo?, ¿Dónde?"),
                            self.create_pillar_card(2, "Ejes y Escalas Apropiadas", "Escalas lineales vs. logarítmicas, puntos de corte clínicos"),
                            self.create_pillar_card(3, "Leyendas y Etiquetas Claras", "Terminología médica estándar, unidades de medida"),
                            self.create_pillar_card(4, "Colores Accesibles", "Paletas daltónicas, contraste adecuado"),
                            self.create_pillar_card(5, "Reproducibilidad", "Código fuente, datos fuente, metodología")
                        ])
                    ], expand=True),
                    
                    ft.VerticalDivider(width=20, color=ft.Colors.TRANSPARENT),
                    
                    # Panel de detalles
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.TOUCH_APP, size=60, color=ft.Colors.GREY_400),
                            ft.Text("Haz clic en cualquier pilar para ver detalles y ejemplos", 
                                   text_align=ft.TextAlign.CENTER, color=ft.Colors.GREY_500)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                           alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=10,
                        height=400,
                        expand=True,
                        padding=20
                    )
                ]),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("Continuar a Práctica Guiada", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.WHITE)
                    ], tight=True),
                    bgcolor=ft.Colors.GREEN_600,
                    on_click=self.next_section,
                    height=50,
                    width=280
                )
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        self.main_content.controls.append(section)

    def create_pillar_card(self, number, title, description):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(f"{number}. {title}", weight=ft.FontWeight.W_600, size=16),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_600)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(description, size=12, color=ft.Colors.GREY_600)
            ]),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=15,
            margin=ft.margin.only(bottom=10),
            on_click=lambda e, n=number: self.show_pillar_detail(n)
        )

    def show_pillar_detail(self, pillar_num):
        # Aquí se mostraría el detalle del pilar seleccionado
        # Por simplicidad, solo mostramos un diálogo
        details = {
            1: "Título Informativo: Debe incluir variable, población, lugar y tiempo",
            2: "Ejes y Escalas: Usar escalas apropiadas según el tipo de datos",
            3: "Leyendas Claras: Terminología médica estándar y unidades",
            4: "Colores Accesibles: Paletas seguras para daltónicos",
            5: "Reproducibilidad: Código y datos disponibles"
        }
        
        dlg = ft.AlertDialog(
            title=ft.Text(f"Pilar {pillar_num}"),
            content=ft.Text(details.get(pillar_num, "Detalle no disponible")),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: self.close_dialog(dlg))]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def close_dialog(self, dialog):
        dialog.open = False
        self.page.update()

    def load_section_3(self):
        """Sección 3: Práctica Guiada"""
        section = ft.Container(
            content=ft.Column([
                # Header
                ft.Row([
                    ft.Icon(ft.Icons.HANDYMAN, size=30, color=ft.Colors.GREEN_600),
                    ft.Text("Práctica Guiada: Mejorando Gráficos Reales", 
                           size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                ]),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Selección de dataset
                ft.Text("Selecciona un Dataset de Salud", size=20, weight=ft.FontWeight.W_600),
                ft.Row([
                    self.create_dataset_card('covid', 'COVID-19', 'Casos por edad y región', ft.Icons.CORONAVIRUS, ft.Colors.RED_500),
                    self.create_dataset_card('diabetes', 'Diabetes', 'Prevalencia por departamento', ft.Icons.FAVORITE, ft.Colors.BLUE_500),
                    self.create_dataset_card('vaccination', 'Vacunación', 'Cobertura infantil', ft.Icons.VACCINES, ft.Colors.GREEN_500)
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Interfaz de gráficos (inicialmente oculta)
                ft.Container(
                    content=ft.Column([
                        ft.Text("Área de trabajo de gráficos", size=16, color=ft.Colors.GREY_600),
                        ft.Text("Selecciona un dataset para comenzar", size=14, color=ft.Colors.GREY_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    height=300,
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=10,
                    padding=20,
                    alignment=ft.alignment.center
                ),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("Ir a Evaluación", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.WHITE)
                    ], tight=True),
                    bgcolor=ft.Colors.PURPLE_600,
                    on_click=self.next_section,
                    height=50,
                    width=200
                )
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        self.main_content.controls.append(section)

    def create_dataset_card(self, dataset_id, title, description, icon, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=40, color=color),
                ft.Text(title, weight=ft.FontWeight.BOLD, size=16),
                ft.Text(description, size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=200,
            height=120,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(2, ft.Colors.GREY_300),
            border_radius=10,
            padding=15,
            on_click=lambda e, ds=dataset_id: self.load_dataset(ds)
        )

    def load_dataset(self, dataset_id):
        self.selected_dataset = dataset_id
        # Aquí se cargarían los gráficos reales
        # Por simplicidad, solo mostramos un mensaje
        dlg = ft.AlertDialog(
            title=ft.Text("Dataset Cargado"),
            content=ft.Text(f"Has seleccionado el dataset: {self.datasets[dataset_id]['title']}"),
            actions=[ft.TextButton("Continuar", on_click=lambda e: self.close_dialog(dlg))]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def load_section_4(self):
        """Sección 4: Evaluación"""
        quiz_questions = [
            {
                "question": "¿Cuál es el elemento MÁS importante en el título de un gráfico médico?",
                "options": [
                    "El nombre del investigador",
                    "La especificación temporal y poblacional",
                    "El tipo de gráfico utilizado",
                    "La fuente de financiamiento"
                ],
                "correct": 1
            },
            {
                "question": "¿Cuándo es apropiado usar una escala logarítmica?",
                "options": [
                    "Siempre que los datos sean positivos",
                    "Para mostrar crecimiento exponencial o grandes rangos",
                    "Solo para datos de laboratorio",
                    "Nunca en gráficos médicos"
                ],
                "correct": 1
            }
        ]
        
        section = ft.Container(
            content=ft.Column([
                # Header
                ft.Row([
                    ft.Icon(ft.Icons.QUIZ, size=30, color=ft.Colors.PURPLE_600),
                    ft.Text("Evaluación Automatizada", 
                           size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                ]),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Quiz
                ft.Text("Quiz de Conocimientos", size=20, weight=ft.FontWeight.W_600),
                ft.Column([
                    self.create_quiz_question(i, q) for i, q in enumerate(quiz_questions)
                ]),
                
                ft.ElevatedButton(
                    "Enviar Quiz",
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    on_click=self.submit_quiz
                ),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Ejercicio práctico
                ft.Text("Ejercicio Práctico", size=20, weight=ft.FontWeight.W_600),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Caso Clínico: Reporte de Hipertensión", weight=ft.FontWeight.BOLD, size=16),
                        ft.Text(
                            "Eres epidemiólogo en el Ministerio de Salud. Debes crear un gráfico que muestre la prevalencia de hipertensión por grupos de edad para un informe que será presentado al Congreso.",
                            size=14
                        ),
                        ft.TextField(
                            label="Tu propuesta de diseño",
                            multiline=True,
                            min_lines=3,
                            max_lines=5,
                            hint_text="Describe cómo diseñarías este gráfico siguiendo la metodología aprendida..."
                        ),
                        ft.ElevatedButton(
                            "Evaluar con IA",
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE,
                            on_click=self.evaluate_exercise
                        )
                    ]),
                    bgcolor=ft.Colors.YELLOW_50,
                    border=ft.border.all(1, ft.Colors.YELLOW_200),
                    border_radius=10,
                    padding=20
                ),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("Ver Rúbrica y Materiales", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.WHITE)
                    ], tight=True),
                    bgcolor=ft.Colors.ORANGE_600,
                    on_click=self.next_section,
                    height=50,
                    width=280
                )
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        self.main_content.controls.append(section)

    def create_quiz_question(self, index, question):
        return ft.Container(
            content=ft.Column([
                ft.Text(f"{index + 1}. {question['question']}", weight=ft.FontWeight.W_600, size=14),
                ft.RadioGroup(
                    content=ft.Column([
                        ft.Radio(value=str(i), label=option) 
                        for i, option in enumerate(question['options'])
                    ])
                )
            ]),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=15,
            margin=ft.margin.only(bottom=10)
        )

    def submit_quiz(self, e):
        # Simulación de evaluación del quiz
        score = random.randint(70, 100)
        self.quiz_score = score
        
        dlg = ft.AlertDialog(
            title=ft.Text("Resultados del Quiz"),
            content=ft.Text(f"Tu puntuación: {score}/100\n{'¡Excelente trabajo!' if score >= 80 else 'Buen intento, revisa los materiales.'}"),
            actions=[ft.TextButton("Continuar", on_click=lambda e: self.close_dialog(dlg))]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def evaluate_exercise(self, e):
        # Simulación de evaluación con IA
        score = random.randint(75, 95)
        
        dlg = ft.AlertDialog(
            title=ft.Text("Evaluación IA"),
            content=ft.Text(f"Puntuación: {score}/100\n\nFortalezas identificadas:\n• Considera aspectos metodológicos\n• Menciona elementos de diseño\n\nSugerencias:\n• Especifica tipo de gráfico\n• Detalla paleta de colores"),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: self.close_dialog(dlg))]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def load_section_5(self):
        """Sección 5: Rúbrica y Materiales"""
        section = ft.Container(
            content=ft.Column([
                # Header
                ft.Row([
                    ft.Icon(ft.Icons.DOWNLOAD, size=30, color=ft.Colors.ORANGE_600),
                    ft.Text("Rúbrica de Evaluación y Materiales Descargables", 
                           size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                ]),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Rúbrica
                ft.Text("Rúbrica de Evidencias", size=20, weight=ft.FontWeight.W_600),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Criterio", weight=ft.FontWeight.BOLD, expand=1),
                            ft.Text("Excelente (4)", weight=ft.FontWeight.BOLD, expand=1),
                            ft.Text("Bueno (3)", weight=ft.FontWeight.BOLD, expand=1),
                            ft.Text("Satisfactorio (2)", weight=ft.FontWeight.BOLD, expand=1),
                            ft.Text("Necesita Mejora (1)", weight=ft.FontWeight.BOLD, expand=1)
                        ], bgcolor=ft.Colors.GREY_100),
                        ft.Divider(height=1, color=ft.Colors.GREY_300),
                        ft.Row([
                            ft.Text("Título Informativo", expand=1),
                            ft.Text("Incluye qué, quién, cuándo, dónde", expand=1, size=12),
                            ft.Text("Incluye 3 de 4 elementos", expand=1, size=12),
                            ft.Text("Incluye 2 de 4 elementos", expand=1, size=12),
                            ft.Text("Título genérico o ausente", expand=1, size=12)
                        ]),
                        ft.Divider(height=1, color=ft.Colors.GREY_300),
                        ft.Row([
                            ft.Text("Escalas y Ejes", expand=1),
                            ft.Text("Escalas apropiadas, ejes etiquetados", expand=1, size=12),
                            ft.Text("Escalas correctas, etiquetas básicas", expand=1, size=12),
                            ft.Text("Escalas funcionales", expand=1, size=12),
                            ft.Text("Escalas confusas o incorrectas", expand=1, size=12)
                        ])
                    ]),
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=10
                ),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Materiales descargables
                ft.Text("Materiales Descargables", size=20, weight=ft.FontWeight.W_600),
                ft.Row([
                    self.create_download_card("Plantillas de Gráficos", "PDF", ft.Icons.PICTURE_AS_PDF, ft.Colors.RED_500),
                    self.create_download_card("Paletas de Colores", "CSS", ft.Icons.PALETTE, ft.Colors.BLUE_500),
                    self.create_download_card("Scripts R/Python", "ZIP", ft.Icons.CODE, ft.Colors.GREEN_500),
                    self.create_download_card("Checklist de Calidad", "PDF", ft.Icons.CHECKLIST, ft.Colors.PURPLE_500)
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("Actividad de Transferencia", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.WHITE)
                    ], tight=True),
                    bgcolor=ft.Colors.INDIGO_600,
                    on_click=self.next_section,
                    height=50,
                    width=280
                )
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        self.main_content.controls.append(section)

    def create_download_card(self, title, file_type, icon, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=30, color=color),
                ft.Text(title, weight=ft.FontWeight.BOLD, size=14, text_align=ft.TextAlign.CENTER),
                ft.ElevatedButton(
                    f"Descargar {file_type}",
                    bgcolor=color,
                    color=ft.Colors.WHITE,
                    on_click=lambda e, t=title: self.download_material(t)
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=200,
            height=150,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            padding=15
        )

    def download_material(self, material):
        dlg = ft.AlertDialog(
            title=ft.Text("Descarga Simulada"),
            content=ft.Text(f"En un entorno real, se descargaría: {material}"),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog(dlg))]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def load_section_6(self):
        """Sección 6: Actividad de Transferencia"""
        section = ft.Container(
            content=ft.Column([
                # Header
                ft.Row([
                    ft.Icon(ft.Icons.ASSIGNMENT, size=30, color=ft.Colors.INDIGO_600),
                    ft.Text("Actividad de Transferencia: Miniinforme Gráfico", 
                           size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)
                ]),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Proyecto final
                ft.Container(
                    content=ft.Column([
                        ft.Text("Proyecto Final: Informe Epidemiológico", size=20, weight=ft.FontWeight.W_600),
                        ft.Text(
                            "Crea un miniinforme de 2 páginas sobre un problema de salud pública actual, aplicando todos los principios de visualización aprendidos.",
                            size=14
                        ),
                        
                        ft.Row([
                            ft.Column([
                                ft.Text("Requisitos del Informe:", weight=ft.FontWeight.BOLD),
                                ft.Text("• 3-4 gráficos diferentes", size=12),
                                ft.Text("• Títulos informativos completos", size=12),
                                ft.Text("• Paleta de colores accesible", size=12),
                                ft.Text("• Interpretación clínica", size=12),
                                ft.Text("• Código fuente reproducible", size=12)
                            ], expand=True),
                            ft.Column([
                                ft.Text("Temas Sugeridos:", weight=ft.FontWeight.BOLD),
                                ft.Text("• Mortalidad materna en Colombia", size=12),
                                ft.Text("• Resistencia antimicrobiana", size=12),
                                ft.Text("• Salud mental post-pandemia", size=12),
                                ft.Text("• Enfermedades tropicales desatendidas", size=12),
                                ft.Text("• Inequidades en vacunación", size=12)
                            ], expand=True)
                        ])
                    ]),
                    bgcolor=ft.Colors.INDIGO_50,
                    border_radius=10,
                    padding=20
                ),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Espacio de trabajo
                ft.Container(
                    content=ft.Column([
                        ft.Text("Espacio de Trabajo del Proyecto", weight=ft.FontWeight.BOLD, size=16),
                        
                        ft.Dropdown(
                            label="Tema Seleccionado",
                            options=[
                                ft.dropdown.Option("maternal", "Mortalidad materna en Colombia"),
                                ft.dropdown.Option("antimicrobial", "Resistencia antimicrobiana"),
                                ft.dropdown.Option("mental", "Salud mental post-pandemia"),
                                ft.dropdown.Option("tropical", "Enfermedades tropicales desatendidas"),
                                ft.dropdown.Option("vaccination", "Inequidades en vacunación"),
                                ft.dropdown.Option("custom", "Tema personalizado")
                            ],
                            width=400
                        ),
                        
                        ft.TextField(
                            label="Justificación del Tema",
                            multiline=True,
                            min_lines=3,
                            hint_text="Explica por qué este tema es relevante para la salud pública..."
                        ),
                        
                        ft.Row([
                            ft.TextField(label="Gráfico 1: Tipo y descripción", expand=True),
                            ft.TextField(label="Gráfico 2: Tipo y descripción", expand=True)
                        ]),
                        
                        ft.Row([
                            ft.TextField(label="Gráfico 3: Tipo y descripción", expand=True),
                            ft.TextField(label="Gráfico 4: Tipo y descripción (opcional)", expand=True)
                        ]),
                        
                        ft.ElevatedButton(
                            "Enviar Propuesta para Revisión IA",
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE,
                            on_click=self.submit_project
                        )
                    ]),
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=10,
                    padding=20
                ),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                ft.Container(
                    content=ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.EMOJI_EVENTS, color=ft.Colors.WHITE),
                            ft.Text("Completar OVA", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=16)
                        ], tight=True),
                        bgcolor=ft.Colors.GREEN_500,
                        on_click=self.complete_ova,
                        height=60,
                        width=300
                    ),
                    alignment=ft.alignment.center
                )
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        self.main_content.controls.append(section)

    def submit_project(self, e):
        dlg = ft.AlertDialog(
            title=ft.Text("✅ Propuesta Aprobada por IA"),
            content=ft.Text("Evaluación del tema: Relevante y bien justificado para salud pública\nGráficos propuestos: Variedad apropiada\n\nRecomendaciones finales:\n• Usa datos del DANE, INS o fuentes oficiales\n• Incluye intervalos de confianza cuando sea apropiado\n• Documenta todas las fuentes y metodología"),
            actions=[ft.TextButton("Continuar", on_click=lambda e: self.close_dialog(dlg))]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def complete_ova(self, e):
        self.show_completion()

    def show_completion(self):
        """Pantalla de finalización"""
        end_time = datetime.now()
        time_spent = end_time - self.start_time
        minutes = int(time_spent.total_seconds() / 60)
        
        completion = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.EMOJI_EVENTS, size=80, color=ft.Colors.YELLOW_600),
                ft.Text("¡Felicitaciones!", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("Has completado exitosamente el OVA de Mini-metodología de Reporte Gráfico", 
                       size=18, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
                
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Conceptos Dominados", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text("5/5", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                        border_radius=10,
                        padding=15,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Tiempo Invertido", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text(f"{minutes} min", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                        border_radius=10,
                        padding=15,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Puntuación Final", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Text(f"{max(85, self.quiz_score)}/100", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                        border_radius=10,
                        padding=15,
                        expand=True
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.DOWNLOAD, color=ft.Colors.BLUE_600),
                            ft.Text("Descargar Certificado", color=ft.Colors.BLUE_600, weight=ft.FontWeight.BOLD)
                        ], tight=True),
                        bgcolor=ft.Colors.WHITE,
                        on_click=self.download_certificate
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.SHARE, color=ft.Colors.WHITE),
                            ft.Text("Compartir Progreso", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
                        ], tight=True),
                        bgcolor=ft.Colors.BLUE_600,
                        on_click=self.share_progress
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            gradient=ft.LinearGradient([ft.Colors.GREEN_400, ft.Colors.BLUE_500]),
            padding=40,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK))
        )
        
        self.main_content.controls.clear()
        self.main_content.controls.append(completion)
        self.current_section = self.total_sections
        self.update_progress()
        self.page.update()

    def download_certificate(self, e):
        dlg = ft.AlertDialog(
            title=ft.Text("Certificado Generado"),
            content=ft.Text("En un entorno real, esto descargaría un PDF personalizado con tu nombre y puntuación."),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog(dlg))]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def share_progress(self, e):
        dlg = ft.AlertDialog(
            title=ft.Text("Compartir Progreso"),
            content=ft.Text("¡Compartir en redes sociales!\n\nEn un entorno real, esto abriría opciones para compartir en redes sociales."),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog(dlg))]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

def main(page: ft.Page):
    app = OVAApp()
    app.main(page)

if __name__ == "__main__":
    # Para ejecutar como aplicación de escritorio
    ft.app(target=main)
    
    # Para ejecutar como aplicación web (descomenta la línea siguiente)
    # ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
