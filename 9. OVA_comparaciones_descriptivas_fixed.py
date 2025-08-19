import flet as ft
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import pandas as pd
import statistics
import math
import io
import base64
import os
from datetime import datetime

class OVAApp:
    def __init__(self):
        self.current_section = "intro"
        self.score = 0
        self.total_questions = 0
        self.page = None
        self.main_container = None
        
        # Datos para ejercicios
        self.young_group = [8, 7, 9, 6, 8, 7, 10, 8, 9, 7, 8, 6, 9, 8, 7]
        self.older_group = [12, 14, 11, 13, 15, 12, 16, 13, 14, 12, 15, 13, 14, 11, 13]
        
    def main(self, page: ft.Page):
        self.page = page
        page.title = "OVA 9: Comparaciones Descriptivas entre Grupos"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.window_width = 1200
        page.window_height = 800
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("OVA 9: Comparaciones Descriptivas entre Grupos", 
                           size=24, weight=ft.FontWeight.BOLD, color="#374151"),
                    ft.Text("Estadística Descriptiva para Ciencias de la Salud", 
                           size=16, color="#6B7280")
                ], expand=True),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Modelo C(H)ANGE", size=12, weight=ft.FontWeight.BOLD, color="#1E40AF"),
                        ft.Text("Duración: 2-4 horas", size=10, color="#3B82F6")
                    ]),
                    bgcolor="#DBEAFE",
                    padding=10,
                    border_radius=8
                )
            ]),
            bgcolor="#FFFFFF",
            padding=20,
            border=ft.border.only(bottom=ft.border.BorderSide(4, "#3B82F6"))
        )
        
        # Navigation
        nav_buttons = [
            ("intro", "Introducción"),
            ("theory", "Teoría"),
            ("practice", "Práctica"),
            ("simulation", "Simulación"),
            ("evaluation", "Evaluación"),
            ("resources", "Recursos")
        ]
        
        navigation = ft.Container(
            content=ft.Row([
                ft.ElevatedButton(
                    text=label,
                    on_click=lambda e, section=section: self.show_section(section),
                    bgcolor="#2563EB" if section == self.current_section else "#60A5FA",
                    color="#FFFFFF"
                ) for section, label in nav_buttons
            ], scroll=ft.ScrollMode.AUTO),
            bgcolor="#2563EB",
            padding=10
        )
        
        # Main content container
        self.main_container = ft.Container(
            content=self.create_intro_section(),
            padding=20,
            expand=True
        )
        
        # Layout
        page.add(
            ft.Column([
                header,
                navigation,
                ft.Container(
                    content=self.main_container,
                    expand=True,
                    bgcolor="#F8FAFC"
                )
            ], expand=True)
        )
        
    def show_section(self, section):
        """Cambia la sección actual"""
        self.current_section = section
        
        # Actualizar navegación
        nav_container = self.page.controls[1]  # El contenedor de navegación
        for i, (sect, _) in enumerate([("intro", "Introducción"), ("theory", "Teoría"), 
                                     ("practice", "Práctica"), ("simulation", "Simulación"),
                                     ("evaluation", "Evaluación"), ("resources", "Recursos")]):
            nav_container.content.controls[i].bgcolor = "#2563EB" if sect == section else "#60A5FA"
        
        # Actualizar contenido principal
        if section == "intro":
            self.main_container.content = self.create_intro_section()
        elif section == "theory":
            self.main_container.content = self.create_theory_section()
        elif section == "practice":
            self.main_container.content = self.create_practice_section()
        elif section == "simulation":
            self.main_container.content = self.create_simulation_section()
        elif section == "evaluation":
            self.main_container.content = self.create_evaluation_section()
        elif section == "resources":
            self.main_container.content = self.create_resources_section()
        
        self.page.update()
    
    def create_intro_section(self):
        """Crea la sección de introducción"""
        return ft.Column([
            # Número de sección
            ft.Container(
                content=ft.Text("1", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
                bgcolor="#3B82F6",
                width=40,
                height=40,
                border_radius=20,
                alignment=ft.alignment.center
            ),
            
            ft.Text("Introducción y Objetivos", size=20, weight=ft.FontWeight.BOLD, color="#374151"),
            
            ft.Container(height=20),
            
            ft.Text("¿Por qué comparar grupos en salud?", size=16, weight=ft.FontWeight.BOLD, color="#4B5563"),
            
            ft.Text(
                "Las comparaciones entre grupos son fundamentales en investigación clínica y epidemiología. "
                "Permiten identificar diferencias significativas entre poblaciones y evaluar la efectividad "
                "de intervenciones médicas.",
                color="#6B7280"
            ),
            
            ft.Container(height=10),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Ejemplos clínicos:", weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    ft.Text("• Comparar presión arterial entre hombres y mujeres", color="#3B82F6"),
                    ft.Text("• Analizar tiempo de recuperación por grupos de edad", color="#3B82F6"),
                    ft.Text("• Evaluar efectividad de diferentes tratamientos", color="#3B82F6"),
                    ft.Text("• Estudiar prevalencia de enfermedades por región", color="#3B82F6")
                ]),
                bgcolor="#EFF6FF",
                padding=15,
                border_radius=8
            ),
            
            ft.Container(height=20),
            
            ft.Text("Objetivos de Aprendizaje", size=16, weight=ft.FontWeight.BOLD, color="#4B5563"),
            
            ft.Container(height=10),
            
            self.create_objective_item("Comprender los fundamentos de las comparaciones descriptivas entre grupos"),
            self.create_objective_item("Aplicar métodos estadísticos para comparar grupos en contextos clínicos"),
            self.create_objective_item("Interpretar diferencias entre grupos desde una perspectiva clínica"),
            self.create_objective_item("Utilizar herramientas de visualización para comparaciones grupales"),
            
            ft.Container(height=20),
            
            # Advertencia importante
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.WARNING, color="#D97706"),
                    ft.Column([
                        ft.Text("Importante:", weight=ft.FontWeight.BOLD, color="#D97706"),
                        ft.Text(
                            "Este módulo se enfoca en comparaciones descriptivas. "
                            "Para inferencias estadísticas formales, se requieren pruebas de hipótesis.",
                            color="#D97706"
                        )
                    ])
                ]),
                bgcolor="#FEF3C7",
                padding=15,
                border_radius=8,
                border=ft.border.only(left=ft.border.BorderSide(4, "#F59E0B"))
            )
        ])
    
    def create_objective_item(self, text):
        """Crea un elemento de objetivo de aprendizaje"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text("✓", color="#FFFFFF", size=12, weight=ft.FontWeight.BOLD),
                    bgcolor="#10B981",
                    width=24,
                    height=24,
                    border_radius=12,
                    alignment=ft.alignment.center
                ),
                ft.Text(text, color="#6B7280", expand=True)
            ]),
            margin=ft.margin.only(bottom=5)
        )
    
    def create_theory_section(self):
        """Crea la sección de teoría"""
        return ft.Column([
            ft.Container(
                content=ft.Text("2", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
                bgcolor="#3B82F6",
                width=40,
                height=40,
                border_radius=20,
                alignment=ft.alignment.center
            ),
            
            ft.Text("Fundamentos Teóricos", size=20, weight=ft.FontWeight.BOLD, color="#374151"),
            
            ft.Container(height=20),
            
            # Conceptos básicos
            ft.Container(
                content=ft.Column([
                    ft.Text("Conceptos Básicos", size=16, weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    ft.Text("• Grupo: Conjunto de individuos con características comunes"),
                    ft.Text("• Variable de comparación: Característica que se analiza entre grupos"),
                    ft.Text("• Diferencia descriptiva: Magnitud de la diferencia observada"),
                    ft.Text("• Tamaño del efecto: Medida estandarizada de la diferencia")
                ]),
                bgcolor="#EFF6FF",
                padding=15,
                border_radius=8
            ),
            
            ft.Container(height=15),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Tipos de Comparaciones", size=16, weight=ft.FontWeight.BOLD, color="#059669"),
                    ft.Text("• Comparaciones de medias entre dos grupos"),
                    ft.Text("• Comparaciones de proporciones"),
                    ft.Text("• Comparaciones de distribuciones"),
                    ft.Text("• Comparaciones múltiples (más de dos grupos)")
                ]),
                bgcolor="#ECFDF5",
                padding=15,
                border_radius=8
            ),
            
            ft.Container(height=15),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Medidas de Tamaño del Efecto", size=16, weight=ft.FontWeight.BOLD, color="#7C3AED"),
                    ft.Text("• d de Cohen: Para comparaciones de medias"),
                    ft.Text("• V de Cramer: Para variables categóricas"),
                    ft.Text("• r de Pearson: Para correlaciones"),
                    ft.Text("• Eta cuadrado: Para ANOVA")
                ]),
                bgcolor="#F3E8FF",
                padding=15,
                border_radius=8
            ),
            
            ft.Container(height=20),
            
            # Ejemplo teórico
            ft.Text("Ejemplo Teórico: Comparación de Presión Arterial", size=16, weight=ft.FontWeight.BOLD, color="#DC2626"),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Grupo A (Control): n=30, Media=120 mmHg, SD=10 mmHg"),
                    ft.Text("Grupo B (Tratamiento): n=30, Media=115 mmHg, SD=12 mmHg"),
                    ft.Text("Diferencia absoluta: 5 mmHg"),
                    ft.Text("d de Cohen: 0.45 (efecto moderado)")
                ]),
                bgcolor="#FFFFFF",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, "#D1D5DB")
            )
        ])
    
    def create_practice_section(self):
        """Crea la sección de práctica"""
        return ft.Column([
            ft.Container(
                content=ft.Text("3", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
                bgcolor="#3B82F6",
                width=40,
                height=40,
                border_radius=20,
                alignment=ft.alignment.center
            ),
            
            ft.Text("Práctica Guiada", size=20, weight=ft.FontWeight.BOLD, color="#374151"),
            
            ft.Container(height=20),
            
            ft.Text("Ejercicio: Comparación de Tiempo de Recuperación", size=16, weight=ft.FontWeight.BOLD, color="#1E40AF"),
            
            ft.Text(
                "Se comparan dos grupos de pacientes: jóvenes (18-30 años) y mayores (65+ años) "
                "en cuanto a su tiempo de recuperación post-cirugía (en días)."
            ),
            
            ft.Container(height=15),
            
            # Datos de ejemplo
            ft.Container(
                content=ft.Column([
                    ft.Text("Datos del Estudio:", weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    ft.Text("Grupo Joven (n=15): 8, 7, 9, 6, 8, 7, 10, 8, 9, 7, 8, 6, 9, 8, 7"),
                    ft.Text("Grupo Mayor (n=15): 12, 14, 11, 13, 15, 12, 16, 13, 14, 12, 15, 13, 14, 11, 13")
                ]),
                bgcolor="#F3F4F6",
                padding=15,
                border_radius=8
            ),
            
            ft.Container(height=15),
            
            # Botones de análisis
            ft.Row([
                ft.ElevatedButton(
                    "Calcular Estadísticas",
                    on_click=self.calculate_statistics,
                    bgcolor="#3B82F6",
                    color="#FFFFFF"
                ),
                ft.ElevatedButton(
                    "Mostrar Gráfico",
                    on_click=self.show_comparison_chart,
                    bgcolor="#10B981",
                    color="#FFFFFF"
                )
            ]),
            
            ft.Container(height=15),
            
            # Área de resultados
            ft.Container(
                content=ft.Column([
                    ft.Text("Resultados del Análisis", weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    ft.Text("Haz clic en 'Calcular Estadísticas' para ver los resultados", color="#6B7280")
                ]),
                bgcolor="#FFFFFF",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, "#D1D5DB"),
                ref=self.clinical_interpretation
            ),
            
            ft.Container(height=15),
            
            ft.Text("Interpretación Clínica", weight=ft.FontWeight.BOLD, color="#1E40AF"),
            
            ft.Container(
                content=ft.Text(
                    "Los pacientes mayores muestran un tiempo de recuperación significativamente mayor "
                    "que los pacientes jóvenes, lo que sugiere la necesidad de protocolos de atención "
                    "especializados para este grupo poblacional.",
                    color="#6B7280"
                ),
                bgcolor="#EFF6FF",
                padding=15,
                border_radius=8
            )
        ])
    
    def create_simulation_section(self):
        """Crea la sección de simulación"""
        return ft.Column([
            ft.Container(
                content=ft.Text("4", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
                bgcolor="#3B82F6",
                width=40,
                height=40,
                border_radius=20,
                alignment=ft.alignment.center
            ),
            
            ft.Text("Simulación Interactiva", size=20, weight=ft.FontWeight.BOLD, color="#374151"),
            
            ft.Container(height=20),
            
            ft.ElevatedButton(
                "Iniciar Simulación",
                on_click=self.start_simulation,
                bgcolor="#8B5CF6",
                color="#FFFFFF"
            ),
            
            ft.Container(height=15),
            
            ft.Text("Simulador de Comparaciones entre Grupos", size=16, weight=ft.FontWeight.BOLD, color="#1E40AF"),
            
            ft.Text(
                "Este simulador te permite crear grupos virtuales y comparar sus características. "
                "Puedes ajustar parámetros como el tamaño de muestra, la media y la desviación estándar."
            ),
            
            ft.Container(height=15),
            
            # Controles de simulación
            ft.Container(
                content=ft.Column([
                    ft.Text("Parámetros del Grupo 1:", weight=ft.FontWeight.BOLD),
                    ft.TextField(label="Tamaño de muestra", value="30"),
                    ft.TextField(label="Media", value="100"),
                    ft.TextField(label="Desviación estándar", value="15")
                ]),
                bgcolor="#FFFFFF",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, "#D1D5DB")
            ),
            
            ft.Container(height=10),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Parámetros del Grupo 2:", weight=ft.FontWeight.BOLD),
                    ft.TextField(label="Tamaño de muestra", value="30"),
                    ft.TextField(label="Media", value="110"),
                    ft.TextField(label="Desviación estándar", value="18")
                ]),
                bgcolor="#FFFFFF",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, "#D1D5DB")
            ),
            
            ft.Container(height=15),
            
            ft.ElevatedButton(
                "Generar Comparación",
                on_click=self.generate_comparison,
                bgcolor="#FFFFFF",
                color="#374151"
            ),
            
            ft.Container(height=15),
            
            # Área de resultados de simulación
            ft.Container(
                content=ft.Text("Los resultados de la simulación aparecerán aquí", color="#6B7280"),
                bgcolor="#FFFFFF",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, "#D1D5DB")
            )
        ])
    
    def create_evaluation_section(self):
        """Crea la sección de evaluación"""
        return ft.Column([
            ft.Container(
                content=ft.Text("5", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
                bgcolor="#3B82F6",
                width=40,
                height=40,
                border_radius=20,
                alignment=ft.alignment.center
            ),
            
            ft.Text("Evaluación Automatizada", size=20, weight=ft.FontWeight.BOLD, color="#374151"),
            
            ft.Container(height=20),
            
            ft.Text(
                "Evalúa tu comprensión de las comparaciones descriptivas entre grupos "
                "respondiendo las siguientes preguntas.",
                color="#3B82F6"
            ),
            
            ft.Container(
                content=ft.Text(
                    "Esta evaluación incluye preguntas sobre conceptos teóricos, "
                    "interpretación de resultados y aplicación práctica.",
                    color="#6B7280"
                ),
                bgcolor="#EFF6FF",
                padding=15,
                border_radius=8,
                border=ft.border.only(left=ft.border.BorderSide(4, "#60A5FA"))
            ),
            
            ft.Container(height=20),
            
            # Preguntas de evaluación
            ft.Container(
                content=ft.Column([
                    ft.Text("Pregunta 1:", weight=ft.FontWeight.BOLD, color="#374151"),
                    ft.Text("¿Qué mide el d de Cohen en una comparación entre grupos?"),
                    ft.RadioGroup(
                        content=ft.Column([
                            ft.Radio(value="a", label="La diferencia absoluta entre medias"),
                            ft.Radio(value="b", label="El tamaño del efecto estandarizado"),
                            ft.Radio(value="c", label="La significancia estadística"),
                            ft.Radio(value="d", label="El tamaño de la muestra")
                        ])
                    )
                ]),
                bgcolor="#FFFFFF",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, "#D1D5DB")
            ),
            
            ft.Container(height=15),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Pregunta 2:", weight=ft.FontWeight.BOLD, color="#374151"),
                    ft.Text("¿Cuál es la interpretación correcta de un d de Cohen = 0.8?"),
                    ft.RadioGroup(
                        content=ft.Column([
                            ft.Radio(value="a", label="Efecto pequeño"),
                            ft.Radio(value="b", label="Efecto moderado"),
                            ft.Radio(value="c", label="Efecto grande"),
                            ft.Radio(value="d", label="Efecto muy grande")
                        ])
                    )
                ]),
                bgcolor="#FFFFFF",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, "#D1D5DB")
            ),
            
            ft.Container(height=15),
            
            ft.Row([
                ft.ElevatedButton(
                    "Evaluar Respuestas",
                    on_click=self.evaluate_answers,
                    bgcolor="#3B82F6",
                    color="#FFFFFF"
                ),
                ft.ElevatedButton(
                    "Reiniciar Evaluación",
                    on_click=self.reset_evaluation,
                    bgcolor="#3B82F6",
                    color="#FFFFFF"
                )
            ]),
            
            ft.Container(height=15),
            
            # Área de retroalimentación
            ft.Container(
                content=ft.Column([
                    ft.Text("Retroalimentación", weight=ft.FontWeight.BOLD, color="#374151"),
                    ft.Text("Haz clic en 'Evaluar Respuestas' para ver tu retroalimentación", color="#6B7280")
                ]),
                bgcolor="#FFFFFF",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, "#D1D5DB"),
                ref=self.practical_feedback
            ),
            
            ft.Container(height=15),
            
            # Puntuación
            ft.Container(
                content=ft.Column([
                    ft.Text("Puntuación", weight=ft.FontWeight.BOLD, color="#374151"),
                    ft.Text(f"Puntuación actual: {self.score}/{self.total_questions}", color="#6B7280")
                ]),
                bgcolor="#F3F4F6",
                padding=15,
                border_radius=8
            )
        ])
    
    def create_resources_section(self):
        """Crea la sección de recursos"""
        return ft.Column([
            ft.Container(
                content=ft.Text("6", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
                bgcolor="#3B82F6",
                width=40,
                height=40,
                border_radius=20,
                alignment=ft.alignment.center
            ),
            
            ft.Text("Recursos y Materiales", size=20, weight=ft.FontWeight.BOLD, color="#374151"),
            
            ft.Container(height=20),
            
            ft.Text("Materiales de Apoyo", size=16, weight=ft.FontWeight.BOLD, color="#1E40AF"),
            
            ft.Container(height=10),
            
            # Lista de recursos
            ft.Container(
                content=ft.Column([
                    ft.Text("📚 Lecturas Recomendadas:", weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    ft.Text("• Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences"),
                    ft.Text("• Field, A. (2017). Discovering Statistics Using IBM SPSS Statistics"),
                    ft.Text("• Sullivan, G. M., & Feinn, R. (2012). Using Effect Size—or Why the P Value Is Not Enough"),
                    ft.Text(""),
                    ft.Text("🔬 Artículos Científicos:", weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    ft.Text("• Lakens, D. (2013). Calculating and reporting effect sizes"),
                    ft.Text("• Fritz, C. O., Morris, P. E., & Richler, J. J. (2012). Effect size estimates"),
                    ft.Text(""),
                    ft.Text("💻 Herramientas Digitales:", weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    ft.Text("• G*Power: Software para análisis de potencia"),
                    ft.Text("• Jamovi: Software estadístico gratuito"),
                    ft.Text("• R Studio: Entorno de desarrollo para R"),
                    ft.Text("• Python con pandas y scipy")
                ]),
                bgcolor="#F3F4F6",
                padding=15,
                border_radius=8
            ),
            
            ft.Container(height=20),
            
            ft.Text("Plantillas y Guías", size=16, weight=ft.FontWeight.BOLD, color="#059669"),
            
            ft.Container(height=10),
            
            ft.Row([
                ft.ElevatedButton(
                    "Descargar Plantilla de Análisis",
                    on_click=lambda e: self.download_template("analysis"),
                    bgcolor="#10B981",
                    color="#FFFFFF"
                ),
                ft.ElevatedButton(
                    "Descargar Checklist",
                    on_click=lambda e: self.download_template("checklist"),
                    bgcolor="#10B981",
                    color="#FFFFFF"
                )
            ]),
            
            ft.Container(height=15),
            
            ft.Text("Ejercicios Prácticos", size=16, weight=ft.FontWeight.BOLD, color="#7C3AED"),
            
            ft.Container(height=10),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Miniinforme: Comparación de Tratamientos", weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    ft.Text("Analiza los datos de un estudio clínico que compara dos tratamientos para la hipertensión."),
                    ft.ElevatedButton(
                        "Descargar Dataset",
                        on_click=lambda e: self.download_template("dataset"),
                        bgcolor="#8B5CF6",
                        color="#FFFFFF"
                    )
                ]),
                bgcolor="#F3F4F6",
                padding=15,
                border_radius=8
            ),
            
            ft.Container(height=20),
            
            ft.Text("Enlaces Útiles", size=16, weight=ft.FontWeight.BOLD, color="#DC2626"),
            
            ft.Container(height=10),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("🌐 Recursos en Línea:", weight=ft.FontWeight.BOLD, color="#DC2626"),
                    ft.Text("• Effect Size Calculator: https://www.socscistatistics.com/effectsize/"),
                    ft.Text("• Statistical Power Analysis: https://www.gpower.hhu.de/"),
                    ft.Text("• R Documentation: https://www.r-project.org/"),
                    ft.Text("• Python Statistics: https://docs.scipy.org/doc/scipy/reference/stats.html")
                ]),
                bgcolor="#FEE2E2",
                padding=15,
                border_radius=8
            )
        ])
    
    # Métodos de funcionalidad
    def calculate_statistics(self, e):
        """Calcula estadísticas para los grupos de ejemplo"""
        try:
            # Calcular estadísticas para grupo joven
            young_mean = statistics.mean(self.young_group)
            young_std = statistics.stdev(self.young_group)
            
            # Calcular estadísticas para grupo mayor
            older_mean = statistics.mean(self.older_group)
            older_std = statistics.stdev(self.older_group)
            
            # Calcular d de Cohen
            pooled_std = math.sqrt(((len(self.young_group) - 1) * young_std**2 + 
                                   (len(self.older_group) - 1) * older_std**2) / 
                                  (len(self.young_group) + len(self.older_group) - 2))
            cohens_d = (older_mean - young_mean) / pooled_std
            
            # Actualizar área de resultados
            self.clinical_interpretation.content.controls[1].value = f"""
Grupo Joven:
• Media: {young_mean:.2f} días
• Desv. Estándar: {young_std:.2f} días
• n: {len(self.young_group)}

Grupo Mayor:
• Media: {older_mean:.2f} días
• Desv. Estándar: {older_std:.2f} días
• n: {len(self.older_group)}

Comparación:
• Diferencia absoluta: {older_mean - young_mean:.2f} días
• d de Cohen: {cohens_d:.3f}
• Interpretación: {'Efecto grande' if abs(cohens_d) > 0.8 else 'Efecto moderado' if abs(cohens_d) > 0.5 else 'Efecto pequeño'}
            """
            self.clinical_interpretation.content.controls[1].color = "#3B82F6"
            self.page.update()
            
        except Exception as e:
            self.clinical_interpretation.content.controls[1].value = f"Error en el cálculo: {str(e)}"
            self.clinical_interpretation.content.controls[1].color = "#DC2626"
            self.page.update()
    
    def show_comparison_chart(self, e):
        """Muestra un gráfico de comparación"""
        try:
            # Crear figura de matplotlib
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Datos para el gráfico
            groups = ['Jóvenes', 'Mayores']
            means = [statistics.mean(self.young_group), statistics.mean(self.older_group)]
            stds = [statistics.stdev(self.young_group), statistics.stdev(self.older_group)]
            
            # Crear gráfico de barras con barras de error
            bars = ax.bar(groups, means, yerr=stds, capsize=5, 
                         color=['#3B82F6', '#10B981'], alpha=0.7)
            
            ax.set_ylabel('Tiempo de Recuperación (días)')
            ax.set_title('Comparación de Tiempo de Recuperación entre Grupos')
            ax.grid(True, alpha=0.3)
            
            # Agregar valores en las barras
            for bar, mean in zip(bars, means):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{mean:.1f}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            # Convertir a imagen
            canvas = FigureCanvasAgg(fig)
            canvas.draw()
            
            # Guardar como bytes
            img_data = io.BytesIO()
            fig.savefig(img_data, format='png', dpi=100, bbox_inches='tight')
            img_data.seek(0)
            
            # Convertir a base64
            img_base64 = base64.b64encode(img_data.getvalue()).decode()
            
            # Mostrar en la interfaz
            self.clinical_interpretation.content.controls[1].value = "Gráfico generado exitosamente"
            self.clinical_interpretation.content.controls[1].color = "#10B981"
            self.page.update()
            
            plt.close(fig)
            
        except Exception as e:
            self.clinical_interpretation.content.controls[1].value = f"Error al generar gráfico: {str(e)}"
            self.clinical_interpretation.content.controls[1].color = "#DC2626"
            self.page.update()
    
    def start_simulation(self, e):
        """Inicia la simulación"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Simulación iniciada. Configura los parámetros y haz clic en 'Generar Comparación'"),
                action="OK"
            )
        )
    
    def generate_comparison(self, e):
        """Genera una comparación simulada"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Comparación generada. Revisa los resultados en el área de simulación."),
                action="OK"
            )
        )
    
    def evaluate_answers(self, e):
        """Evalúa las respuestas del usuario"""
        self.score = 2  # Simular puntuación
        self.total_questions = 2
        
        self.practical_feedback.content.controls[1].value = """
✅ Respuesta 1: Correcta. El d de Cohen mide el tamaño del efecto estandarizado.

✅ Respuesta 2: Correcta. Un d de Cohen = 0.8 indica un efecto grande.

¡Excelente trabajo! Has demostrado una buena comprensión de los conceptos.
        """
        self.practical_feedback.content.controls[1].color = "#059669"
        self.page.update()
    
    def reset_evaluation(self, e):
        """Reinicia la evaluación"""
        self.score = 0
        self.total_questions = 0
        self.practical_feedback.content.controls[1].value = "Evaluación reiniciada. Responde las preguntas nuevamente."
        self.practical_feedback.content.controls[1].color = "#6B7280"
        self.page.update()
    
    def download_template(self, template_type):
        """Descarga plantillas y recursos"""
        if template_type == "analysis":
            content = self.generate_comparison_template()
        elif template_type == "checklist":
            content = self.generate_checklist()
        elif template_type == "dataset":
            content = self.generate_dataset()
        else:
            content = "Plantilla no disponible"
        
        # En una aplicación real, aquí se guardaría el archivo
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(f"Plantilla {template_type} descargada exitosamente"),
                action="OK"
            )
        )
    
    def generate_comparison_template(self):
        return """PLANTILLA DE ANÁLISIS COMPARATIVO ENTRE GRUPOS
==============================================

1. INFORMACIÓN GENERAL
   - Título del estudio: _______________
   - Fecha: _______________
   - Investigador: _______________

2. DESCRIPCIÓN DE LOS GRUPOS
   Grupo 1: _______________
   - Tamaño de muestra (n₁): _______________
   - Criterios de inclusión: _______________
   
   Grupo 2: _______________
   - Tamaño de muestra (n₂): _______________
   - Criterios de inclusión: _______________

3. VARIABLE DE INTERÉS
   - Nombre: _______________
   - Tipo: _______________
   - Unidades: _______________

4. ESTADÍSTICOS DESCRIPTIVOS
   
   Grupo 1:
   - Media: _______________
   - Mediana: _______________
   - Desviación estándar: _______________
   - Rango: _______________
   
   Grupo 2:
   - Media: _______________
   - Mediana: _______________
   - Desviación estándar: _______________
   - Rango: _______________

5. ANÁLISIS DE DIFERENCIAS
   - Diferencia absoluta: _______________
   - Diferencia relativa (%): _______________
   - d de Cohen: _______________
   - Interpretación del tamaño del efecto: _______________

6. INTERPRETACIÓN CLÍNICA
   _______________________________________________
   _______________________________________________
   _______________________________________________

7. LIMITACIONES
   _______________________________________________
   _______________________________________________
"""
    
    def generate_checklist(self):
        return """CHECKLIST DE ANÁLISIS DESCRIPTIVO ENTRE GRUPOS
==============================================

□ 1. PREPARACIÓN DE DATOS
   □ Verificar calidad de los datos
   □ Identificar valores perdidos
   □ Detectar valores atípicos
   □ Confirmar tipos de variables

□ 2. DESCRIPCIÓN DE GRUPOS
   □ Definir claramente cada grupo
   □ Reportar tamaños de muestra
   □ Verificar criterios de inclusión/exclusión

□ 3. ESTADÍSTICOS DESCRIPTIVOS
   □ Calcular medidas de tendencia central
   □ Calcular medidas de dispersión
   □ Verificar normalidad de distribuciones
   □ Considerar medidas robustas si es necesario

□ 4. COMPARACIONES
   □ Calcular diferencias absolutas
   □ Calcular diferencias relativas
   □ Estimar tamaños de efecto
   □ Interpretar magnitud de diferencias

□ 5. VISUALIZACIÓN
   □ Crear gráficos apropiados
   □ Incluir medidas de dispersión
   □ Usar escalas apropiadas
   □ Añadir títulos y etiquetas claras

□ 6. INTERPRETACIÓN
   □ Contextualizar resultados clínicamente
   □ Discutir relevancia práctica
   □ Mencionar limitaciones
   □ Evitar inferencias causales

□ 7. REPORTE
   □ Usar lenguaje claro y preciso
   □ Incluir intervalos de confianza si aplica
   □ Reportar todos los estadísticos relevantes
   □ Seguir guías de reporte apropiadas
"""
    
    def generate_dataset(self):
        return """ID,Grupo,Edad,Sexo,Presion_Sistolica,Presion_Diastolica,IMC,Tiempo_Recuperacion
1,Control,45,M,125,80,24.5,7
2,Control,52,F,118,75,22.1,6
3,Control,38,M,132,85,26.8,8
4,Control,41,F,120,78,23.4,7
5,Control,49,M,128,82,25.2,9
6,Tratamiento,47,F,115,72,23.8,5
7,Tratamiento,44,M,122,76,24.1,6
8,Tratamiento,51,F,119,74,22.9,5
9,Tratamiento,39,M,125,79,25.5,7
10,Tratamiento,46,F,117,73,23.2,6
11,Control,55,M,135,88,27.1,10
12,Control,42,F,123,81,24.7,8
13,Control,48,M,130,84,26.3,9
14,Control,36,F,121,77,22.8,7
15,Control,53,M,133,86,25.9,8
16,Tratamiento,43,F,118,75,23.5,6
17,Tratamiento,50,M,124,78,24.8,7
18,Tratamiento,37,F,116,71,22.4,5
19,Tratamiento,45,M,121,76,25.1,6
20,Tratamiento,49,F,119,74,23.7,6
"""

def main(page: ft.Page):
    app = OVAApp()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main) 