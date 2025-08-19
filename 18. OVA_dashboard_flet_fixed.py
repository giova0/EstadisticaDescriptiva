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
        self.progress_text = ft.Text("0% Completado", size=12, color="#FFFFFF")
        
        return ft.Container(
            content=ft.Column([
                ft.Text("OVA 18: Dashboard Descriptivo Básico", 
                       size=28, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ft.Text("Universidad Antonio Nariño - Estadística Descriptiva", 
                       size=16, color="#FFFFFF"),
                ft.Text("Módulo de Aprendizaje Interactivo", 
                       size=12, color="#FFFFFF"),
                ft.Row([
                    ft.Text("Progreso del Módulo", size=12, color="#FFFFFF"),
                    ft.Container(
                        content=ft.ProgressBar(width=200, color="#3B82F6", bgcolor="#D1D5DB"),
                        ref=self.progress_bar
                    ),
                    self.progress_text
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#1E40AF",
            padding=20,
            border_radius=10
        )

    def create_navigation(self, page):
        """Crear navegación entre secciones"""
        sections = [
            ("intro", "Introducción"),
            ("theory", "Teoría"),
            ("dashboard", "Dashboard"),
            ("cases", "Casos Clínicos"),
            ("exercises", "Ejercicios"),
            ("evaluation", "Evaluación")
        ]
        
        nav_items = []
        for section_id, section_name in sections:
            is_current = self.current_section == section_id
            nav_items.append(
                ft.Container(
                    content=ft.Text(section_name, size=12),
                    bgcolor="#2563EB" if is_current else "#D1D5DB",
                    color="#FFFFFF" if is_current else "#000000",
                    padding=10,
                    border_radius=5,
                    on_click=lambda e, s=section_id: self.show_section(page, s)
                )
            )
        
        return ft.Container(
            content=ft.Row(nav_items, alignment=ft.MainAxisAlignment.CENTER),
            bgcolor="#FFFFFF",
            padding=10,
            border=ft.border.all(1, "#D1D5DB")
        )

    def create_intro_section(self, page):
        """Crear sección de introducción"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Bienvenido al Dashboard Descriptivo Básico", 
                       size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Text("En este módulo aprenderás a crear y interpretar dashboards descriptivos para ciencias de la salud.", 
                       size=16, text_align=ft.TextAlign.CENTER, color="#6B7280"),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Objetivos de Aprendizaje:", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("• Comprender los principios del modelo C(H)ANGE", color="#374151"),
                        ft.Text("• Aplicar estadística descriptiva en dashboards de salud", color="#374151"),
                        ft.Text("• Interpretar indicadores clave de rendimiento (KPIs)", color="#374151"),
                        ft.Text("• Crear visualizaciones efectivas para datos clínicos", color="#374151")
                    ]),
                    bgcolor="#EBF8FF",
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Modelo C(H)ANGE:", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Row([ft.Container(content=ft.Text("C", color="#FFFFFF"), bgcolor="#DC2626", padding=5, border_radius=15, width=30, height=30, alignment=ft.alignment.center), ft.Text("Combinatoria en muestreo")]),
                        ft.Row([ft.Container(content=ft.Text("A", color="#FFFFFF"), bgcolor="#2563EB", padding=5, border_radius=15, width=30, height=30, alignment=ft.alignment.center), ft.Text("Álgebra en fórmulas estadísticas")]),
                        ft.Row([ft.Container(content=ft.Text("N", color="#FFFFFF"), bgcolor="#CA8A04", padding=5, border_radius=15, width=30, height=30, alignment=ft.alignment.center), ft.Text("Números y medidas de tendencia")]),
                        ft.Row([ft.Container(content=ft.Text("G", color="#FFFFFF"), bgcolor="#9333EA", padding=5, border_radius=15, width=30, height=30, alignment=ft.alignment.center), ft.Text("Geometría en visualizaciones")]),
                        ft.Row([ft.Container(content=ft.Text("E", color="#FFFFFF"), bgcolor="#16A34A", padding=5, border_radius=15, width=30, height=30, alignment=ft.alignment.center), ft.Text("Estadística aplicada")])
                    ]),
                    bgcolor="#F0FDF4",
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(
                    content=ft.Text("¡Comienza tu aprendizaje haciendo clic en 'Teoría' en la navegación!", 
                                   size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    bgcolor="#2563EB",
                    color="#FFFFFF",
                    padding=20,
                    border_radius=10,
                    alignment=ft.alignment.center
                )
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )

    def create_theory_section(self, page):
        """Crear sección de teoría"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Fundamentos Teóricos", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("¿Qué es un Dashboard Descriptivo?", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Un dashboard descriptivo es una herramienta visual que presenta información estadística de manera clara y comprensible, permitiendo identificar patrones, tendencias y anomalías en los datos.", color="#374151")
                    ]),
                    bgcolor="#FFFFFF",
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Componentes Principales:", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("• KPIs (Indicadores Clave de Rendimiento)", color="#374151"),
                        ft.Text("• Gráficos y visualizaciones", color="#374151"),
                        ft.Text("• Tablas de datos resumidos", color="#374151"),
                        ft.Text("• Alertas y umbrales", color="#374151")
                    ]),
                    bgcolor="#F3F4F6",
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Medidas Estadísticas en Dashboards:", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Tendencia Central", weight=ft.FontWeight.BOLD, color="#7C3AED"),
                        ft.Text("• Media aritmética: promedio de los valores", color="#374151"),
                        ft.Text("• Mediana: valor central de los datos ordenados", color="#374151"),
                        ft.Text("• Moda: valor más frecuente", color="#374151"),
                        ft.Container(height=10),
                        ft.Text("Dispersión", weight=ft.FontWeight.BOLD, color="#7C3AED"),
                        ft.Text("• Desviación estándar: variabilidad de los datos", color="#374151"),
                        ft.Text("• Rango: diferencia entre máximo y mínimo", color="#374151"),
                        ft.Text("• Rango intercuartílico: variabilidad del 50% central", color="#374151")
                    ]),
                    bgcolor="#FDF2F8",
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Principios de Visualización:", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("• Simplicidad: menos es más", color="#374151"),
                        ft.Text("• Consistencia: usar colores y estilos uniformes", color="#374151"),
                        ft.Text("• Contexto: proporcionar información de referencia", color="#374151"),
                        ft.Text("• Accesibilidad: considerar daltonismo y otras discapacidades", color="#374151")
                    ]),
                    bgcolor="#FEF3C7",
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(
                    content=ft.Text("¡Ahora explora el Dashboard Interactivo!", 
                                   size=16, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    bgcolor="#16A34A",
                    color="#FFFFFF",
                    padding=20,
                    border_radius=10,
                    alignment=ft.alignment.center
                )
            ], spacing=20),
            padding=20
        )

    def create_dashboard_section(self, page):
        """Crear sección de dashboard interactivo"""
        # Crear tarjetas de KPIs
        kpi_cards = [
            {
                "title": "Casos COVID-19",
                "value": str(self.health_data["covid"]["total_cases"]),
                "subtitle": "Total de casos",
                "color": "#2563EB",
            },
            {
                "title": "Casos Diabetes",
                "value": str(self.health_data["diabetes"]["total_cases"]),
                "subtitle": "Total de casos",
                "color": "#16A34A",
            },
            {
                "title": "Casos Hipertensión",
                "value": str(self.health_data["hipertension"]["total_cases"]),
                "subtitle": "Total de casos",
                "color": "#CA8A04",
            },
            {
                "title": "Casos Críticos",
                "value": str(self.health_data["covid"]["critical"] + self.health_data["diabetes"]["critical"] + self.health_data["hipertension"]["critical"]),
                "subtitle": "Total críticos",
                "color": "#DC2626",
            }
        ]
        
        kpi_row = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text(card["title"], size=12, color="#FFFFFF"),
                    ft.Text(card["value"], size=24, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ft.Text(card["subtitle"], size=10, color="#FFFFFF")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=card["color"],
                padding=20,
                border_radius=10,
                width=150,
                height=120
            ) for card in kpi_cards
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        # Crear gráfico de barras
        chart_data = [self.health_data["covid"]["total_cases"], 
                     self.health_data["diabetes"]["total_cases"], 
                     self.health_data["hipertension"]["total_cases"]]
        chart_labels = ["COVID-19", "Diabetes", "Hipertensión"]
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Dashboard Interactivo - Datos de Salud", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                
                ft.Text("Indicadores Clave de Rendimiento (KPIs)", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                kpi_row,
                
                ft.Container(height=20),
                
                ft.Text("Distribución de Casos por Condición", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                ft.Container(
                    content=ft.Image(src=self.create_chart_image("bar", chart_data, "Casos por Condición", chart_labels)),
                    bgcolor="#F9FAFB",
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Interpretación:", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("• La hipertensión presenta la mayor carga de casos", color="#374151"),
                        ft.Text("• El COVID-19 muestra una distribución moderada", color="#374151"),
                        ft.Text("• La diabetes tiene la menor prevalencia en este período", color="#374151"),
                        ft.Text("• Los casos críticos representan aproximadamente el 3% del total", color="#374151")
                    ]),
                    bgcolor="#F3F4F6",
                    padding=20,
                    border_radius=10
                )
            ], spacing=20),
            padding=20
        )

    def create_cases_section(self, page):
        """Crear sección de casos clínicos"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Casos Clínicos - Análisis de Dashboards", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                
                # Caso 1
                ft.Container(
                    content=ft.Column([
                        ft.Text("Caso 1: Servicio de Emergencias", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Hospital Regional - Servicio de Emergencias", color="#6B7280"),
                        
                        ft.Row([
                            ft.Container(
                                content=ft.Text("Urgente", color="#FFFFFF"),
                                bgcolor="#DC2626",
                                padding=10,
                                border_radius=5
                            ),
                            ft.Text("Prioridad Alta", color="#374151")
                        ]),
                        
                        ft.Text("Datos del último mes:", color="#374151"),
                        ft.Text("• Total de pacientes: 1,247", color="#374151"),
                        ft.Text("• Tiempo promedio de espera: 45 minutos", color="#374151"),
                        ft.Text("• Tasa de ocupación: 87%", color="#374151"),
                        ft.Text("• Satisfacción del paciente: 4.2/5", color="#374151")
                    ]),
                    bgcolor="#FFFFFF",
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Pregunta de Análisis:", weight=ft.FontWeight.BOLD, color="#1E40AF"),
                        ft.Text("¿Qué indicadores sugieren la distribución de edades?", color="#1E40AF"),
                        
                        ft.TextField(
                            label="Tu respuesta",
                            multiline=True,
                            min_lines=3,
                            max_lines=5,
                            border_color="#D1D5DB"
                        ),
                        
                        ft.ElevatedButton(
                            "Analizar Respuesta",
                            bgcolor="#EBF8FF",
                            color="#1E40AF",
                            on_click=lambda e: self.analyze_case_response(page, "case1")
                        )
                    ]),
                    bgcolor="#F3F4F6",
                    padding=20,
                    border_radius=10
                ),
                
                # Caso 2
                ft.Container(
                    content=ft.Column([
                        ft.Text("Caso 2: Consulta Externa", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Clínica Cardiovascular - Consulta Externa", color="#6B7280"),
                        
                        ft.Row([
                            ft.Container(
                                content=ft.Text("Seguimiento", color="#FFFFFF"),
                                bgcolor="#CA8A04",
                                padding=10,
                                border_radius=5
                            ),
                            ft.Text("Prioridad Media", color="#374151")
                        ]),
                        
                        ft.Text("Datos del último trimestre:", color="#374151"),
                        ft.Text("• Total de consultas: 892", color="#374151"),
                        ft.Text("• Edad promedio: 52.1 años", color="#374151"),
                        ft.Text("• Tasa de adherencia al tratamiento: 78%", color="#374151"),
                        ft.Text("• Reconsultas programadas: 65%", color="#374151")
                    ]),
                    bgcolor="#FFFFFF",
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Pregunta de Interpretación:", weight=ft.FontWeight.BOLD, color="#16A34A"),
                        ft.Text("Basándote en las estadísticas descriptivas, ¿cuál es tu recomendación clínica?", color="#16A34A"),
                        
                        ft.TextField(
                            label="Tu recomendación",
                            multiline=True,
                            min_lines=3,
                            max_lines=5,
                            border_color="#D1D5DB"
                        ),
                        
                        ft.ElevatedButton(
                            "Evaluar Recomendación",
                            bgcolor="#F0FDF4",
                            color="#16A34A",
                            on_click=lambda e: self.analyze_case_response(page, "case2")
                        )
                    ]),
                    bgcolor="#F3F4F6",
                    padding=20,
                    border_radius=10
                )
            ], spacing=20),
            padding=20
        )

    def analyze_case_response(self, page, case_id):
        """Analizar respuesta del caso clínico"""
        if case_id == "case1":
            color = "#16A34A"
            message = "Excelente análisis. Los indicadores de edad promedio, distribución por rangos etarios y mediana de edad son clave para entender la población atendida."
        else:
            color = "#DC2626"
            message = "Buena recomendación. Considera también la adherencia al tratamiento y la necesidad de seguimiento personalizado."
        
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=color
            )
        )

    def create_exercises_section(self, page):
        """Crear sección de ejercicios"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Ejercicios Prácticos", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ejercicio 1: Cálculo de Medidas Descriptivas", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Calcula las medidas de tendencia central y dispersión para el siguiente conjunto de datos:", color="#374151"),
                        ft.Text("Datos: 25, 30, 35, 40, 45, 50, 55, 60, 65, 70", color="#374151", weight=ft.FontWeight.BOLD),
                        
                        ft.TextField(
                            label="Media aritmética",
                            border_color="#D1D5DB"
                        ),
                        ft.TextField(
                            label="Mediana",
                            border_color="#D1D5DB"
                        ),
                        ft.TextField(
                            label="Desviación estándar",
                            border_color="#D1D5DB"
                        ),
                        
                        ft.ElevatedButton(
                            "Verificar Respuestas",
                            bgcolor="#EBF8FF",
                            color="#2563EB",
                            on_click=lambda e: self.check_exercise_answers(page)
                        )
                    ]),
                    bgcolor="#FFFFFF",
                    padding=20,
                    border_radius=10
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ejercicio 2: Interpretación de Dashboard", size=18, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.Text("Observa el siguiente dashboard y responde:", color="#374151"),
                        
                        ft.Text("En un dashboard de salud pública, si la tasa de incidencia de una enfermedad aumenta de 2.5% a 3.8% en una semana, ¿qué interpretación harías?", color="#374151"),
                        
                        ft.TextField(
                            label="Tu interpretación",
                            multiline=True,
                            min_lines=3,
                            max_lines=5,
                            border_color="#D1D5DB"
                        ),
                        
                        ft.ElevatedButton(
                            "Evaluar Interpretación",
                            bgcolor="#F0FDF4",
                            color="#16A34A",
                            on_click=lambda e: self.evaluate_interpretation(page)
                        )
                    ]),
                    bgcolor="#F9FAFB",
                    padding=20,
                    border_radius=10
                )
            ], spacing=20),
            padding=20
        )

    def check_exercise_answers(self, page):
        """Verificar respuestas del ejercicio"""
        # Respuestas correctas
        correct_answers = {
            "media": 47.5,
            "mediana": 47.5,
            "desviacion": 15.14
        }
        
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Respuestas correctas: Media=47.5, Mediana=47.5, Desviación=15.14"),
                bgcolor="#16A34A"
            )
        )

    def evaluate_interpretation(self, page):
        """Evaluar interpretación del ejercicio"""
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Buena interpretación. El aumento del 52% en la tasa de incidencia sugiere una posible aceleración del brote que requiere atención inmediata."),
                bgcolor="#16A34A"
            )
        )

    def create_evaluation_section(self, page):
        """Crear sección de evaluación"""
        self.timer_text = ft.Text("30:00", size=20, weight=ft.FontWeight.BOLD, color="#3730A3")
        self.eval_progress_text = ft.Text("0/5", weight=ft.FontWeight.BOLD, color="#3730A3")
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Evaluación Final", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                
                ft.Row([
                    ft.Text("Instrucciones", size=18, weight=ft.FontWeight.BOLD, color="#3730A3"),
                    ft.Text("• Responde 5 preguntas de opción múltiple", color="#3730A3"),
                    ft.Text("• Tienes 30 minutos para completar la evaluación", color="#3730A3"),
                    ft.Text("• Necesitas un mínimo de 70% para aprobar.", color="#3730A3"),
                    ft.Text("Tiempo restante:", size=12, color="#3730A3"),
                    self.timer_text,
                    ft.Text("Progreso:", size=12, color="#3730A3"),
                    self.eval_progress_text
                ]),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("¿Estás listo para comenzar la evaluación?", size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                        ft.ElevatedButton(
                            "Comenzar Evaluación",
                            bgcolor="#3730A3",
                            color="#FFFFFF",
                            on_click=lambda e: self.start_evaluation(page)
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor="#EEF2FF",
                    padding=20,
                    border_radius=10
                )
            ], spacing=20),
            padding=20
        )

    def start_evaluation(self, page):
        """Iniciar evaluación"""
        self.current_question = 0
        self.evaluation_answers = {}
        self.time_remaining = 1800  # 30 minutos
        self.timer_running = True
        
        # Iniciar timer
        def update_timer():
            while self.timer_running and self.time_remaining > 0:
                time.sleep(1)
                self.time_remaining -= 1
                minutes = self.time_remaining // 60
                seconds = self.time_remaining % 60
                self.timer_text.value = f"{minutes:02d}:{seconds:02d}"
                page.update()
                
                if self.time_remaining <= 0:
                    self.finish_evaluation(page)
                    break
        
        threading.Thread(target=update_timer, daemon=True).start()
        self.show_evaluation_question(page)

    def show_evaluation_question(self, page):
        """Mostrar pregunta de evaluación"""
        if self.current_question >= len(self.evaluation_questions):
            self.finish_evaluation(page)
            return
        
        question_data = self.evaluation_questions[self.current_question]
        
        # Limpiar contenido actual
        page.controls.clear()
        
        # Recrear header y navegación
        header = self.create_header()
        page.add(header)
        
        nav = self.create_navigation(page)
        page.add(nav)
        
        # Crear contenido de la pregunta
        question_content = ft.Container(
            content=ft.Column([
                ft.Text(f"Pregunta {self.current_question + 1} de {len(self.evaluation_questions)}", 
                       size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                
                ft.Text(question_data["question"], size=16, color="#374151"),
                
                ft.Column([
                    ft.ElevatedButton(
                        option,
                        bgcolor="#F3F4F6",
                        color="#1F2937",
                        on_click=lambda e, idx=i: self.select_answer(page, idx)
                    ) for i, option in enumerate(question_data["options"])
                ], spacing=10),
                
                ft.Row([
                    ft.Text("Tiempo restante:", color="#6B7280"),
                    self.timer_text
                ])
            ], spacing=20),
            padding=20
        )
        
        page.add(question_content)
        page.update()

    def select_answer(self, page, answer_index):
        """Seleccionar respuesta de evaluación"""
        self.evaluation_answers[self.current_question] = answer_index
        self.current_question += 1
        
        if self.current_question < len(self.evaluation_questions):
            self.show_evaluation_question(page)
        else:
            self.finish_evaluation(page)

    def finish_evaluation(self, page):
        """Finalizar evaluación"""
        self.timer_running = False
        
        # Calcular puntaje
        correct_answers = 0
        for i, question_data in enumerate(self.evaluation_questions):
            if i in self.evaluation_answers:
                if self.evaluation_answers[i] == question_data["correct"]:
                    correct_answers += 1
        
        score = (correct_answers / len(self.evaluation_questions)) * 100
        
        # Limpiar contenido actual
        page.controls.clear()
        
        # Recrear header y navegación
        header = self.create_header()
        page.add(header)
        
        nav = self.create_navigation(page)
        page.add(nav)
        
        # Mostrar resultados
        result_content = ft.Container(
            content=ft.Column([
                ft.Text("Resultados de la Evaluación", size=24, weight=ft.FontWeight.BOLD, color="#1F2937"),
                
                ft.Text(f"Puntaje: {score:.1f}%", size=20, weight=ft.FontWeight.BOLD, 
                       color="#16A34A" if score >= 70 else "#DC2626"),
                
                ft.Text(f"Respuestas correctas: {correct_answers}/{len(self.evaluation_questions)}", 
                       size=16, color="#374151"),
                
                ft.Text("Estado: APROBADO" if score >= 70 else "Estado: NO APROBADO", 
                       size=18, weight=ft.FontWeight.BOLD,
                       color="#16A34A" if score >= 70 else "#DC2626"),
                
                ft.Container(
                    content=ft.Text("¡Felicitaciones! Has completado el módulo de Dashboard Descriptivo Básico.", 
                                   size=16, color="#FFFFFF"),
                    bgcolor="#16A34A" if score >= 70 else "#DC2626",
                    padding=20,
                    border_radius=10,
                    alignment=ft.alignment.center
                )
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20
        )
        
        page.add(result_content)
        page.update()

def main(page: ft.Page):
    page.title = "OVA 18: Dashboard Descriptivo Básico"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    
    ova = OVADashboard()
    ova.show_section(page, "intro")

if __name__ == "__main__":
    ft.app(target=main) 