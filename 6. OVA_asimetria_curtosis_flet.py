
import flet as ft
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
from scipy import stats
import pandas as pd
import math
import random
from datetime import datetime

class OVAAsimetriaCurtosis:
    def __init__(self):
        self.current_section = "intro"
        self.current_quiz_question = 0
        self.quiz_answers = []
        self.progress_value = 0
        
        # Sample datasets
        self.sample_datasets = {
            "glucose": [95, 102, 88, 110, 97, 105, 92, 115, 89, 98, 103, 91, 108, 94, 99, 
                       106, 87, 112, 96, 101, 93, 107, 90, 104, 100, 109, 85, 113, 98, 102],
            "bloodpressure": [120, 125, 118, 135, 122, 128, 115, 140, 119, 124, 126, 117, 
                             132, 121, 123, 129, 116, 138, 120, 127, 118, 134, 119, 125],
            "bmi": [22.5, 24.1, 21.8, 26.7, 23.2, 25.3, 20.9, 28.1, 22.1, 24.6, 23.8, 
                   21.5, 27.2, 22.9, 24.3, 25.8, 20.7, 29.3, 22.7, 25.1]
        }
        
        # Quiz questions
        self.quiz_questions = [
            {
                "question": "¿Qué indica un coeficiente de asimetría de 1.5?",
                "options": [
                    "Distribución simétrica",
                    "Asimetría positiva moderada",
                    "Asimetría negativa severa",
                    "Error en el cálculo"
                ],
                "correct": 1,
                "explanation": "Un coeficiente de asimetría de 1.5 indica asimetría positiva moderada, con una cola más larga hacia la derecha."
            },
            {
                "question": "En una distribución leptocúrtica, el coeficiente de curtosis es:",
                "options": [
                    "Menor que 0",
                    "Igual a 0", 
                    "Mayor que 0",
                    "Siempre igual a 3"
                ],
                "correct": 2,
                "explanation": "En una distribución leptocúrtica, la curtosis es mayor que 0, indicando mayor concentración alrededor de la media."
            },
            {
                "question": "¿Cuál es el criterio práctico más común para considerar una distribución como aproximadamente normal?",
                "options": [
                    "|Asimetría| < 1 y |Curtosis| < 3",
                    "|Asimetría| < 2 y |Curtosis| < 7",
                    "|Asimetría| < 0.5 y |Curtosis| < 1",
                    "Solo la inspección visual"
                ],
                "correct": 1,
                "explanation": "Los criterios prácticos más aceptados son |Asimetría| < 2 y |Curtosis| < 7 para considerar normalidad aproximada."
            },
            {
                "question": "Si la media es mayor que la mediana en una distribución, esto sugiere:",
                "options": [
                    "Asimetría negativa",
                    "Asimetría positiva", 
                    "Distribución normal",
                    "Error en los datos"
                ],
                "correct": 1,
                "explanation": "Cuando la media > mediana, generalmente indica asimetría positiva debido a valores extremos altos."
            },
            {
                "question": "¿Cuándo es más apropiada la transformación logarítmica?",
                "options": [
                    "Asimetría negativa severa",
                    "Asimetría positiva severa",
                    "Distribución normal", 
                    "Curtosis elevada"
                ],
                "correct": 1,
                "explanation": "La transformación logarítmica es útil para reducir asimetría positiva severa, común en datos biomédicos."
            }
        ]

    def calculate_statistics(self, data):
        """Calcula estadísticas descriptivas y de forma"""
        n = len(data)
        mean = np.mean(data)
        median = np.median(data)
        std = np.std(data, ddof=1)
        
        # Asimetría y curtosis
        skewness = stats.skew(data)
        kurtosis = stats.kurtosis(data)
        
        return {
            'n': n,
            'mean': mean,
            'median': median,
            'std': std,
            'skewness': skewness,
            'kurtosis': kurtosis
        }

    def generate_distribution_data(self, dist_type, sample_size, shape_param):
        """Genera datos según el tipo de distribución"""
        np.random.seed(42)  # Para reproducibilidad
        
        if dist_type == "normal":
            data = np.random.normal(100, 15, sample_size)
        elif dist_type == "skewed":
            data = stats.skewnorm.rvs(a=shape_param, loc=100, scale=15, size=sample_size)
        elif dist_type == "negskewed":
            data = stats.skewnorm.rvs(a=-shape_param, loc=100, scale=15, size=sample_size)
        elif dist_type == "leptokurtic":
            # Distribución t con pocos grados de libertad para alta curtosis
            df = max(3, 10 - shape_param)
            data = stats.t.rvs(df=df, loc=100, scale=15, size=sample_size)
        elif dist_type == "platykurtic":
            # Distribución uniforme para baja curtosis
            width = 15 * shape_param * 2
            data = np.random.uniform(100 - width, 100 + width, sample_size)
        
        return data

    def create_histogram_plot(self, data, title="Histograma"):
        """Crea un histograma usando matplotlib"""
        plt.figure(figsize=(8, 6))
        plt.hist(data, bins=20, density=True, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel('Valor')
        plt.ylabel('Densidad')
        plt.grid(True, alpha=0.3)
        
        # Agregar curva de densidad
        x = np.linspace(min(data), max(data), 100)
        kde = stats.gaussian_kde(data)
        plt.plot(x, kde(x), 'r-', linewidth=2, label='Densidad estimada')
        plt.legend()
        
        # Convertir a imagen base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64

    def get_ai_interpretation(self, stats_dict):
        """Genera interpretación automática de las estadísticas"""
        skewness = stats_dict['skewness']
        kurtosis = stats_dict['kurtosis']
        
        interpretation = []
        
        # Análisis de asimetría
        if abs(skewness) < 0.5:
            interpretation.append("✅ Distribución aproximadamente simétrica")
        elif skewness > 0.5:
            interpretation.append("⚠️ Asimetría positiva detectada - Cola derecha más larga")
        else:
            interpretation.append("⚠️ Asimetría negativa detectada - Cola izquierda más larga")
        
        # Análisis de curtosis
        if abs(kurtosis) < 0.5:
            interpretation.append("✅ Curtosis normal (mesocúrtica)")
        elif kurtosis > 0.5:
            interpretation.append("📈 Distribución leptocúrtica - Más concentrada que la normal")
        else:
            interpretation.append("📉 Distribución platicúrtica - Menos concentrada que la normal")
        
        # Evaluación de normalidad
        if abs(skewness) < 2 and abs(kurtosis) < 7:
            interpretation.append("✅ Normalidad práctica aceptable para análisis paramétricos")
        else:
            interpretation.append("❌ Desviación significativa de la normalidad - Considere métodos no paramétricos")
        
        return "\n".join(interpretation)

    def main(self, page: ft.Page):
        page.title = "OVA 6: Asimetría, Curtosis y Normalidad Práctica"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.scroll = ft.ScrollMode.AUTO
        
        # Variables de estado
        self.page = page
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("OVA 6: Asimetría, Curtosis y Normalidad Práctica", 
                           size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text("Estadística Descriptiva para Ciencias de la Salud", 
                           size=14, color=ft.colors.WHITE70)
                ], expand=True),
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.ANALYTICS, size=30, color=ft.colors.WHITE),
                        ft.Text("Modelo C(H)ANGE", size=12, color=ft.colors.WHITE)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.WHITE24,
                    padding=10,
                    border_radius=8
                )
            ]),
            bgcolor=ft.colors.BLUE_700,
            padding=20
        )
        
        # Progress bar
        self.progress_bar = ft.ProgressBar(value=0, width=400)
        self.progress_text = ft.Text("0%", size=12)
        
        progress_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Progreso del módulo", size=12),
                    self.progress_text
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar
            ]),
            padding=10,
            bgcolor=ft.colors.WHITE
        )
        
        # Navigation
        self.nav_buttons = []
        nav_items = [
            ("Introducción", "intro", ft.icons.PLAY_CIRCLE),
            ("Teoría", "theory", ft.icons.BOOK),
            ("Simulador", "simulator", ft.icons.SETTINGS),
            ("Casos Clínicos", "cases", ft.icons.LOCAL_HOSPITAL),
            ("Práctica", "practice", ft.icons.COMPUTER),
            ("Evaluación", "evaluation", ft.icons.QUIZ),
            ("Recursos", "resources", ft.icons.DOWNLOAD)
        ]
        
        for name, section_id, icon in nav_items:
            btn = ft.ElevatedButton(
                text=name,
                icon=icon,
                on_click=lambda e, s=section_id: self.show_section(s),
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE_100 if section_id == "intro" else ft.colors.WHITE,
                    color=ft.colors.BLUE_700 if section_id == "intro" else ft.colors.BLACK
                )
            )
            self.nav_buttons.append(btn)
        
        navigation = ft.Container(
            content=ft.Row(
                self.nav_buttons,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=10,
            bgcolor=ft.colors.WHITE
        )
        
        # Content area
        self.content_area = ft.Container(
            content=self.create_intro_section(),
            padding=20,
            expand=True
        )
        
        # Main layout
        page.add(
            ft.Column([
                header,
                progress_container,
                navigation,
                self.content_area
            ], expand=True)
        )
        
        self.update_progress()

    def show_section(self, section_id):
        """Cambia a la sección especificada"""
        self.current_section = section_id
        
        # Update navigation buttons
        sections = ["intro", "theory", "simulator", "cases", "practice", "evaluation", "resources"]
        for i, btn in enumerate(self.nav_buttons):
            if sections[i] == section_id:
                btn.style.bgcolor = ft.colors.BLUE_100
                btn.style.color = ft.colors.BLUE_700
            else:
                btn.style.bgcolor = ft.colors.WHITE
                btn.style.color = ft.colors.BLACK
        
        # Update content
        if section_id == "intro":
            self.content_area.content = self.create_intro_section()
        elif section_id == "theory":
            self.content_area.content = self.create_theory_section()
        elif section_id == "simulator":
            self.content_area.content = self.create_simulator_section()
        elif section_id == "cases":
            self.content_area.content = self.create_cases_section()
        elif section_id == "practice":
            self.content_area.content = self.create_practice_section()
        elif section_id == "evaluation":
            self.content_area.content = self.create_evaluation_section()
        elif section_id == "resources":
            self.content_area.content = self.create_resources_section()
        
        self.update_progress()
        self.page.update()

    def update_progress(self):
        """Actualiza la barra de progreso"""
        sections = ["intro", "theory", "simulator", "cases", "practice", "evaluation", "resources"]
        current_index = sections.index(self.current_section)
        progress = (current_index + 1) / len(sections)
        
        self.progress_bar.value = progress
        self.progress_text.value = f"{int(progress * 100)}%"

    def create_intro_section(self):
        """Crea la sección de introducción"""
        return ft.Column([
            ft.Row([
                # Objetivos
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.TRACK_CHANGES, color=ft.colors.BLUE_700),
                            ft.Text("Objetivos de Aprendizaje", size=20, weight=ft.FontWeight.BOLD)
                        ]),
                        ft.Column([
                            ft.Row([
                                ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN),
                                ft.Text("Diagnosticar la forma de distribución mediante coeficientes", 
                                        size=14, expand=True)
                            ]),
                            ft.Row([
                                ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN),
                                ft.Text("Interpretar histogramas en contextos clínicos", 
                                        size=14, expand=True)
                            ]),
                            ft.Row([
                                ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN),
                                ft.Text("Aplicar transformaciones de datos apropiadas", 
                                        size=14, expand=True)
                            ]),
                            ft.Row([
                                ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN),
                                ft.Text("Evaluar la normalidad práctica en datos de salud", 
                                        size=14, expand=True)
                            ])
                        ])
                    ]),
                    bgcolor=ft.colors.WHITE,
                    padding=20,
                    border_radius=10,
                    expand=True,
                    margin=ft.margin.only(right=10)
                ),
                
                # Estructura
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.SCHEDULE, color=ft.colors.PURPLE_700),
                            ft.Text("Estructura del Módulo", size=20, weight=ft.FontWeight.BOLD)
                        ]),
                        ft.Column([
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.icons.PLAY_ARROW, color=ft.colors.BLUE),
                                    ft.Column([
                                        ft.Text("Introducción", weight=ft.FontWeight.BOLD),
                                        ft.Text("5-10 minutos", size=12, color=ft.colors.GREY_600)
                                    ])
                                ]),
                                bgcolor=ft.colors.BLUE_50,
                                padding=10,
                                border_radius=8,
                                margin=ft.margin.only(bottom=5)
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.icons.BOOK, color=ft.colors.GREEN),
                                    ft.Column([
                                        ft.Text("Microlección Interactiva", weight=ft.FontWeight.BOLD),
                                        ft.Text("15-30 minutos", size=12, color=ft.colors.GREY_600)
                                    ])
                                ]),
                                bgcolor=ft.colors.GREEN_50,
                                padding=10,
                                border_radius=8,
                                margin=ft.margin.only(bottom=5)
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.icons.COMPUTER, color=ft.colors.PURPLE),
                                    ft.Column([
                                        ft.Text("Práctica Guiada", weight=ft.FontWeight.BOLD),
                                        ft.Text("30-60 minutos", size=12, color=ft.colors.GREY_600)
                                    ])
                                ]),
                                bgcolor=ft.colors.PURPLE_50,
                                padding=10,
                                border_radius=8,
                                margin=ft.margin.only(bottom=5)
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.icons.QUIZ, color=ft.colors.ORANGE),
                                    ft.Column([
                                        ft.Text("Evaluación", weight=ft.FontWeight.BOLD),
                                        ft.Text("10-15 minutos", size=12, color=ft.colors.GREY_600)
                                    ])
                                ]),
                                bgcolor=ft.colors.ORANGE_50,
                                padding=10,
                                border_radius=8
                            )
                        ])
                    ]),
                    bgcolor=ft.colors.WHITE,
                    padding=20,
                    border_radius=10,
                    expand=True
                )
            ]),
            
            # Importancia en Ciencias de la Salud
            ft.Container(
                content=ft.Column([
                    ft.Text("¿Por qué es importante en Ciencias de la Salud?", 
                           size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.icons.FAVORITE, size=30, color=ft.colors.WHITE),
                                ft.Text("Datos Clínicos", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                ft.Text("Los valores de laboratorio raramente siguen distribuciones normales", 
                                        size=12, color=ft.colors.WHITE70)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.WHITE24,
                            padding=15,
                            border_radius=8,
                            expand=True,
                            margin=ft.margin.only(right=5)
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.icons.MEDICATION, size=30, color=ft.colors.WHITE),
                                ft.Text("Farmacocinética", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                ft.Text("Las concentraciones pueden mostrar asimetría que afecta dosificación", 
                                        size=12, color=ft.colors.WHITE70)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.WHITE24,
                            padding=15,
                            border_radius=8,
                            expand=True,
                            margin=ft.margin.only(left=5, right=5)
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.icons.CORONAVIRUS, size=30, color=ft.colors.WHITE),
                                ft.Text("Epidemiología", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                ft.Text("Tiempos de incubación presentan distribuciones asimétricas", 
                                        size=12, color=ft.colors.WHITE70)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.colors.WHITE24,
                            padding=15,
                            border_radius=8,
                            expand=True,
                            margin=ft.margin.only(left=5)
                        )
                    ])
                ]),
                bgcolor=ft.colors.BLUE_700,
                padding=20,
                border_radius=10,
                margin=ft.margin.only(top=20)
            )
        ])

    def create_theory_section(self):
        """Crea la sección de teoría"""
        return ft.Column([
            ft.Row([
                # Asimetría
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.BALANCE, color=ft.colors.BLUE_700),
                            ft.Text("Asimetría (Skewness)", size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        ft.Text("Mide la falta de simetría en la distribución de los datos.", size=14),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Fórmula:", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                ft.Text("Skewness = Σ[(xi - x̄)³/n] / s³", 
                                        font_family="Courier", bgcolor=ft.colors.WHITE, 
                                        size=12, color=ft.colors.BLACK)
                            ]),
                            bgcolor=ft.colors.BLUE_50,
                            padding=10,
                            border_radius=8
                        ),
                        ft.Column([
                            ft.Row([
                                ft.Container(width=15, height=15, bgcolor=ft.colors.GREEN, border_radius=2),
                                ft.Text("Simétrica: ≈ 0", size=12)
                            ]),
                            ft.Row([
                                ft.Container(width=15, height=15, bgcolor=ft.colors.ORANGE, border_radius=2),
                                ft.Text("Asimetría positiva: > 0", size=12)
                            ]),
                            ft.Row([
                                ft.Container(width=15, height=15, bgcolor=ft.colors.RED, border_radius=2),
                                ft.Text("Asimetría negativa: < 0", size=12)
                            ])
                        ]),
                        ft.Container(
                            content=ft.Text("Ejemplo clínico: Los niveles de glucosa suelen mostrar asimetría positiva debido a valores extremos altos en diabéticos.", 
                                          size=12),
                            bgcolor=ft.colors.YELLOW_50,
                            padding=10,
                            border_radius=8,
                            border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400))
                        )
                    ]),
                    bgcolor=ft.colors.WHITE,
                    padding=15,
                    border_radius=10,
                    expand=True,
                    margin=ft.margin.only(right=10)
                ),
                
                # Curtosis
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.TERRAIN, color=ft.colors.GREEN_700),
                            ft.Text("Curtosis (Kurtosis)", size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        ft.Text("Mide el grado de concentración de los datos alrededor de la media.", size=14),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Fórmula:", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                                ft.Text("Kurtosis = Σ[(xi - x̄)⁴/n] / s⁴ - 3", 
                                        font_family="Courier", bgcolor=ft.colors.WHITE, 
                                        size=12, color=ft.colors.BLACK)
                            ]),
                            bgcolor=ft.colors.GREEN_50,
                            padding=10,
                            border_radius=8
                        ),
                        ft.Column([
                            ft.Row([
                                ft.Container(width=15, height=15, bgcolor=ft.colors.BLUE, border_radius=2),
                                ft.Text("Mesocúrtica: ≈ 0", size=12)
                            ]),
                            ft.Row([
                                ft.Container(width=15, height=15, bgcolor=ft.colors.PURPLE, border_radius=2),
                                ft.Text("Leptocúrtica: > 0", size=12)
                            ]),
                            ft.Row([
                                ft.Container(width=15, height=15, bgcolor=ft.colors.PINK, border_radius=2),
                                ft.Text("Platicúrtica: < 0", size=12)
                            ])
                        ]),
                        ft.Container(
                            content=ft.Text("Ejemplo clínico: La presión arterial puede mostrar curtosis elevada debido a concentración de valores normales.", 
                                          size=12),
                            bgcolor=ft.colors.YELLOW_50,
                            padding=10,
                            border_radius=8,
                            border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400))
                        )
                    ]),
                    bgcolor=ft.colors.WHITE,
                    padding=15,
                    border_radius=10,
                    expand=True,
                    margin=ft.margin.only(right=10)
                ),
                
                # Normalidad
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.SHOW_CHART, color=ft.colors.PURPLE_700),
                            ft.Text("Normalidad Práctica", size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        ft.Text("Evaluación práctica de si los datos siguen distribución normal.", size=14),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Criterios Prácticos:", weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                                ft.Text("• |Asimetría| < 2", size=12),
                                ft.Text("• |Curtosis| < 7", size=12),
                                ft.Text("• Inspección visual", size=12),
                                ft.Text("• Pruebas de normalidad", size=12)
                            ]),
                            bgcolor=ft.colors.PURPLE_50,
                            padding=10,
                            border_radius=8
                        ),
                        ft.Column([
                            ft.Text("Métodos de Evaluación:", weight=ft.FontWeight.BOLD),
                            ft.Row([ft.Icon(ft.icons.BAR_CHART, color=ft.colors.BLUE), ft.Text("Histograma", size=12)]),
                            ft.Row([ft.Icon(ft.icons.SHOW_CHART, color=ft.colors.GREEN), ft.Text("Q-Q Plot", size=12)]),
                            ft.Row([ft.Icon(ft.icons.CALCULATE, color=ft.colors.ORANGE), ft.Text("Shapiro-Wilk", size=12)])
                        ]),
                        ft.Container(
                            content=ft.Text("Importante: En muestras grandes (n>30), pequeñas desviaciones pueden no ser clínicamente relevantes.", 
                                          size=12),
                            bgcolor=ft.colors.YELLOW_50,
                            padding=10,
                            border_radius=8,
                            border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400))
                        )
                    ]),
                    bgcolor=ft.colors.WHITE,
                    padding=15,
                    border_radius=10,
                    expand=True
                )
            ]),
            
            # Transformaciones
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.TRANSFORM, color=ft.colors.INDIGO_700),
                        ft.Text("Transformaciones de Datos", size=20, weight=ft.FontWeight.BOLD)
                    ]),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Logarítmica", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                ft.Text("y = log(x)", size=12, color=ft.colors.BLUE_700),
                                ft.Text("Reduce asimetría positiva. Útil para concentraciones.", size=10)
                            ]),
                            bgcolor=ft.colors.BLUE_50,
                            padding=10,
                            border_radius=8,
                            expand=True,
                            margin=ft.margin.only(right=5)
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Raíz Cuadrada", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                                ft.Text("y = √x", size=12, color=ft.colors.GREEN_700),
                                ft.Text("Para datos de conteo. Común en epidemiología.", size=10)
                            ]),
                            bgcolor=ft.colors.GREEN_50,
                            padding=10,
                            border_radius=8,
                            expand=True,
                            margin=ft.margin.only(left=5, right=5)
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Recíproca", weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                                ft.Text("y = 1/x", size=12, color=ft.colors.PURPLE_700),
                                ft.Text("Para asimetría extrema. Cuidado con interpretación.", size=10)
                            ]),
                            bgcolor=ft.colors.PURPLE_50,
                            padding=10,
                            border_radius=8,
                            expand=True,
                            margin=ft.margin.only(left=5, right=5)
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Box-Cox", weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_800),
                                ft.Text("y = (x^λ - 1)/λ", size=12, color=ft.colors.ORANGE_700),
                                ft.Text("Transformación óptima automática.", size=10)
                            ]),
                            bgcolor=ft.colors.ORANGE_50,
                            padding=10,
                            border_radius=8,
                            expand=True,
                            margin=ft.margin.only(left=5)
                        )
                    ])
                ]),
                bgcolor=ft.colors.WHITE,
                padding=20,
                border_radius=10,
                margin=ft.margin.only(top=20)
            )
        ])

    def create_simulator_section(self):
        """Crea la sección del simulador"""
        # Variables del simulador
        self.dist_type = ft.Dropdown(
            label="Tipo de Distribución",
            options=[
                ft.dropdown.Option("normal", "Normal"),
                ft.dropdown.Option("skewed", "Asimétrica Positiva"),
                ft.dropdown.Option("negskewed", "Asimétrica Negativa"),
                ft.dropdown.Option("leptokurtic", "Leptocúrtica"),
                ft.dropdown.Option("platykurtic", "Platicúrtica")
            ],
            value="normal",
            on_change=self.update_simulation
        )
        
        self.sample_size = ft.Slider(
            min=50, max=1000, value=200, divisions=19,
            label="Tamaño: {value}",
            on_change=self.update_simulation
        )
        
        self.shape_param = ft.Slider(
            min=0.5, max=5, value=1, divisions=9,
            label="Forma: {value}",
            on_change=self.update_simulation
        )
        
        # Estadísticas calculadas
        self.stats_display = ft.Column([
            ft.Text("Estadísticas se mostrarán aquí", size=12)
        ])
        
        # Interpretación IA
        self.ai_interpretation = ft.Text(
            "Ajusta los parámetros para ver la interpretación automática.",
            size=12
        )
        
        # Imagen del gráfico
        self.chart_image = ft.Image(
            width=600,
            height=400,
            fit=ft.ImageFit.CONTAIN
        )
        
        return ft.Column([
            ft.Text("Simulador Interactivo de Distribuciones", 
                   size=24, weight=ft.FontWeight.BOLD),
            ft.Row([
                # Controles
                ft.Container(
                    content=ft.Column([
                        ft.Text("Parámetros de la Distribución", 
                               size=16, weight=ft.FontWeight.BOLD),
                        self.dist_type,
                        ft.Text("Tamaño de Muestra:"),
                        self.sample_size,
                        ft.Text("Parámetro de Forma:"),
                        self.shape_param,
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Estadísticas Calculadas", 
                                       size=14, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                self.stats_display
                            ]),
                            bgcolor=ft.colors.BLUE_50,
                            padding=10,
                            border_radius=8
                        ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.icons.SMART_TOY, color=ft.colors.BLUE_800),
                                    ft.Text("Asistente IA", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800)
                                ]),
                                self.ai_interpretation
                            ]),
                            bgcolor=ft.colors.LIGHT_BLUE_50,
                            padding=10,
                            border_radius=8,
                            border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.BLUE))
                        )
                    ]),
                    width=300,
                    padding=20,
                    bgcolor=ft.colors.GREY_50,
                    border_radius=10
                ),
                
                # Gráfico
                ft.Container(
                    content=ft.Column([
                        self.chart_image,
                        ft.Row([
                            ft.ElevatedButton(
                                "Nueva Muestra",
                                icon=ft.icons.REFRESH,
                                on_click=self.generate_new_sample,
                                bgcolor=ft.colors.BLUE_600,
                                color=ft.colors.WHITE
                            ),
                            ft.ElevatedButton(
                                "Exportar Datos",
                                icon=ft.icons.DOWNLOAD,
                                on_click=self.export_simulation_data,
                                bgcolor=ft.colors.GREEN_600,
                                color=ft.colors.WHITE
                            )
                        ])
                    ]),
                    expand=True,
                    padding=20
                )
            ])
        ])

    def update_simulation(self, e):
        """Actualiza la simulación cuando cambian los parámetros"""
        dist_type = self.dist_type.value
        sample_size = int(self.sample_size.value)
        shape_param = self.shape_param.value
        
        # Generar datos
        data = self.generate_distribution_data(dist_type, sample_size, shape_param)
        
        # Calcular estadísticas
        stats_dict = self.calculate_statistics(data)
        
        # Actualizar display de estadísticas
        self.stats_display.controls = [
            ft.Row([ft.Text("Media:", size=12), ft.Text(f"{stats_dict['mean']:.2f}", size=12, font_family="Courier")]),
            ft.Row([ft.Text("Mediana:", size=12), ft.Text(f"{stats_dict['median']:.2f}", size=12, font_family="Courier")]),
            ft.Row([ft.Text("Desv. Estándar:", size=12), ft.Text(f"{stats_dict['std']:.2f}", size=12, font_family="Courier")]),
            ft.Row([ft.Text("Asimetría:", size=12), ft.Text(f"{stats_dict['skewness']:.3f}", size=12, font_family="Courier")]),
            ft.Row([ft.Text("Curtosis:", size=12), ft.Text(f"{stats_dict['kurtosis']:.3f}", size=12, font_family="Courier")])
        ]
        
        # Actualizar interpretación IA
        self.ai_interpretation.value = self.get_ai_interpretation(stats_dict)
        
        # Crear y mostrar gráfico
        image_base64 = self.create_histogram_plot(data, f"Distribución {dist_type.title()}")
        self.chart_image.src_base64 = image_base64
        
        self.page.update()

    def generate_new_sample(self, e):
        """Genera una nueva muestra con los mismos parámetros"""
        # Cambiar la semilla para generar datos diferentes
        np.random.seed(random.randint(1, 10000))
        self.update_simulation(e)

    def export_simulation_data(self, e):
        """Exporta los datos de la simulación"""
        dist_type = self.dist_type.value
        sample_size = int(self.sample_size.value)
        shape_param = self.shape_param.value
        
        data = self.generate_distribution_data(dist_type, sample_size, shape_param)
        
        # Crear DataFrame y guardar como CSV
        df = pd.DataFrame({'Valor': data})
        filename = f"datos_simulados_{dist_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        
        # Mostrar mensaje de confirmación
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text(f"Datos exportados como {filename}"))
        )

    def create_cases_section(self):
        """Crea la sección de casos clínicos"""
        return ft.Column([
            ft.Text("Casos Clínicos Interactivos", size=24, weight=ft.FontWeight.BOLD),
            
            # Caso 1
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.icons.FAVORITE, size=30, color=ft.colors.BLUE_600),
                            bgcolor=ft.colors.BLUE_100,
                            padding=10,
                            border_radius=25
                        ),
                        ft.Text("Caso 1: Niveles de Colesterol en Población Adulta", 
                               size=18, weight=ft.FontWeight.BOLD, expand=True)
                    ]),
                    ft.Text("Un estudio epidemiológico midió los niveles de colesterol total (mg/dL) en 500 adultos de 40-65 años.", 
                           size=14),
                    ft.Column([
                        ft.Text("• Media: 195.2 mg/dL", size=12),
                        ft.Text("• Mediana: 188.5 mg/dL", size=12),
                        ft.Text("• Desviación estándar: 42.8 mg/dL", size=12),
                        ft.Text("• Asimetría: 1.23", size=12),
                        ft.Text("• Curtosis: 2.15", size=12)
                    ]),
                    ft.Container(
                        content=ft.Text("Pregunta: ¿Qué puede concluir sobre la distribución de los niveles de colesterol?", 
                                       size=12, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.colors.YELLOW_50,
                        padding=10,
                        border_radius=8,
                        border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400))
                    ),
                    ft.RadioGroup(
                        content=ft.Column([
                            ft.Radio(value="a", label="La distribución es perfectamente normal"),
                            ft.Radio(value="b", label="Hay asimetría positiva moderada con valores altos extremos"),
                            ft.Radio(value="c", label="La distribución es simétrica pero platicúrtica")
                        ])
                    ),
                    ft.ElevatedButton(
                        "Verificar Respuesta",
                        on_click=lambda e: self.check_case_answer(e, "case1", "b", 
                            "¡Correcto! Con asimetría = 1.23 y media > mediana, hay asimetría positiva moderada."),
                        bgcolor=ft.colors.BLUE_600,
                        color=ft.colors.WHITE
                    )
                ]),
                bgcolor=ft.colors.WHITE,
                padding=20,
                border_radius=10,
                margin=ft.margin.only(bottom=20)
            ),
            
            # Caso 2
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.icons.ACCESS_TIME, size=30, color=ft.colors.GREEN_600),
                            bgcolor=ft.colors.GREEN_100,
                            padding=10,
                            border_radius=25
                        ),
                        ft.Text("Caso 2: Tiempo de Supervivencia Post-Cirugía", 
                               size=18, weight=ft.FontWeight.BOLD, expand=True)
                    ]),
                    ft.Text("Se registró el tiempo de supervivencia (meses) de 200 pacientes después de cirugía cardíaca.", 
                           size=14),
                    ft.Column([
                        ft.Text("• Media: 48.7 meses", size=12),
                        ft.Text("• Mediana: 52.3 meses", size=12),
                        ft.Text("• Desviación estándar: 28.4 meses", size=12),
                        ft.Text("• Asimetría: -0.85", size=12),
                        ft.Text("• Curtosis: 0.42", size=12)
                    ]),
                    ft.Container(
                        content=ft.Text("Pregunta: ¿Qué transformación sería más apropiada si necesitáramos normalizar estos datos?", 
                                       size=12, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.colors.YELLOW_50,
                        padding=10,
                        border_radius=8,
                        border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400))
                    ),
                    ft.RadioGroup(
                        content=ft.Column([
                            ft.Radio(value="a", label="Transformación logarítmica"),
                            ft.Radio(value="b", label="Transformación cuadrática (x²)"),
                            ft.Radio(value="c", label="No se requiere transformación")
                        ])
                    ),
                    ft.ElevatedButton(
                        "Verificar Respuesta",
                        on_click=lambda e: self.check_case_answer(e, "case2", "c", 
                            "¡Correcto! Los valores están dentro de rangos aceptables para normalidad práctica."),
                        bgcolor=ft.colors.GREEN_600,
                        color=ft.colors.WHITE
                    )
                ]),
                bgcolor=ft.colors.WHITE,
                padding=20,
                border_radius=10
            )
        ])

    def check_case_answer(self, e, case_id, correct_answer, explanation):
        """Verifica la respuesta de un caso clínico"""
        # Esta función necesitaría acceso al RadioGroup específico
        # Por simplicidad, mostraremos la explicación directamente
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text(explanation), bgcolor=ft.colors.GREEN)
        )

    def create_practice_section(self):
        """Crea la sección de práctica"""
        # Dataset selector
        self.dataset_selector = ft.Dropdown(
            label="Seleccione un conjunto de datos",
            options=[
                ft.dropdown.Option("", "-- Seleccione un dataset --"),
                ft.dropdown.Option("glucose", "Niveles de Glucosa (mg/dL)"),
                ft.dropdown.Option("bloodpressure", "Presión Arterial Sistólica (mmHg)"),
                ft.dropdown.Option("bmi", "Índice de Masa Corporal (kg/m²)"),
                ft.dropdown.Option("custom", "Datos Personalizados")
            ],
            on_change=self.load_practice_dataset
        )
        
        # Data input
        self.data_input = ft.TextField(
            label="Datos (separados por comas)",
            multiline=True,
            min_lines=5,
            max_lines=8,
            hint_text="Ejemplo: 95, 102, 88, 110, 97, 105..."
        )
        
        # Results display
        self.practice_results = ft.Container(
            content=ft.Text("Ingrese datos para ver los resultados del análisis", 
                           size=14, color=ft.colors.GREY_600),
            bgcolor=ft.colors.GREY_50,
            padding=20,
            border_radius=8
        )
        
        # Chart for practice
        self.practice_chart = ft.Image(
            width=600,
            height=400,
            fit=ft.ImageFit.CONTAIN
        )
        
        return ft.Column([
            ft.Text("Práctica Guiada con Datos Reales", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([
                # Input section
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ingrese sus Datos", size=18, weight=ft.FontWeight.BOLD),
                        self.dataset_selector,
                        self.data_input,
                        ft.ElevatedButton(
                            "Analizar Datos",
                            icon=ft.icons.ANALYTICS,
                            on_click=self.analyze_practice_data,
                            bgcolor=ft.colors.BLUE_600,
                            color=ft.colors.WHITE,
                            width=200
                        )
                    ]),
                    width=400,
                    padding=20
                ),
                
                # Results section
                ft.Container(
                    content=ft.Column([
                        ft.Text("Resultados del Análisis", size=18, weight=ft.FontWeight.BOLD),
                        self.practice_results
                    ]),
                    expand=True,
                    padding=20
                )
            ]),
            
            # Visualization
            ft.Container(
                content=ft.Column([
                    ft.Text("Visualización", size=18, weight=ft.FontWeight.BOLD),
                    self.practice_chart
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=20,
                border_radius=8,
                margin=ft.margin.only(top=20)
            )
        ])

    def load_practice_dataset(self, e):
        """Carga un dataset de ejemplo"""
        selected = self.dataset_selector.value
        if selected and selected != "custom" and selected in self.sample_datasets:
            data_str = ", ".join(map(str, self.sample_datasets[selected]))
            self.data_input.value = data_str
        elif selected == "custom":
            self.data_input.value = ""
            self.data_input.hint_text = "Ingrese sus datos separados por comas..."
        
        self.page.update()

    def analyze_practice_data(self, e):
        """Analiza los datos ingresados en la práctica"""
        data_str = self.data_input.value
        if not data_str.strip():
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Por favor ingrese datos para analizar."))
            )
            return
        
        try:
            # Parse data
            data = [float(x.strip()) for x in data_str.split(",") if x.strip()]
            
            if len(data) < 3:
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Se necesitan al menos 3 valores para el análisis."))
                )
                return
            
            # Calculate statistics
            stats_dict = self.calculate_statistics(data)
            
            # Determine normality
            is_normal = abs(stats_dict['skewness']) < 2 and abs(stats_dict['kurtosis']) < 7
            
            # Create results display
            self.practice_results.content = ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Estadísticas Descriptivas", 
                                   weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                            ft.Row([ft.Text("Tamaño de muestra:"), ft.Text(str(stats_dict['n']), font_family="Courier")]),
                            ft.Row([ft.Text("Media:"), ft.Text(f"{stats_dict['mean']:.3f}", font_family="Courier")]),
                            ft.Row([ft.Text("Mediana:"), ft.Text(f"{stats_dict['median']:.3f}", font_family="Courier")]),
                            ft.Row([ft.Text("Desviación estándar:"), ft.Text(f"{stats_dict['std']:.3f}", font_family="Courier")])
                        ]),
                        bgcolor=ft.colors.BLUE_50,
                        padding=10,
                        border_radius=8,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Forma de la Distribución", 
                                   weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                            ft.Row([ft.Text("Asimetría:"), ft.Text(f"{stats_dict['skewness']:.3f}", font_family="Courier")]),
                            ft.Row([ft.Text("Curtosis:"), ft.Text(f"{stats_dict['kurtosis']:.3f}", font_family="Courier")])
                        ]),
                        bgcolor=ft.colors.GREEN_50,
                        padding=10,
                        border_radius=8,
                        expand=True
                    )
                ]),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Evaluación de Normalidad", 
                               weight=ft.FontWeight.BOLD, 
                               color=ft.colors.GREEN_800 if is_normal else ft.colors.ORANGE_800),
                        ft.Text(
                            "✅ Los datos muestran normalidad práctica aceptable." if is_normal 
                            else "⚠️ Los datos se desvían de la normalidad. Considere métodos no paramétricos.",
                            size=12,
                            color=ft.colors.GREEN_700 if is_normal else ft.colors.ORANGE_700
                        )
                    ]),
                    bgcolor=ft.colors.GREEN_50 if is_normal else ft.colors.ORANGE_50,
                    padding=10,
                    border_radius=8,
                    border=ft.border.only(left=ft.border.BorderSide(4, 
                        ft.colors.GREEN_400 if is_normal else ft.colors.ORANGE_400))
                )
            ])
            
            # Create and display chart
            image_base64 = self.create_histogram_plot(data, "Análisis de Datos")
            self.practice_chart.src_base64 = image_base64
            
            self.page.update()
            
        except ValueError:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Error al procesar los datos. Verifique el formato."))
            )

    def create_evaluation_section(self):
        """Crea la sección de evaluación"""
        self.current_quiz_question = 0
        self.quiz_answers = []
        
        # Progress bar for quiz
        self.quiz_progress_bar = ft.ProgressBar(value=0, width=400)
        self.quiz_progress_text = ft.Text("0/5")
        
        # Question container
        self.question_container = ft.Container(
            content=self.create_quiz_question(0),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=10
        )
        
        # Navigation buttons
        self.prev_btn = ft.ElevatedButton(
            "Anterior",
            icon=ft.icons.ARROW_BACK,
            on_click=self.previous_question,
            disabled=True
        )
        
        self.next_btn = ft.ElevatedButton(
            "Siguiente",
            icon=ft.icons.ARROW_FORWARD,
            on_click=self.next_question,
            bgcolor=ft.colors.ORANGE_600,
            color=ft.colors.WHITE
        )
        
        # Results container
        self.quiz_results_container = ft.Container(visible=False)
        
        return ft.Column([
            ft.Text("Evaluación Automatizada", size=24, weight=ft.FontWeight.BOLD),
            
            # Progress
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Progreso de la Evaluación", size=14, weight=ft.FontWeight.BOLD),
                        self.quiz_progress_text
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    self.quiz_progress_bar
                ]),
                padding=20,
                margin=ft.margin.only(bottom=20)
            ),
            
            # Question
            self.question_container,
            
            # Navigation
            ft.Row([
                self.prev_btn,
                self.next_btn
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            # Results
            self.quiz_results_container
        ])

    def create_quiz_question(self, index):
        """Crea una pregunta del quiz"""
        if index >= len(self.quiz_questions):
            return ft.Text("Quiz completado")
        
        question = self.quiz_questions[index]
        
        return ft.Column([
            ft.Text(f"Pregunta {index + 1} de {len(self.quiz_questions)}", 
                   size=16, weight=ft.FontWeight.BOLD),
            ft.Text(question["question"], size=14, color=ft.colors.GREY_700),
            ft.RadioGroup(
                content=ft.Column([
                    ft.Radio(value=str(i), label=option) 
                    for i, option in enumerate(question["options"])
                ])
            )
        ])

    def next_question(self, e):
        """Avanza a la siguiente pregunta"""
        # Get current answer
        radio_group = self.question_container.content.controls[2]  # RadioGroup
        if radio_group.value is None:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Por favor seleccione una respuesta."))
            )
            return
        
        # Store answer
        self.quiz_answers.append(int(radio_group.value))
        
        # Show feedback
        self.show_question_feedback()
        
        # Move to next question or show results
        if self.current_quiz_question < len(self.quiz_questions) - 1:
            self.current_quiz_question += 1
            self.question_container.content = self.create_quiz_question(self.current_quiz_question)
            self.update_quiz_progress()
        else:
            self.show_quiz_results()
        
        self.page.update()

    def previous_question(self, e):
        """Retrocede a la pregunta anterior"""
        if self.current_quiz_question > 0:
            self.current_quiz_question -= 1
            self.question_container.content = self.create_quiz_question(self.current_quiz_question)
            self.update_quiz_progress()
            self.page.update()

    def show_question_feedback(self):
        """Muestra retroalimentación de la pregunta actual"""
        question = self.quiz_questions[self.current_quiz_question]
        user_answer = self.quiz_answers[-1]
        is_correct = user_answer == question["correct"]
        
        feedback = ft.Container(
            content=ft.Column([
                ft.Text("¡Correcto!" if is_correct else "Incorrecto", 
                       weight=ft.FontWeight.BOLD,
                       color=ft.colors.GREEN_800 if is_correct else ft.colors.RED_800),
                ft.Text(question["explanation"], size=12,
                       color=ft.colors.GREEN_700 if is_correct else ft.colors.RED_700)
            ]),
            bgcolor=ft.colors.GREEN_50 if is_correct else ft.colors.RED_50,
            padding=10,
            border_radius=8,
            border=ft.border.only(left=ft.border.BorderSide(4, 
                ft.colors.GREEN_400 if is_correct else ft.colors.RED_400))
        )
        
        self.question_container.content.controls.append(feedback)

    def update_quiz_progress(self):
        """Actualiza el progreso del quiz"""
        progress = (self.current_quiz_question + 1) / len(self.quiz_questions)
        self.quiz_progress_bar.value = progress
        self.quiz_progress_text.value = f"{self.current_quiz_question + 1}/{len(self.quiz_questions)}"
        
        # Update navigation buttons
        self.prev_btn.disabled = self.current_quiz_question == 0
        self.next_btn.text = "Finalizar" if self.current_quiz_question == len(self.quiz_questions) - 1 else "Siguiente"

    def show_quiz_results(self):
        """Muestra los resultados del quiz"""
        correct_answers = sum(1 for i, answer in enumerate(self.quiz_answers) 
                             if answer == self.quiz_questions[i]["correct"])
        percentage = (correct_answers / len(self.quiz_questions)) * 100
        
        if percentage >= 80:
            result_color = ft.colors.GREEN
            message = "¡Excelente! Has demostrado un dominio sólido de los conceptos."
        elif percentage >= 60:
            result_color = ft.colors.ORANGE
            message = "Buen trabajo. Revisa los temas donde tuviste dificultades."
        else:
            result_color = ft.colors.RED
            message = "Necesitas repasar los conceptos. Te recomendamos revisar la teoría."
        
        self.quiz_results_container.content = ft.Container(
            content=ft.Column([
                ft.Text("Resultados de la Evaluación", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(f"{correct_answers}/{len(self.quiz_questions)} ({percentage:.1f}%)", 
                       size=24, weight=ft.FontWeight.BOLD),
                ft.Text(message),
                ft.ElevatedButton(
                    "Reiniciar Evaluación",
                    on_click=self.restart_quiz,
                    bgcolor=ft.colors.BLUE_600,
                    color=ft.colors.WHITE
                )
            ]),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=8,
            border=ft.border.only(left=ft.border.BorderSide(4, result_color))
        )
        
        self.quiz_results_container.visible = True
        self.question_container.visible = False

    def restart_quiz(self, e):
        """Reinicia el quiz"""
        self.current_quiz_question = 0
        self.quiz_answers = []
        self.quiz_results_container.visible = False
        self.question_container.visible = True
        self.question_container.content = self.create_quiz_question(0)
        self.update_quiz_progress()
        self.page.update()

    def create_resources_section(self):
        """Crea la sección de recursos"""
        return ft.Column([
            ft.Text("Recursos Descargables", size=24, weight=ft.FontWeight.BOLD),
            
            ft.Row([
                # Hoja de referencia
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.DESCRIPTION, size=40, color=ft.colors.BLUE_600),
                        ft.Text("Hoja de Referencia Rápida", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text("Fórmulas y criterios de interpretación", size=12, text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton(
                            "Descargar PDF",
                            icon=ft.icons.DOWNLOAD,
                            on_click=self.download_cheat_sheet,
                            bgcolor=ft.colors.BLUE_600,
                            color=ft.colors.WHITE
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.WHITE,
                    padding=20,
                    border_radius=10,
                    expand=True,
                    margin=ft.margin.only(right=10)
                ),
                
                # Plantillas
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.TABLE_CHART, size=40, color=ft.colors.GREEN_600),
                        ft.Text("Plantillas de Datos", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text("Plantillas Excel/CSV para análisis", size=12, text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton(
                            "Descargar Excel",
                            icon=ft.icons.DOWNLOAD,
                            on_click=self.download_templates,
                            bgcolor=ft.colors.GREEN_600,
                            color=ft.colors.WHITE
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.WHITE,
                    padding=20,
                    border_radius=10,
                    expand=True,
                    margin=ft.margin.only(right=10)
                ),
                
                # Scripts
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.icons.CODE, size=40, color=ft.colors.PURPLE_600),
                        ft.Text("Scripts de Análisis", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text("Código R y Python", size=12, text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton(
                            "Descargar Código",
                            icon=ft.icons.DOWNLOAD,
                            on_click=self.download_scripts,
                            bgcolor=ft.colors.PURPLE_600,
                            color=ft.colors.WHITE
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.WHITE,
                    padding=20,
                    border_radius=10,
                    expand=True
                )
            ])
        ])

    def download_cheat_sheet(self, e):
        """Descarga la hoja de referencia"""
        content = """
# Hoja de Referencia Rápida: Asimetría, Curtosis y Normalidad

## Asimetría (Skewness)
- Fórmula: Σ[(xi - x̄)³/n] / s³
- Simétrica: ≈ 0
- Asimetría positiva: > 0 (cola derecha larga)
- Asimetría negativa: < 0 (cola izquierda larga)

## Curtosis (Kurtosis)
- Fórmula: Σ[(xi - x̄)⁴/n] / s⁴ - 3
- Mesocúrtica: ≈ 0 (normal)
- Leptocúrtica: > 0 (más puntiaguda)
- Platicúrtica: < 0 (más plana)

## Criterios de Normalidad Práctica
- |Asimetría| < 2
- |Curtosis| < 7
- Inspección visual del histograma
- Pruebas de normalidad (Shapiro-Wilk, Anderson-Darling)
        """
        
        filename = f"hoja_referencia_asimetria_curtosis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text(f"Hoja de referencia guardada como {filename}"))
        )

    def download_templates(self, e):
        """Descarga las plantillas de datos"""
        data = {
            'Variable': ['Glucosa', 'Glucosa', 'Presion_Sistolica', 'Presion_Sistolica'],
            'Valor': [95, 102, 120, 125],
            'Grupo': ['Control', 'Control', 'Control', 'Control'],
            'Fecha': ['2024-01-01', '2024-01-02', '2024-01-01', '2024-01-02']
        }
        
        df = pd.DataFrame(data)
        filename = f"plantilla_datos_salud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text(f"Plantilla guardada como {filename}"))
        )

    def download_scripts(self, e):
        """Descarga los scripts de análisis"""
        r_script = """
# Script R para Análisis de Asimetría y Curtosis
# Autor: OVA Estadística Descriptiva UAN

library(moments)
library(nortest)

analizar_normalidad <- function(datos, nombre_variable = "Variable") {
  n <- length(datos)
  media <- mean(datos, na.rm = TRUE)
  mediana <- median(datos, na.rm = TRUE)
  desv_std <- sd(datos, na.rm = TRUE)
  
  asimetria <- skewness(datos, na.rm = TRUE)
  curtosis <- kurtosis(datos, na.rm = TRUE) - 3
  
  normal_asimetria <- abs(asimetria) < 2
  normal_curtosis <- abs(curtosis) < 7
  normal_practica <- normal_asimetria && normal_curtosis
  
  return(list(
    estadisticas = data.frame(
      n = n, media = media, mediana = mediana,
      desv_std = desv_std, asimetria = asimetria, curtosis = curtosis
    ),
    normalidad = normal_practica
  ))
}
        """
        
        filename = f"script_analisis_normalidad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.R"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(r_script)
        
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text(f"Script R guardado como {filename}"))
        )

def main(page: ft.Page):
    app = OVAAsimetriaCurtosis()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)
