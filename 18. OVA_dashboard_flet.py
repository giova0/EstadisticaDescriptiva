
import flet as ft
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import threading
import time
import io
import base64
from datetime import datetime
import math

class OVADashboard:
    def __init__(self):
        self.current_section = "intro"
        self.progress = 0
        self.current_question = 0
        self.evaluation_answers = {}
        self.timer_running = False
        self.time_remaining = 1800  # 30 minutos
        self.case_answers = {}
        self.exercise_answers = {}
        
        # Datos simulados para dashboards
        self.health_data = {
            "covid": {
                "total_cases": 1247,
                "recovered": 1089,
                "in_treatment": 134,
                "critical": 24,
                "mean_age": 45.2,
                "std_age": 12.8,
                "median_age": 43.0,
                "range_age": "18-89"
            },
            "diabetes": {
                "total_cases": 892,
                "recovered": 756,
                "in_treatment": 98,
                "critical": 38,
                "mean_age": 52.1,
                "std_age": 15.2,
                "median_age": 49.0,
                "range_age": "25-78"
            },
            "hipertension": {
                "total_cases": 1456,
                "recovered": 1234,
                "in_treatment": 187,
                "critical": 35,
                "mean_age": 58.7,
                "std_age": 11.9,
                "median_age": 57.0,
                "range_age": "35-85"
            }
        }
        
        # Preguntas de evaluación
        self.evaluation_questions = [
            {
                "question": "¿Cuál es la principal función de un dashboard descriptivo en ciencias de la salud?",
                "options": [
                    "Predecir futuros brotes epidemiológicos",
                    "Presentar datos estadísticos de manera visual y comprensible",
                    "Diagnosticar enfermedades automáticamente",
                    "Calcular dosis de medicamentos"
                ],
                "correct": 1,
                "explanation": "Un dashboard descriptivo tiene como función principal presentar datos estadísticos de manera visual y comprensible, facilitando la identificación de patrones y tendencias."
            },
            {
                "question": "En el modelo C(H)ANGE, ¿qué representa la 'E'?",
                "options": [
                    "Epidemiología",
                    "Estadística",
                    "Evaluación",
                    "Evidencia"
                ],
                "correct": 1,
                "explanation": "En el modelo C(H)ANGE, la 'E' representa Estadística, integrando conceptos estadísticos con otras áreas matemáticas."
            },
            {
                "question": "Si tienes los datos: 120, 125, 130, 135, 140, ¿cuál es la mediana?",
                "options": [
                    "125",
                    "130",
                    "135",
                    "132.5"
                ],
                "correct": 1,
                "explanation": "La mediana es el valor central cuando los datos están ordenados. En este caso, 130 es el valor del medio."
            },
            {
                "question": "¿Qué medida de dispersión es más apropiada cuando hay valores extremos en los datos?",
                "options": [
                    "Desviación estándar",
                    "Varianza",
                    "Rango intercuartílico",
                    "Coeficiente de variación"
                ],
                "correct": 2,
                "explanation": "El rango intercuartílico es menos sensible a valores extremos que otras medidas de dispersión."
            },
            {
                "question": "En un dashboard de salud pública, ¿cuál es el KPI más importante para monitorear un brote?",
                "options": [
                    "Costo total del tratamiento",
                    "Número de médicos disponibles",
                    "Tasa de incidencia diaria",
                    "Satisfacción del paciente"
                ],
                "correct": 2,
                "explanation": "La tasa de incidencia diaria es crucial para monitorear la evolución y control de un brote epidemiológico."
            }
        ]

    def create_chart_image(self, chart_type, data, title="", labels=None):
        """Crear gráfico usando matplotlib y convertir a imagen base64"""
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('white')
        
        if chart_type == "line":
            if labels:
                ax.plot(labels, data, marker='o', linewidth=2, markersize=6)
            else:
                ax.plot(data, marker='o', linewidth=2, markersize=6)
            ax.grid(True, alpha=0.3)
            
        elif chart_type == "bar":
            if labels:
                bars = ax.bar(labels, data, color=['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#6B7280'])
                # Rotar etiquetas si son muchas
                if len(labels) > 6:
                    plt.xticks(rotation=45)
            else:
                bars = ax.bar(range(len(data)), data)
                
        elif chart_type == "pie":
            colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#6B7280']
            ax.pie(data, labels=labels, autopct='%1.1f%%', colors=colors[:len(data)])
            
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        # Convertir a base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{image_base64}"

    def update_progress(self, page):
        """Actualizar barra de progreso"""
        sections = ["intro", "theory", "dashboard", "cases", "exercises", "evaluation"]
        current_index = sections.index(self.current_section)
        self.progress = ((current_index + 1) / len(sections)) * 100
        
        if hasattr(self, 'progress_bar'):
            self.progress_bar.value = self.progress / 100
            self.progress_text.value = f"{int(self.progress)}% Completado"
            page.update()

    def show_section(self, page, section_name):
        """Mostrar sección específica"""
        self.current_section = section_name
        
        # Limpiar contenido actual
        page.controls.clear()
        
        # Crear header
        header = self.create_header()
        page.add(header)
        
        # Crear navegación
        nav = self.create_navigation(page)
        page.add(nav)
        
        # Mostrar contenido de la sección
        if section_name == "intro":
            content = self.create_intro_section(page)
        elif section_name == "theory":
            content = self.create_theory_section(page)
        elif section_name == "dashboard":
            content = self.create_dashboard_section(page)
        elif section_name == "cases":
            content = self.create_cases_section(page)
        elif section_name == "exercises":
            content = self.create_exercises_section(page)
        elif section_name == "evaluation":
            content = self.create_evaluation_section(page)
            
        page.add(content)
        self.update_progress(page)
        page.update()

    def create_header(self):
        """Crear header de la aplicación"""
        self.progress_bar = ft.ProgressBar(value=0, width=200, height=10)
        self.progress_text = ft.Text("0% Completado", size=12, color=ft.colors.WHITE)
        
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("Dashboard Descriptivo Básico", 
                           size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text("Estadística Descriptiva para Ciencias de la Salud", 
                           size=16, color=ft.colors.WHITE70),
                    ft.Text("Modelo Pedagógico C(H)ANGE", 
                           size=12, color=ft.colors.WHITE60)
                ], expand=True),
                ft.Column([
                    ft.Text("Progreso del Módulo", size=12, color=ft.colors.WHITE),
                    self.progress_bar,
                    self.progress_text
                ], horizontal_alignment=ft.CrossAxisAlignment.END)
            ]),
            padding=20,
            bgcolor=ft.colors.BLUE_700,
            border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
        )

    def create_navigation(self, page):
        """Crear barra de navegación"""
        nav_buttons = [
            ("Introducción", "intro", ft.icons.PLAY_CIRCLE),
            ("Marco Teórico", "theory", ft.icons.BOOK),
            ("Dashboard", "dashboard", ft.icons.DASHBOARD),
            ("Casos Clínicos", "cases", ft.icons.LOCAL_HOSPITAL),
            ("Ejercicios", "exercises", ft.icons.ASSIGNMENT),
            ("Evaluación", "evaluation", ft.icons.QUIZ)
        ]
        
        buttons = []
        for text, section, icon in nav_buttons:
            is_current = section == self.current_section
            button = ft.ElevatedButton(
                text=text,
                icon=icon,
                on_click=lambda e, s=section: self.show_section(page, s),
                bgcolor=ft.colors.BLUE_600 if is_current else ft.colors.GREY_300,
                color=ft.colors.WHITE if is_current else ft.colors.BLACK,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8)
                )
            )
            buttons.append(button)
            
        return ft.Container(
            content=ft.Row(buttons, scroll=ft.ScrollMode.AUTO),
            padding=10,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300)
        )

    def create_intro_section(self, page):
        """Crear sección de introducción"""
        return ft.Container(
            content=ft.Column([
                ft.Container(height=20),
                ft.Text("¡Bienvenido al OVA de Dashboard Descriptivo!", 
                       size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Container(height=10),
                ft.Text("Aprende a crear y interpretar dashboards estadísticos aplicados a las ciencias de la salud mediante el modelo pedagógico C(H)ANGE y herramientas de inteligencia artificial.",
                       size=16, text_align=ft.TextAlign.CENTER, color=ft.colors.GREY_700),
                ft.Container(height=30),
                
                ft.Row([
                    # Objetivos de Aprendizaje
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🎯 Objetivos de Aprendizaje", size=20, weight=ft.FontWeight.BOLD),
                            ft.Container(height=10),
                            ft.Text("✓ Comprender los fundamentos de la estadística descriptiva en salud"),
                            ft.Text("✓ Crear dashboards efectivos para visualizar datos de salud"),
                            ft.Text("✓ Interpretar métricas clave en epidemiología y salud pública"),
                            ft.Text("✓ Aplicar el pensamiento estadístico crítico en casos reales")
                        ]),
                        bgcolor=ft.colors.BLUE_50,
                        padding=20,
                        border_radius=10,
                        expand=True
                    ),
                    ft.Container(width=20),
                    # Modelo C(H)ANGE
                    ft.Container(
                        content=ft.Column([
                            ft.Text("⚙️ Modelo C(H)ANGE", size=20, weight=ft.FontWeight.BOLD),
                            ft.Container(height=10),
                            ft.Row([ft.Container(content=ft.Text("C", color=ft.colors.WHITE), bgcolor=ft.colors.RED, padding=5, border_radius=15, width=30, height=30, alignment=ft.alignment.center), ft.Text("Combinatoria en muestreo")]),
                            ft.Row([ft.Container(content=ft.Text("A", color=ft.colors.WHITE), bgcolor=ft.colors.BLUE, padding=5, border_radius=15, width=30, height=30, alignment=ft.alignment.center), ft.Text("Álgebra en fórmulas estadísticas")]),
                            ft.Row([ft.Container(content=ft.Text("N", color=ft.colors.WHITE), bgcolor=ft.colors.YELLOW_700, padding=5, border_radius=15, width=30, height=30, alignment=ft.alignment.center), ft.Text("Números y medidas de tendencia")]),
                            ft.Row([ft.Container(content=ft.Text("G", color=ft.colors.WHITE), bgcolor=ft.colors.PURPLE, padding=5, border_radius=15, width=30, height=30, alignment=ft.alignment.center), ft.Text("Geometría en visualizaciones")]),
                            ft.Row([ft.Container(content=ft.Text("E", color=ft.colors.WHITE), bgcolor=ft.colors.GREEN, padding=5, border_radius=15, width=30, height=30, alignment=ft.alignment.center), ft.Text("Estadística aplicada")])
                        ]),
                        bgcolor=ft.colors.GREEN_50,
                        padding=20,
                        border_radius=10,
                        expand=True
                    )
                ]),
                
                ft.Container(height=30),
                ft.ElevatedButton(
                    "Comenzar Aprendizaje →",
                    on_click=lambda e: self.show_section(page, "theory"),
                    bgcolor=ft.colors.BLUE_600,
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=30, vertical=15)
                    )
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )

    def create_theory_section(self, page):
        """Crear sección de marco teórico"""
        return ft.Container(
            content=ft.Column([
                ft.Text("📚 Marco Teórico", size=28, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                
                ft.Row([
                    # Columna izquierda
                    ft.Column([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("¿Qué es un Dashboard Descriptivo?", size=18, weight=ft.FontWeight.BOLD),
                                ft.Container(height=10),
                                ft.Text("Un dashboard descriptivo es una herramienta visual que presenta datos estadísticos de manera clara y comprensible, permitiendo la identificación rápida de patrones, tendencias y anomalías en datos de salud."),
                                ft.Container(height=10),
                                ft.Text("Componentes Clave:", weight=ft.FontWeight.BOLD),
                                ft.Text("• Métricas de tendencia central"),
                                ft.Text("• Medidas de dispersión"),
                                ft.Text("• Visualizaciones gráficas"),
                                ft.Text("• Indicadores de alerta")
                            ]),
                            bgcolor=ft.colors.BLUE_50,
                            padding=15,
                            border_radius=10
                        ),
                        ft.Container(height=15),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Estadística Descriptiva en Salud", size=18, weight=ft.FontWeight.BOLD),
                                ft.Container(height=10),
                                ft.Text("La estadística descriptiva en ciencias de la salud permite resumir y presentar datos epidemiológicos, clínicos y de salud pública de manera significativa."),
                                ft.Container(height=10),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("📊", size=24),
                                            ft.Text("Frecuencias", size=12, weight=ft.FontWeight.BOLD)
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        bgcolor=ft.colors.WHITE,
                                        padding=10,
                                        border_radius=8,
                                        expand=True
                                    ),
                                    ft.Container(width=10),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("📈", size=24),
                                            ft.Text("Tendencias", size=12, weight=ft.FontWeight.BOLD)
                                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        bgcolor=ft.colors.WHITE,
                                        padding=10,
                                        border_radius=8,
                                        expand=True
                                    )
                                ])
                            ]),
                            bgcolor=ft.colors.GREEN_50,
                            padding=15,
                            border_radius=10
                        )
                    ], expand=True),
                    
                    ft.Container(width=20),
                    
                    # Columna derecha
                    ft.Column([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Medidas Estadísticas Clave", size=18, weight=ft.FontWeight.BOLD),
                                ft.Container(height=10),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Tendencia Central", weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
                                        ft.Text("Media: Promedio aritmético de los datos", size=12),
                                        ft.Text("Mediana: Valor central de los datos ordenados", size=12),
                                        ft.Text("Moda: Valor más frecuente", size=12)
                                    ]),
                                    bgcolor=ft.colors.WHITE,
                                    padding=10,
                                    border_radius=8
                                ),
                                ft.Container(height=10),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Dispersión", weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_700),
                                        ft.Text("Rango: Diferencia entre máximo y mínimo", size=12),
                                        ft.Text("Desviación Estándar: Medida de variabilidad", size=12),
                                        ft.Text("Coeficiente de Variación: Variabilidad relativa", size=12)
                                    ]),
                                    bgcolor=ft.colors.WHITE,
                                    padding=10,
                                    border_radius=8
                                )
                            ]),
                            bgcolor=ft.colors.PURPLE_50,
                            padding=15,
                            border_radius=10
                        ),
                        ft.Container(height=15),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Aplicaciones en Salud", size=18, weight=ft.FontWeight.BOLD),
                                ft.Container(height=10),
                                ft.Row([ft.Text("🦠", size=16), ft.Text("Vigilancia epidemiológica", size=12)]),
                                ft.Row([ft.Text("💓", size=16), ft.Text("Monitoreo de signos vitales", size=12)]),
                                ft.Row([ft.Text("💊", size=16), ft.Text("Efectividad de tratamientos", size=12)]),
                                ft.Row([ft.Text("🏥", size=16), ft.Text("Gestión hospitalaria", size=12)])
                            ]),
                            bgcolor=ft.colors.YELLOW_50,
                            padding=15,
                            border_radius=10
                        )
                    ], expand=True)
                ]),
                
                ft.Container(height=30),
                ft.ElevatedButton(
                    "Explorar Dashboard →",
                    on_click=lambda e: self.show_section(page, "dashboard"),
                    bgcolor=ft.colors.GREEN_600,
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=30, vertical=15)
                    )
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )

    def create_dashboard_section(self, page):
        """Crear sección de dashboard interactivo"""
        # Crear gráficos
        time_series_data = [45, 52, 48, 61, 55, 67, 73, 69, 58, 62, 56, 49]
        time_labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        age_data = [23, 156, 298, 387, 267, 116]
        age_labels = ['0-18', '19-30', '31-45', '46-60', '61-75', '76+']
        
        time_chart = self.create_chart_image("line", time_series_data, "Tendencia Temporal", time_labels)
        age_chart = self.create_chart_image("bar", age_data, "Distribución por Edad", age_labels)
        
        # Dropdown para seleccionar dataset
        dataset_dropdown = ft.Dropdown(
            label="Seleccionar Dataset",
            options=[
                ft.dropdown.Option("covid", "COVID-19"),
                ft.dropdown.Option("diabetes", "Diabetes"),
                ft.dropdown.Option("hipertension", "Hipertensión")
            ],
            value="covid",
            on_change=lambda e: self.update_dashboard_data(page, e.control.value)
        )
        
        # KPI Cards
        self.kpi_cards = self.create_kpi_cards("covid")
        
        # Tabla de estadísticas
        stats_table = self.create_stats_table("covid")
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("📊 Dashboard Interactivo de Salud", size=28, weight=ft.FontWeight.BOLD),
                    dataset_dropdown,
                    ft.ElevatedButton(
                        "🔄 Actualizar",
                        on_click=lambda e: self.refresh_dashboard(page)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Container(height=20),
                
                # KPI Cards
                ft.Row(self.kpi_cards, scroll=ft.ScrollMode.AUTO),
                
                ft.Container(height=20),
                
                # Gráficos
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Tendencia Temporal", size=16, weight=ft.FontWeight.BOLD),
                            ft.Image(src=time_chart, width=400, height=250, fit=ft.ImageFit.CONTAIN)
                        ]),
                        bgcolor=ft.colors.GREY_50,
                        padding=15,
                        border_radius=10,
                        expand=True
                    ),
                    ft.Container(width=20),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Distribución por Edad", size=16, weight=ft.FontWeight.BOLD),
                            ft.Image(src=age_chart, width=400, height=250, fit=ft.ImageFit.CONTAIN)
                        ]),
                        bgcolor=ft.colors.GREY_50,
                        padding=15,
                        border_radius=10,
                        expand=True
                    )
                ]),
                
                ft.Container(height=20),
                
                # Tabla de estadísticas
                stats_table
            ]),
            padding=20
        )

    def create_kpi_cards(self, dataset):
        """Crear tarjetas KPI"""
        data = self.health_data[dataset]
        
        cards = [
            {
                "title": "Total Casos",
                "value": f"{data['total_cases']:,}",
                "subtitle": "+12% vs mes anterior",
                "color": ft.colors.BLUE_600,
                "icon": "👥"
            },
            {
                "title": "Recuperados",
                "value": f"{data['recovered']:,}",
                "subtitle": f"{(data['recovered']/data['total_cases']*100):.1f}% del total",
                "color": ft.colors.GREEN_600,
                "icon": "💚"
            },
            {
                "title": "En Tratamiento",
                "value": f"{data['in_treatment']:,}",
                "subtitle": f"{(data['in_treatment']/data['total_cases']*100):.1f}% del total",
                "color": ft.colors.YELLOW_600,
                "icon": "🏥"
            },
            {
                "title": "Casos Críticos",
                "value": f"{data['critical']:,}",
                "subtitle": f"{(data['critical']/data['total_cases']*100):.1f}% del total",
                "color": ft.colors.RED_600,
                "icon": "⚠️"
            }
        ]
        
        kpi_widgets = []
        for card in cards:
            widget = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(card["title"], size=12, color=ft.colors.WHITE70),
                            ft.Text(card["value"], size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Text(card["subtitle"], size=10, color=ft.colors.WHITE60)
                        ], expand=True),
                        ft.Text(card["icon"], size=32)
                    ])
                ]),
                bgcolor=card["color"],
                padding=15,
                border_radius=10,
                width=200,
                height=120
            )
            kpi_widgets.append(widget)
            
        return kpi_widgets

    def create_stats_table(self, dataset):
        """Crear tabla de estadísticas"""
        data = self.health_data[dataset]
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Estadísticas Descriptivas", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Métrica", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("Valor", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("Interpretación", weight=ft.FontWeight.BOLD))
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Media de Edad")),
                            ft.DataCell(ft.Text(f"{data['mean_age']} años")),
                            ft.DataCell(ft.Text("Edad promedio de pacientes"))
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Desviación Estándar")),
                            ft.DataCell(ft.Text(f"{data['std_age']} años")),
                            ft.DataCell(ft.Text("Variabilidad en edades"))
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Mediana")),
                            ft.DataCell(ft.Text(f"{data['median_age']} años")),
                            ft.DataCell(ft.Text("Valor central"))
                        ]),
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text("Rango")),
                            ft.DataCell(ft.Text(f"{data['range_age']} años")),
                            ft.DataCell(ft.Text("Amplitud de datos"))
                        ])
                    ]
                )
            ]),
            bgcolor=ft.colors.GREY_50,
            padding=15,
            border_radius=10
        )

    def update_dashboard_data(self, page, dataset):
        """Actualizar datos del dashboard"""
        # Actualizar KPI cards
        new_cards = self.create_kpi_cards(dataset)
        # Aquí necesitarías actualizar los widgets existentes
        page.update()

    def refresh_dashboard(self, page):
        """Simular actualización del dashboard"""
        # Mostrar indicador de carga
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Actualizando dashboard...")))
        page.update()

    def create_cases_section(self, page):
        """Crear sección de casos clínicos"""
        # Gráfico para caso 1
        case1_data = [3, 8, 12, 9, 7, 4, 2]
        case1_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70']
        case1_chart = self.create_chart_image("bar", case1_data, "Casos por Edad", case1_labels)
        
        # Gráfico para caso 2
        days = list(range(1, 31))
        systolic = [145, 142, 148, 155, 138, 162, 149, 144, 151, 139, 147, 153, 141, 158, 146, 143, 150, 156, 140, 152, 148, 145, 159, 142, 147, 154, 141, 149, 146, 143]
        case2_chart = self.create_chart_image("line", systolic, "Presión Arterial - 30 días", [f"D{i}" for i in days[::5]])
        
        return ft.Container(
            content=ft.Column([
                ft.Text("👨‍⚕️ Casos Clínicos Interactivos", size=28, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                
                # Caso 1
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Column([
                                ft.Text("Caso 1: Brote de Gastroenteritis", size=20, weight=ft.FontWeight.BOLD),
                                ft.Text("Hospital Regional - Servicio de Emergencias", color=ft.colors.GREY_600)
                            ], expand=True),
                            ft.Container(
                                content=ft.Text("Urgente", color=ft.colors.WHITE),
                                bgcolor=ft.colors.RED_600,
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=15
                            )
                        ]),
                        ft.Container(height=15),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Situación:", weight=ft.FontWeight.BOLD),
                                ft.Text("En las últimas 48 horas, el hospital ha registrado un aumento significativo de casos de gastroenteritis. Se necesita analizar los datos para identificar patrones y tomar decisiones informadas."),
                                ft.Container(height=10),
                                
                                ft.Row([
                                    ft.Column([
                                        ft.Text("Datos Disponibles:", weight=ft.FontWeight.BOLD),
                                        ft.Text("• 45 casos registrados"),
                                        ft.Text("• Edades: 8-67 años"),
                                        ft.Text("• Síntomas: náuseas, vómitos, diarrea"),
                                        ft.Text("• Tiempo de evolución: 6-24 horas")
                                    ], expand=True),
                                    ft.Container(
                                        content=ft.Image(src=case1_chart, width=300, height=200, fit=ft.ImageFit.CONTAIN),
                                        bgcolor=ft.colors.WHITE,
                                        padding=10,
                                        border_radius=8
                                    )
                                ])
                            ]),
                            bgcolor=ft.colors.GREY_50,
                            padding=15,
                            border_radius=10
                        ),
                        
                        ft.Container(height=15),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Pregunta de Análisis:", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                ft.Text("¿Cuál es la edad promedio de los pacientes afectados y qué nos indica la distribución de edades?", color=ft.colors.BLUE_700),
                                ft.Container(height=10),
                                
                                ft.Column([
                                    ft.ElevatedButton(
                                        "A) Media: 32 años, distribución normal",
                                        on_click=lambda e: self.select_case_answer(page, "case1", "a"),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                                    ),
                                    ft.ElevatedButton(
                                        "B) Media: 28 años, sesgo hacia jóvenes",
                                        on_click=lambda e: self.select_case_answer(page, "case1", "b"),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                                    ),
                                    ft.ElevatedButton(
                                        "C) Media: 35 años, distribución bimodal",
                                        on_click=lambda e: self.select_case_answer(page, "case1", "c"),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                                    )
                                ])
                            ]),
                            bgcolor=ft.colors.BLUE_50,
                            padding=15,
                            border_radius=10
                        )
                    ]),
                    border=ft.border.all(1, ft.colors.GREY_300),
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(height=30),
                
                # Caso 2
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Column([
                                ft.Text("Caso 2: Monitoreo de Presión Arterial", size=20, weight=ft.FontWeight.BOLD),
                                ft.Text("Clínica Cardiovascular - Consulta Externa", color=ft.colors.GREY_600)
                            ], expand=True),
                            ft.Container(
                                content=ft.Text("Seguimiento", color=ft.colors.WHITE),
                                bgcolor=ft.colors.YELLOW_600,
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=15
                            )
                        ]),
                        ft.Container(height=15),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Situación:", weight=ft.FontWeight.BOLD),
                                ft.Text("Un paciente de 55 años ha estado monitoreando su presión arterial durante 30 días. Necesitas analizar las mediciones para evaluar el control de su hipertensión."),
                                ft.Container(height=10),
                                
                                ft.Row([
                                    ft.Column([
                                        ft.Text("Mediciones (mmHg):", weight=ft.FontWeight.BOLD),
                                        ft.Text("Sistólica: 125-165 (Media: 142)"),
                                        ft.Text("Diastólica: 78-98 (Media: 88)"),
                                        ft.Text("Desv. Estándar: Sist: 12.5, Diast: 6.8"),
                                        ft.Text("Mediciones fuera de rango: 23%")
                                    ], expand=True),
                                    ft.Container(
                                        content=ft.Image(src=case2_chart, width=300, height=200, fit=ft.ImageFit.CONTAIN),
                                        bgcolor=ft.colors.WHITE,
                                        padding=10,
                                        border_radius=8
                                    )
                                ])
                            ]),
                            bgcolor=ft.colors.GREY_50,
                            padding=15,
                            border_radius=10
                        ),
                        
                        ft.Container(height=15),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Pregunta de Interpretación:", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                                ft.Text("Basándote en las estadísticas descriptivas, ¿cuál es tu recomendación clínica?", color=ft.colors.GREEN_700),
                                ft.Container(height=10),
                                
                                ft.Column([
                                    ft.ElevatedButton(
                                        "A) Control óptimo, mantener tratamiento actual",
                                        on_click=lambda e: self.select_case_answer(page, "case2", "a"),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                                    ),
                                    ft.ElevatedButton(
                                        "B) Control subóptimo, considerar ajuste de medicación",
                                        on_click=lambda e: self.select_case_answer(page, "case2", "b"),
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                                    )
                                ])
                            ]),
                            bgcolor=ft.colors.GREEN_50,
                            padding=15,
                            border_radius=10
                        )
                    ]),
                    border=ft.border.all(1, ft.colors.GREY_300),
                    padding=20,
                    border_radius=10
                )
            ]),
            padding=20
        )

    def select_case_answer(self, page, case_id, answer):
        """Manejar selección de respuesta en casos clínicos"""
        self.case_answers[case_id] = answer
        
        # Mostrar retroalimentación
        if case_id == "case1":
            if answer == "b":
                feedback = "✅ ¡Correcto! La media de edad es aproximadamente 28 años con un sesgo hacia pacientes jóvenes, lo que sugiere una posible fuente de contaminación común en lugares frecuentados por este grupo etario."
                color = ft.colors.GREEN_600
            else:
                feedback = "❌ Incorrecto. Revisa los datos de edad. La distribución muestra una concentración en pacientes jóvenes, con una media de aproximadamente 28 años."
                color = ft.colors.RED_600
        elif case_id == "case2":
            if answer == "b":
                feedback = "✅ ¡Correcto! Con una media de 142/88 mmHg y 23% de mediciones fuera del rango objetivo, se recomienda considerar un ajuste en la medicación antihipertensiva."
                color = ft.colors.GREEN_600
            else:
                feedback = "❌ Incorrecto. Los valores promedio (142/88 mmHg) están por encima del objetivo terapéutico (<140/90 mmHg), indicando un control subóptimo."
                color = ft.colors.RED_600
        
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(feedback),
                bgcolor=color
            )
        )

    def create_exercises_section(self, page):
        """Crear sección de ejercicios"""
        # Crear gráfico para ejercicio 2
        exercise_data = [65, 78, 90, 81, 95, 87, 102]
        exercise_labels = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio']
        exercise_chart = self.create_chart_image("line", exercise_data, "Casos Registrados por Mes", exercise_labels)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📝 Ejercicios Prácticos", size=28, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                
                # Ejercicio 1
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ejercicio 1: Cálculo de Medidas de Tendencia Central", size=20, weight=ft.FontWeight.BOLD),
                        ft.Container(height=15),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Los siguientes datos representan los niveles de glucosa en sangre (mg/dL) de 15 pacientes diabéticos:"),
                                ft.Container(height=10),
                                ft.Container(
                                    content=ft.Text("120, 135, 142, 128, 156, 134, 149, 138, 125, 162, 144, 131, 147, 139, 153", 
                                                   style=ft.TextStyle(font_family="monospace")),
                                    bgcolor=ft.colors.WHITE,
                                    padding=10,
                                    border_radius=8
                                )
                            ]),
                            bgcolor=ft.colors.BLUE_50,
                            padding=15,
                            border_radius=10
                        ),
                        
                        ft.Container(height=15),
                        
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Media:", weight=ft.FontWeight.BOLD),
                                    ft.TextField(
                                        label="Ingresa la media",
                                        keyboard_type=ft.KeyboardType.NUMBER,
                                        on_change=lambda e: setattr(self, 'ex1_mean', e.control.value)
                                    )
                                ]),
                                bgcolor=ft.colors.GREY_50,
                                padding=15,
                                border_radius=10,
                                expand=True
                            ),
                            ft.Container(width=10),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Mediana:", weight=ft.FontWeight.BOLD),
                                    ft.TextField(
                                        label="Ingresa la mediana",
                                        keyboard_type=ft.KeyboardType.NUMBER,
                                        on_change=lambda e: setattr(self, 'ex1_median', e.control.value)
                                    )
                                ]),
                                bgcolor=ft.colors.GREY_50,
                                padding=15,
                                border_radius=10,
                                expand=True
                            ),
                            ft.Container(width=10),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Desviación Estándar:", weight=ft.FontWeight.BOLD),
                                    ft.TextField(
                                        label="Ingresa la desv. estándar",
                                        keyboard_type=ft.KeyboardType.NUMBER,
                                        on_change=lambda e: setattr(self, 'ex1_std', e.control.value)
                                    )
                                ]),
                                bgcolor=ft.colors.GREY_50,
                                padding=15,
                                border_radius=10,
                                expand=True
                            )
                        ]),
                        
                        ft.Container(height=15),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "Verificar Respuestas",
                                on_click=lambda e: self.check_exercise1(page),
                                bgcolor=ft.colors.BLUE_600,
                                color=ft.colors.WHITE
                            ),
                            ft.TextButton(
                                "💡 Mostrar Pista",
                                on_click=lambda e: self.show_exercise_hint(page, "ex1")
                            )
                        ])
                    ]),
                    border=ft.border.all(1, ft.colors.GREY_300),
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(height=30),
                
                # Ejercicio 2
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ejercicio 2: Interpretación de Dashboard", size=20, weight=ft.FontWeight.BOLD),
                        ft.Container(height=15),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Observa el siguiente dashboard de un hospital y responde las preguntas:"),
                                ft.Container(height=10),
                                ft.Container(
                                    content=ft.Image(src=exercise_chart, width=500, height=300, fit=ft.ImageFit.CONTAIN),
                                    bgcolor=ft.colors.WHITE,
                                    padding=15,
                                    border_radius=8
                                )
                            ]),
                            bgcolor=ft.colors.GREEN_50,
                            padding=15,
                            border_radius=10
                        ),
                        
                        ft.Container(height=15),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("1. ¿En qué mes se registró el mayor número de casos?", weight=ft.FontWeight.BOLD),
                                ft.Container(height=10),
                                ft.Row([
                                    ft.ElevatedButton("Enero", on_click=lambda e: self.select_exercise_answer(page, "q1", "enero")),
                                    ft.ElevatedButton("Marzo", on_click=lambda e: self.select_exercise_answer(page, "q1", "marzo")),
                                    ft.ElevatedButton("Mayo", on_click=lambda e: self.select_exercise_answer(page, "q1", "mayo")),
                                    ft.ElevatedButton("Julio", on_click=lambda e: self.select_exercise_answer(page, "q1", "julio"))
                                ])
                            ]),
                            bgcolor=ft.colors.GREY_50,
                            padding=15,
                            border_radius=10
                        ),
                        
                        ft.Container(height=10),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("2. ¿Cuál es la tendencia general observada?", weight=ft.FontWeight.BOLD),
                                ft.Container(height=10),
                                ft.Row([
                                    ft.ElevatedButton("Tendencia creciente", on_click=lambda e: self.select_exercise_answer(page, "q2", "creciente")),
                                    ft.ElevatedButton("Tendencia decreciente", on_click=lambda e: self.select_exercise_answer(page, "q2", "decreciente")),
                                    ft.ElevatedButton("Relativamente estable", on_click=lambda e: self.select_exercise_answer(page, "q2", "estable"))
                                ])
                            ]),
                            bgcolor=ft.colors.GREY_50,
                            padding=15,
                            border_radius=10
                        )
                    ]),
                    border=ft.border.all(1, ft.colors.GREY_300),
                    padding=20,
                    border_radius=10
                )
            ]),
            padding=20
        )

    def check_exercise1(self, page):
        """Verificar respuestas del ejercicio 1"""
        try:
            mean_input = float(getattr(self, 'ex1_mean', 0))
            median_input = float(getattr(self, 'ex1_median', 0))
            std_input = float(getattr(self, 'ex1_std', 0))
            
            # Valores correctos
            correct_mean = 141.0
            correct_median = 139.0
            correct_std = 12.4
            
            tolerance = 2
            score = 0
            results = []
            
            if abs(mean_input - correct_mean) <= tolerance:
                results.append("✓ Media correcta")
                score += 1
            else:
                results.append(f"✗ Media incorrecta (Correcto: {correct_mean})")
                
            if abs(median_input - correct_median) <= tolerance:
                results.append("✓ Mediana correcta")
                score += 1
            else:
                results.append(f"✗ Mediana incorrecta (Correcto: {correct_median})")
                
            if abs(std_input - correct_std) <= tolerance:
                results.append("✓ Desviación estándar correcta")
                score += 1
            else:
                results.append(f"✗ Desviación estándar incorrecta (Correcto: {correct_std})")
            
            percentage = round((score / 3) * 100)
            feedback = f"Resultados ({percentage}%):\n" + "\n".join(results)
            
            if score == 3:
                feedback += "\n¡Excelente! Has calculado correctamente todas las medidas."
                color = ft.colors.GREEN_600
            else:
                feedback += "\nRevisa los cálculos y vuelve a intentarlo."
                color = ft.colors.ORANGE_600
                
            page.show_snack_bar(ft.SnackBar(content=ft.Text(feedback), bgcolor=color))
            
        except ValueError:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Por favor ingresa valores numéricos válidos"), bgcolor=ft.colors.RED_600))

    def show_exercise_hint(self, page, exercise_id):
        """Mostrar pista para ejercicio"""
        if exercise_id == "ex1":
            hint = "Pista: Para calcular la media, suma todos los valores y divide entre el número de observaciones (15). Para la mediana, ordena los datos y toma el valor central."
            page.show_snack_bar(ft.SnackBar(content=ft.Text(hint), bgcolor=ft.colors.BLUE_600))

    def select_exercise_answer(self, page, question_id, answer):
        """Manejar respuestas de ejercicios"""
        self.exercise_answers[question_id] = answer
        
        if question_id == "q1":
            if answer == "julio":
                feedback = "✅ Correcto. Julio registró 102 casos, el valor más alto."
                color = ft.colors.GREEN_600
            else:
                feedback = "❌ Incorrecto. Observa el gráfico: julio tiene el pico más alto."
                color = ft.colors.RED_600
        elif question_id == "q2":
            if answer == "creciente":
                feedback = "✅ Correcto. Se observa una tendencia general creciente a lo largo del tiempo."
                color = ft.colors.GREEN_600
            else:
                feedback = "❌ Incorrecto. Aunque hay fluctuaciones, la tendencia general es ascendente."
                color = ft.colors.RED_600
        
        page.show_snack_bar(ft.SnackBar(content=ft.Text(feedback), bgcolor=color))

    def create_evaluation_section(self, page):
        """Crear sección de evaluación"""
        self.timer_text = ft.Text("30:00", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_800)
        self.eval_progress_text = ft.Text("0/5", weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_800)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📋 Evaluación Final", size=28, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("ℹ️", size=20),
                            ft.Text("Instrucciones", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_800)
                        ]),
                        ft.Container(height=10),
                        ft.Text("Esta evaluación consta de 5 preguntas que abarcan todos los conceptos aprendidos en este OVA. Tienes 30 minutos para completarla. Se requiere un mínimo de 70% para aprobar.", color=ft.colors.INDIGO_700),
                        ft.Container(height=15),
                        ft.Row([
                            ft.Row([
                                ft.Text("Tiempo restante:", size=12, color=ft.colors.INDIGO_600),
                                self.timer_text
                            ]),
                            ft.Row([
                                ft.Text("Progreso:", size=12, color=ft.colors.INDIGO_600),
                                self.eval_progress_text
                            ])
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    bgcolor=ft.colors.INDIGO_50,
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(height=20),
                
                # Contenedor para preguntas
                ft.Container(
                    content=self.create_evaluation_question(0),
                    key="question_container"
                ),
                
                ft.Container(height=20),
                
                ft.Row([
                    ft.ElevatedButton(
                        "⬅️ Anterior",
                        on_click=lambda e: self.previous_question(page),
                        disabled=True,
                        key="prev_btn"
                    ),
                    ft.ElevatedButton(
                        "Siguiente ➡️",
                        on_click=lambda e: self.next_question(page),
                        bgcolor=ft.colors.INDIGO_600,
                        color=ft.colors.WHITE,
                        key="next_btn"
                    ),
                    ft.ElevatedButton(
                        "✅ Enviar Evaluación",
                        on_click=lambda e: self.submit_evaluation(page),
                        bgcolor=ft.colors.GREEN_600,
                        color=ft.colors.WHITE,
                        visible=False,
                        key="submit_btn"
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]),
            padding=20
        )

    def create_evaluation_question(self, question_index):
        """Crear pregunta de evaluación"""
        if question_index >= len(self.evaluation_questions):
            return ft.Text("Pregunta no encontrada")
            
        q = self.evaluation_questions[question_index]
        
        option_buttons = []
        for i, option in enumerate(q["options"]):
            button = ft.ElevatedButton(
                f"{chr(65 + i)}) {option}",
                on_click=lambda e, idx=i: self.select_evaluation_answer(question_index, idx),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.padding.all(15)
                ),
                width=600
            )
            option_buttons.append(button)
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(f"Pregunta {question_index + 1} de {len(self.evaluation_questions)}", 
                           size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Puntos: 20", size=12, color=ft.colors.GREY_600)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=15),
                ft.Text(q["question"], size=14),
                ft.Container(height=15),
                ft.Column(option_buttons, spacing=10)
            ]),
            bgcolor=ft.colors.GREY_50,
            padding=20,
            border_radius=10
        )

    def select_evaluation_answer(self, question_index, option_index):
        """Seleccionar respuesta de evaluación"""
        self.evaluation_answers[question_index] = option_index
        self.update_evaluation_progress()

    def update_evaluation_progress(self):
        """Actualizar progreso de evaluación"""
        answered = len(self.evaluation_answers)
        total = len(self.evaluation_questions)
        self.eval_progress_text.value = f"{answered}/{total}"

    def next_question(self, page):
        """Ir a siguiente pregunta"""
        if self.current_question < len(self.evaluation_questions) - 1:
            self.current_question += 1
            # Actualizar contenido de pregunta
            # Aquí necesitarías actualizar el contenedor de preguntas
            page.update()

    def previous_question(self, page):
        """Ir a pregunta anterior"""
        if self.current_question > 0:
            self.current_question -= 1
            # Actualizar contenido de pregunta
            page.update()

    def start_timer(self, page):
        """Iniciar temporizador de evaluación"""
        def update_timer():
            while self.timer_running and self.time_remaining > 0:
                minutes = self.time_remaining // 60
                seconds = self.time_remaining % 60
                self.timer_text.value = f"{minutes:02d}:{seconds:02d}"
                page.update()
                time.sleep(1)
                self.time_remaining -= 1
            
            if self.time_remaining <= 0:
                self.submit_evaluation(page)
        
        self.timer_running = True
        timer_thread = threading.Thread(target=update_timer)
        timer_thread.daemon = True
        timer_thread.start()

    def submit_evaluation(self, page):
        """Enviar evaluación"""
        self.timer_running = False
        
        correct_answers = 0
        total_questions = len(self.evaluation_questions)
        
        for i, q in enumerate(self.evaluation_questions):
            user_answer = self.evaluation_answers.get(i)
            if user_answer == q["correct"]:
                correct_answers += 1
        
        score = round((correct_answers / total_questions) * 100)
        passed = score >= 70
        
        result_text = f"Puntuación: {score}%\n{correct_answers} de {total_questions} respuestas correctas"
        
        if passed:
            result_text += "\n¡Felicitaciones! Has completado exitosamente el OVA."
            color = ft.colors.GREEN_600
        else:
            result_text += "\nNecesitas mejorar. Te recomendamos revisar el contenido."
            color = ft.colors.RED_600
        
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(result_text),
                bgcolor=color,
                duration=10000
            )
        )

def main(page: ft.Page):
    page.title = "OVA Dashboard Descriptivo - Ciencias de la Salud"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1200
    page.window_height = 800
    page.window_resizable = True
    page.scroll = ft.ScrollMode.AUTO
    
    # Crear instancia de la aplicación
    app = OVADashboard()
    
    # Mostrar sección inicial
    app.show_section(page, "intro")

if __name__ == "__main__":
    ft.app(target=main)
