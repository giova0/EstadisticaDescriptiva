
import flet as ft
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
import base64
import random
import json
import os
from datetime import datetime

class OVA14App:
    def __init__(self):
        self.current_section = 0
        self.quiz_score = 0
        self.quiz_questions = []
        self.current_question = 0
        self.user_responses = {}
        self.progress = 0
        self.accessibility_mode = False
        
        # Datos para simulaciones
        self.bias_data = {
            "seleccion": {
                "title": "Sesgo de Selección",
                "description": "Ocurre cuando la muestra no es representativa de la población objetivo.",
                "examples": [
                    "Muestreo por conveniencia en hospitales",
                    "Autoselección de participantes", 
                    "Pérdidas diferenciales de seguimiento"
                ],
                "impact": "Puede sobrestimar o subestimar la prevalencia real",
                "solutions": [
                    "Muestreo aleatorio estratificado",
                    "Análisis de no respondedores",
                    "Ponderación por probabilidad de selección"
                ]
            },
            "informacion": {
                "title": "Sesgo de Información",
                "description": "Error sistemático en la medición o clasificación de variables.",
                "examples": [
                    "Autorreporte de peso y talla",
                    "Sesgo de memoria en exposiciones pasadas",
                    "Variabilidad entre observadores"
                ],
                "impact": "Puede llevar a clasificación errónea de casos",
                "solutions": [
                    "Estandarización de instrumentos",
                    "Validación de mediciones",
                    "Enmascaramiento de evaluadores"
                ]
            },
            "confusion": {
                "title": "Factor de Confusión", 
                "description": "Variable asociada tanto con la exposición como con el desenlace.",
                "examples": [
                    "Edad en estudios de enfermedades crónicas",
                    "Nivel socioeconómico en estudios nutricionales",
                    "Comorbilidades en estudios clínicos"
                ],
                "impact": "Distorsiona la asociación real entre variables",
                "solutions": [
                    "Estratificación por factor de confusión",
                    "Análisis multivariado",
                    "Emparejamiento en el diseño"
                ]
            }
        }
        
        # Preguntas del quiz
        self.quiz_data = [
            {
                "question": "¿Cuál es la principal característica del sesgo de selección?",
                "options": [
                    "Error en la medición de variables",
                    "Muestra no representativa de la población",
                    "Presencia de factores de confusión",
                    "Pérdida de datos durante el análisis"
                ],
                "correct": 1,
                "explanation": "El sesgo de selección ocurre cuando la muestra no es representativa de la población objetivo, lo que afecta la validez externa del estudio."
            },
            {
                "question": "En un estudio sobre obesidad donde el peso es autorreportado, ¿qué tipo de sesgo es más probable?",
                "options": [
                    "Sesgo de selección",
                    "Sesgo de información", 
                    "Factor de confusión",
                    "Sesgo de publicación"
                ],
                "correct": 1,
                "explanation": "El autorreporte de peso típicamente lleva a subestimación, constituyendo un sesgo de información por error sistemático en la medición."
            },
            {
                "question": "¿Cuál de las siguientes estrategias NO es efectiva para minimizar sesgos de selección?",
                "options": [
                    "Muestreo aleatorio estratificado",
                    "Análisis de no respondedores",
                    "Estandarización de instrumentos",
                    "Ponderación por probabilidad de selección"
                ],
                "correct": 2,
                "explanation": "La estandarización de instrumentos es una estrategia para minimizar sesgos de información, no de selección."
            },
            {
                "question": "Un factor de confusión debe estar asociado con:",
                "options": [
                    "Solo la exposición",
                    "Solo el desenlace", 
                    "Tanto la exposición como el desenlace",
                    "Ninguna de las variables principales"
                ],
                "correct": 2,
                "explanation": "Un factor de confusión debe estar asociado tanto con la exposición como con el desenlace para distorsionar la asociación real."
            },
            {
                "question": "¿Cuál es el impacto más probable de un sesgo de información no diferencial?",
                "options": [
                    "Sobrestimación de la asociación",
                    "Subestimación de la asociación",
                    "No afecta la asociación",
                    "Invierte la dirección de la asociación"
                ],
                "correct": 1,
                "explanation": "El sesgo de información no diferencial típicamente lleva a subestimación de la asociación real (sesgo hacia el nulo)."
            }
        ]

    def main(self, page: ft.Page):
        self.page = page
        page.title = "OVA 14: Diseño y Sesgos en Estudios Descriptivos"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1200
        page.window_height = 800
        page.scroll = ft.ScrollMode.AUTO
        
        # Configurar tema
        page.theme = ft.Theme(
            color_scheme_seed=ft.colors.BLUE,
            visual_density=ft.ThemeVisualDensity.COMFORTABLE
        )
        
        # Variables de UI
        self.progress_bar = ft.ProgressBar(width=400, color=ft.colors.BLUE, bgcolor=ft.colors.GREY_300)
        self.progress_text = ft.Text("0%", size=14, color=ft.colors.GREY_700)
        self.content_area = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        
        # Crear navegación
        self.nav_buttons = []
        sections = ["Introducción", "Microlección", "Práctica", "Evaluación", "Transferencia", "Recursos"]
        
        for i, section in enumerate(sections):
            btn = ft.ElevatedButton(
                text=f"{i+1}. {section}",
                on_click=lambda e, idx=i: self.go_to_section(idx),
                style=ft.ButtonStyle(
                    color=ft.colors.BLUE_700 if i == 0 else ft.colors.GREY_600,
                    bgcolor=ft.colors.BLUE_50 if i == 0 else ft.colors.GREY_100
                )
            )
            self.nav_buttons.append(btn)
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text("OVA 14: Diseño y Sesgos en Estudios Descriptivos", 
                               size=24, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800),
                        ft.Text("Estadística Descriptiva para Ciencias de la Salud - Modelo C(H)ANGE", 
                               size=14, color=ft.colors.GREY_600)
                    ], expand=True),
                    ft.Column([
                        ft.ElevatedButton(
                            text="🔍 Accesibilidad",
                            on_click=self.toggle_accessibility,
                            bgcolor=ft.colors.PURPLE_600,
                            color=ft.colors.WHITE
                        ),
                        ft.Column([
                            ft.Text("Duración estimada", size=12, color=ft.colors.GREY_500),
                            ft.Text("2-4 horas", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600)
                        ])
                    ])
                ]),
                ft.Divider(height=1, color=ft.colors.BLUE_600, thickness=4)
            ]),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
        
        # Progress bar
        progress_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Progreso del aprendizaje", size=12, color=ft.colors.GREY_600),
                    self.progress_text
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar
            ]),
            padding=10,
            bgcolor=ft.colors.WHITE
        )
        
        # Navigation
        nav_container = ft.Container(
            content=ft.Row(
                self.nav_buttons,
                scroll=ft.ScrollMode.AUTO,
                spacing=5
            ),
            padding=10,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
        
        # Layout principal
        page.add(
            ft.Column([
                header,
                progress_container,
                nav_container,
                ft.Container(
                    content=self.content_area,
                    padding=20,
                    expand=True
                )
            ], expand=True)
        )
        
        # Mostrar sección inicial
        self.show_introduction()
        self.update_progress()

    def toggle_accessibility(self, e):
        self.accessibility_mode = not self.accessibility_mode
        if self.accessibility_mode:
            self.page.theme_mode = ft.ThemeMode.DARK
            e.control.text = "🔍 Modo Normal"
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            e.control.text = "🔍 Accesibilidad"
        self.page.update()

    def go_to_section(self, section_index):
        self.current_section = section_index
        
        # Actualizar botones de navegación
        for i, btn in enumerate(self.nav_buttons):
            if i == section_index:
                btn.style.color = ft.colors.BLUE_700
                btn.style.bgcolor = ft.colors.BLUE_50
            else:
                btn.style.color = ft.colors.GREY_600
                btn.style.bgcolor = ft.colors.GREY_100
        
        # Mostrar sección correspondiente
        sections = [
            self.show_introduction,
            self.show_microleccion,
            self.show_practica,
            self.show_evaluacion,
            self.show_transferencia,
            self.show_recursos
        ]
        
        sections[section_index]()
        self.update_progress()
        self.page.update()

    def next_section(self, e):
        if self.current_section < 5:
            self.go_to_section(self.current_section + 1)

    def update_progress(self):
        progress = ((self.current_section + 1) / 6) * 100
        self.progress_bar.value = progress / 100
        self.progress_text.value = f"{int(progress)}%"
        self.page.update()

    def show_introduction(self):
        self.content_area.controls.clear()
        
        # Contenido de introducción
        intro_content = ft.Container(
            content=ft.Column([
                # Bienvenida
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.CHECK_CIRCLE, size=64, color=ft.colors.BLUE_600),
                        ft.Text("Bienvenido a la OVA 14", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text(
                            "Aprenderás a reconocer y evaluar fuentes de sesgo en estudios descriptivos de ciencias de la salud, "
                            "desarrollando pensamiento crítico para la interpretación de evidencia científica.",
                            size=16, text_align=ft.TextAlign.CENTER, color=ft.colors.GREY_600
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20
                ),
                
                # Objetivos y modelo C(H)ANGE
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("🎯", size=20),
                                    bgcolor=ft.colors.BLUE_600,
                                    border_radius=20,
                                    padding=8
                                ),
                                ft.Text("Objetivo Principal", size=18, weight=ft.FontWeight.BOLD)
                            ]),
                            ft.Text(
                                "Reconocer fuentes de sesgo y limitaciones en estudios descriptivos, evaluando su impacto "
                                "en la validez de los resultados y las conclusiones en el contexto de las ciencias de la salud.",
                                size=14, color=ft.colors.GREY_700
                            )
                        ]),
                        bgcolor=ft.colors.BLUE_50,
                        padding=15,
                        border_radius=10,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("⚡", size=20),
                                    bgcolor=ft.colors.GREEN_600,
                                    border_radius=20,
                                    padding=8
                                ),
                                ft.Text("Modelo C(H)ANGE", size=18, weight=ft.FontWeight.BOLD)
                            ]),
                            ft.Text(
                                "Integraremos conceptos de combinatoria (muestreo), álgebra (cálculos), números (estadísticas), "
                                "geometría (visualización) y estadística aplicada a problemas reales de salud.",
                                size=14, color=ft.colors.GREY_700
                            )
                        ]),
                        bgcolor=ft.colors.GREEN_50,
                        padding=15,
                        border_radius=10,
                        expand=True
                    )
                ], spacing=20),
                
                # Competencias
                ft.Container(
                    content=ft.Column([
                        ft.Text("🧠 Competencias a Desarrollar", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_800),
                        ft.Row([
                            ft.Column([
                                ft.Text("✓ Identificar sesgos de selección en muestras de salud", size=14),
                                ft.Text("✓ Reconocer sesgos de información en mediciones clínicas", size=14),
                                ft.Text("✓ Evaluar factores de confusión en análisis descriptivos", size=14)
                            ], expand=True),
                            ft.Column([
                                ft.Text("✓ Cuantificar el impacto de sesgos en resultados", size=14),
                                ft.Text("✓ Proponer estrategias de minimización de sesgos", size=14),
                                ft.Text("✓ Comunicar limitaciones de manera transparente", size=14)
                            ], expand=True)
                        ])
                    ]),
                    bgcolor=ft.colors.YELLOW_50,
                    padding=15,
                    border_radius=10,
                    border=ft.border.left(4, ft.colors.YELLOW_400)
                ),
                
                # Botón continuar
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Comenzar Aprendizaje →",
                        on_click=self.next_section,
                        bgcolor=ft.colors.BLUE_600,
                        color=ft.colors.WHITE,
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.all(15)
                        )
                    ),
                    alignment=ft.alignment.center,
                    padding=20
                )
            ], spacing=20),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
        
        self.content_area.controls.append(intro_content)

    def show_microleccion(self):
        self.content_area.controls.clear()
        
        # Título
        title = ft.Text("Microlección Interactiva", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        
        # Tipos de sesgos
        bias_cards = ft.Row([
            self.create_bias_card("seleccion", "👥", "Sesgo de Selección", "Distorsión por participantes no representativos", ft.colors.RED_50, ft.colors.RED_200),
            self.create_bias_card("informacion", "📊", "Sesgo de Información", "Error en medición o clasificación de variables", ft.colors.BLUE_50, ft.colors.BLUE_200),
            self.create_bias_card("confusion", "🔗", "Factor de Confusión", "Variable que distorsiona la asociación real", ft.colors.GREEN_50, ft.colors.GREEN_200)
        ], spacing=20)
        
        # Panel de detalles (inicialmente oculto)
        self.bias_details = ft.Container(
            content=ft.Text("Selecciona un tipo de sesgo para ver los detalles", text_align=ft.TextAlign.CENTER),
            bgcolor=ft.colors.GREY_50,
            padding=20,
            border_radius=10,
            visible=False
        )
        
        # Simulador
        simulator = self.create_simulator()
        
        # Botón continuar
        continue_btn = ft.Container(
            content=ft.ElevatedButton(
                text="Continuar a Práctica →",
                on_click=self.next_section,
                bgcolor=ft.colors.BLUE_600,
                color=ft.colors.WHITE
            ),
            alignment=ft.alignment.center,
            padding=20
        )
        
        content = ft.Container(
            content=ft.Column([
                title,
                ft.Text("Tipos Principales de Sesgos en Estudios Descriptivos", size=20, weight=ft.FontWeight.BOLD),
                bias_cards,
                self.bias_details,
                simulator,
                continue_btn
            ], spacing=20),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
        
        self.content_area.controls.append(content)

    def create_bias_card(self, bias_type, icon, title, description, bg_color, border_color):
        def on_click(e):
            self.show_bias_details(bias_type)
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(icon, size=32),
                    bgcolor=bg_color,
                    border_radius=50,
                    padding=15,
                    alignment=ft.alignment.center
                ),
                ft.Text(title, size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(description, size=12, text_align=ft.TextAlign.CENTER, color=ft.colors.GREY_700)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=bg_color,
            border=ft.border.all(2, border_color),
            border_radius=10,
            padding=15,
            on_click=on_click,
            expand=True,
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)
        )

    def show_bias_details(self, bias_type):
        details = self.bias_data[bias_type]
        
        examples_text = "\n".join([f"• {example}" for example in details["examples"]])
        solutions_text = "\n".join([f"• {solution}" for solution in details["solutions"]])
        
        self.bias_details.content = ft.Column([
            ft.Text(details["title"], size=20, weight=ft.FontWeight.BOLD),
            ft.Text(details["description"], size=14, color=ft.colors.GREY_700),
            ft.Row([
                ft.Column([
                    ft.Text("Ejemplos Comunes:", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(examples_text, size=12)
                ], expand=True),
                ft.Column([
                    ft.Text("Estrategias de Prevención:", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(solutions_text, size=12)
                ], expand=True)
            ]),
            ft.Container(
                content=ft.Text(f"Impacto: {details['impact']}", size=14, weight=ft.FontWeight.BOLD),
                bgcolor=ft.colors.YELLOW_50,
                padding=10,
                border_radius=5,
                border=ft.border.left(4, ft.colors.YELLOW_400)
            )
        ])
        self.bias_details.visible = True
        self.page.update()

    def create_simulator(self):
        # Controles del simulador
        self.sample_size_slider = ft.Slider(
            min=100, max=1000, value=500, divisions=18,
            label="Tamaño: {value}",
            on_change=self.update_simulation
        )
        
        self.selection_bias_slider = ft.Slider(
            min=0, max=50, value=0, divisions=10,
            label="Selección: {value}%",
            on_change=self.update_simulation
        )
        
        self.information_bias_slider = ft.Slider(
            min=0, max=30, value=0, divisions=6,
            label="Información: {value}%", 
            on_change=self.update_simulation
        )
        
        # Gráfico placeholder
        self.simulation_chart = ft.Container(
            content=ft.Text("Gráfico de simulación aparecerá aquí", text_align=ft.TextAlign.CENTER),
            bgcolor=ft.colors.GREY_100,
            height=300,
            border_radius=10,
            alignment=ft.alignment.center
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("🎮 Simulador de Sesgos", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Explora cómo diferentes sesgos afectan los resultados de un estudio sobre hipertensión arterial.", size=14),
                ft.Row([
                    ft.Column([
                        ft.Text("Configuración del Estudio", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("Tamaño de muestra"),
                        self.sample_size_slider,
                        ft.Text("Sesgo de selección (%)"),
                        self.selection_bias_slider,
                        ft.Text("Sesgo de información (%)"),
                        self.information_bias_slider,
                        ft.ElevatedButton(
                            text="Ejecutar Simulación",
                            on_click=self.run_simulation,
                            bgcolor=ft.colors.PURPLE_600,
                            color=ft.colors.WHITE
                        )
                    ], expand=True),
                    self.simulation_chart
                ], spacing=20)
            ]),
            bgcolor=ft.colors.PURPLE_50,
            padding=15,
            border_radius=10
        )

    def update_simulation(self, e):
        # Actualizar valores en tiempo real
        pass

    def run_simulation(self, e):
        selection_bias = self.selection_bias_slider.value
        information_bias = self.information_bias_slider.value
        
        real_prevalence = 25
        observed_prevalence = real_prevalence * (1 + selection_bias/100) * (1 + information_bias/100)
        
        # Crear gráfico con matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        categories = ['Población Real', 'Muestra Observada', 'Muestra Corregida']
        values = [real_prevalence, observed_prevalence, real_prevalence]
        colors = ['#3B82F6', '#EF4444', '#10B981']
        
        bars = ax.bar(categories, values, color=colors)
        ax.set_ylabel('Prevalencia (%)')
        ax.set_title('Impacto de Sesgos en Prevalencia de Hipertensión')
        ax.set_ylim(0, 50)
        
        # Agregar valores en las barras
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{value:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Convertir a imagen
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        plt.close()
        
        # Actualizar el contenedor del gráfico
        self.simulation_chart.content = ft.Image(
            src_base64=img_base64,
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )
        
        # Mostrar interpretación
        difference = ((observed_prevalence - real_prevalence) / real_prevalence * 100)
        direction = 'sobrestimación' if difference > 0 else 'subestimación'
        
        dialog = ft.AlertDialog(
            title=ft.Text("Resultado de la Simulación"),
            content=ft.Text(
                f"Prevalencia real: {real_prevalence}%\n"
                f"Prevalencia observada: {observed_prevalence:.1f}%\n"
                f"Diferencia: {abs(difference):.1f}% ({direction})\n\n"
                f"Los sesgos de selección ({selection_bias}%) e información ({information_bias}%) "
                f"han resultado en una {direction} de {abs(difference):.1f}% respecto a la prevalencia real."
            ),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: self.close_dialog())]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()

    def show_practica(self):
        self.content_area.controls.clear()
        
        # Caso de estudio
        case_study = ft.Container(
            content=ft.Column([
                ft.Text("📋 Caso de Estudio: Prevalencia de Diabetes en Adultos Mayores", 
                        size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                ft.Text(
                    "Un hospital universitario realizó un estudio descriptivo para estimar la prevalencia de diabetes "
                    "en adultos mayores de 65 años. Se reclutaron 800 pacientes que asistieron a consulta externa "
                    "durante 3 meses consecutivos.",
                    size=14, color=ft.colors.BLUE_700
                )
            ]),
            bgcolor=ft.colors.BLUE_50,
            padding=15,
            border_radius=10,
            border=ft.border.left(4, ft.colors.BLUE_500)
        )
        
        # Datos del estudio
        study_data = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Datos del Estudio", size=16, weight=ft.FontWeight.BOLD),
                    ft.Column([
                        self.create_data_row("Total de participantes:", "800"),
                        self.create_data_row("Casos de diabetes:", "240"),
                        self.create_data_row("Prevalencia observada:", "30%", ft.colors.BLUE_600),
                        self.create_data_row("Edad promedio:", "72.5 años")
                    ])
                ]),
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10,
                padding=15,
                expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Características de la Muestra", size=16, weight=ft.FontWeight.BOLD),
                    self.create_sample_chart()
                ]),
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10,
                padding=15,
                expand=True
            )
        ], spacing=20)
        
        # Análisis de sesgos
        bias_analysis = self.create_bias_analysis()
        
        # Ejercicio de corrección
        correction_exercise = self.create_correction_exercise()
        
        content = ft.Container(
            content=ft.Column([
                ft.Text("Práctica Guiada con Casos Reales", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                case_study,
                study_data,
                bias_analysis,
                correction_exercise,
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Ir a Evaluación →",
                        on_click=self.next_section,
                        bgcolor=ft.colors.BLUE_600,
                        color=ft.colors.WHITE
                    ),
                    alignment=ft.alignment.center,
                    padding=20
                )
            ], spacing=20),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
        
        self.content_area.controls.append(content)

    def create_data_row(self, label, value, color=None):
        return ft.Row([
            ft.Text(label, size=12),
            ft.Text(value, size=12, weight=ft.FontWeight.BOLD, color=color or ft.colors.BLACK)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def create_sample_chart(self):
        # Crear gráfico de dona simple
        fig, ax = plt.subplots(figsize=(6, 4))
        sizes = [45, 55]
        labels = ['Hombres', 'Mujeres']
        colors = ['#3B82F6', '#EC4899']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribución por Sexo')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        plt.close()
        
        return ft.Image(
            src_base64=img_base64,
            width=300,
            height=200,
            fit=ft.ImageFit.CONTAIN
        )

    def create_bias_analysis(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("🔍 Análisis de Sesgos Potenciales", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW_800),
                ft.Column([
                    self.create_bias_analysis_item(
                        "1", "Sesgo de Selección", "⚠️ Alto Riesgo", ft.colors.RED_600,
                        "Muestreo por conveniencia en consulta externa",
                        "Los pacientes que asisten a consulta pueden tener mayor prevalencia de enfermedades",
                        "Muestreo aleatorio en la comunidad o estratificación por estado de salud"
                    ),
                    self.create_bias_analysis_item(
                        "2", "Sesgo de Información", "⚠️ Riesgo Moderado", ft.colors.YELLOW_600,
                        "Diagnóstico basado solo en registros médicos",
                        "Posible subdiagnóstico de diabetes no detectada",
                        "Pruebas de laboratorio estandarizadas para todos los participantes"
                    ),
                    self.create_bias_analysis_item(
                        "3", "Factores de Confusión", "✓ Bajo Riesgo", ft.colors.GREEN_600,
                        "Edad, sexo, índice de masa corporal considerados",
                        "Análisis estratificado por grupos de edad y sexo",
                        "Estimaciones más precisas por subgrupos"
                    )
                ])
            ]),
            bgcolor=ft.colors.YELLOW_50,
            padding=15,
            border_radius=10
        )

    def create_bias_analysis_item(self, number, title, risk, risk_color, problem, impact, solution):
        def toggle_explanation(e):
            explanation.visible = not explanation.visible
            self.page.update()
        
        explanation = ft.Container(
            content=ft.Column([
                ft.Text(f"Problema identificado: {problem}", size=12, weight=ft.FontWeight.BOLD),
                ft.Text(f"Impacto: {impact}", size=12),
                ft.Text(f"Solución: {solution}", size=12)
            ]),
            bgcolor=ft.colors.WHITE,
            padding=10,
            border_radius=5,
            border=ft.border.left(4, risk_color),
            visible=False
        )
        
        return ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Row([
                        ft.Container(
                            content=ft.Text(number, size=12, color=ft.colors.WHITE),
                            bgcolor=risk_color,
                            border_radius=15,
                            padding=5,
                            width=30,
                            height=30,
                            alignment=ft.alignment.center
                        ),
                        ft.Text(title, size=14, weight=ft.FontWeight.BOLD)
                    ]),
                    ft.Text(risk, size=12, color=risk_color)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=ft.colors.WHITE,
                padding=10,
                border_radius=5,
                border=ft.border.all(1, ft.colors.GREY_300),
                on_click=toggle_explanation
            ),
            explanation
        ])

    def create_correction_exercise(self):
        self.selection_correction = ft.TextField(
            label="Factor de corrección por sesgo de selección",
            value="1.0",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=300
        )
        
        self.information_correction = ft.TextField(
            label="Factor de corrección por sesgo de información", 
            value="1.0",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=300
        )
        
        self.correction_result = ft.Container(
            content=ft.Text("Los resultados aparecerán aquí"),
            bgcolor=ft.colors.WHITE,
            padding=15,
            border_radius=5,
            border=ft.border.all(1, ft.colors.GREY_300),
            visible=False
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("💡 Ejercicio: Corrección de Sesgos", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                ft.Text("Calcula la prevalencia corregida considerando los sesgos identificados:", size=14),
                ft.Row([
                    self.selection_correction,
                    self.information_correction
                ], spacing=20),
                ft.ElevatedButton(
                    text="Calcular Prevalencia Corregida",
                    on_click=self.calculate_corrected_prevalence,
                    bgcolor=ft.colors.PURPLE_600,
                    color=ft.colors.WHITE
                ),
                self.correction_result
            ]),
            bgcolor=ft.colors.PURPLE_50,
            padding=15,
            border_radius=10
        )

    def calculate_corrected_prevalence(self, e):
        try:
            original_prevalence = 30
            selection_correction = float(self.selection_correction.value)
            information_correction = float(self.information_correction.value)
            
            corrected_prevalence = original_prevalence * selection_correction * information_correction
            
            direction = 'sobrestimación' if corrected_prevalence > original_prevalence else 'subestimación'
            difference = abs(corrected_prevalence - original_prevalence)
            
            self.correction_result.content = ft.Column([
                ft.Text("Resultado del Análisis:", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Column([
                        ft.Text("Prevalencia Original:", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{original_prevalence}%", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_600)
                    ]),
                    ft.Column([
                        ft.Text("Prevalencia Corregida:", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{corrected_prevalence:.1f}%", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_600)
                    ])
                ]),
                ft.Container(
                    content=ft.Text(
                        f"Interpretación: Después de aplicar las correcciones por sesgos, "
                        f"la prevalencia estimada es {corrected_prevalence:.1f}%, lo que representa "
                        f"una {direction} de {difference:.1f} puntos porcentuales respecto a la estimación original.",
                        size=12
                    ),
                    bgcolor=ft.colors.GREY_50,
                    padding=10,
                    border_radius=5
                )
            ])
            self.correction_result.visible = True
            self.page.update()
            
        except ValueError:
            self.show_error_dialog("Por favor ingresa valores numéricos válidos")

    def show_error_dialog(self, message):
        dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_evaluacion(self):
        self.content_area.controls.clear()
        
        # Instrucciones
        instructions = ft.Container(
            content=ft.Column([
                ft.Text("📝 Instrucciones", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                ft.Text(
                    "Responde las siguientes preguntas sobre sesgos en estudios descriptivos. "
                    "Recibirás retroalimentación inmediata para cada respuesta.",
                    size=14, color=ft.colors.BLUE_700
                )
            ]),
            bgcolor=ft.colors.BLUE_50,
            padding=15,
            border_radius=10,
            border=ft.border.left(4, ft.colors.BLUE_500)
        )
        
        # Contenedor para el quiz
        self.quiz_container = ft.Column()
        
        # Resultados del quiz (inicialmente oculto)
        self.quiz_results = ft.Container(
            content=ft.Column([
                ft.Text("🎉 Resultados de la Evaluación", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                ft.Text("", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700),  # Score display
                ft.Text("", size=14, color=ft.colors.GREEN_700)  # Feedback
            ]),
            bgcolor=ft.colors.GREEN_50,
            padding=15,
            border_radius=10,
            border=ft.border.left(4, ft.colors.GREEN_500),
            visible=False
        )
        
        # Botones
        self.start_quiz_btn = ft.ElevatedButton(
            text="Iniciar Evaluación",
            on_click=self.start_quiz,
            bgcolor=ft.colors.GREEN_600,
            color=ft.colors.WHITE
        )
        
        self.next_to_transfer_btn = ft.ElevatedButton(
            text="Continuar a Transferencia →",
            on_click=self.next_section,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            visible=False
        )
        
        content = ft.Container(
            content=ft.Column([
                ft.Text("Evaluación Automatizada", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                instructions,
                self.quiz_container,
                self.quiz_results,
                ft.Container(
                    content=ft.Row([
                        self.start_quiz_btn,
                        self.next_to_transfer_btn
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    alignment=ft.alignment.center,
                    padding=20
                )
            ], spacing=20),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
        
        self.content_area.controls.append(content)

    def start_quiz(self, e):
        self.quiz_questions = self.quiz_data.copy()
        self.current_question = 0
        self.quiz_score = 0
        
        self.start_quiz_btn.visible = False
        self.generate_quiz_question()
        self.page.update()

    def generate_quiz_question(self):
        if self.current_question >= len(self.quiz_questions):
            self.show_quiz_results()
            return
        
        question = self.quiz_questions[self.current_question]
        
        # Crear radio group para las opciones
        self.answer_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value=str(i), label=option) 
                for i, option in enumerate(question["options"])
            ])
        )
        
        self.quiz_container.controls.clear()
        self.quiz_container.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"Pregunta {self.current_question + 1} de {len(self.quiz_questions)}", 
                               size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Puntuación: {self.quiz_score}/{self.current_question}", 
                               size=12, color=ft.colors.GREY_500)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(question["question"], size=16, weight=ft.FontWeight.BOLD),
                    self.answer_group,
                    ft.ElevatedButton(
                        text="Responder",
                        on_click=self.submit_answer,
                        bgcolor=ft.colors.BLUE_600,
                        color=ft.colors.WHITE
                    ),
                    ft.Container(height=20)  # Espacio para feedback
                ]),
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10,
                padding=15
            )
        )
        self.page.update()

    def submit_answer(self, e):
        if not self.answer_group.value:
            self.show_error_dialog("Por favor selecciona una respuesta")
            return
        
        answer_index = int(self.answer_group.value)
        question = self.quiz_questions[self.current_question]
        is_correct = answer_index == question["correct"]
        
        if is_correct:
            self.quiz_score += 1
        
        # Mostrar feedback
        feedback_color = ft.colors.GREEN_50 if is_correct else ft.colors.RED_50
        feedback_border = ft.colors.GREEN_400 if is_correct else ft.colors.RED_400
        feedback_text_color = ft.colors.GREEN_800 if is_correct else ft.colors.RED_800
        
        feedback = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("✅" if is_correct else "❌", size=20),
                    ft.Text("¡Correcto!" if is_correct else "Incorrecto", 
                           size=16, weight=ft.FontWeight.BOLD, color=feedback_text_color)
                ]),
                ft.Text(question["explanation"], size=14, color=feedback_text_color)
            ]),
            bgcolor=feedback_color,
            padding=15,
            border_radius=10,
            border=ft.border.left(4, feedback_border)
        )
        
        self.quiz_container.controls.append(feedback)
        self.page.update()
        
        # Continuar a la siguiente pregunta después de 3 segundos
        self.page.run_task(self.next_question_delayed)

    async def next_question_delayed(self):
        import asyncio
        await asyncio.sleep(3)
        self.current_question += 1
        self.generate_quiz_question()

    def show_quiz_results(self):
        percentage = (self.quiz_score / len(self.quiz_questions) * 100)
        
        if percentage >= 80:
            feedback_text = "¡Excelente! Has demostrado un sólido entendimiento de los sesgos en estudios descriptivos."
        elif percentage >= 60:
            feedback_text = "Buen trabajo. Tienes una comprensión adecuada, pero podrías revisar algunos conceptos."
        else:
            feedback_text = "Te recomendamos revisar el material y practicar más antes de continuar."
        
        # Actualizar contenido de resultados
        self.quiz_results.content.controls[1].value = f"{self.quiz_score}/{len(self.quiz_questions)} ({percentage:.0f}%)"
        self.quiz_results.content.controls[2].value = feedback_text
        
        self.quiz_container.controls.clear()
        self.quiz_results.visible = True
        self.next_to_transfer_btn.visible = True
        self.page.update()

    def show_transferencia(self):
        self.content_area.controls.clear()
        
        # Proyecto
        project_intro = ft.Container(
            content=ft.Column([
                ft.Text("🎯 Proyecto: Análisis Crítico de Estudio", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_800),
                ft.Text(
                    "Analiza un estudio descriptivo real y elabora un informe sobre los sesgos potenciales "
                    "y su impacto en la validez de los resultados.",
                    size=14, color=ft.colors.ORANGE_700
                )
            ]),
            bgcolor=ft.colors.ORANGE_50,
            padding=15,
            border_radius=10
        )
        
        # Caso para análisis
        case_study = ft.Container(
            content=ft.Column([
                ft.Text("📄 Estudio para Analizar", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Column([
                        ft.Text('"Prevalencia de Obesidad en Estudiantes Universitarios"', 
                               size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "Metodología: Se invitó a participar a todos los estudiantes de una universidad "
                            "mediante correo electrónico. Participaron 1,200 estudiantes (tasa de respuesta: 15%). "
                            "El peso y la talla fueron autorreportados mediante encuesta online.",
                            size=12
                        ),
                        ft.Text(
                            "Resultados: La prevalencia de obesidad (IMC ≥30) fue del 12% "
                            "(IC 95%: 10.1-13.9%). La prevalencia fue mayor en hombres (15%) que en mujeres (9%).",
                            size=12
                        ),
                        ft.Text(
                            'Conclusión: "La prevalencia de obesidad en estudiantes universitarios '
                            'es menor que la reportada en la población general del país (25%)."',
                            size=12
                        )
                    ]),
                    bgcolor=ft.colors.WHITE,
                    padding=15,
                    border_radius=5,
                    border=ft.border.all(1, ft.colors.GREY_300)
                )
            ]),
            bgcolor=ft.colors.GREY_50,
            padding=15,
            border_radius=10
        )
        
        # Formulario de análisis
        analysis_form = self.create_analysis_form()
        
        content = ft.Container(
            content=ft.Column([
                ft.Text("Actividad de Transferencia", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                project_intro,
                case_study,
                analysis_form,
                ft.Container(
                    content=ft.Row([
                        ft.ElevatedButton(
                            text="📄 Generar Informe",
                            on_click=self.generate_report,
                            bgcolor=ft.colors.ORANGE_600,
                            color=ft.colors.WHITE
                        ),
                        ft.ElevatedButton(
                            text="Ver Recursos →",
                            on_click=self.next_section,
                            bgcolor=ft.colors.BLUE_600,
                            color=ft.colors.WHITE
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    padding=20
                )
            ], spacing=20),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
        
        self.content_area.controls.append(content)

    def create_analysis_form(self):
        self.selection_bias_analysis = ft.TextField(
            label="Sesgos de selección identificados",
            multiline=True,
            min_lines=3,
            max_lines=5,
            hint_text="Describe los sesgos de selección que identificas en este estudio..."
        )
        
        self.information_bias_analysis = ft.TextField(
            label="Sesgos de información identificados",
            multiline=True,
            min_lines=3,
            max_lines=5,
            hint_text="Describe los sesgos de información que identificas..."
        )
        
        self.internal_validity_impact = ft.TextField(
            label="¿Cómo afectan estos sesgos la validez interna?",
            multiline=True,
            min_lines=3,
            max_lines=5,
            hint_text="Analiza el impacto en la validez interna..."
        )
        
        self.external_validity_impact = ft.TextField(
            label="¿Cómo afectan la validez externa (generalización)?",
            multiline=True,
            min_lines=3,
            max_lines=5,
            hint_text="Analiza el impacto en la generalización de resultados..."
        )
        
        self.improvement_strategies = ft.TextField(
            label="Estrategias para minimizar sesgos",
            multiline=True,
            min_lines=4,
            max_lines=6,
            hint_text="Propón estrategias específicas para mejorar el diseño del estudio..."
        )
        
        self.interpretation_recommendations = ft.TextField(
            label="Recomendaciones para la interpretación de resultados",
            multiline=True,
            min_lines=3,
            max_lines=5,
            hint_text="¿Cómo deberían interpretarse los resultados considerando las limitaciones?"
        )
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("1. Identificación de Sesgos", size=16, weight=ft.FontWeight.BOLD),
                    self.selection_bias_analysis,
                    self.information_bias_analysis
                ]),
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10,
                padding=15
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("2. Evaluación del Impacto", size=16, weight=ft.FontWeight.BOLD),
                    self.internal_validity_impact,
                    self.external_validity_impact
                ]),
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10,
                padding=15
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("3. Propuestas de Mejora", size=16, weight=ft.FontWeight.BOLD),
                    self.improvement_strategies,
                    self.interpretation_recommendations
                ]),
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10,
                padding=15
            )
        ], spacing=20)

    def generate_report(self, e):
        # Validar que todos los campos estén completos
        if not all([
            self.selection_bias_analysis.value,
            self.information_bias_analysis.value,
            self.internal_validity_impact.value,
            self.external_validity_impact.value
        ]):
            self.show_error_dialog("Por favor completa todos los campos del análisis")
            return
        
        # Generar PDF
        try:
            filename = f"informe_analisis_sesgos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Center
            )
            story.append(Paragraph("Informe de Análisis de Sesgos", title_style))
            story.append(Paragraph("Estudio: Prevalencia de Obesidad en Estudiantes Universitarios", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Contenido
            sections = [
                ("1. Sesgos de Selección Identificados:", self.selection_bias_analysis.value),
                ("2. Sesgos de Información Identificados:", self.information_bias_analysis.value),
                ("3. Impacto en Validez Interna:", self.internal_validity_impact.value),
                ("4. Impacto en Validez Externa:", self.external_validity_impact.value),
                ("5. Estrategias de Mejora:", self.improvement_strategies.value or "No especificado"),
                ("6. Recomendaciones de Interpretación:", self.interpretation_recommendations.value or "No especificado")
            ]
            
            for title, content in sections:
                story.append(Paragraph(title, styles['Heading3']))
                story.append(Paragraph(content, styles['Normal']))
                story.append(Spacer(1, 12))
            
            doc.build(story)
            
            # Mostrar confirmación
            dialog = ft.AlertDialog(
                title=ft.Text("Informe Generado"),
                content=ft.Text(f"¡Informe generado exitosamente!\nArchivo guardado como: {filename}"),
                actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
            )
            self.page.dialog = dialog
            dialog.open = True
            self.page.update()
            
        except Exception as ex:
            self.show_error_dialog(f"Error al generar el informe: {str(ex)}")

    def show_recursos(self):
        self.content_area.controls.clear()
        
        # Checklist
        checklist = ft.Container(
            content=ft.Column([
                ft.Text("📋 Checklist de Evaluación de Sesgos", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                ft.Column([
                    self.create_checklist_item("¿La muestra es representativa de la población objetivo?"),
                    self.create_checklist_item("¿Se utilizaron métodos estandarizados de medición?"),
                    self.create_checklist_item("¿Se consideraron factores de confusión relevantes?"),
                    self.create_checklist_item("¿Se reportaron las limitaciones del estudio?"),
                    self.create_checklist_item("¿Los resultados son clínicamente relevantes?")
                ]),
                ft.ElevatedButton(
                    text="📥 Descargar Checklist",
                    on_click=self.download_checklist,
                    bgcolor=ft.colors.BLUE_600,
                    color=ft.colors.WHITE
                )
            ]),
            bgcolor=ft.colors.BLUE_50,
            padding=15,
            border_radius=10,
            expand=True
        )
        
        # Rúbrica
        rubric = ft.Container(
            content=ft.Column([
                ft.Text("📊 Rúbrica de Evaluación", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                ft.Column([
                    self.create_rubric_item("Excelente (4 puntos)", "Identifica todos los sesgos y propone soluciones viables", ft.colors.GREEN_800),
                    self.create_rubric_item("Bueno (3 puntos)", "Identifica la mayoría de sesgos con análisis adecuado", ft.colors.YELLOW_800),
                    self.create_rubric_item("Regular (2 puntos)", "Identifica algunos sesgos pero análisis superficial", ft.colors.ORANGE_800),
                    self.create_rubric_item("Insuficiente (1 punto)", "No identifica sesgos principales o análisis incorrecto", ft.colors.RED_800)
                ]),
                ft.ElevatedButton(
                    text="📥 Descargar Rúbrica",
                    on_click=self.download_rubric,
                    bgcolor=ft.colors.GREEN_600,
                    color=ft.colors.WHITE
                )
            ]),
            bgcolor=ft.colors.GREEN_50,
            padding=15,
            border_radius=10,
            expand=True
        )
        
        # Plantillas
        templates = ft.Container(
            content=ft.Column([
                ft.Text("📝 Plantillas y Herramientas", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                ft.Column([
                    self.create_template_button("Plantilla de Análisis de Sesgos", "Formato estructurado para evaluar sesgos", "bias-analysis"),
                    self.create_template_button("Guía de Crítica de Estudios", "Pasos para evaluar estudios descriptivos", "study-critique"),
                    self.create_template_button("Guías de Reporte", "Estándares para reportar limitaciones", "reporting-guidelines")
                ])
            ]),
            bgcolor=ft.colors.PURPLE_50,
            padding=15,
            border_radius=10
        )
        
        # Referencias
        references = ft.Container(
            content=ft.Column([
                ft.Text("📚 Referencias y Lecturas Adicionales", size=18, weight=ft.FontWeight.BOLD),
                ft.Column([
                    self.create_reference("Rothman, K. J., Greenland, S., & Lash, T. L. (2008)", 
                                        "Modern Epidemiology. 3rd Edition. Lippincott Williams & Wilkins."),
                    self.create_reference("Hernández-Ávila, M., Garrido, F., & Salinas-Rodríguez, A. (2000)",
                                        "Sesgos en estudios epidemiológicos. Salud Pública de México, 42(5), 438-446."),
                    self.create_reference("Delgado-Rodríguez, M., & Llorca, J. (2004)",
                                        "Bias. Journal of Epidemiology & Community Health, 58(8), 635-641.")
                ])
            ]),
            bgcolor=ft.colors.GREY_50,
            padding=15,
            border_radius=10
        )
        
        content = ft.Container(
            content=ft.Column([
                ft.Text("Recursos y Materiales Descargables", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([checklist, rubric], spacing=20),
                templates,
                references,
                ft.Container(
                    content=ft.ElevatedButton(
                        text="🎓 Completar OVA",
                        on_click=self.complete_course,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.GREEN_600,
                            color=ft.colors.WHITE,
                            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.all(15)
                        )
                    ),
                    alignment=ft.alignment.center,
                    padding=20
                )
            ], spacing=20),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
        
        self.content_area.controls.append(content)

    def create_checklist_item(self, text):
        return ft.Row([
            ft.Checkbox(value=False),
            ft.Text(text, size=12, color=ft.colors.BLUE_700, expand=True)
        ])

    def create_rubric_item(self, level, description, color):
        return ft.Container(
            content=ft.Column([
                ft.Text(level, size=14, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(description, size=12, color=color)
            ]),
            bgcolor=ft.colors.WHITE,
            padding=10,
            border_radius=5,
            border=ft.border.all(1, ft.colors.GREY_300)
        )

    def create_template_button(self, title, description, template_type):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                ft.Text(description, size=12, color=ft.colors.PURPLE_600)
            ]),
            bgcolor=ft.colors.WHITE,
            padding=15,
            border_radius=5,
            border=ft.border.all(1, ft.colors.GREY_300),
            on_click=lambda e, t=template_type: self.download_template(t)
        )

    def create_reference(self, author, title):
        return ft.Container(
            content=ft.Column([
                ft.Text(author, size=12, weight=ft.FontWeight.BOLD),
                ft.Text(title, size=12, color=ft.colors.GREY_600)
            ]),
            bgcolor=ft.colors.WHITE,
            padding=10,
            border_radius=5,
            border=ft.border.all(1, ft.colors.GREY_300)
        )

    def download_checklist(self, e):
        self.create_pdf_document("checklist_evaluacion_sesgos.pdf", "Checklist de Evaluación de Sesgos", [
            "□ ¿La muestra es representativa de la población objetivo?",
            "□ ¿Se utilizaron métodos estandarizados de medición?",
            "□ ¿Se consideraron factores de confusión relevantes?",
            "□ ¿Se reportaron las limitaciones del estudio?",
            "□ ¿Los resultados son clínicamente relevantes?",
            "□ ¿Se evaluó la validez interna del estudio?",
            "□ ¿Se consideró la generalización de los resultados?",
            "□ ¿Se utilizaron métodos apropiados de análisis?",
            "□ ¿Se reportaron intervalos de confianza?",
            "□ ¿Se discutieron sesgos potenciales?"
        ])

    def download_rubric(self, e):
        rubric_content = [
            "EXCELENTE (4 puntos):",
            "• Identifica todos los sesgos principales",
            "• Analiza el impacto de manera precisa",
            "• Propone soluciones viables y específicas",
            "",
            "BUENO (3 puntos):",
            "• Identifica la mayoría de sesgos",
            "• Análisis adecuado del impacto",
            "• Propone algunas soluciones",
            "",
            "REGULAR (2 puntos):",
            "• Identifica algunos sesgos",
            "• Análisis superficial",
            "• Soluciones generales",
            "",
            "INSUFICIENTE (1 punto):",
            "• No identifica sesgos principales",
            "• Análisis incorrecto o ausente",
            "• No propone soluciones"
        ]
        self.create_pdf_document("rubrica_evaluacion_sesgos.pdf", "Rúbrica de Evaluación - Análisis de Sesgos", rubric_content)

    def download_template(self, template_type):
        templates = {
            "bias-analysis": {
                "title": "Plantilla de Análisis de Sesgos",
                "content": [
                    "1. INFORMACIÓN DEL ESTUDIO",
                    "Título: ________________________________",
                    "Tipo de estudio: _______________________",
                    "Población objetivo: ____________________",
                    "Tamaño de muestra: ____________________",
                    "",
                    "2. SESGOS DE SELECCIÓN",
                    "Método de muestreo: ___________________",
                    "Tasa de respuesta: ____________________",
                    "Criterios de inclusión/exclusión: _______",
                    "Evaluación del riesgo: _________________",
                    "",
                    "3. SESGOS DE INFORMACIÓN",
                    "Métodos de medición: __________________",
                    "Validación de instrumentos: ____________",
                    "Enmascaramiento: ______________________",
                    "Evaluación del riesgo: _________________",
                    "",
                    "4. FACTORES DE CONFUSIÓN",
                    "Variables consideradas: ________________",
                    "Métodos de control: ___________________",
                    "Análisis estratificado: ________________"
                ]
            }
        }
        
        template = templates.get(template_type, {"title": "Plantilla", "content": ["Contenido no disponible"]})
        filename = f"{template_type}.pdf"
        self.create_pdf_document(filename, template["title"], template["content"])

    def create_pdf_document(self, filename, title, content):
        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 12))
            
            # Contenido
            for line in content:
                if line.strip():
                    if line.startswith('PASO') or line.includes('ESTRUCTURA') or line.match(r'^\d+\.'):
                        story.append(Paragraph(line, styles['Heading3']))
                    else:
                        story.append(Paragraph(line, styles['Normal']))
                else:
                    story.append(Spacer(1, 6))
            
            doc.build(story)
            
            dialog = ft.AlertDialog(
                title=ft.Text("Descarga Completada"),
                content=ft.Text(f"Archivo guardado como: {filename}"),
                actions=[ft.TextButton("OK", on_click=lambda e: self.close_dialog())]
            )
            self.page.dialog = dialog
            dialog.open = True
            self.page.update()
            
        except Exception as ex:
            self.show_error_dialog(f"Error al crear el documento: {str(ex)}")

    def complete_course(self, e):
        dialog = ft.AlertDialog(
            title=ft.Text("¡Felicitaciones!"),
            content=ft.Text(
                "Has completado exitosamente la OVA 14: Diseño y Sesgos en Estudios Descriptivos.\n\n"
                "Has desarrollado competencias clave para:\n"
                "• Identificar sesgos en estudios de salud\n"
                "• Evaluar la validez de resultados\n"
                "• Proponer mejoras metodológicas\n"
                "• Comunicar limitaciones de manera transparente\n\n"
                "¡Continúa aplicando estos conocimientos en tu práctica profesional!"
            ),
            actions=[ft.TextButton("Finalizar", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

def main(page: ft.Page):
    app = OVA14App()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)
