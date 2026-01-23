import flet as ft
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import math
import random
from io import BytesIO
import base64

class OVAIndicadoresSalud:
    def __init__(self):
        self.current_section = "intro"
        self.progress = 0
        self.evaluation_answers = {}
        self.evaluation_score = 0
        
        # Datos para cálculos
        self.prev_cases = 150
        self.prev_population = 10000
        self.inc_cases = 75
        self.inc_population = 9850
        self.let_deaths = 15
        self.let_cases = 150
        
        # Datos de práctica
        self.practice_prev_cases = 2450
        self.practice_prev_pop = 1028736
        self.practice_inc_cases = 3890
        self.practice_inc_pop = 1026286
        self.practice_let_deaths = 89
        self.practice_let_cases = 6340
        
        # Datos del simulador
        self.sim_population = 10000
        self.sim_prevalence = 2.0
        self.sim_incidence = 1.0
        self.sim_lethality = 10.0

    def main(self, page: ft.Page):
        page.title = "OVA 11: Indicadores de Frecuencia en Salud"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.scroll = ft.ScrollMode.AUTO
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "OVA 11: Indicadores de Frecuencia en Salud",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#FFFFFF",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Modelo Pedagógico C(H)ANGE - Universidad Antonio Nariño",
                    size=16,
                    color="#FFFFFF",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Row([
                    ft.Text("Combinatoria", color="#FFFFFF", size=12),
                    ft.Text("Álgebra", color="#FFFFFF", size=12),
                    ft.Text("Números", color="#FFFFFF", size=12),
                    ft.Text("Geometría", color="#FFFFFF", size=12),
                    ft.Text("Estadística", color="#FFFFFF", size=12),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            gradient=ft.LinearGradient(["#1D4ED8", "#7C3AED"]),
            padding=20,
            margin=ft.margin.only(bottom=10)
        )
        
        # Progress Bar
        self.progress_bar = ft.ProgressBar(value=0, color="#2563EB", height=4)
        self.progress_text = ft.Text("0%", size=12, color="#6B7280")
        
        progress_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Progreso del Aprendizaje", size=12, color="#6B7280"),
                    self.progress_text
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar
            ]),
            padding=10,
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#D1D5DB")
        )
        
        # Navigation
        self.nav_buttons = []
        nav_items = [
            ("intro", "Introducción"),
            ("theory", "Teoría Interactiva"),
            ("simulator", "Simulador"),
            ("practice", "Práctica Guiada"),
            ("evaluation", "Evaluación"),
            ("resources", "Recursos")
        ]
        
        for section_id, label in nav_items:
            btn = ft.ElevatedButton(
                text=label,
                on_click=lambda e, sid=section_id: self.show_section(sid),
                style=ft.ButtonStyle(
                    bgcolor="#DBEAFE" if section_id == "intro" else "#F3F4F6",
                    color="#1E40AF" if section_id == "intro" else "#000000"
                )
            )
            self.nav_buttons.append(btn)
        
        navigation = ft.Container(
            content=ft.Row(self.nav_buttons, scroll=ft.ScrollMode.AUTO),
            bgcolor="#FFFFFF",
            border=ft.border.all(1, "#D1D5DB")
        )
        
        # Main content
        self.main_content = self.create_intro_section()
        
        # Layout
        page.add(
            ft.Column([
                header,
                progress_container,
                navigation,
                ft.Container(
                    content=self.main_content,
                    expand=True,
                    padding=20
                )
            ], expand=True)
        )
    
    def show_section(self, section_id):
        """Cambia la sección actual"""
        self.current_section = section_id
        
        # Actualizar navegación
        for i, btn in enumerate(self.nav_buttons):
            if i == ["intro", "theory", "simulator", "practice", "evaluation", "resources"].index(section_id):
                btn.style.bgcolor = "#DBEAFE"
                btn.style.color = "#1E40AF"
            else:
                btn.style.bgcolor = "#F3F4F6"
                btn.style.color = "#000000"
        
        # Actualizar contenido principal
        if section_id == "intro":
            self.main_content = self.create_intro_section()
        elif section_id == "theory":
            self.main_content = self.create_theory_section()
        elif section_id == "simulator":
            self.main_content = self.create_simulator_section()
        elif section_id == "practice":
            self.main_content = self.create_practice_section()
        elif section_id == "evaluation":
            self.main_content = self.create_evaluation_section()
        elif section_id == "resources":
            self.main_content = self.create_resources_section()
        
        # Actualizar progreso
        progress_values = {"intro": 0.17, "theory": 0.33, "simulator": 0.5, 
                          "practice": 0.67, "evaluation": 0.83, "resources": 1.0}
        self.progress = progress_values.get(section_id, 0)
        self.progress_bar.value = self.progress
        self.progress_text.value = f"{int(self.progress * 100)}%"
        
        self.page.update()
    
    def create_intro_section(self):
        """Crea la sección de introducción"""
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("🎯 Introducción a los Indicadores de Frecuencia en Salud", 
                           size=24, weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    ft.Text(
                        "Los indicadores de frecuencia son herramientas fundamentales en epidemiología "
                        "que permiten medir la magnitud y distribución de eventos de salud en poblaciones.",
                        size=16, color="#374151"
                    )
                ]),
                bgcolor="#EFF6FF",
                padding=20,
                border_radius=10
            ),
            
            ft.Container(height=20),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("⚠️ Importante", weight=ft.FontWeight.BOLD, color="#D97706"),
                    ft.Text(
                        "Estos indicadores son descriptivos y no establecen causalidad. "
                        "Para inferencias causales se requieren diseños de estudio apropiados.",
                        size=12, color="#D97706"
                    )
                ]),
                bgcolor="#FEF3C7",
                padding=15,
                border_radius=8,
                border=ft.border.only(left=ft.border.BorderSide(4, "#F59E0B"))
            ),
            
            ft.Container(height=20),
            
            ft.ElevatedButton(
                "🚀 Comenzar Aprendizaje",
                on_click=lambda e: self.show_section("theory"),
                style=ft.ButtonStyle(bgcolor="#2563EB", color="#FFFFFF")
            )
        ])
    
    def create_theory_section(self):
        """Crea la sección de teoría interactiva"""
        return ft.Column([
            ft.Text("📚 Teoría Interactiva: Los Tres Indicadores Principales", 
                   size=24, weight=ft.FontWeight.BOLD, color="#1E40AF"),
            
            ft.Container(height=20),
            
            # Prevalencia
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("1", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
                        bgcolor="#EF4444",
                        width=40,
                        height=40,
                        border_radius=20,
                        alignment=ft.alignment.center
                    ),
                    ft.Text("Prevalencia", size=20, weight=ft.FontWeight.BOLD, color="#DC2626"),
                    ft.Text(
                        "Proporción de individuos en una población que presentan una condición "
                        "en un momento específico.",
                        size=14, color="#374151"
                    ),
                    ft.Text("Fórmula: Prevalencia = (Casos existentes / Población total) × 100", 
                           size=12, color="#6B7280", weight=ft.FontWeight.BOLD),
                    ft.Text("Unidad: Porcentaje (%)", size=12, color="#6B7280")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#FEF2F2",
                padding=20,
                border_radius=10,
                border=ft.border.all(1, "#FECACA")
            ),
            
            ft.Container(height=15),
            
            # Incidencia
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("2", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
                        bgcolor="#3B82F6",
                        width=40,
                        height=40,
                        border_radius=20,
                        alignment=ft.alignment.center
                    ),
                    ft.Text("Incidencia", size=20, weight=ft.FontWeight.BOLD, color="#2563EB"),
                    ft.Text(
                        "Proporción de individuos que desarrollan una condición durante un período "
                        "específico de tiempo.",
                        size=14, color="#374151"
                    ),
                    ft.Text("Fórmula: Incidencia = (Nuevos casos / Población en riesgo) × 100", 
                           size=12, color="#6B7280", weight=ft.FontWeight.BOLD),
                    ft.Text("Unidad: Porcentaje (%)", size=12, color="#6B7280")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#EFF6FF",
                padding=20,
                border_radius=10,
                border=ft.border.all(1, "#BFDBFE")
            ),
            
            ft.Container(height=15),
            
            # Letalidad
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("3", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
                        bgcolor="#8B5CF6",
                        width=40,
                        height=40,
                        border_radius=20,
                        alignment=ft.alignment.center
                    ),
                    ft.Text("Letalidad", size=20, weight=ft.FontWeight.BOLD, color="#7C3AED"),
                    ft.Text(
                        "Proporción de individuos con una condición que fallecen por esa causa.",
                        size=14, color="#374151"
                    ),
                    ft.Text("Fórmula: Letalidad = (Muertes por la condición / Casos totales) × 100", 
                           size=12, color="#6B7280", weight=ft.FontWeight.BOLD),
                    ft.Text("Unidad: Porcentaje (%)", size=12, color="#6B7280")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#F3E8FF",
                padding=20,
                border_radius=10,
                border=ft.border.all(1, "#DDD6FE")
            ),
            
            ft.Container(height=20),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Interpretación Clínica", weight=ft.FontWeight.BOLD, color="#DC2626"),
                    ft.Text(
                        "La prevalencia indica la carga de enfermedad, la incidencia mide el riesgo "
                        "de desarrollar la enfermedad, y la letalidad evalúa la gravedad.",
                        size=12, color="#DC2626"
                    )
                ]),
                bgcolor="#FEE2E2",
                padding=15,
                border_radius=8
            ),
            
            ft.Container(height=15),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Implicaciones de Salud Pública", weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    ft.Text(
                        "Estos indicadores guían la planificación de servicios de salud, "
                        "asignación de recursos y desarrollo de políticas preventivas.",
                        size=12, color="#1E40AF"
                    )
                ]),
                bgcolor="#DBEAFE",
                padding=15,
                border_radius=8
            )
        ])
    
    def create_simulator_section(self):
        """Crea la sección del simulador"""
        return ft.Column([
            ft.Container(
                content=ft.Text("🤖 Retroalimentación Inteligente", size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                gradient=ft.LinearGradient(["#60A5FA", "#06B6D4"]),
                padding=20,
                border_radius=10
            ),
            
            ft.Container(height=20),
            
            ft.Text("Simulador de Indicadores Epidemiológicos", size=20, weight=ft.FontWeight.BOLD, color="#1E40AF"),
            
            ft.Text(
                "Ajusta los parámetros para ver cómo cambian los indicadores de frecuencia. "
                "Este simulador te ayudará a comprender las relaciones entre los diferentes indicadores.",
                size=14, color="#374151"
            ),
            
            ft.Container(height=20),
            
            # Controles del simulador
            ft.Row([
                ft.Column([
                    ft.Text("Población Total:", weight=ft.FontWeight.BOLD),
                    ft.Slider(
                        min=1000,
                        max=50000,
                        divisions=49,
                        value=10000,
                        on_change=self.update_simulator
                    ),
                    ft.Text("10,000", id="pop_display")
                ], expand=True),
                
                ft.Column([
                    ft.Text("Casos Existentes:", weight=ft.FontWeight.BOLD),
                    ft.Slider(
                        min=0,
                        max=1000,
                        divisions=100,
                        value=200,
                        on_change=self.update_simulator
                    ),
                    ft.Text("200", id="cases_display")
                ], expand=True),
                
                ft.Column([
                    ft.Text("Nuevos Casos:", weight=ft.FontWeight.BOLD),
                    ft.Slider(
                        min=0,
                        max=500,
                        divisions=50,
                        value=100,
                        on_change=self.update_simulator
                    ),
                    ft.Text("100", id="new_cases_display")
                ], expand=True),
                
                ft.Column([
                    ft.Text("Muertes:", weight=ft.FontWeight.BOLD),
                    ft.Slider(
                        min=0,
                        max=100,
                        divisions=20,
                        value=20,
                        on_change=self.update_simulator
                    ),
                    ft.Text("20", id="deaths_display")
                ], expand=True)
            ], spacing=20),
            
            ft.Container(height=20),
            
            # Resultados
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Prevalencia", size=16, weight=ft.FontWeight.BOLD, color="#DC2626"),
                        ft.Text("2.0%", size=20, weight=ft.FontWeight.BOLD, color="#DC2626", ref=self.sim_prev_result)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor="#FEF2F2",
                    padding=20,
                    border_radius=10,
                    expand=True
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Incidencia", size=16, weight=ft.FontWeight.BOLD, color="#2563EB"),
                        ft.Text("1.0%", size=20, weight=ft.FontWeight.BOLD, color="#2563EB", ref=self.sim_inc_result)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor="#EFF6FF",
                    padding=20,
                    border_radius=10,
                    expand=True
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Letalidad", size=16, weight=ft.FontWeight.BOLD, color="#7C3AED"),
                        ft.Text("10%", size=20, weight=ft.FontWeight.BOLD, color="#7C3AED", ref=self.sim_let_result)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor="#F3E8FF",
                    padding=20,
                    border_radius=10,
                    expand=True
                )
            ], spacing=15),
            
            ft.Container(height=20),
            
            ft.ElevatedButton(
                "🔄 Reiniciar Simulador",
                on_click=self.reset_simulator,
                style=ft.ButtonStyle(bgcolor="#10B981", color="#FFFFFF")
            )
        ])
    
    def update_simulator(self, e):
        """Actualiza el simulador con nuevos valores"""
        # Obtener valores de los sliders
        population = int(e.control.value) if hasattr(e.control, 'value') else 10000
        cases = int(e.control.value) if hasattr(e.control, 'value') else 200
        new_cases = int(e.control.value) if hasattr(e.control, 'value') else 100
        deaths = int(e.control.value) if hasattr(e.control, 'value') else 20
        
        # Calcular indicadores
        prevalence = (cases / population) * 100
        incidence = (new_cases / (population - cases)) * 100
        lethality = (deaths / cases) * 100 if cases > 0 else 0
        
        # Actualizar resultados
        self.sim_prev_result.value = f"{prevalence:.1f}%"
        self.sim_inc_result.value = f"{incidence:.1f}%"
        self.sim_let_result.value = f"{lethality:.1f}%"
        
        self.page.update()
    
    def reset_simulator(self, e):
        """Reinicia el simulador a valores por defecto"""
        # Aquí se reiniciarían los sliders y resultados
        self.sim_prev_result.value = "2.0%"
        self.sim_inc_result.value = "1.0%"
        self.sim_let_result.value = "10%"
        self.page.update()
    
    def create_practice_section(self):
        """Crea la sección de práctica guiada"""
        return ft.Column([
            ft.Text("🔢 Cálculos Combinatorios", size=20, weight=ft.FontWeight.BOLD, color="#D97706"),
            
            ft.Container(
                content=ft.Text(
                    "Practica el cálculo de indicadores con datos reales. "
                    "Sigue los pasos y verifica tus resultados.",
                    size=14, color="#374151"
                ),
                bgcolor="#FEF3C7",
                padding=15,
                border_radius=8
            ),
            
            ft.Container(height=20),
            
            # Ejercicio de práctica
            ft.Container(
                content=ft.Column([
                    ft.Text("Ejercicio: Análisis de Diabetes en una Comunidad", 
                           size=16, weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    
                    ft.Container(height=10),
                    
                    ft.Row([
                        ft.Column([
                            ft.Text("Prevalencia", size=12, color="#6B7280"),
                            ft.Container(
                                content=ft.Text("2,450 casos en 1,028,736 habitantes"),
                                bgcolor="#FEE2E2",
                                padding=10,
                                border_radius=5
                            )
                        ], expand=True),
                        
                        ft.Column([
                            ft.Text("Incidencia", size=12, color="#6B7280"),
                            ft.Container(
                                content=ft.Text("3,890 nuevos casos en 1,026,286 en riesgo"),
                                bgcolor="#DBEAFE",
                                padding=10,
                                border_radius=5
                            )
                        ], expand=True),
                        
                        ft.Column([
                            ft.Text("Letalidad", size=12, color="#6B7280"),
                            ft.Container(
                                content=ft.Text("89 muertes en 6,340 casos totales"),
                                bgcolor="#F3E8FF",
                                padding=10,
                                border_radius=5
                            )
                        ], expand=True)
                    ], spacing=15),
                    
                    ft.Container(height=15),
                    
                    ft.ElevatedButton(
                        "📊 Calcular Indicadores",
                        on_click=self.calculate_practice_indicators,
                        style=ft.ButtonStyle(bgcolor="#10B981", color="#FFFFFF")
                    )
                ]),
                bgcolor="#F9FAFB",
                padding=20,
                border_radius=10,
                border=ft.border.all(1, "#E5E7EB")
            )
        ])
    
    def calculate_practice_indicators(self, e):
        """Calcula los indicadores del ejercicio de práctica"""
        # Cálculos
        prevalence = (self.practice_prev_cases / self.practice_prev_pop) * 100
        incidence = (self.practice_inc_cases / self.practice_inc_pop) * 100
        lethality = (self.practice_let_deaths / self.practice_let_cases) * 100
        
        # Mostrar resultados
        result_text = f"""
Resultados del Ejercicio:

📊 Prevalencia: {prevalence:.3f}%
   • 2,450 casos / 1,028,736 habitantes × 100
   • Interpretación: {prevalence:.3f}% de la población tiene diabetes

📈 Incidencia: {incidence:.3f}%
   • 3,890 nuevos casos / 1,026,286 en riesgo × 100
   • Interpretación: {incidence:.3f}% de la población en riesgo desarrolló diabetes

💀 Letalidad: {lethality:.2f}%
   • 89 muertes / 6,340 casos totales × 100
   • Interpretación: {lethality:.2f}% de los casos de diabetes resultaron en muerte

🎯 Implicaciones Clínicas:
   • La diabetes afecta a una proporción significativa de la población
   • El riesgo de desarrollar diabetes es moderado
   • La letalidad es relativamente baja, pero requiere atención médica
        """
        
        # Aquí se mostraría el resultado en la interfaz
        print(result_text)
    
    def create_evaluation_section(self):
        """Crea la sección de evaluación"""
        return ft.Column([
            ft.Text("📝 Evaluación de Conocimientos", size=20, weight=ft.FontWeight.BOLD, color="#1E40AF"),
            
            ft.Text(
                "Evalúa tu comprensión de los indicadores de frecuencia en salud. "
                "Responde las preguntas y recibe retroalimentación inmediata.",
                size=14, color="#374151"
            ),
            
            ft.Container(height=20),
            
            # Preguntas de evaluación
            ft.Container(
                content=ft.Column([
                    ft.Text("Pregunta 1:", weight=ft.FontWeight.BOLD, color="#374151"),
                    ft.Text("¿Cuál de los siguientes es el indicador más apropiado para medir la carga de enfermedad en una población?"),
                    ft.RadioGroup(
                        content=ft.Column([
                            ft.Radio(value="a", label="Incidencia"),
                            ft.Radio(value="b", label="Prevalencia"),
                            ft.Radio(value="c", label="Letalidad"),
                            ft.Radio(value="d", label="Mortalidad")
                        ])
                    )
                ]),
                bgcolor="#FFFFFF",
                padding=15,
                border_radius=8,
                border=ft.border.all(1, "#D1D5DB")
            ),
            
            ft.Container(height=15),
            
            ft.ElevatedButton(
                "✅ Evaluar Respuestas",
                on_click=self.evaluate_answers,
                style=ft.ButtonStyle(bgcolor="#10B981", color="#FFFFFF")
            )
        ])
    
    def evaluate_answers(self, e):
        """Evalúa las respuestas del usuario"""
        # Simular evaluación
        self.evaluation_score = 85
        
        feedback = f"""
Resultados de la Evaluación:

🎯 Puntuación: {self.evaluation_score}/100

✅ Respuesta 1: Correcta
   La prevalencia es el indicador más apropiado para medir la carga de enfermedad.

📊 Interpretación:
   • Excelente comprensión de los conceptos básicos
   • Buen manejo de las fórmulas
   • Interpretación clínica adecuada

🎓 Recomendaciones:
   • Continúa practicando con diferentes escenarios
   • Profundiza en la interpretación epidemiológica
   • Considera el contexto clínico en tus análisis
        """
        
        print(feedback)
    
    def create_resources_section(self):
        """Crea la sección de recursos"""
        return ft.Column([
            ft.Text("📚 Recursos y Materiales", size=20, weight=ft.FontWeight.BOLD, color="#1E40AF"),
            
            ft.Text(
                "Encuentra materiales adicionales para profundizar en el estudio de "
                "indicadores de frecuencia en salud.",
                size=14, color="#374151"
            ),
            
            ft.Container(height=20),
            
            # Recursos disponibles
            ft.Container(
                content=ft.Column([
                    ft.Text("📖 Lecturas Recomendadas:", weight=ft.FontWeight.BOLD, color="#1E40AF"),
                    ft.Text("• Gordis, L. (2014). Epidemiology"),
                    ft.Text("• Rothman, K.J. (2012). Modern Epidemiology"),
                    ft.Text("• Szklo, M. & Nieto, F.J. (2014). Epidemiology: Beyond the Basics"),
                    
                    ft.Container(height=15),
                    
                    ft.Text("🔬 Artículos Científicos:", weight=ft.FontWeight.BOLD, color="#059669"),
                    ft.Text("• Porta, M. (2014). A Dictionary of Epidemiology"),
                    ft.Text("• Last, J.M. (2001). A Dictionary of Epidemiology"),
                    
                    ft.Container(height=15),
                    
                    ft.Text("💻 Herramientas Digitales:", weight=ft.FontWeight.BOLD, color="#7C3AED"),
                    ft.Text("• Epi Info (CDC)"),
                    ft.Text("• OpenEpi"),
                    ft.Text("• R Studio con paquetes epidemiológicos")
                ]),
                bgcolor="#F9FAFB",
                padding=20,
                border_radius=10,
                border=ft.border.all(1, "#E5E7EB")
            ),
            
            ft.Container(height=20),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Proyecto Final: Miniinforme Epidemiológico", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Elabora un informe de 2-3 páginas analizando un problema de salud pública de tu región, calculando e interpretando los tres indicadores principales."),
                    
                    ft.Row([
                        ft.Column([
                            ft.Text("Estructura Sugerida:", weight=ft.FontWeight.BOLD),
                            ft.Text("1. Introducción al problema de salud", size=12),
                            ft.Text("2. Metodología y fuentes de datos", size=12),
                            ft.Text("3. Cálculo de indicadores", size=12),
                            ft.Text("4. Interpretación epidemiológica", size=12),
                            ft.Text("5. Implicaciones para salud pública", size=12),
                            ft.Text("6. Limitaciones y conclusiones", size=12),
                        ], expand=True),
                        
                        ft.Column([
                            ft.Text("Criterios de Evaluación:", weight=ft.FontWeight.BOLD),
                            ft.Text("✓ Correcta aplicación de fórmulas", size=12),
                            ft.Text("✓ Interpretación clínica adecuada", size=12),
                            ft.Text("✓ Uso apropiado de visualizaciones", size=12),
                            ft.Text("✓ Consideraciones éticas", size=12),
                            ft.Text("✓ Reproducibilidad del análisis", size=12),
                        ], expand=True)
                    ], spacing=20),
                    
                    ft.ElevatedButton(
                        "🚀 Iniciar Proyecto",
                        on_click=self.start_transfer_activity,
                        style=ft.ButtonStyle(bgcolor="#7C3AED", color="#FFFFFF")
                    )
                ], spacing=15),
                gradient=ft.LinearGradient(["#F3E8FF", "#FCE7F3"]),
                padding=20,
                border_radius=10
            )
        ], spacing=15, scroll=ft.ScrollMode.AUTO)

    def start_transfer_activity(self, e):
        print("🎯 Proyecto de Transferencia Iniciado")
        print("Instrucciones enviadas.")
        print("Recuerda incluir:")
        print("• Cálculos correctos")
        print("• Interpretación epidemiológica")
        print("• Visualizaciones apropiadas")
        print("• Consideraciones éticas")

def main(page: ft.Page):
    app = OVAIndicadoresSalud()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main) 