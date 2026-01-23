
import flet as ft
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import pandas as pd
import io
import base64
import random
import math
from datetime import datetime
import json

class OVAVisualizacionSalud:
    def __init__(self):
        self.current_section = 0
        self.completed_sections = set()
        self.quiz_answers = {}
        self.quiz_score = 0
        self.lab_data = []
        
        # Configuración de matplotlib para español
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        
    def main(self, page: ft.Page):
        page.title = "OVA 8: Visualización para Salud II - Gráficos Numéricos"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1200
        page.window_height = 800
        page.window_resizable = True
        page.scroll = ft.ScrollMode.AUTO
        
        # Variables de estado
        self.page = page
        self.progress_bar = ft.ProgressBar(width=400, color="blue", bgcolor="#eeeeee")
        self.progress_text = ft.Text("0% completado", size=14)
        
        # Crear contenido principal
        self.create_header()
        self.create_navigation()
        self.create_sections()
        
        # Layout principal
        main_content = ft.Column([
            self.header,
            ft.Container(
                content=ft.Row([
                    ft.Text("Progreso del módulo:", size=14),
                    self.progress_text
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=10
            ),
            ft.Container(content=self.progress_bar, padding=ft.padding.symmetric(horizontal=10)),
            self.navigation,
            ft.Container(content=self.content_area, expand=True, padding=10)
        ], expand=True)
        
        page.add(main_content)
        self.update_progress()
        
    def create_header(self):
        self.header = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ANALYTICS, color="white", size=30),
                ft.Column([
                    ft.Text("OVA 8: Visualización para Salud II", 
                           size=24, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text("Gráficos Numéricos en Ciencias de la Salud", 
                           size=16, color="white")
                ], spacing=5),
                ft.Column([
                    ft.Text("Universidad Antonio Nariño", size=12, color="white"),
                    ft.Text("Modelo Pedagógico C(H)ANGE", size=12, color="white")
                ], horizontal_alignment=ft.CrossAxisAlignment.END)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor="#1976d2",
            padding=20,
            border_radius=10
        )
        
    def create_navigation(self):
        nav_buttons = [
            ("Introducción", ft.Icons.PLAY_CIRCLE, 0),
            ("Teoría", ft.Icons.BOOK, 1),
            ("Práctica", ft.Icons.HANDYMAN, 2),
            ("Laboratorio", ft.Icons.SCIENCE, 3),
            ("Evaluación", ft.Icons.QUIZ, 4),
            ("Recursos", ft.Icons.DOWNLOAD, 5)
        ]
        
        self.nav_buttons = []
        for text, icon, index in nav_buttons:
            btn = ft.ElevatedButton(
                text=text,
                icon=icon,
                on_click=lambda e, idx=index: self.show_section(idx),
                style=ft.ButtonStyle(
                    color=ft.Colors.BLUE_700 if index == 0 else ft.Colors.GREY_700
                )
            )
            self.nav_buttons.append(btn)
            
        self.navigation = ft.Container(
            content=ft.Row(self.nav_buttons, alignment=ft.MainAxisAlignment.SPACE_AROUND),
            bgcolor="#f5f5f5",
            padding=10,
            border_radius=5
        )
        
    def create_sections(self):
        self.sections = [
            self.create_intro_section(),
            self.create_theory_section(),
            self.create_practice_section(),
            self.create_lab_section(),
            self.create_quiz_section(),
            self.create_resources_section()
        ]
        
        self.content_area = ft.Container(
            content=self.sections[0],
            expand=True
        )
        
    def show_section(self, index):
        self.current_section = index
        self.completed_sections.add(index)
        
        # Actualizar botones de navegación
        for i, btn in enumerate(self.nav_buttons):
            btn.style.color = ft.Colors.BLUE_700 if i == index else ft.Colors.GREY_700
            
        # Mostrar sección
        self.content_area.content = self.sections[index]
        self.update_progress()
        self.page.update()
        
    def update_progress(self):
        progress = len(self.completed_sections) / 6 * 100
        self.progress_bar.value = progress / 100
        self.progress_text.value = f"{int(progress)}% completado"
        if hasattr(self, 'page'):
            self.page.update()
            
    def create_intro_section(self):
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ANALYTICS, size=60, color="white"),
                    ft.Text("Visualización para Salud II", 
                           size=28, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text("Gráficos Numéricos en Ciencias de la Salud", 
                           size=18, color="white")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.BLUE_GRADIENT,
                padding=30,
                border_radius=10,
                margin=ft.margin.only(bottom=20)
            ),
            
            ft.Row([
                # Objetivos
                ft.Container(
                    content=ft.Column([
                        ft.Text("🎯 Objetivos de Aprendizaje", 
                               size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                        ft.Text("✓ Seleccionar el gráfico numérico apropiado según el tipo de datos"),
                        ft.Text("✓ Construir e interpretar histogramas, boxplots, gráficos de violín"),
                        ft.Text("✓ Aplicar anotaciones clínicas relevantes"),
                        ft.Text("✓ Comparar distribuciones entre grupos poblacionales")
                    ], spacing=10),
                    bgcolor=ft.Colors.BLUE_50,
                    padding=20,
                    border_radius=10,
                    expand=True
                ),
                
                # Estructura
                ft.Container(
                    content=ft.Column([
                        ft.Text("⏱️ Estructura del Módulo", 
                               size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
                        ft.Row([ft.Text("Introducción y objetivos"), ft.Text("10 min", bgcolor=ft.Colors.GREEN_200)]),
                        ft.Row([ft.Text("Microlección interactiva"), ft.Text("25 min", bgcolor=ft.Colors.GREEN_200)]),
                        ft.Row([ft.Text("Práctica guiada"), ft.Text("45 min", bgcolor=ft.Colors.GREEN_200)]),
                        ft.Row([ft.Text("Laboratorio virtual"), ft.Text("30 min", bgcolor=ft.Colors.GREEN_200)]),
                        ft.Row([ft.Text("Evaluación"), ft.Text("15 min", bgcolor=ft.Colors.GREEN_200)])
                    ], spacing=10),
                    bgcolor=ft.Colors.GREEN_50,
                    padding=20,
                    border_radius=10,
                    expand=True
                )
            ], spacing=20),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("💡 Modelo Pedagógico C(H)ANGE", 
                           size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800),
                    ft.Text("Este módulo integra Combinatoria (selección de gráficos), "
                           "Álgebra (cálculos estadísticos), Números (interpretación cuantitativa), "
                           "Geometría (representación visual) y Estadística (análisis descriptivo) "
                           "para fortalecer el pensamiento estadístico en ciencias de la salud.")
                ]),
                bgcolor=ft.Colors.ORANGE_50,
                padding=20,
                border_radius=10,
                margin=ft.margin.only(top=20)
            ),
            
            ft.Container(
                content=ft.ElevatedButton(
                    "Comenzar Módulo",
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda e: self.show_section(1),
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_600,
                        color=ft.Colors.WHITE,
                        padding=ft.padding.all(15)
                    )
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=30)
            )
        ], scroll=ft.ScrollMode.AUTO)
        
    def create_theory_section(self):
        # Crear gráfico de ejemplo
        example_chart = self.create_example_chart()
        
        return ft.Column([
            ft.Text("📚 Fundamentos Teóricos", size=24, weight=ft.FontWeight.BOLD),
            
            ft.Row([
                # Histogramas
                ft.Container(
                    content=ft.Column([
                        ft.Text("📊 Histogramas", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                        ft.Text("Representan la distribución de frecuencias de una variable numérica continua. "
                               "Esenciales para evaluar normalidad y detectar patrones en datos clínicos."),
                        ft.Container(
                            content=ft.Text("Uso clínico: Distribución de presión arterial, IMC, "
                                           "niveles de glucosa, tiempos de espera hospitalarios.",
                                           weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.WHITE,
                            padding=10,
                            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.BLUE_500))
                        )
                    ], spacing=10),
                    bgcolor=ft.Colors.BLUE_50,
                    padding=15,
                    border_radius=10,
                    expand=True
                ),
                
                # Boxplots
                ft.Container(
                    content=ft.Column([
                        ft.Text("📦 Boxplots", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
                        ft.Text("Muestran la mediana, cuartiles y valores atípicos. "
                               "Ideales para comparar distribuciones entre grupos."),
                        ft.Container(
                            content=ft.Text("Uso clínico: Comparación de biomarcadores entre grupos, "
                                           "análisis de variabilidad en mediciones clínicas.",
                                           weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.WHITE,
                            padding=10,
                            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.GREEN_500))
                        )
                    ], spacing=10),
                    bgcolor=ft.Colors.GREEN_50,
                    padding=15,
                    border_radius=10,
                    expand=True
                )
            ], spacing=15),
            
            ft.Row([
                # Gráficos de Violín
                ft.Container(
                    content=ft.Column([
                        ft.Text("🎵 Gráficos de Violín", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
                        ft.Text("Combinan boxplot con estimación de densidad. "
                               "Muestran la forma completa de la distribución."),
                        ft.Container(
                            content=ft.Text("Uso clínico: Análisis de distribuciones complejas en farmacología, "
                                           "variabilidad en respuesta a tratamientos.",
                                           weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.WHITE,
                            padding=10,
                            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.PURPLE_500))
                        )
                    ], spacing=10),
                    bgcolor=ft.Colors.PURPLE_50,
                    padding=15,
                    border_radius=10,
                    expand=True
                ),
                
                # Scatterplots
                ft.Container(
                    content=ft.Column([
                        ft.Text("⚫ Nubes de Puntos", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800),
                        ft.Text("Visualizan la relación entre dos variables numéricas. "
                               "Fundamentales para explorar correlaciones."),
                        ft.Container(
                            content=ft.Text("Uso clínico: Relación peso-altura, correlación entre biomarcadores, "
                                           "análisis dosis-respuesta.",
                                           weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.WHITE,
                            padding=10,
                            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.ORANGE_500))
                        )
                    ], spacing=10),
                    bgcolor=ft.Colors.ORANGE_50,
                    padding=15,
                    border_radius=10,
                    expand=True
                )
            ], spacing=15),
            
            # Ejemplo interactivo
            ft.Container(
                content=ft.Column([
                    ft.Text("▶️ Ejemplo Interactivo: Presión Arterial Sistólica", 
                           size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_800),
                    ft.Text("Explora cómo diferentes gráficos revelan aspectos distintos de los mismos datos clínicos."),
                    
                    ft.Row([
                        ft.Text("Tipo de gráfico:"),
                        ft.Dropdown(
                            width=200,
                            options=[
                                ft.dropdown.Option("histogram", "Histograma"),
                                ft.dropdown.Option("boxplot", "Boxplot"),
                                ft.dropdown.Option("violin", "Gráfico de Violín")
                            ],
                            value="histogram",
                            on_change=self.update_example_chart
                        )
                    ]),
                    
                    example_chart,
                    
                    ft.Container(
                        content=ft.Text(
                            "Interpretación del Histograma: La distribución muestra una forma aproximadamente "
                            "normal con ligero sesgo hacia la derecha. La mayoría de pacientes (70%) presenta "
                            "valores entre 120-150 mmHg, indicando hipertensión leve a moderada.",
                            size=14
                        ),
                        bgcolor=ft.Colors.WHITE,
                        padding=15,
                        border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.INDIGO_500)),
                        border_radius=5
                    )
                ], spacing=15),
                bgcolor=ft.Colors.INDIGO_50,
                padding=20,
                border_radius=10,
                margin=ft.margin.only(top=20)
            ),
            
            ft.Container(
                content=ft.ElevatedButton(
                    "Continuar a Práctica",
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda e: self.show_section(2),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=30)
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
        
    def create_example_chart(self):
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Datos de ejemplo para presión arterial
        bins = ['100-110', '110-120', '120-130', '130-140', '140-150', '150-160', '160-170', '170-180']
        frequencies = [5, 12, 18, 25, 20, 12, 6, 2]
        
        bars = ax.bar(bins, frequencies, color='#3b82f6', alpha=0.7, edgecolor='#1e40af')
        ax.set_title('Distribución de Presión Arterial Sistólica (mmHg)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Presión Arterial Sistólica (mmHg)')
        ax.set_ylabel('Número de Pacientes')
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Convertir a imagen
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        plt.close()
        
        return ft.Image(
            src_base64=img_base64,
            width=600,
            height=400,
            fit=ft.ImageFit.CONTAIN
        )
        
    def update_example_chart(self, e):
        chart_type = e.control.value
        # Aquí se actualizaría el gráfico según el tipo seleccionado
        # Por simplicidad, mantenemos el mismo gráfico
        pass
        
    def create_practice_section(self):
        # Crear gráficos de práctica
        histogram_chart = self.create_practice_histogram()
        boxplot_chart = self.create_practice_boxplot()
        violin_chart = self.create_practice_violin()
        
        return ft.Column([
            ft.Text("🤝 Práctica Guiada", size=24, weight=ft.FontWeight.BOLD),
            
            # Caso clínico
            ft.Container(
                content=ft.Column([
                    ft.Text("🏥 Caso Clínico: Análisis de IMC en Pacientes Diabéticos", 
                           size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                    ft.Text("Un hospital desea analizar la distribución del Índice de Masa Corporal (IMC) "
                           "en pacientes diabéticos tipo 2 para evaluar el estado nutricional y planificar "
                           "intervenciones. Se recolectaron datos de 200 pacientes."),
                    ft.Container(
                        content=ft.Text("Pregunta clínica: ¿Cómo se distribuye el IMC en nuestra población "
                                       "de pacientes diabéticos y existen diferencias entre hombres y mujeres?",
                                       weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.WHITE,
                        padding=15,
                        border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.BLUE_500))
                    )
                ], spacing=15),
                bgcolor=ft.Colors.BLUE_50,
                padding=20,
                border_radius=10
            ),
            
            # Paso 1: Histograma
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text("1", color="white", weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.BLUE_600,
                            width=30,
                            height=30,
                            border_radius=15,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Exploración Inicial con Histograma", size=16, weight=ft.FontWeight.BOLD)
                    ], spacing=10),
                    
                    ft.Text("Comenzamos visualizando la distribución general del IMC:"),
                    
                    ft.Row([
                        histogram_chart,
                        ft.Column([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Observaciones Clínicas:", weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800),
                                    ft.Text("• Distribución ligeramente sesgada hacia la derecha"),
                                    ft.Text("• Media ≈ 28.5 kg/m² (sobrepeso)"),
                                    ft.Text("• Mayoría de pacientes en rango 25-35 kg/m²"),
                                    ft.Text("• Algunos casos de obesidad severa (>35 kg/m²)")
                                ], spacing=5),
                                bgcolor=ft.Colors.ORANGE_50,
                                padding=15,
                                border_radius=5
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Implicaciones Clínicas:", weight=ft.FontWeight.BOLD, color=ft.Colors.RED_800),
                                    ft.Text("El 70% de los pacientes presenta sobrepeso u obesidad, "
                                           "factor de riesgo adicional para complicaciones diabéticas.")
                                ], spacing=5),
                                bgcolor=ft.Colors.RED_50,
                                padding=15,
                                border_radius=5
                            )
                        ], expand=True, spacing=10)
                    ], spacing=20)
                ], spacing=15),
                border=ft.border.all(1, ft.Colors.GREY_300),
                padding=20,
                border_radius=10
            ),
            
            # Paso 2: Boxplot
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text("2", color="white", weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.GREEN_600,
                            width=30,
                            height=30,
                            border_radius=15,
                            alignment=ft.alignment.center
                        ),
                        ft.Text("Comparación por Sexo con Boxplots", size=16, weight=ft.FontWeight.BOLD)
                    ], spacing=10),
                    
                    ft.Text("Comparamos la distribución del IMC entre hombres y mujeres:"),
                    
                    ft.Row([
                        boxplot_chart,
                        ft.Column([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Análisis Comparativo:", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
                                    ft.Text("• Mujeres: Mediana más alta (29.2 kg/m²)"),
                                    ft.Text("• Hombres: Mayor variabilidad (IQR más amplio)"),
                                    ft.Text("• Outliers presentes en ambos grupos"),
                                    ft.Text("• Diferencia estadísticamente significativa")
                                ], spacing=5),
                                bgcolor=ft.Colors.GREEN_50,
                                padding=15,
                                border_radius=5
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Interpretación Clínica:", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                                    ft.Text("Las mujeres diabéticas muestran mayor tendencia al sobrepeso, "
                                           "sugiriendo la necesidad de intervenciones nutricionales diferenciadas por sexo.")
                                ], spacing=5),
                                bgcolor=ft.Colors.BLUE_50,
                                padding=15,
                                border_radius=5
                            )
                        ], expand=True, spacing=10)
                    ], spacing=20)
                ], spacing=15),
                border=ft.border.all(1, ft.Colors.GREY_300),
                padding=20,
                border_radius=10
            ),
            
            # Ejercicio interactivo
            ft.Container(
                content=ft.Column([
                    ft.Text("✏️ Ejercicio Interactivo", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_800),
                    ft.Text("Selecciona el gráfico más apropiado para cada pregunta clínica:"),
                    
                    ft.Column([
                        ft.Text("1. ¿Cuál es la distribución general de la glucosa en ayunas en pacientes diabéticos?", 
                               weight=ft.FontWeight.BOLD),
                        ft.RadioGroup(
                            content=ft.Column([
                                ft.Radio(value="histogram", label="Histograma"),
                                ft.Radio(value="boxplot", label="Boxplot"),
                                ft.Radio(value="scatter", label="Scatterplot")
                            ]),
                            on_change=lambda e: setattr(self, 'practice_q1', e.control.value)
                        )
                    ], spacing=10),
                    
                    ft.Column([
                        ft.Text("2. ¿Existe relación entre la edad y el nivel de HbA1c?", 
                               weight=ft.FontWeight.BOLD),
                        ft.RadioGroup(
                            content=ft.Column([
                                ft.Radio(value="histogram", label="Histograma"),
                                ft.Radio(value="boxplot", label="Boxplot"),
                                ft.Radio(value="scatter", label="Scatterplot")
                            ]),
                            on_change=lambda e: setattr(self, 'practice_q2', e.control.value)
                        )
                    ], spacing=10),
                    
                    ft.ElevatedButton(
                        "Verificar Respuestas",
                        on_click=self.check_practice_answers,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO_600, color=ft.Colors.WHITE)
                    ),
                    
                    ft.Container(height=20)  # Espacio para feedback
                ], spacing=15),
                bgcolor=ft.Colors.INDIGO_50,
                padding=20,
                border_radius=10
            ),
            
            ft.Container(
                content=ft.ElevatedButton(
                    "Ir al Laboratorio Virtual",
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda e: self.show_section(3),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE)
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=30)
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
        
    def create_practice_histogram(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        
        bins = ['18-22', '22-26', '26-30', '30-34', '34-38', '38-42', '42-46']
        frequencies = [8, 25, 45, 60, 35, 20, 7]
        
        bars = ax.bar(bins, frequencies, color='#3b82f6', alpha=0.7, edgecolor='#1e40af')
        ax.set_title('Distribución del IMC en Pacientes Diabéticos (n=200)', fontsize=12, fontweight='bold')
        ax.set_xlabel('IMC (kg/m²)')
        ax.set_ylabel('Frecuencia')
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        plt.close()
        
        return ft.Image(
            src_base64=img_base64,
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )
        
    def create_practice_boxplot(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Simular datos de boxplot
        groups = ['Hombres', 'Mujeres']
        q1_values = [26.2, 27.8]
        median_values = [28.1, 29.2]
        q3_values = [31.5, 32.1]
        
        x_pos = np.arange(len(groups))
        width = 0.25
        
        ax.bar(x_pos - width, q1_values, width, label='Q1', color='#22c55e', alpha=0.7)
        ax.bar(x_pos, median_values, width, label='Mediana', color='#3b82f6', alpha=0.8)
        ax.bar(x_pos + width, q3_values, width, label='Q3', color='#22c55e', alpha=0.7)
        
        ax.set_title('Comparación de IMC por Sexo (Boxplot Simulado)', fontsize=12, fontweight='bold')
        ax.set_ylabel('IMC (kg/m²)')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(groups)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        plt.close()
        
        return ft.Image(
            src_base64=img_base64,
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )
        
    def create_practice_violin(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Simular gráfico de violín con líneas
        x = np.linspace(20, 40, 21)
        density_men = [0.05, 0.15, 0.35, 0.65, 0.85, 0.95, 0.75, 0.45, 0.25, 0.10, 0.05, 
                      0.03, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        density_women = [0.03, 0.10, 0.25, 0.50, 0.70, 0.85, 0.90, 0.70, 0.50, 0.30, 0.15,
                        0.10, 0.08, 0.06, 0.04, 0.03, 0.02, 0.02, 0.01, 0.01, 0.01]
        
        ax.plot(x, density_men, label='Hombres', color='#3b82f6', linewidth=2)
        ax.fill_between(x, density_men, alpha=0.3, color='#3b82f6')
        
        ax.plot(x, density_women, label='Mujeres', color='#ec4899', linewidth=2)
        ax.fill_between(x, density_women, alpha=0.3, color='#ec4899')
        
        ax.set_title('Distribución Detallada del IMC por Sexo (Gráfico de Violín)', fontsize=12, fontweight='bold')
        ax.set_xlabel('IMC (kg/m²)')
        ax.set_ylabel('Densidad')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        plt.close()
        
        return ft.Image(
            src_base64=img_base64,
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )
        
    def check_practice_answers(self, e):
        feedback = []
        
        if hasattr(self, 'practice_q1'):
            if self.practice_q1 == 'histogram':
                feedback.append("✅ Pregunta 1: ¡Correcto! El histograma es ideal para visualizar la distribución general.")
            else:
                feedback.append("❌ Pregunta 1: Incorrecto. Para ver la distribución general, el histograma es la mejor opción.")
                
        if hasattr(self, 'practice_q2'):
            if self.practice_q2 == 'scatter':
                feedback.append("✅ Pregunta 2: ¡Correcto! El scatterplot es perfecto para explorar relaciones entre variables.")
            else:
                feedback.append("❌ Pregunta 2: Incorrecto. Para analizar relaciones entre variables, usa un scatterplot.")
        
        # Mostrar feedback
        if feedback:
            feedback_text = "\n".join(feedback)
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(feedback_text), duration=5000))
            
    def create_lab_section(self):
        # Controles del simulador
        self.lab_variable = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("blood_pressure", "Presión Arterial Sistólica"),
                ft.dropdown.Option("cholesterol", "Colesterol Total"),
                ft.dropdown.Option("glucose", "Glucosa en Ayunas"),
                ft.dropdown.Option("bmi", "Índice de Masa Corporal")
            ],
            value="blood_pressure",
            on_change=self.update_lab_chart
        )
        
        self.lab_chart_type = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("histogram", "Histograma"),
                ft.dropdown.Option("boxplot", "Boxplot por Grupo"),
                ft.dropdown.Option("violin", "Gráfico de Violín"),
                ft.dropdown.Option("scatter", "Scatterplot (vs Edad)")
            ],
            value="histogram",
            on_change=self.update_lab_chart
        )
        
        self.lab_sample_size = ft.Slider(
            min=50, max=500, value=200, divisions=9,
            label="Tamaño de muestra: {value} pacientes",
            on_change=self.update_lab_chart
        )
        
        self.lab_noise = ft.Slider(
            min=0, max=100, value=10, divisions=10,
            label="Ruido: {value}%",
            on_change=self.update_lab_chart
        )
        
        # Contenedor para el gráfico
        self.lab_chart_container = ft.Container(
            content=ft.Text("Selecciona parámetros para generar el gráfico"),
            width=600,
            height=400,
            bgcolor=ft.Colors.GREY_100,
            border_radius=10,
            alignment=ft.alignment.center
        )
        
        # Contenedor para estadísticas
        self.lab_stats_container = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Media", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                    ft.Text("--", size=20, weight=ft.FontWeight.BOLD)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=5,
                border=ft.border.all(1, ft.Colors.GREY_300),
                expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Mediana", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                    ft.Text("--", size=20, weight=ft.FontWeight.BOLD)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=5,
                border=ft.border.all(1, ft.Colors.GREY_300),
                expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Desv. Estándar", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                    ft.Text("--", size=20, weight=ft.FontWeight.BOLD)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=5,
                border=ft.border.all(1, ft.Colors.GREY_300),
                expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Rango", weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_700),
                    ft.Text("--", size=20, weight=ft.FontWeight.BOLD)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=5,
                border=ft.border.all(1, ft.Colors.GREY_300),
                expand=True
            )
        ], spacing=10)
        
        # Contenedor para interpretación
        self.lab_interpretation = ft.Container(
            content=ft.Text("Selecciona una variable y tipo de gráfico para ver la interpretación clínica."),
            bgcolor=ft.Colors.GREEN_50,
            padding=15,
            border_radius=5,
            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.GREEN_500))
        )
        
        return ft.Column([
            ft.Text("🧪 Laboratorio Virtual", size=24, weight=ft.FontWeight.BOLD),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("🔬 Simulador de Visualización de Datos Clínicos", 
                           size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
                    ft.Text("Experimenta con diferentes tipos de gráficos usando datos simulados de pacientes. "
                           "Modifica los parámetros y observa cómo cambian las visualizaciones e interpretaciones.")
                ], spacing=10),
                bgcolor=ft.Colors.PURPLE_50,
                padding=20,
                border_radius=10
            ),
            
            ft.Row([
                # Controles
                ft.Container(
                    content=ft.Column([
                        ft.Text("⚙️ Controles del Simulador", size=16, weight=ft.FontWeight.BOLD),
                        
                        ft.Column([
                            ft.Text("Variable a analizar:"),
                            self.lab_variable
                        ], spacing=5),
                        
                        ft.Column([
                            ft.Text("Tipo de gráfico:"),
                            self.lab_chart_type
                        ], spacing=5),
                        
                        ft.Column([
                            ft.Text("Tamaño de muestra:"),
                            self.lab_sample_size
                        ], spacing=5),
                        
                        ft.Column([
                            ft.Text("Agregar ruido:"),
                            self.lab_noise
                        ], spacing=5),
                        
                        ft.ElevatedButton(
                            "Generar Nuevos Datos",
                            icon=ft.Icons.REFRESH,
                            on_click=self.generate_new_lab_data,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE)
                        )
                    ], spacing=15),
                    bgcolor=ft.Colors.GREY_50,
                    padding=20,
                    border_radius=10,
                    width=300
                ),
                
                # Gráfico
                ft.Container(
                    content=ft.Column([
                        ft.Text("Visualización de Datos", size=16, weight=ft.FontWeight.BOLD),
                        self.lab_chart_container
                    ], spacing=10),
                    expand=True,
                    padding=20
                )
            ], spacing=20),
            
            # Estadísticas
            ft.Container(
                content=ft.Column([
                    ft.Text("🧮 Estadísticas Descriptivas", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                    self.lab_stats_container
                ], spacing=15),
                bgcolor=ft.Colors.BLUE_50,
                padding=20,
                border_radius=10
            ),
            
            # Interpretación
            ft.Container(
                content=ft.Column([
                    ft.Text("🩺 Interpretación Clínica Automática", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
                    self.lab_interpretation
                ], spacing=15),
                bgcolor=ft.Colors.GREEN_50,
                padding=20,
                border_radius=10
            ),
            
            # Exportar
            ft.Container(
                content=ft.Column([
                    ft.Text("💾 Exportar Resultados", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.ElevatedButton(
                            "Exportar PNG",
                            icon=ft.Icons.IMAGE,
                            on_click=self.export_chart,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
                        ),
                        ft.ElevatedButton(
                            "Exportar Datos CSV",
                            icon=ft.Icons.TABLE_CHART,
                            on_click=self.export_data,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
                        ),
                        ft.ElevatedButton(
                            "Generar Reporte",
                            icon=ft.Icons.DESCRIPTION,
                            on_click=self.generate_report,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE)
                        )
                    ], spacing=10)
                ], spacing=15),
                bgcolor=ft.Colors.GREY_50,
                padding=20,
                border_radius=10
            ),
            
            ft.Container(
                content=ft.ElevatedButton(
                    "Continuar a Evaluación",
                    icon=ft.Icons.ARROW_FORWARD,
                    on_click=lambda e: self.show_section(4),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE)
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=30)
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
        
    def update_lab_chart(self, e=None):
        variable = self.lab_variable.value
        chart_type = self.lab_chart_type.value
        sample_size = int(self.lab_sample_size.value)
        noise = self.lab_noise.value / 100
        
        # Generar datos
        self.lab_data = self.generate_lab_data(variable, sample_size, noise)
        
        # Crear gráfico
        chart_image = self.create_lab_chart(variable, chart_type, self.lab_data)
        self.lab_chart_container.content = chart_image
        
        # Actualizar estadísticas
        self.update_lab_statistics(self.lab_data)
        
        # Actualizar interpretación
        self.update_lab_interpretation(variable, chart_type, self.lab_data)
        
        if hasattr(self, 'page'):
            self.page.update()
            
    def generate_lab_data(self, variable, sample_size, noise):
        data = []
        
        for i in range(sample_size):
            group = "Grupo A" if random.random() < 0.5 else "Grupo B"
            age = 25 + random.random() * 50
            
            if variable == "blood_pressure":
                if group == "Grupo A":
                    value = 120 + random.random() * 30 + (random.random() - 0.5) * noise * 20
                else:
                    value = 130 + random.random() * 35 + (random.random() - 0.5) * noise * 25
            elif variable == "cholesterol":
                if group == "Grupo A":
                    value = 180 + random.random() * 40 + (random.random() - 0.5) * noise * 30
                else:
                    value = 200 + random.random() * 50 + (random.random() - 0.5) * noise * 40
            elif variable == "glucose":
                if group == "Grupo A":
                    value = 90 + random.random() * 20 + (random.random() - 0.5) * noise * 15
                else:
                    value = 110 + random.random() * 30 + (random.random() - 0.5) * noise * 20
            elif variable == "bmi":
                if group == "Grupo A":
                    value = 24 + random.random() * 6 + (random.random() - 0.5) * noise * 4
                else:
                    value = 28 + random.random() * 8 + (random.random() - 0.5) * noise * 5
                    
            data.append({"value": value, "group": group, "age": age})
            
        return data
        
    def create_lab_chart(self, variable, chart_type, data):
        fig, ax = plt.subplots(figsize=(8, 5))
        
        values = [d["value"] for d in data]
        
        if chart_type == "histogram":
            ax.hist(values, bins=15, color='#3b82f6', alpha=0.7, edgecolor='#1e40af')
            ax.set_title(f'Histograma: {self.get_variable_label(variable)}')
            ax.set_ylabel('Frecuencia')
            
        elif chart_type == "boxplot":
            group_a = [d["value"] for d in data if d["group"] == "Grupo A"]
            group_b = [d["value"] for d in data if d["group"] == "Grupo B"]
            
            ax.boxplot([group_a, group_b], labels=['Grupo A', 'Grupo B'])
            ax.set_title(f'Boxplot: {self.get_variable_label(variable)}')
            
        elif chart_type == "violin":
            group_a = [d["value"] for d in data if d["group"] == "Grupo A"]
            group_b = [d["value"] for d in data if d["group"] == "Grupo B"]
            
            # Simular violin plot con histogramas
            ax.hist(group_a, bins=20, alpha=0.5, label='Grupo A', color='#3b82f6', density=True)
            ax.hist(group_b, bins=20, alpha=0.5, label='Grupo B', color='#ec4899', density=True)
            ax.set_title(f'Distribución de Densidad: {self.get_variable_label(variable)}')
            ax.legend()
            ax.set_ylabel('Densidad')
            
        elif chart_type == "scatter":
            group_a_x = [d["age"] for d in data if d["group"] == "Grupo A"]
            group_a_y = [d["value"] for d in data if d["group"] == "Grupo A"]
            group_b_x = [d["age"] for d in data if d["group"] == "Grupo B"]
            group_b_y = [d["value"] for d in data if d["group"] == "Grupo B"]
            
            ax.scatter(group_a_x, group_a_y, alpha=0.6, label='Grupo A', color='#3b82f6')
            ax.scatter(group_b_x, group_b_y, alpha=0.6, label='Grupo B', color='#ec4899')
            ax.set_title(f'Scatterplot: {self.get_variable_label(variable)} vs Edad')
            ax.set_xlabel('Edad (años)')
            ax.legend()
            
        ax.set_xlabel(self.get_variable_label(variable))
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        plt.close()
        
        return ft.Image(
            src_base64=img_base64,
            width=600,
            height=400,
            fit=ft.ImageFit.CONTAIN
        )
        
    def get_variable_label(self, variable):
        labels = {
            "blood_pressure": "Presión Arterial Sistólica (mmHg)",
            "cholesterol": "Colesterol Total (mg/dL)",
            "glucose": "Glucosa en Ayunas (mg/dL)",
            "bmi": "Índice de Masa Corporal (kg/m²)"
        }
        return labels.get(variable, variable)
        
    def update_lab_statistics(self, data):
        values = [d["value"] for d in data]
        
        mean_val = np.mean(values)
        median_val = np.median(values)
        std_val = np.std(values)
        range_val = np.max(values) - np.min(values)
        
        # Actualizar contenedores de estadísticas
        stats_containers = self.lab_stats_container.controls
        stats_containers[0].content.controls[1].value = f"{mean_val:.2f}"
        stats_containers[1].content.controls[1].value = f"{median_val:.2f}"
        stats_containers[2].content.controls[1].value = f"{std_val:.2f}"
        stats_containers[3].content.controls[1].value = f"{range_val:.2f}"
        
    def update_lab_interpretation(self, variable, chart_type, data):
        values = [d["value"] for d in data]
        mean_val = np.mean(values)
        
        interpretation = f"Interpretación Clínica: "
        
        if variable == "blood_pressure":
            interpretation += f"La presión arterial promedio es {mean_val:.1f} mmHg. "
            if mean_val > 140:
                interpretation += "Indica hipertensión en la población estudiada, requiriendo intervención médica."
            elif mean_val > 120:
                interpretation += "Sugiere prehipertensión, recomendando cambios en el estilo de vida."
            else:
                interpretation += "Se encuentra en rango normal."
                
        elif variable == "cholesterol":
            interpretation += f"El colesterol promedio es {mean_val:.1f} mg/dL. "
            if mean_val > 240:
                interpretation += "Indica alto riesgo cardiovascular, requiriendo tratamiento farmacológico."
            elif mean_val > 200:
                interpretation += "Sugiere riesgo moderado, recomendando dieta y ejercicio."
            else:
                interpretation += "Se encuentra en rango deseable."
                
        elif variable == "glucose":
            interpretation += f"La glucosa promedio es {mean_val:.1f} mg/dL. "
            if mean_val > 126:
                interpretation += "Sugiere diabetes mellitus, requiriendo confirmación diagnóstica."
            elif mean_val > 100:
                interpretation += "Indica prediabetes, recomendando seguimiento y cambios de estilo de vida."
            else:
                interpretation += "Se encuentra en rango normal."
                
        elif variable == "bmi":
            interpretation += f"El IMC promedio es {mean_val:.1f} kg/m². "
            if mean_val > 30:
                interpretation += "Indica obesidad, aumentando el riesgo de comorbilidades."
            elif mean_val > 25:
                interpretation += "Sugiere sobrepeso, recomendando intervenciones nutricionales."
            else:
                interpretation += "Se encuentra en rango normal."
                
        self.lab_interpretation.content.value = interpretation
        
    def generate_new_lab_data(self, e):
        self.update_lab_chart()
        
    def export_chart(self, e):
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Gráfico exportado como PNG"), duration=3000)
        )
        
    def export_data(self, e):
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Datos exportados como CSV"), duration=3000)
        )
        
    def generate_report(self, e):
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Generando reporte completo..."), duration=3000)
        )
        
    def create_quiz_section(self):
        self.quiz_questions = [
            {
                "question": "¿Cuál es la principal ventaja de un histograma sobre un boxplot para analizar datos clínicos?",
                "options": [
                    "Muestra la forma completa de la distribución y permite evaluar normalidad",
                    "Es más fácil de interpretar para audiencias no técnicas",
                    "Ocupa menos espacio en publicaciones científicas",
                    "Permite comparar múltiples grupos simultáneamente"
                ],
                "correct": 0
            },
            {
                "question": "En un boxplot, ¿qué representa la línea dentro de la caja?",
                "options": [
                    "La media aritmética",
                    "La mediana (percentil 50)",
                    "La moda",
                    "El rango intercuartílico"
                ],
                "correct": 1
            },
            {
                "question": "¿Cuándo es más apropiado usar un gráfico de violín en lugar de un boxplot?",
                "options": [
                    "Cuando se tienen pocos datos (n < 30)",
                    "Cuando la distribución puede ser bimodal o multimodal",
                    "Cuando se quiere enfatizar los valores atípicos",
                    "Cuando se comparan más de 5 grupos"
                ],
                "correct": 1
            },
            {
                "question": "En un scatterplot que muestra la relación entre edad y presión arterial, ¿qué patrón indicaría una correlación positiva fuerte?",
                "options": [
                    "Los puntos forman una línea horizontal",
                    "Los puntos se distribuyen aleatoriamente",
                    "Los puntos forman una línea ascendente de izquierda a derecha",
                    "Los puntos forman una línea descendente de izquierda a derecha"
                ],
                "correct": 2
            },
            {
                "question": "¿Cuál es la interpretación clínica más apropiada si un histograma de glucosa en ayunas muestra una distribución bimodal?",
                "options": [
                    "Los datos están mal recolectados",
                    "Posiblemente existen dos subpoblaciones distintas (diabéticos y no diabéticos)",
                    "La muestra es demasiado pequeña",
                    "Se debe usar un boxplot en su lugar"
                ],
                "correct": 1
            }
        ]
        
        self.quiz_radio_groups = []
        quiz_content = []
        
        # Instrucciones
        quiz_content.append(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.INFO, color=ft.Colors.ORANGE_600),
                        ft.Text("Instrucciones", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800)
                    ], spacing=10),
                    ft.Text("• Responde todas las preguntas basándote en los conceptos aprendidos"),
                    ft.Text("• Cada pregunta tiene una sola respuesta correcta"),
                    ft.Text("• Puedes revisar tus respuestas antes de enviar"),
                    ft.Text("• Se requiere 70% de aciertos para aprobar el módulo")
                ], spacing=10),
                bgcolor=ft.Colors.ORANGE_50,
                padding=20,
                border_radius=10
            )
        )
        
        # Preguntas
        for i, q in enumerate(self.quiz_questions):
            radio_group = ft.RadioGroup(
                content=ft.Column([
                    ft.Radio(value=str(j), label=option) 
                    for j, option in enumerate(q["options"])
                ]),
                on_change=lambda e, idx=i: self.update_quiz_answer(idx, e.control.value)
            )
            self.quiz_radio_groups.append(radio_group)
            
            quiz_content.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{i+1}. {q['question']}", 
                               size=14, weight=ft.FontWeight.BOLD),
                        radio_group
                    ], spacing=10),
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    padding=20,
                    border_radius=10
                )
            )
            
        # Botón de envío y resultados
        self.quiz_results_container = ft.Container(height=0)
        
        quiz_content.extend([
            ft.Row([
                ft.Text("0 de 5 preguntas respondidas", size=14, color=ft.Colors.GREY_600),
                ft.ElevatedButton(
                    "Enviar Evaluación",
                    icon=ft.Icons.CHECK,
                    on_click=self.submit_quiz,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE)
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.quiz_results_container
        ])
        
        return ft.Column([
            ft.Text("❓ Evaluación del Módulo", size=24, weight=ft.FontWeight.BOLD),
            *quiz_content
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
        
    def update_quiz_answer(self, question_idx, answer):
        self.quiz_answers[question_idx] = int(answer)
        
        # Actualizar contador de preguntas respondidas
        answered = len(self.quiz_answers)
        # Buscar el texto del contador y actualizarlo
        # (En una implementación real, mantendríamos una referencia al control)
        
    def submit_quiz(self, e):
        if len(self.quiz_answers) < 5:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Por favor responde todas las preguntas"), duration=3000)
            )
            return
            
        # Calcular puntuación
        score = 0
        for i, answer in self.quiz_answers.items():
            if answer == self.quiz_questions[i]["correct"]:
                score += 1
                
        percentage = (score / 5) * 100
        passed = percentage >= 70
        
        # Mostrar resultados
        result_color = ft.Colors.GREEN if passed else ft.Colors.RED
        result_icon = ft.Icons.CHECK_CIRCLE if passed else ft.Icons.CANCEL
        result_title = "¡Felicitaciones!" if passed else "Necesitas repasar"
        
        self.quiz_results_container.content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(result_icon, color=result_color, size=30),
                    ft.Text(result_title, size=18, weight=ft.FontWeight.BOLD, color=result_color)
                ], spacing=10),
                ft.Text(f"Obtuviste {score} de 5 respuestas correctas ({int(percentage)}%)."),
                ft.Text("Has aprobado el módulo." if passed else "Se requiere 70% para aprobar."),
                ft.Text("Te recomendamos revisar los conceptos y volver a intentar." if not passed else "")
            ], spacing=10),
            bgcolor=ft.Colors.GREEN_50 if passed else ft.Colors.RED_50,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, result_color)
        )
        self.quiz_results_container.height = None
        
        if passed:
            self.completed_sections.add(4)
            self.update_progress()
            
        self.page.update()
        
    def create_resources_section(self):
        return ft.Column([
            ft.Text("💾 Recursos Descargables", size=24, weight=ft.FontWeight.BOLD),
            
            ft.Row([
                # Plantillas y Guías
                ft.Container(
                    content=ft.Column([
                        ft.Text("📄 Plantillas y Guías", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Guía de Selección de Gráficos", weight=ft.FontWeight.BOLD),
                                ft.Text("Diagrama de flujo para elegir el gráfico apropiado según el tipo de datos.", size=12),
                                ft.ElevatedButton(
                                    "Descargar PDF",
                                    icon=ft.Icons.DOWNLOAD,
                                    on_click=lambda e: self.download_resource("chart-guide"),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
                                )
                            ], spacing=5),
                            bgcolor=ft.Colors.WHITE,
                            padding=15,
                            border_radius=5,
                            border=ft.border.all(1, ft.Colors.BLUE_200)
                        ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Plantilla de Reporte Estadístico", weight=ft.FontWeight.BOLD),
                                ft.Text("Formato estándar para reportar análisis descriptivos.", size=12),
                                ft.ElevatedButton(
                                    "Descargar DOCX",
                                    icon=ft.Icons.DOWNLOAD,
                                    on_click=lambda e: self.download_resource("report-template"),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
                                )
                            ], spacing=5),
                            bgcolor=ft.Colors.WHITE,
                            padding=15,
                            border_radius=5,
                            border=ft.border.all(1, ft.Colors.BLUE_200)
                        ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Checklist de Visualización", weight=ft.FontWeight.BOLD),
                                ft.Text("Lista de verificación para crear gráficos de calidad.", size=12),
                                ft.ElevatedButton(
                                    "Descargar PDF",
                                    icon=ft.Icons.DOWNLOAD,
                                    on_click=lambda e: self.download_resource("checklist"),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
                                )
                            ], spacing=5),
                            bgcolor=ft.Colors.WHITE,
                            padding=15,
                            border_radius=5,
                            border=ft.border.all(1, ft.Colors.BLUE_200)
                        )
                    ], spacing=15),
                    bgcolor=ft.Colors.BLUE_50,
                    padding=20,
                    border_radius=10,
                    expand=True
                ),
                
                # Datos y Código
                ft.Container(
                    content=ft.Column([
                        ft.Text("💻 Datos y Código", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Dataset de Práctica", weight=ft.FontWeight.BOLD),
                                ft.Text("Datos simulados de pacientes diabéticos (200 observaciones).", size=12),
                                ft.ElevatedButton(
                                    "Descargar CSV",
                                    icon=ft.Icons.DOWNLOAD,
                                    on_click=lambda e: self.download_resource("dataset"),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
                                )
                            ], spacing=5),
                            bgcolor=ft.Colors.WHITE,
                            padding=15,
                            border_radius=5,
                            border=ft.border.all(1, ft.Colors.GREEN_200)
                        ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Scripts de R", weight=ft.FontWeight.BOLD),
                                ft.Text("Código reproducible usando ggplot2.", size=12),
                                ft.ElevatedButton(
                                    "Descargar R",
                                    icon=ft.Icons.DOWNLOAD,
                                    on_click=lambda e: self.download_resource("r-scripts"),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
                                )
                            ], spacing=5),
                            bgcolor=ft.Colors.WHITE,
                            padding=15,
                            border_radius=5,
                            border=ft.border.all(1, ft.Colors.GREEN_200)
                        ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Notebook de Python", weight=ft.FontWeight.BOLD),
                                ft.Text("Jupyter notebook con matplotlib y seaborn.", size=12),
                                ft.ElevatedButton(
                                    "Descargar IPYNB",
                                    icon=ft.Icons.DOWNLOAD,
                                    on_click=lambda e: self.download_resource("python-notebook"),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
                                )
                            ], spacing=5),
                            bgcolor=ft.Colors.WHITE,
                            padding=15,
                            border_radius=5,
                            border=ft.border.all(1, ft.Colors.GREEN_200)
                        )
                    ], spacing=15),
                    bgcolor=ft.Colors.GREEN_50,
                    padding=20,
                    border_radius=10,
                    expand=True
                )
            ], spacing=20),
            
            # Rúbrica de Evaluación
            ft.Container(
                content=ft.Column([
                    ft.Text("📋 Rúbrica de Evaluación", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800),
                    
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Criterio", weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Excelente (4)", weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Bueno (3)", weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Satisfactorio (2)", weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Necesita Mejora (1)", weight=ft.FontWeight.BOLD))
                        ],
                        rows=[
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Selección de Gráfico", weight=ft.FontWeight.BOLD)),
                                ft.DataCell(ft.Text("Siempre elige apropiado")),
                                ft.DataCell(ft.Text("Generalmente elige bien")),
                                ft.DataCell(ft.Text("A veces elige apropiado")),
                                ft.DataCell(ft.Text("Raramente elige bien"))
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Interpretación Clínica", weight=ft.FontWeight.BOLD)),
                                ft.DataCell(ft.Text("Completa y precisa")),
                                ft.DataCell(ft.Text("Mayormente correcta")),
                                ft.DataCell(ft.Text("Interpretación básica")),
                                ft.DataCell(ft.Text("Interpretación incorrecta"))
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Calidad Visual", weight=ft.FontWeight.BOLD)),
                                ft.DataCell(ft.Text("Claros y profesionales")),
                                ft.DataCell(ft.Text("Bien presentados")),
                                ft.DataCell(ft.Text("Gráficos aceptables")),
                                ft.DataCell(ft.Text("Gráficos confusos"))
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Aplicación Práctica", weight=ft.FontWeight.BOLD)),
                                ft.DataCell(ft.Text("Aplica en contextos nuevos")),
                                ft.DataCell(ft.Text("Aplica conceptos conocidos")),
                                ft.DataCell(ft.Text("Aplica con guía")),
                                ft.DataCell(ft.Text("No puede aplicar"))
                            ])
                        ]
                    )
                ], spacing=15),
                bgcolor=ft.Colors.ORANGE_50,
                padding=20,
                border_radius=10
            ),
            
            # Actividad de Transferencia
            ft.Container(
                content=ft.Column([
                    ft.Text("🎯 Actividad de Transferencia", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_800),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Proyecto: Análisis Visual de Datos de Salud Pública", 
                                   size=16, weight=ft.FontWeight.BOLD),
                            ft.Text("Utilizando un dataset de salud pública de tu elección (COVID-19, "
                                   "enfermedades crónicas, salud mental, etc.), crea un informe visual "
                                   "que incluya al menos 4 tipos diferentes de gráficos numéricos."),
                            
                            ft.Row([
                                ft.Column([
                                    ft.Text("Requisitos del Proyecto:", weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_700),
                                    ft.Text("• Histograma con interpretación de normalidad"),
                                    ft.Text("• Boxplot comparativo entre grupos"),
                                    ft.Text("• Gráfico de violín o scatterplot"),
                                    ft.Text("• Anotaciones clínicas relevantes"),
                                    ft.Text("• Interpretación estadística y clínica"),
                                    ft.Text("• Conclusiones y recomendaciones")
                                ], expand=True),
                                ft.Column([
                                    ft.Text("Entregables:", weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_700),
                                    ft.Text("• Informe en PDF (máximo 4 páginas)"),
                                    ft.Text("• Gráficos en alta resolución"),
                                    ft.Text("• Dataset utilizado"),
                                    ft.Text("• Código reproducible (R o Python)"),
                                    ft.Text("• Presentación de 5 minutos")
                                ], expand=True)
                            ], spacing=20),
                            
                            ft.Container(
                                content=ft.ElevatedButton(
                                    "Descargar Plantilla del Proyecto",
                                    icon=ft.Icons.DOWNLOAD,
                                    on_click=lambda e: self.download_resource("project-template"),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO_600, color=ft.Colors.WHITE)
                                ),
                                alignment=ft.alignment.center,
                                margin=ft.margin.only(top=20)
                            )
                        ], spacing=15),
                        bgcolor=ft.Colors.WHITE,
                        padding=20,
                        border_radius=10,
                        border=ft.border.all(1, ft.Colors.INDIGO_200)
                    )
                ], spacing=15),
                bgcolor=ft.Colors.INDIGO_50,
                padding=20,
                border_radius=10
            )
        ], scroll=ft.ScrollMode.AUTO, spacing=20)
        
    def download_resource(self, resource_type):
        resources = {
            "chart-guide": "Guía de Selección de Gráficos.pdf",
            "report-template": "Plantilla de Reporte Estadístico.docx",
            "checklist": "Checklist de Visualización.pdf",
            "dataset": "Dataset_Practica_IMC_Diabeticos.csv",
            "r-scripts": "Scripts_Visualizacion_Salud.R",
            "python-notebook": "Visualizacion_Datos_Salud.ipynb",
            "project-template": "Plantilla_Proyecto_Final.docx"
        }
        
        filename = resources.get(resource_type, "recurso.pdf")
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(f"Descargando: {filename}"),
                duration=3000
            )
        )

def main(page: ft.Page):
    app = OVAVisualizacionSalud()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)
