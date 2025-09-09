
import flet as ft
import json
import os
from datetime import datetime

class OVA17App:
    def __init__(self):
        self.current_section = "intro"
        self.current_slide = 0
        self.current_question = 0
        self.practice_step = 1
        self.quiz_answers = {}
        self.progress = 0
        
        # Datos de las slides de la microlección
        self.lesson_slides = [
            {
                "title": "1. Estructura IMRyD Adaptada para Salud",
                "content": """
                Introducción (I):
                • Contexto epidemiológico
                • Justificación clínica
                • Objetivo específico

                Métodos (M):
                • Diseño del estudio
                • Población y muestra
                • Variables medidas
                • Análisis estadístico

                Resultados (R):
                • Características descriptivas
                • Hallazgos principales
                • Tablas y figuras

                Discusión (D):
                • Interpretación clínica
                • Limitaciones
                • Implicaciones prácticas

                Ejemplo: "Prevalencia de hipertensión arterial en adultos mayores de 65 años en Bogotá: análisis descriptivo de la ENSIN 2015"
                """
            },
            {
                "title": "2. Tablas Científicas: Estándares de Calidad",
                "content": """
                Elementos Esenciales:

                • Título descriptivo: Debe explicar qué, quién, cuándo y dónde
                • Encabezados claros: Variables en filas, categorías en columnas
                • Estadísticos apropiados: n (%), media (DE), mediana (IQR)
                • Notas al pie: Definiciones, abreviaciones, fuentes

                Ejemplo: Tabla 1. Características basales
                Variable          | Total (n=500)
                Edad, años*       | 67.3 (12.8)
                Sexo masculino†   | 312 (62.4)

                *Media (desviación estándar)
                †n (porcentaje)
                """
            },
            {
                "title": "3. Interpretación Clínica de Resultados",
                "content": """
                Principios de Interpretación:

                Significancia Estadística vs Clínica:
                • p < 0.05 no siempre es clínicamente relevante
                • Considerar intervalos de confianza
                • Evaluar magnitud del efecto

                Contexto Clínico:
                • Relevancia para la práctica médica
                • Impacto en decisiones terapéuticas
                • Consideraciones de costo-efectividad

                Ejemplo de Interpretación:
                Resultado estadístico: "La mortalidad en UCI fue del 29.0% (IC 95%: 25.1-33.2%)"
                Interpretación clínica: "La mortalidad observada está dentro del rango esperado para pacientes críticos con COVID-19..."
                """
            },
            {
                "title": "4. Comunicación Efectiva para Audiencias Clínicas",
                "content": """
                Audiencias Objetivo:

                Médicos Clínicos:
                • Enfoque en aplicabilidad
                • Implicaciones diagnósticas
                • Decisiones terapéuticas

                Administradores:
                • Impacto en recursos
                • Indicadores de calidad
                • Políticas institucionales

                Salud Pública:
                • Tendencias poblacionales
                • Intervenciones preventivas
                • Políticas sanitarias

                Estrategias de Comunicación:
                • Lenguaje claro y preciso
                • Estructura lógica
                • Evidencia de apoyo
                """
            },
            {
                "title": "5. Limitaciones y Consideraciones Éticas",
                "content": """
                Limitaciones Comunes:
                • Diseño del estudio: Limitaciones inherentes al tipo de estudio
                • Sesgos de selección: Representatividad de la muestra
                • Variables confusoras: Factores no controlados
                • Generalización: Aplicabilidad a otras poblaciones

                Consideraciones Éticas:
                • Confidencialidad: Protección de datos personales
                • Transparencia: Reporte honesto de métodos
                • Responsabilidad: Interpretación cuidadosa

                Ejemplo de Limitaciones:
                "Este estudio presenta limitaciones inherentes a su diseño retrospectivo, incluyendo posibles sesgos de información en los registros clínicos..."
                """
            }
        ]
        
        # Preguntas del quiz
        self.quiz_questions = [
            {
                "question": "¿Cuál es el orden correcto de las secciones en un resumen ejecutivo siguiendo la estructura IMRyD?",
                "options": [
                    "Introducción → Resultados → Métodos → Discusión",
                    "Introducción → Métodos → Resultados → Discusión",
                    "Métodos → Introducción → Resultados → Discusión",
                    "Resultados → Métodos → Introducción → Discusión"
                ],
                "correct": 1,
                "explanation": "La estructura IMRyD sigue el orden lógico: Introducción (contexto y objetivos), Métodos (cómo se hizo), Resultados (qué se encontró), y Discusión (qué significa)."
            },
            {
                "question": "En una tabla científica, ¿cuál es la forma correcta de presentar variables continuas?",
                "options": [
                    "Solo la media",
                    "Media (desviación estándar) o mediana (rango intercuartílico)",
                    "Solo la mediana",
                    "Únicamente el rango"
                ],
                "correct": 1,
                "explanation": "Las variables continuas deben presentarse con medidas de tendencia central y dispersión apropiadas según la distribución de los datos."
            },
            {
                "question": "¿Qué elemento es MÁS importante al interpretar resultados para audiencias clínicas?",
                "options": [
                    "El valor p exacto",
                    "La significancia estadística únicamente",
                    "La relevancia clínica y aplicabilidad práctica",
                    "El tamaño de la muestra"
                ],
                "correct": 2,
                "explanation": "La relevancia clínica y aplicabilidad práctica son fundamentales para que los profesionales de salud puedan tomar decisiones informadas."
            },
            {
                "question": "En la sección de limitaciones, es esencial mencionar:",
                "options": [
                    "Solo las limitaciones del diseño del estudio",
                    "Únicamente los sesgos de selección",
                    "Todas las limitaciones que puedan afectar la interpretación de resultados",
                    "Solo las limitaciones estadísticas"
                ],
                "correct": 2,
                "explanation": "Una sección completa de limitaciones debe abordar todos los aspectos que puedan influir en la interpretación y generalización de los resultados."
            },
            {
                "question": "¿Cuál es la característica principal de una tabla 'lista para publicación'?",
                "options": [
                    "Debe tener muchos colores",
                    "Debe ser autoexplicativa con título descriptivo, encabezados claros y notas al pie",
                    "Debe incluir todos los datos sin excepción",
                    "Solo debe usar números enteros"
                ],
                "correct": 1,
                "explanation": "Una tabla lista para publicación debe ser autoexplicativa, con elementos que permitan su comprensión independiente del texto principal."
            }
        ]

    def main(self, page: ft.Page):
        page.title = "OVA 17: Resúmenes Ejecutivos y Escritura Científica"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1200
        page.window_height = 800
        page.scroll = ft.ScrollMode.AUTO
        
        # Variables de UI
        self.page = page
        self.progress_bar = ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee")
        self.progress_text = ft.Text("0%", size=14, color=ft.Colors.WHITE)
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Text("OVA 17: Resúmenes Ejecutivos y Escritura Científica", 
                       size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("Estadística Descriptiva para Ciencias de la Salud - Universidad Antonio Nariño", 
                       size=16, color=ft.Colors.WHITE70),
                ft.Row([
                    ft.Text("Progreso del módulo:", size=14, color=ft.Colors.WHITE),
                    self.progress_text
                ]),
                self.progress_bar
            ]),
            padding=20,
            bgcolor=ft.Colors.BLUE_700,
            border_radius=0
        )
        
        # Navigation
        self.nav_buttons = {
            "intro": ft.ElevatedButton("📚 Introducción", on_click=lambda _: self.show_section("intro"), 
                                     bgcolor=ft.Colors.BLUE_100, color=ft.Colors.BLUE_700),
            "lesson": ft.ElevatedButton("📖 Microlección", on_click=lambda _: self.show_section("lesson")),
            "practice": ft.ElevatedButton("🤝 Práctica Guiada", on_click=lambda _: self.show_section("practice")),
            "evaluation": ft.ElevatedButton("📋 Evaluación", on_click=lambda _: self.show_section("evaluation")),
            "resources": ft.ElevatedButton("💾 Recursos", on_click=lambda _: self.show_section("resources"))
        }
        
        navigation = ft.Container(
            content=ft.Row([
                self.nav_buttons["intro"],
                self.nav_buttons["lesson"],
                self.nav_buttons["practice"],
                self.nav_buttons["evaluation"],
                self.nav_buttons["resources"]
            ], scroll=ft.ScrollMode.AUTO),
            padding=10,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )
        
        # Content area
        self.content_area = ft.Container(
            content=self.create_intro_section(),
            padding=20,
            expand=True
        )
        
        # AI Assistant
        self.ai_messages = ft.Column([], height=200, scroll=ft.ScrollMode.AUTO)
        self.ai_input = ft.TextField(hint_text="Pregunta sobre escritura científica...", expand=True)
        
        ai_panel = ft.Container(
            content=ft.Column([
                ft.Text("🤖 Asistente IA - Modelo C(H)ANGE", weight=ft.FontWeight.BOLD),
                self.ai_messages,
                ft.Row([
                    self.ai_input,
                    ft.ElevatedButton("Enviar", on_click=self.send_ai_message)
                ])
            ]),
            padding=15,
            bgcolor=ft.Colors.PURPLE_50,
            border_radius=10,
            visible=False
        )
        
        self.ai_panel = ai_panel
        
        # Main layout
        main_content = ft.Column([
            header,
            navigation,
            ft.Row([
                self.content_area,
                ft.Container(
                    content=ft.Column([
                        ft.ElevatedButton("🤖 Asistente IA", 
                                        on_click=self.toggle_ai,
                                        bgcolor=ft.Colors.PURPLE_600,
                                        color=ft.Colors.WHITE),
                        ai_panel
                    ]),
                    width=300,
                    padding=10
                )
            ], expand=True)
        ], expand=True)
        
        page.add(main_content)
        self.update_progress()

    def show_section(self, section_id):
        # Actualizar navegación
        for btn_id, btn in self.nav_buttons.items():
            if btn_id == section_id:
                btn.bgcolor = ft.Colors.BLUE_100
                btn.color = ft.Colors.BLUE_700
            else:
                btn.bgcolor = None
                btn.color = None
        
        # Mostrar sección correspondiente
        if section_id == "intro":
            self.content_area.content = self.create_intro_section()
        elif section_id == "lesson":
            self.content_area.content = self.create_lesson_section()
        elif section_id == "practice":
            self.content_area.content = self.create_practice_section()
        elif section_id == "evaluation":
            self.content_area.content = self.create_evaluation_section()
        elif section_id == "resources":
            self.content_area.content = self.create_resources_section()
        
        self.current_section = section_id
        self.update_progress()
        self.page.update()

    def create_intro_section(self):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TRACK_CHANGES, color=ft.Colors.BLUE_600, size=40),
                    ft.Text("Objetivos de Aprendizaje", size=24, weight=ft.FontWeight.BOLD)
                ]),
                ft.Divider(),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Al finalizar esta OVA, serás capaz de:", 
                                   size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                            ft.Column([
                                ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500), 
                                       ft.Text("Estructurar resúmenes ejecutivos siguiendo el formato IMRyD adaptado")]),
                                ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500), 
                                       ft.Text("Crear tablas 'listas para publicación' con estándares científicos")]),
                                ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500), 
                                       ft.Text("Redactar notas y pies de página informativos y precisos")]),
                                ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500), 
                                       ft.Text("Comunicar resultados estadísticos a audiencias clínicas")])
                            ])
                        ]),
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Modelo Pedagógico C(H)ANGE", 
                                   size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                            ft.Column([
                                ft.Row([ft.Container(ft.Text("C", color=ft.Colors.WHITE), 
                                                   bgcolor=ft.Colors.PURPLE_400, padding=5, border_radius=5),
                                       ft.Text("Combinatoria en diseños de estudio")]),
                                ft.Row([ft.Container(ft.Text("H", color=ft.Colors.WHITE), 
                                                   bgcolor=ft.Colors.BLUE_400, padding=5, border_radius=5),
                                       ft.Text("Heurística en interpretación")]),
                                ft.Row([ft.Container(ft.Text("A", color=ft.Colors.WHITE), 
                                                   bgcolor=ft.Colors.GREEN_400, padding=5, border_radius=5),
                                       ft.Text("Álgebra en cálculos estadísticos")]),
                                ft.Row([ft.Container(ft.Text("N", color=ft.Colors.WHITE), 
                                                   bgcolor=ft.Colors.YELLOW_600, padding=5, border_radius=5),
                                       ft.Text("Números y medidas de salud")]),
                                ft.Row([ft.Container(ft.Text("G", color=ft.Colors.WHITE), 
                                                   bgcolor=ft.Colors.RED_400, padding=5, border_radius=5),
                                       ft.Text("Geometría en visualización")]),
                                ft.Row([ft.Container(ft.Text("E", color=ft.Colors.WHITE), 
                                                   bgcolor=ft.Colors.INDIGO_400, padding=5, border_radius=5),
                                       ft.Text("Estadística aplicada")])
                            ])
                        ]),
                        expand=True,
                        bgcolor=ft.Colors.PURPLE_50,
                        padding=15,
                        border_radius=10
                    )
                ]),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME, color=ft.Colors.YELLOW_600),
                        ft.Text("Duración estimada: 2-4 horas", weight=ft.FontWeight.BOLD),
                        ft.Text("Este módulo incluye actividades interactivas, casos prácticos y evaluación automatizada.")
                    ]),
                    bgcolor=ft.Colors.YELLOW_50,
                    padding=15,
                    border_radius=10,
                    border=ft.border.all(2, ft.Colors.YELLOW_400)
                ),
                ft.ElevatedButton("Comenzar Microlección →", 
                                on_click=lambda _: self.show_section("lesson"),
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                                size=ft.ControlSize.LARGE)
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )

    def create_lesson_section(self):
        self.slide_content = ft.Container(
            content=self.create_slide_content(),
            expand=True
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.BOOK, color=ft.Colors.BLUE_600, size=40),
                    ft.Text("Microlección: Escritura Científica en Salud", 
                           size=24, weight=ft.FontWeight.BOLD)
                ]),
                ft.Divider(),
                ft.Row([
                    self.slide_content,
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Conceptos Clave", size=18, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Text("Resumen Ejecutivo: Síntesis concisa de un estudio que permite toma de decisiones rápida."),
                                bgcolor=ft.Colors.BLUE_50,
                                padding=10,
                                border_radius=5,
                                border=ft.border.all(2, ft.Colors.BLUE_500)
                            ),
                            ft.Container(
                                content=ft.Text("Tabla Lista para Publicación: Formato estandarizado que cumple criterios editoriales."),
                                bgcolor=ft.Colors.GREEN_50,
                                padding=10,
                                border_radius=5,
                                border=ft.border.all(2, ft.Colors.GREEN_500)
                            ),
                            ft.Container(
                                content=ft.Text("Significancia Clínica: Relevancia práctica de los hallazgos para la atención médica."),
                                bgcolor=ft.Colors.PURPLE_50,
                                padding=10,
                                border_radius=5,
                                border=ft.border.all(2, ft.Colors.PURPLE_500)
                            ),
                            ft.Text("Checklist Rápido", size=16, weight=ft.FontWeight.BOLD),
                            ft.Column([
                                ft.Checkbox(label="Objetivo claro y específico"),
                                ft.Checkbox(label="Métodos reproducibles"),
                                ft.Checkbox(label="Resultados con IC"),
                                ft.Checkbox(label="Limitaciones explícitas")
                            ])
                        ]),
                        width=300,
                        bgcolor=ft.Colors.GREY_50,
                        padding=15,
                        border_radius=10
                    )
                ], expand=True),
                ft.Row([
                    ft.ElevatedButton("← Anterior", 
                                    on_click=self.prev_slide,
                                    disabled=self.current_slide == 0),
                    ft.Text(f"{self.current_slide + 1} / {len(self.lesson_slides)}", 
                           bgcolor=ft.Colors.BLUE_100, 
                           color=ft.Colors.BLUE_700),
                    ft.ElevatedButton("Siguiente →" if self.current_slide < len(self.lesson_slides) - 1 else "Ir a Práctica →", 
                                    on_click=self.next_slide)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )

    def create_slide_content(self):
        slide = self.lesson_slides[self.current_slide]
        return ft.Column([
            ft.Text(slide["title"], size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
            ft.Container(
                content=ft.Text(slide["content"], size=14),
                bgcolor=ft.Colors.BLUE_50,
                padding=15,
                border_radius=10,
                border=ft.border.all(1, ft.Colors.BLUE_200)
            )
        ])

    def prev_slide(self, e):
        if self.current_slide > 0:
            self.current_slide -= 1
            self.slide_content.content = self.create_slide_content()
            self.page.update()

    def next_slide(self, e):
        if self.current_slide < len(self.lesson_slides) - 1:
            self.current_slide += 1
            self.slide_content.content = self.create_slide_content()
        else:
            self.show_section("practice")
        self.page.update()

    def create_practice_section(self):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.HANDSHAKE, color=ft.Colors.GREEN_600, size=40),
                    ft.Text("Práctica Guiada: Caso Clínico Real", 
                           size=24, weight=ft.FontWeight.BOLD)
                ]),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.LOCAL_HOSPITAL, color=ft.Colors.GREEN_800),
                            ft.Text("Caso: Análisis de Mortalidad por COVID-19 en UCI", 
                                   size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800)
                        ]),
                        ft.Text("Trabajarás con datos simulados de 500 pacientes ingresados a UCI durante la pandemia. Tu objetivo es crear un resumen ejecutivo para el comité de calidad del hospital.")
                    ]),
                    bgcolor=ft.Colors.GREEN_50,
                    padding=15,
                    border_radius=10,
                    border=ft.border.all(2, ft.Colors.GREEN_400)
                ),
                ft.Row([
                    ft.Container(
                        content=self.create_practice_step_content(),
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🤔 Guía de Escritura", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Introducción efectiva debe incluir:", weight=ft.FontWeight.BOLD),
                                    ft.Text("• Contexto epidemiológico actual"),
                                    ft.Text("• Importancia del problema"),
                                    ft.Text("• Objetivo específico del análisis")
                                ]),
                                bgcolor=ft.Colors.BLUE_50,
                                padding=10,
                                border_radius=5,
                                border=ft.border.all(2, ft.Colors.BLUE_500)
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Palabras clave sugeridas:", weight=ft.FontWeight.BOLD),
                                    ft.Row([
                                        ft.Container(ft.Text("mortalidad"), bgcolor=ft.Colors.GREEN_100, padding=5, border_radius=3),
                                        ft.Container(ft.Text("UCI"), bgcolor=ft.Colors.GREEN_100, padding=5, border_radius=3)
                                    ]),
                                    ft.Row([
                                        ft.Container(ft.Text("factores de riesgo"), bgcolor=ft.Colors.GREEN_100, padding=5, border_radius=3),
                                        ft.Container(ft.Text("análisis descriptivo"), bgcolor=ft.Colors.GREEN_100, padding=5, border_radius=3)
                                    ])
                                ]),
                                bgcolor=ft.Colors.GREEN_50,
                                padding=10,
                                border_radius=5,
                                border=ft.border.all(2, ft.Colors.GREEN_500)
                            )
                        ]),
                        width=300,
                        bgcolor=ft.Colors.BLUE_50,
                        padding=15,
                        border_radius=10
                    )
                ])
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )

    def create_practice_step_content(self):
        steps = [
            {
                "title": "Análisis de Datos",
                "content": """Dataset: Pacientes UCI COVID-19
                
Variable          | n   | %    | Media (DE)
Edad (años)       | 500 | -    | 67.3 (12.8)
Sexo masculino    | 312 | 62.4 | -
Mortalidad        | 145 | 29.0 | -
Días estancia     | 500 | -    | 12.5 (8.9)"""
            },
            {
                "title": "Redacción de Métodos",
                "content": """Información del Estudio:
• Diseño: Estudio descriptivo retrospectivo
• Período: Marzo 2020 - Diciembre 2021
• Población: Pacientes adultos ingresados a UCI con diagnóstico confirmado de COVID-19
• Variables: Edad, sexo, comorbilidades, días de estancia, desenlace vital"""
            },
            {
                "title": "Presentación de Resultados",
                "content": """Hallazgos Principales:
• La edad promedio fue 67.3 años (DE: 12.8)
• El 62.4% fueron hombres
• La mortalidad global fue del 29.0%
• La estancia promedio fue 12.5 días (DE: 8.9)"""
            },
            {
                "title": "Discusión y Conclusiones",
                "content": """Puntos Clave para Discusión:
• Comparación con literatura internacional
• Implicaciones clínicas de los hallazgos
• Limitaciones del estudio
• Recomendaciones para la práctica"""
            }
        ]
        
        step = steps[self.practice_step - 1]
        
        return ft.Column([
            ft.Row([
                ft.Container(ft.Text(f"Paso {self.practice_step}", color=ft.Colors.WHITE), 
                           bgcolor=ft.Colors.GREEN_600, padding=8, border_radius=20),
                ft.Text(step["title"], size=18, weight=ft.FontWeight.BOLD)
            ]),
            ft.Container(
                content=ft.Text(step["content"], size=14),
                bgcolor=ft.Colors.GREY_50,
                padding=15,
                border_radius=10
            ),
            ft.TextField(
                label=f"Redacta tu respuesta para el {step['title'].lower()}:",
                multiline=True,
                min_lines=3,
                max_lines=5
            ),
            ft.ElevatedButton(
                f"Continuar al Paso {self.practice_step + 1}" if self.practice_step < 4 else "Ir a Evaluación",
                on_click=self.next_practice_step,
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE
            )
        ])

    def next_practice_step(self, e):
        if self.practice_step < 4:
            self.practice_step += 1
            self.content_area.content = self.create_practice_section()
        else:
            self.show_section("evaluation")
        self.page.update()

    def create_evaluation_section(self):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.QUIZ, color=ft.Colors.PURPLE_600, size=40),
                    ft.Text("Evaluación Automatizada", 
                           size=24, weight=ft.FontWeight.BOLD)
                ]),
                ft.Divider(),
                ft.Row([
                    ft.Container(
                        content=self.create_quiz_content(),
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Progreso de Evaluación", size=16, weight=ft.FontWeight.BOLD),
                            ft.Column([
                                ft.Row([ft.Text(f"Pregunta {i+1}"), 
                                       ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500) 
                                       if i < self.current_question else ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.GREY_300)])
                                for i in range(len(self.quiz_questions))
                            ]),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Criterios de Evaluación", weight=ft.FontWeight.BOLD),
                                    ft.Text("• Estructura IMRyD (25%)"),
                                    ft.Text("• Tablas científicas (25%)"),
                                    ft.Text("• Interpretación clínica (25%)"),
                                    ft.Text("• Comunicación efectiva (25%)")
                                ]),
                                bgcolor=ft.Colors.BLUE_50,
                                padding=10,
                                border_radius=5
                            ),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.INFO, color=ft.Colors.GREEN_800),
                                    ft.Text("Puntuación mínima: 70%")
                                ]),
                                bgcolor=ft.Colors.GREEN_50,
                                padding=10,
                                border_radius=5
                            )
                        ]),
                        width=300,
                        bgcolor=ft.Colors.GREY_50,
                        padding=15,
                        border_radius=10
                    )
                ])
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )

    def create_quiz_content(self):
        if self.current_question < len(self.quiz_questions):
            question = self.quiz_questions[self.current_question]
            
            options = []
            for i, option in enumerate(question["options"]):
                options.append(
                    ft.RadioListTile(
                        value=i,
                        title=ft.Text(option),
                        group_value=self.quiz_answers.get(self.current_question, -1)
                    )
                )
            
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Pregunta {self.current_question + 1} de {len(self.quiz_questions)}", 
                               size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(question["question"], size=16),
                        ft.Column(options)
                    ]),
                    bgcolor=ft.Colors.PURPLE_50,
                    padding=15,
                    border_radius=10
                ),
                ft.Row([
                    ft.ElevatedButton("← Anterior", 
                                    on_click=self.prev_question,
                                    disabled=self.current_question == 0),
                    ft.ElevatedButton("Siguiente →" if self.current_question < len(self.quiz_questions) - 1 else "Finalizar", 
                                    on_click=self.next_question,
                                    bgcolor=ft.Colors.PURPLE_600,
                                    color=ft.Colors.WHITE)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        else:
            return self.create_quiz_results()

    def prev_question(self, e):
        if self.current_question > 0:
            self.current_question -= 1
            self.content_area.content = self.create_evaluation_section()
            self.page.update()

    def next_question(self, e):
        if self.current_question < len(self.quiz_questions) - 1:
            self.current_question += 1
        else:
            self.current_question = len(self.quiz_questions)  # Mostrar resultados
        
        self.content_area.content = self.create_evaluation_section()
        self.page.update()

    def create_quiz_results(self):
        correct_answers = sum(1 for i, q in enumerate(self.quiz_questions) 
                            if self.quiz_answers.get(i, -1) == q["correct"])
        score = round((correct_answers / len(self.quiz_questions)) * 100)
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.EMOJI_EVENTS, color=ft.Colors.YELLOW_600, size=60),
                    ft.Text("¡Evaluación Completada!", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text(str(correct_answers), size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600),
                                ft.Text("Respuestas Correctas", size=14, color=ft.Colors.GREEN_700)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.GREEN_50,
                            padding=15,
                            border_radius=10,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(f"{score}%", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                                ft.Text("Puntuación Final", size=14, color=ft.Colors.BLUE_700)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.BLUE_50,
                            padding=15,
                            border_radius=10,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D", 
                                       size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_600),
                                ft.Text("Calificación", size=14, color=ft.Colors.PURPLE_700)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.PURPLE_50,
                            padding=15,
                            border_radius=10,
                            expand=True
                        )
                    ]),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Retroalimentación Personalizada", weight=ft.FontWeight.BOLD),
                            ft.Text("Excelente dominio de la estructura IMRyD. Se recomienda practicar más la redacción de limitaciones en la sección de discusión." 
                                   if score >= 80 else "Buen trabajo. Revisa los conceptos de interpretación clínica y estructura de tablas científicas.")
                        ]),
                        bgcolor=ft.Colors.YELLOW_50,
                        padding=15,
                        border_radius=10,
                        border=ft.border.all(2, ft.Colors.YELLOW_400)
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20
            )
        ])

    def create_resources_section(self):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.DOWNLOAD, color=ft.Colors.INDIGO_600, size=40),
                    ft.Text("Recursos Descargables y Actividad de Transferencia", 
                           size=24, weight=ft.FontWeight.BOLD)
                ]),
                ft.Divider(),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Material Descargable", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_700),
                            ft.Column([
                                self.create_resource_item("📄", "Plantilla Resumen Ejecutivo", 
                                                         "Formato estándar IMRyD para ciencias de la salud", "template"),
                                self.create_resource_item("📊", "Guía de Tablas Científicas", 
                                                         "Estándares para tablas 'listas para publicación'", "tables"),
                                self.create_resource_item("📋", "Checklist de Calidad", 
                                                         "Lista de verificación para escritura científica", "checklist"),
                                self.create_resource_item("💾", "Dataset de Práctica", 
                                                         "Datos simulados COVID-19 UCI (CSV)", "dataset")
                            ]),
                            ft.Text("Rúbrica de Evaluación", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Criterios de Evaluación:", weight=ft.FontWeight.BOLD),
                                    ft.Text("• Excelente (4): Cumple perfectamente todos los criterios"),
                                    ft.Text("• Bueno (3): Cumple la mayoría de criterios con pequeñas inconsistencias"),
                                    ft.Text("• Satisfactorio (2): Cumple criterios básicos pero requiere mejoras"),
                                    ft.Text("• Insuficiente (1): No cumple criterios mínimos")
                                ]),
                                bgcolor=ft.Colors.GREY_50,
                                padding=15,
                                border_radius=10
                            )
                        ]),
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Actividad de Transferencia", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Icon(ft.Icons.ASSIGNMENT, color=ft.Colors.GREEN_800),
                                        ft.Text("Proyecto Final: Miniinforme Clínico", weight=ft.FontWeight.BOLD)
                                    ]),
                                    ft.Text("Elabora un resumen ejecutivo completo sobre un problema de salud pública de tu elección, utilizando datos reales o simulados."),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Especificaciones del Proyecto:", weight=ft.FontWeight.BOLD),
                                            ft.Text("• Extensión: 2-3 páginas"),
                                            ft.Text("• Incluir al menos 2 tablas científicas"),
                                            ft.Text("• Mínimo 1 gráfico con interpretación"),
                                            ft.Text("• Referencias bibliográficas (formato Vancouver)"),
                                            ft.Text("• Entrega en formato PDF reproducible")
                                        ]),
                                        bgcolor=ft.Colors.WHITE,
                                        padding=10,
                                        border_radius=5,
                                        border=ft.border.all(2, ft.Colors.GREEN_500)
                                    )
                                ]),
                                bgcolor=ft.Colors.GREEN_50,
                                padding=15,
                                border_radius=10
                            ),
                            ft.Dropdown(
                                label="Selecciona tu tema de investigación:",
                                options=[
                                    ft.dropdown.Option("diabetes", "Prevalencia de diabetes tipo 2 en adultos"),
                                    ft.dropdown.Option("hipertension", "Hipertensión arterial en embarazadas"),
                                    ft.dropdown.Option("obesidad", "Obesidad infantil en edad escolar"),
                                    ft.dropdown.Option("covid", "Secuelas post-COVID en personal sanitario"),
                                    ft.dropdown.Option("cancer", "Detección temprana de cáncer de mama"),
                                    ft.dropdown.Option("custom", "Tema personalizado")
                                ]
                            ),
                            ft.TextField(
                                label="Justificación (¿Por qué es importante este tema?):",
                                multiline=True,
                                min_lines=3,
                                max_lines=5
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Icon(ft.Icons.CALENDAR_TODAY, color=ft.Colors.YELLOW_800),
                                        ft.Text("Cronograma Sugerido", weight=ft.FontWeight.BOLD)
                                    ]),
                                    ft.Text("Semana 1: Búsqueda bibliográfica y definición de objetivos"),
                                    ft.Text("Semana 2: Análisis de datos y creación de tablas"),
                                    ft.Text("Semana 3: Redacción del borrador inicial"),
                                    ft.Text("Semana 4: Revisión, correcciones y entrega final")
                                ]),
                                bgcolor=ft.Colors.YELLOW_50,
                                padding=15,
                                border_radius=10,
                                border=ft.border.all(2, ft.Colors.YELLOW_400)
                            ),
                            ft.ElevatedButton("🚀 Iniciar Proyecto de Transferencia", 
                                            on_click=self.start_transfer_project,
                                            bgcolor=ft.Colors.GREEN_600,
                                            color=ft.Colors.WHITE,
                                            size=ft.ControlSize.LARGE)
                        ]),
                        width=400
                    )
                ])
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )

    def create_resource_item(self, icon, title, description, resource_type):
        return ft.Container(
            content=ft.Row([
                ft.Text(icon, size=24),
                ft.Column([
                    ft.Text(title, weight=ft.FontWeight.BOLD),
                    ft.Text(description, size=12, color=ft.Colors.GREY_600)
                ], expand=True),
                ft.ElevatedButton("💾 Descargar", 
                                on_click=lambda _: self.download_resource(resource_type),
                                bgcolor=ft.Colors.INDIGO_600,
                                color=ft.Colors.WHITE)
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=15,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.GREY_200)
        )

    def download_resource(self, resource_type):
        resources = {
            'template': 'Plantilla_Resumen_Ejecutivo.docx',
            'tables': 'Guia_Tablas_Cientificas.pdf',
            'checklist': 'Checklist_Escritura_Cientifica.pdf',
            'dataset': 'Dataset_COVID_UCI.csv'
        }
        
        filename = resources.get(resource_type, 'recurso.txt')
        
        # Crear contenido simulado
        content = f"Contenido del recurso: {filename}\nGenerado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Guardar archivo
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            self.show_notification(f"{filename} descargado exitosamente", "success")
        except Exception as e:
            self.show_notification(f"Error al descargar: {str(e)}", "error")

    def start_transfer_project(self, e):
        self.show_notification("¡Proyecto de transferencia iniciado! Revisa tu correo para más detalles.", "success")

    def toggle_ai(self, e):
        self.ai_panel.visible = not self.ai_panel.visible
        if self.ai_panel.visible:
            self.add_ai_message("¡Hola! Soy tu asistente IA especializado en escritura científica. ¿En qué puedo ayudarte hoy?", "ai")
        self.page.update()

    def send_ai_message(self, e):
        message = self.ai_input.value.strip()
        if message:
            self.add_ai_message(message, "user")
            self.ai_input.value = ""
            
            # Simular respuesta de IA
            response = self.generate_ai_response(message)
            self.add_ai_message(response, "ai")
            self.page.update()

    def add_ai_message(self, message, sender):
        color = ft.Colors.PURPLE_100 if sender == "ai" else ft.Colors.BLUE_100
        text_color = ft.Colors.PURPLE_800 if sender == "ai" else ft.Colors.BLUE_800
        
        self.ai_messages.controls.append(
            ft.Container(
                content=ft.Text(f"{'🤖 IA:' if sender == 'ai' else '👤 Tú:'} {message}", 
                               color=text_color, size=12),
                bgcolor=color,
                padding=8,
                border_radius=5,
                margin=ft.margin.only(bottom=5)
            )
        )

    def generate_ai_response(self, message):
        responses = {
            'imrad': 'La estructura IMRyD (Introducción, Métodos, Resultados, Discusión) es fundamental para la escritura científica. Cada sección tiene un propósito específico y debe fluir lógicamente hacia la siguiente.',
            'tabla': 'Para crear tablas científicas efectivas, asegúrate de incluir: título descriptivo, encabezados claros, estadísticos apropiados (n, %, media±DE), y notas al pie explicativas.',
            'limitaciones': 'Las limitaciones deben ser honestas y específicas. Incluye limitaciones del diseño, sesgos potenciales, y factores que puedan afectar la generalización de resultados.',
            'interpretacion': 'La interpretación clínica debe conectar los hallazgos estadísticos con la práctica médica. Considera la relevancia clínica, no solo la significancia estadística.',
            'default': 'Basándome en el modelo C(H)ANGE, te sugiero considerar los aspectos combinatorios, algebraicos, numéricos, geométricos y estadísticos de tu pregunta. ¿Podrías ser más específico sobre qué aspecto de la escritura científica te interesa?'
        }
        
        message_lower = message.lower()
        
        if 'imrad' in message_lower or 'estructura' in message_lower:
            return responses['imrad']
        elif 'tabla' in message_lower:
            return responses['tabla']
        elif 'limitacion' in message_lower:
            return responses['limitaciones']
        elif 'interpretacion' in message_lower or 'clinica' in message_lower:
            return responses['interpretacion']
        else:
            return responses['default']

    def update_progress(self):
        sections = ["intro", "lesson", "practice", "evaluation", "resources"]
        current_index = sections.index(self.current_section)
        self.progress = ((current_index + 1) / len(sections)) * 100
        
        self.progress_bar.value = self.progress / 100
        self.progress_text.value = f"{round(self.progress)}%"
        
        if hasattr(self, 'page'):
            self.page.update()

    def show_notification(self, message, type_msg):
        color = ft.Colors.GREEN_500 if type_msg == "success" else ft.Colors.RED_500 if type_msg == "error" else ft.Colors.BLUE_500
        icon = ft.Icons.CHECK_CIRCLE if type_msg == "success" else ft.Icons.ERROR if type_msg == "error" else ft.Icons.INFO
        
        snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(icon, color=ft.Colors.WHITE),
                ft.Text(message, color=ft.Colors.WHITE)
            ]),
            bgcolor=color
        )
        
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()

def main(page: ft.Page):
    app = OVA17App()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
