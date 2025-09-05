
import flet as ft
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
import random
import json
from datetime import datetime
import os

class OVAApp:
    def __init__(self):
        self.current_section = "intro"
        self.progress = 0
        self.quiz_score = 0
        self.checklist_completed = 0
        self.ai_messages = {
            "default": "¡Hola! Soy tu asistente de inteligencia artificial. Te guiaré paso a paso para crear flujos de trabajo reproducibles en estadística para ciencias de la salud.",
            "reproducibility": "¡Excelente elección! La reproducibilidad es fundamental en investigación médica. Te ayudo a implementar las mejores prácticas.",
            "documentation": "La documentación es tu mejor aliada. Te mostraré cómo crear documentación que realmente sea útil.",
            "versioning": "El control de versiones puede parecer complejo, pero te guiaré paso a paso para dominarlo.",
            "workflow": "Un buen flujo de trabajo es como un protocolo médico: estructurado, claro y repetible."
        }
        
        # Datos simulados de hipertensión
        self.hypertension_data = [
            {"id": 1, "edad": 45, "sexo": "M", "pas": 140, "pad": 90, "imc": 28.5, "tratamiento": "Si"},
            {"id": 2, "edad": 52, "sexo": "F", "pas": 135, "pad": 85, "imc": 26.2, "tratamiento": "Si"},
            {"id": 3, "edad": 38, "sexo": "M", "pas": 145, "pad": 95, "imc": 30.1, "tratamiento": "No"},
            {"id": 4, "edad": 61, "sexo": "F", "pas": 150, "pad": 88, "imc": 24.8, "tratamiento": "Si"},
            {"id": 5, "edad": 47, "sexo": "M", "pas": 138, "pad": 92, "imc": 27.3, "tratamiento": "Si"}
        ]

    def main(self, page: ft.Page):
        page.title = "OVA 16: Flujo de Trabajo Reproducible"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.scroll = ft.ScrollMode.AUTO
        
        # Variables de estado
        self.page = page
        self.ai_message_text = ft.Text(
            self.ai_messages["default"],
            size=14,
            color=ft.Colors.GREY_700
        )
        
        # Crear componentes principales
        self.create_header()
        self.create_progress_bar()
        self.create_navigation()
        self.create_sections()
        
        # Layout principal
        main_content = ft.Column([
            self.header,
            self.progress_container,
            self.navigation,
            self.content_container
        ], spacing=0)
        
        page.add(main_content)
        self.show_section("intro")

    def create_header(self):
        self.header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("OVA 16: Flujo de Trabajo Reproducible", 
                           size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                    ft.Text("Estadística para Ciencias de la Salud - Modelo C(H)ANGE", 
                           size=16, color=ft.Colors.GREY_600)
                ], expand=True),
                ft.Row([
                    ft.Container(
                        content=ft.Text("Duración: 2-4 horas", weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_800),
                        bgcolor=ft.Colors.BLUE_100,
                        padding=ft.padding.all(10),
                        border_radius=8
                    ),
                    ft.Container(
                        content=ft.Text("Nivel: Intermedio", weight=ft.FontWeight.W_500, color=ft.Colors.GREEN_800),
                        bgcolor=ft.Colors.GREEN_100,
                        padding=ft.padding.all(10),
                        border_radius=8
                    )
                ], spacing=10)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.all(20),
            border=ft.border.only(bottom=ft.border.BorderSide(4, ft.Colors.BLUE_500))
        )

    def create_progress_bar(self):
        self.progress_text = ft.Text("0% Completado", size=12, color=ft.Colors.GREY_600)
        self.progress_bar = ft.ProgressBar(value=0, color=ft.Colors.BLUE_500, bgcolor=ft.Colors.GREY_200)
        
        self.progress_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Progreso del Aprendizaje", size=12, color=ft.Colors.GREY_600),
                    self.progress_text
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar
            ], spacing=5),
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.all(15)
        )

    def create_navigation(self):
        nav_buttons = [
            ("intro", "Introducción", ft.Icons.PLAY_CIRCLE),
            ("theory", "Microlección", ft.Icons.BOOK),
            ("simulator", "Simulador", ft.Icons.SETTINGS),
            ("practice", "Práctica Guiada", ft.Icons.HANDYMAN),
            ("evaluation", "Evaluación", ft.Icons.ASSIGNMENT_TURNED_IN),
            ("resources", "Recursos", ft.Icons.DOWNLOAD)
        ]
        
        self.nav_buttons = {}
        nav_row = []
        
        for section_id, label, icon in nav_buttons:
            btn = ft.TextButton(
                text=label,
                icon=icon,
                on_click=lambda e, s=section_id: self.show_section(s),
                style=ft.ButtonStyle(
                    color=ft.Colors.GREY_600 if section_id != "intro" else ft.Colors.BLUE_600,
                    bgcolor=ft.Colors.TRANSPARENT
                )
            )
            self.nav_buttons[section_id] = btn
            nav_row.append(btn)
        
        self.navigation = ft.Container(
            content=ft.Row(nav_row, scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300))
        )

    def create_sections(self):
        self.content_container = ft.Container(
            content=ft.Column([], scroll=ft.ScrollMode.AUTO),
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.BLUE_GREY_50,
            expand=True
        )

    def show_section(self, section_id):
        self.current_section = section_id
        self.update_progress()
        self.update_navigation()
        
        # Limpiar contenido actual
        self.content_container.content.controls.clear()
        
        # Mostrar sección correspondiente
        if section_id == "intro":
            self.show_intro_section()
        elif section_id == "theory":
            self.show_theory_section()
        elif section_id == "simulator":
            self.show_simulator_section()
        elif section_id == "practice":
            self.show_practice_section()
        elif section_id == "evaluation":
            self.show_evaluation_section()
        elif section_id == "resources":
            self.show_resources_section()
        
        self.page.update()

    def update_progress(self):
        sections = ["intro", "theory", "simulator", "practice", "evaluation", "resources"]
        current_index = sections.index(self.current_section)
        self.progress = (current_index + 1) / len(sections)
        
        self.progress_bar.value = self.progress
        self.progress_text.value = f"{int(self.progress * 100)}% Completado"

    def update_navigation(self):
        for section_id, btn in self.nav_buttons.items():
            if section_id == self.current_section:
                btn.style.color = ft.Colors.BLUE_600
            else:
                btn.style.color = ft.Colors.GREY_600

    def create_card(self, content, bgcolor=ft.Colors.WHITE, padding=20):
        return ft.Container(
            content=content,
            bgcolor=bgcolor,
            padding=ft.padding.all(padding),
            border_radius=12,
            margin=ft.margin.only(bottom=20),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
            )
        )

    def show_intro_section(self):
        # Título principal
        title_section = ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.BIOTECH, size=60, color=ft.Colors.BLUE_600),
                alignment=ft.alignment.center,
                margin=ft.margin.only(bottom=20)
            ),
            ft.Text("Bienvenido al Flujo de Trabajo Reproducible", 
                   size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Text("Aprende a documentar, versionar y reproducir análisis estadísticos en ciencias de la salud utilizando el modelo pedagógico C(H)ANGE e inteligencia artificial.",
                   size=16, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # Objetivos y modelo CHANGE
        objectives_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TARGET_OUTLINED, color=ft.Colors.BLUE_600),
                    ft.Text("Objetivos de Aprendizaje", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
                ]),
                ft.Column([
                    self.create_objective_item("Documentar análisis estadísticos de forma reproducible"),
                    self.create_objective_item("Implementar control de versiones en proyectos de salud"),
                    self.create_objective_item("Crear scripts reutilizables con buenas prácticas"),
                    self.create_objective_item("Aplicar el modelo C(H)ANGE en flujos de trabajo")
                ])
            ]),
            bgcolor=ft.Colors.BLUE_50,
            padding=ft.padding.all(20),
            border_radius=8,
            expand=True
        )

        change_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PSYCHOLOGY, color=ft.Colors.GREEN_600),
                    ft.Text("Modelo C(H)ANGE Integrado", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800)
                ]),
                ft.Column([
                    self.create_change_item("C", "Combinatoria: Organización de archivos y carpetas", ft.Colors.RED_100),
                    self.create_change_item("A", "Álgebra: Variables y funciones en scripts", ft.Colors.YELLOW_100),
                    self.create_change_item("N", "Números: Semillas aleatorias y versiones", ft.Colors.BLUE_100),
                    self.create_change_item("G", "Geometría: Diagramas de flujo de trabajo", ft.Colors.PURPLE_100),
                    self.create_change_item("E", "Estadística: Análisis reproducible", ft.Colors.GREEN_100)
                ])
            ]),
            bgcolor=ft.Colors.GREEN_50,
            padding=ft.padding.all(20),
            border_radius=8,
            expand=True
        )

        # Caso clínico
        case_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.MEDICAL_SERVICES, color=ft.Colors.ORANGE_600),
                    ft.Text("Caso Clínico: Estudio de Hipertensión", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800)
                ]),
                ft.Text("Un equipo de investigación está analizando datos de 1,000 pacientes con hipertensión. Después de 6 meses, necesitan reproducir exactamente los mismos resultados para una publicación científica, pero el análisis original no está documentado adecuadamente.",
                       size=14, color=ft.Colors.GREY_700),
                ft.Container(
                    content=ft.Text("\"¿Cómo podemos asegurar que nuestros análisis estadísticos sean completamente reproducibles y transparentes para la comunidad científica?\"",
                                   size=12, color=ft.Colors.GREY_600, italic=True),
                    bgcolor=ft.Colors.WHITE,
                    padding=ft.padding.all(15),
                    border_radius=8,
                    margin=ft.margin.only(top=10)
                )
            ]),
            bgcolor=ft.Colors.ORANGE_50,
            padding=ft.padding.all(20),
            border_radius=8,
            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.ORANGE_500))
        )

        # Botón continuar
        continue_btn = ft.Container(
            content=ft.ElevatedButton(
                text="Comenzar Microlección",
                icon=ft.Icons.ARROW_FORWARD,
                on_click=lambda e: self.show_section("theory"),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_500,
                    color=ft.Colors.WHITE,
                    padding=ft.padding.symmetric(horizontal=30, vertical=15)
                )
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=20)
        )

        # Agregar todo al contenedor
        self.content_container.content.controls.extend([
            self.create_card(title_section),
            self.create_card(ft.Row([objectives_card, change_card], spacing=20)),
            self.create_card(case_card),
            continue_btn
        ])

    def create_objective_item(self, text):
        return ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500, size=20),
            ft.Text(text, size=14, color=ft.Colors.GREY_700, expand=True)
        ], spacing=10)

    def create_change_item(self, letter, description, bgcolor):
        return ft.Row([
            ft.Container(
                content=ft.Text(letter, size=12, weight=ft.FontWeight.BOLD),
                bgcolor=bgcolor,
                padding=ft.padding.all(8),
                border_radius=4,
                width=30,
                height=30,
                alignment=ft.alignment.center
            ),
            ft.Text(description, size=14, color=ft.Colors.GREY_700, expand=True)
        ], spacing=10)

    def show_theory_section(self):
        # Título
        title = ft.Text("Microlección: Fundamentos de Reproducibilidad", 
                       size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)

        # Asistente IA
        ai_assistant = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.SMART_TOY, color=ft.Colors.PURPLE_600, size=30),
                    bgcolor=ft.Colors.PURPLE_100,
                    padding=ft.padding.all(15),
                    border_radius=50
                ),
                ft.Column([
                    ft.Text("Asistente IA - BioStat Helper", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_800),
                    self.ai_message_text
                ], expand=True)
            ], spacing=15),
            bgcolor=ft.Colors.PURPLE_50,
            padding=ft.padding.all(20),
            border_radius=8,
            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.PURPLE_500))
        )

        # Conceptos fundamentales
        concepts_column = ft.Column([
            ft.Text("Conceptos Fundamentales", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
            self.create_concept_card("Reproducibilidad", "Capacidad de obtener los mismos resultados usando los mismos datos y métodos.", 
                                   ft.Colors.BLUE_50, ft.Colors.BLUE_500, "reproducibility"),
            self.create_concept_card("Documentación", "Registro detallado de todos los pasos, decisiones y métodos utilizados.", 
                                   ft.Colors.GREEN_50, ft.Colors.GREEN_500, "documentation"),
            self.create_concept_card("Control de Versiones", "Sistema para rastrear cambios en archivos y código a lo largo del tiempo.", 
                                   ft.Colors.YELLOW_50, ft.Colors.YELLOW_600, "versioning"),
            self.create_concept_card("Flujo de Trabajo", "Secuencia organizada de pasos para completar un análisis estadístico.", 
                                   ft.Colors.PURPLE_50, ft.Colors.PURPLE_500, "workflow")
        ], spacing=15)

        # Panel de detalles
        self.concept_detail = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.MOUSE, size=60, color=ft.Colors.GREY_400),
                ft.Text("Haz clic en un concepto para ver más detalles", 
                       color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
               alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=ft.Colors.GREY_50,
            padding=ft.padding.all(30),
            border_radius=8,
            height=400,
            expand=True
        )

        # Diagrama de flujo
        workflow_diagram = self.create_workflow_diagram()

        # Botón continuar
        continue_btn = ft.Container(
            content=ft.ElevatedButton(
                text="Ir al Simulador",
                icon=ft.Icons.SETTINGS,
                on_click=lambda e: self.show_section("simulator"),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREEN_500,
                    color=ft.Colors.WHITE,
                    padding=ft.padding.symmetric(horizontal=30, vertical=15)
                )
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=20)
        )

        # Agregar contenido
        self.content_container.content.controls.extend([
            self.create_card(ft.Column([title, ai_assistant], spacing=20)),
            self.create_card(ft.Row([concepts_column, self.concept_detail], spacing=20)),
            self.create_card(workflow_diagram),
            continue_btn
        ])

    def create_concept_card(self, title, description, bgcolor, border_color, concept_id):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, weight=ft.FontWeight.BOLD, size=16),
                ft.Text(description, size=12, color=ft.Colors.GREY_700)
            ]),
            bgcolor=bgcolor,
            padding=ft.padding.all(15),
            border_radius=8,
            border=ft.border.only(left=ft.border.BorderSide(4, border_color)),
            on_click=lambda e, cid=concept_id: self.show_concept_detail(cid),
            ink=True
        )

    def show_concept_detail(self, concept_id):
        details = {
            "reproducibility": {
                "title": "Reproducibilidad en Estadística",
                "content": [
                    "La reproducibilidad es la capacidad de obtener los mismos resultados cuando se repite un análisis con los mismos datos y métodos.",
                    "Elementos clave:",
                    "• Código fuente disponible",
                    "• Datos originales accesibles", 
                    "• Entorno computacional documentado",
                    "• Pasos del análisis claramente descritos",
                    "En ciencias de la salud:",
                    "La reproducibilidad es crucial para validar hallazgos clínicos y garantizar la confiabilidad de la evidencia médica."
                ]
            },
            "documentation": {
                "title": "Documentación Efectiva",
                "content": [
                    "La documentación adecuada permite que otros (incluido tu yo futuro) entiendan y reproduzcan tu trabajo.",
                    "Tipos de documentación:",
                    "• Comentarios en el código",
                    "• README con instrucciones",
                    "• Diccionario de datos",
                    "• Bitácora de decisiones",
                    "Ejemplo clínico:",
                    "Documentar por qué se excluyeron ciertos pacientes o por qué se eligió un método estadístico específico."
                ]
            },
            "versioning": {
                "title": "Control de Versiones",
                "content": [
                    "El control de versiones rastrea cambios en archivos y permite colaboración efectiva.",
                    "Herramientas populares:",
                    "• Git (más común)",
                    "• SVN (Subversion)",
                    "• Mercurial",
                    "Beneficios en investigación:",
                    "• Historial completo de cambios",
                    "• Colaboración sin conflictos",
                    "• Recuperación de versiones anteriores",
                    "• Transparencia en el proceso"
                ]
            },
            "workflow": {
                "title": "Flujo de Trabajo Estructurado",
                "content": [
                    "Un flujo de trabajo bien estructurado organiza las tareas de manera lógica y eficiente.",
                    "Fases típicas:",
                    "1. Planificación y diseño",
                    "2. Recolección de datos",
                    "3. Limpieza y preparación",
                    "4. Análisis exploratorio",
                    "5. Análisis confirmatorio",
                    "6. Interpretación y reporte",
                    "Modelo C(H)ANGE aplicado:",
                    "Cada fase integra elementos de combinatoria, álgebra, números, geometría y estadística."
                ]
            }
        }

        detail = details[concept_id]
        content_widgets = [ft.Text(detail["title"], size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)]
        
        for line in detail["content"]:
            if line.endswith(":"):
                content_widgets.append(ft.Text(line, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800, size=14))
            else:
                content_widgets.append(ft.Text(line, size=12, color=ft.Colors.GREY_700))

        self.concept_detail.content = ft.Column(content_widgets, spacing=8, scroll=ft.ScrollMode.AUTO)
        self.ai_message_text.value = self.ai_messages[concept_id]
        self.page.update()

    def create_workflow_diagram(self):
        steps = [
            ("Organización", "Estructura de carpetas", ft.Colors.BLUE_100, ft.Icons.FOLDER_OPEN),
            ("Codificación", "Scripts documentados", ft.Colors.GREEN_100, ft.Icons.CODE),
            ("Versionado", "Control de cambios", ft.Colors.YELLOW_100, ft.Icons.SAVE),
            ("Compartir", "Reproducibilidad", ft.Colors.PURPLE_100, ft.Icons.SHARE)
        ]

        step_widgets = []
        for i, (title, subtitle, color, icon) in enumerate(steps):
            step_widget = ft.Container(
                content=ft.Column([
                    ft.Icon(icon, size=30, color=ft.Colors.GREY_700),
                    ft.Text(f"{i+1}. {title}", weight=ft.FontWeight.BOLD, size=14, text_align=ft.TextAlign.CENTER),
                    ft.Text(subtitle, size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=color,
                padding=ft.padding.all(15),
                border_radius=8,
                width=150,
                on_click=lambda e, step=i+1: self.highlight_workflow_step(step),
                ink=True
            )
            step_widgets.append(step_widget)
            
            if i < len(steps) - 1:
                step_widgets.append(ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.GREY_400))

        return ft.Column([
            ft.Text("Flujo de Trabajo Reproducible", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
            ft.Container(
                content=ft.Row(step_widgets, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                bgcolor=ft.Colors.GREY_50,
                padding=ft.padding.all(20),
                border_radius=8
            )
        ], spacing=15)

    def highlight_workflow_step(self, step):
        descriptions = {
            1: "Organiza tu proyecto con una estructura de carpetas clara y consistente. Esto facilita la navegación y colaboración.",
            2: "Escribe código limpio y bien documentado. Cada función y decisión importante debe estar explicada.",
            3: "Implementa control de versiones para rastrear cambios y facilitar la colaboración en equipo.",
            4: "Comparte tu trabajo de manera que otros puedan reproducir exactamente tus resultados."
        }
        self.ai_message_text.value = descriptions[step]
        self.page.update()

    def show_simulator_section(self):
        title = ft.Text("Simulador de Flujo de Trabajo", 
                       size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)

        # Panel de control
        self.project_type = ft.Dropdown(
            label="Tipo de Proyecto",
            options=[
                ft.dropdown.Option("hypertension", "Estudio de Hipertensión"),
                ft.dropdown.Option("diabetes", "Análisis de Diabetes"),
                ft.dropdown.Option("covid", "Investigación COVID-19"),
                ft.dropdown.Option("cancer", "Registro de Cáncer")
            ],
            value="hypertension",
            on_change=self.update_project_structure
        )

        self.folder_structure = ft.Text(
            self.get_folder_structure("hypertension"),
            font_family="Courier New",
            size=12,
            color=ft.Colors.GREY_700
        )

        self.random_seed = ft.TextField(
            label="Semilla Aleatoria",
            value="123",
            width=200
        )

        self.programming_language = ft.Dropdown(
            label="Lenguaje de Programación",
            options=[
                ft.dropdown.Option("r", "R"),
                ft.dropdown.Option("python", "Python")
            ],
            value="r",
            width=200
        )

        generate_btn = ft.ElevatedButton(
            text="Generar Flujo de Trabajo",
            icon=ft.Icons.AUTO_FIX_HIGH,
            on_click=self.generate_workflow,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_500,
                color=ft.Colors.WHITE
            )
        )

        control_panel = ft.Column([
            ft.Text("Panel de Control", size=18, weight=ft.FontWeight.BOLD),
            self.project_type,
            ft.Text("Estructura de Carpetas Sugerida", weight=ft.FontWeight.BOLD, size=14),
            ft.Container(
                content=self.folder_structure,
                bgcolor=ft.Colors.GREY_50,
                padding=ft.padding.all(15),
                border_radius=8
            ),
            ft.Row([self.random_seed, self.programming_language], spacing=10),
            generate_btn
        ], spacing=15)

        # Panel de resultados
        self.generated_code = ft.Text(
            "Selecciona las opciones y haz clic en 'Generar Flujo de Trabajo'",
            font_family="Courier New",
            size=12,
            color=ft.Colors.GREY_400
        )

        self.ai_validation = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SMART_TOY, color=ft.Colors.BLUE_600),
                ft.Column([
                    ft.Text("Validación IA", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                    ft.Text("", size=12, color=ft.Colors.GREY_700)
                ], expand=True)
            ]),
            bgcolor=ft.Colors.BLUE_50,
            padding=ft.padding.all(15),
            border_radius=8,
            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.BLUE_500)),
            visible=False
        )

        # Métricas de calidad
        self.doc_progress = ft.ProgressBar(value=0, color=ft.Colors.GREEN_500)
        self.repro_progress = ft.ProgressBar(value=0, color=ft.Colors.BLUE_500)
        self.practices_progress = ft.ProgressBar(value=0, color=ft.Colors.PURPLE_500)

        metrics = ft.Column([
            ft.Text("Métricas de Calidad del Código", weight=ft.FontWeight.BOLD, size=14),
            ft.Row([ft.Text("Documentación", size=12), self.doc_progress, ft.Text("0%", size=12)]),
            ft.Row([ft.Text("Reproducibilidad", size=12), self.repro_progress, ft.Text("0%", size=12)]),
            ft.Row([ft.Text("Buenas Prácticas", size=12), self.practices_progress, ft.Text("0%", size=12)])
        ], spacing=10)

        results_panel = ft.Column([
            ft.Text("Código Generado", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([self.generated_code], scroll=ft.ScrollMode.AUTO),
                bgcolor=ft.Colors.GREY_900,
                padding=ft.padding.all(15),
                border_radius=8,
                height=300
            ),
            self.ai_validation,
            metrics
        ], spacing=15)

        # Botón continuar
        continue_btn = ft.Container(
            content=ft.ElevatedButton(
                text="Continuar con Práctica Guiada",
                icon=ft.Icons.HANDYMAN,
                on_click=lambda e: self.show_section("practice"),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.PURPLE_500,
                    color=ft.Colors.WHITE,
                    padding=ft.padding.symmetric(horizontal=30, vertical=15)
                )
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=20)
        )

        # Agregar contenido
        self.content_container.content.controls.extend([
            self.create_card(title),
            self.create_card(ft.Row([
                ft.Container(content=control_panel, expand=True),
                ft.Container(content=results_panel, expand=True)
            ], spacing=20)),
            continue_btn
        ])

    def get_folder_structure(self, project_type):
        structures = {
            "hypertension": """proyecto_hipertension/
├── data/
│   ├── raw/
│   │   └── hipertension_raw.csv
│   └── processed/
│       └── hipertension_clean.csv
├── scripts/
│   ├── 01_data_cleaning.R
│   ├── 02_descriptive_analysis.R
│   └── 03_visualization.R
├── results/
│   ├── tables/
│   └── figures/
├── docs/
│   ├── README.md
│   └── data_dictionary.md
└── renv.lock""",
            "diabetes": """proyecto_diabetes/
├── data/
│   ├── raw/
│   │   └── diabetes_raw.csv
│   └── processed/
│       └── diabetes_clean.csv
├── scripts/
│   ├── 01_data_prep.py
│   ├── 02_eda.py
│   └── 03_modeling.py
├── results/
│   ├── models/
│   └── reports/
├── notebooks/
│   └── exploratory_analysis.ipynb
└── requirements.txt""",
            "covid": """proyecto_covid/
├── data/
│   ├── epidemiological/
│   └── clinical/
├── scripts/
│   ├── data_processing/
│   ├── analysis/
│   └── visualization/
├── results/
│   ├── daily_reports/
│   └── weekly_summaries/
├── docs/
└── config/""",
            "cancer": """registro_cancer/
├── data/
│   ├── registry/
│   ├── follow_up/
│   └── outcomes/
├── scripts/
│   ├── quality_control/
│   ├── survival_analysis/
│   └── reporting/
├── results/
│   ├── annual_reports/
│   └── publications/
├── docs/
└── templates/"""
        }
        return structures.get(project_type, "")

    def update_project_structure(self, e):
        project_type = self.project_type.value
        self.folder_structure.value = self.get_folder_structure(project_type)
        self.page.update()

    def generate_workflow(self, e):
        project_type = self.project_type.value
        language = self.programming_language.value
        seed = self.random_seed.value

        if language == "r":
            code = self.generate_r_code(project_type, seed)
        else:
            code = self.generate_python_code(project_type, seed)

        self.generated_code.value = code
        self.generated_code.color = ft.Colors.GREEN_400

        # Mostrar validación IA
        self.ai_validation.visible = True
        validation_text = self.ai_validation.content.controls[1].controls[1]
        validation_text.value = "✅ Código validado: Incluye documentación, reproducibilidad y buenas prácticas. Puntuación: 95/100"

        # Actualizar métricas
        self.update_quality_metrics(0.95, 0.90, 0.88)
        self.page.update()

    def generate_r_code(self, project_type, seed):
        return f"""# Análisis de {project_type.title()}
# Autor: [Tu nombre]
# Fecha: {datetime.now().strftime('%Y-%m-%d')}
# Versión: 1.0

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

# Limpiar entorno
rm(list = ls())

# Cargar librerías necesarias
library(tidyverse)
library(here)
library(ggplot2)
library(knitr)

# Configurar semilla para reproducibilidad
set.seed({seed})

# Información de la sesión
sessionInfo()

# ============================================
# ESTRUCTURA DE DIRECTORIOS
# ============================================

# Crear directorios si no existen
dirs <- c("data/raw", "data/processed", "scripts", 
          "results/tables", "results/figures", "docs")
sapply(dirs, function(x) dir.create(x, recursive = TRUE, showWarnings = FALSE))

# ============================================
# CARGA Y PREPARACIÓN DE DATOS
# ============================================

# Cargar datos
datos_raw <- read.csv(here("data", "raw", "{project_type}_raw.csv"))

# Documentar estructura inicial
cat("Dimensiones originales:", dim(datos_raw), "\\n")
cat("Variables:", names(datos_raw), "\\n")

# Verificar calidad de datos
missing_summary <- sapply(datos_raw, function(x) sum(is.na(x)))
print(missing_summary)

# ============================================
# ANÁLISIS DESCRIPTIVO
# ============================================

# Estadísticas descriptivas
summary_stats <- datos_raw %>%
  summarise_if(is.numeric, list(
    media = ~mean(., na.rm = TRUE),
    mediana = ~median(., na.rm = TRUE),
    sd = ~sd(., na.rm = TRUE)
  ))

# Guardar resultados
write.csv(summary_stats, here("results", "tables", "estadisticas_descriptivas.csv"))

cat("Flujo de trabajo generado exitosamente!\\n")"""

    def generate_python_code(self, project_type, seed):
        return f'''"""
Análisis de {project_type.title()}
Autor: [Tu nombre]
Fecha: {datetime.now().strftime('%Y-%m-%d')}
Versión: 1.0
"""

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configurar semilla para reproducibilidad
np.random.seed({seed})

# ============================================
# ESTRUCTURA DE DIRECTORIOS
# ============================================

# Crear directorios si no existen
directories = [
    'data/raw', 'data/processed', 'scripts',
    'results/tables', 'results/figures', 'docs'
]

for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)

# ============================================
# CARGA Y PREPARACIÓN DE DATOS
# ============================================

# Cargar datos
datos_raw = pd.read_csv('data/raw/{project_type}_raw.csv')

# Documentar estructura inicial
print(f"Dimensiones originales: {{datos_raw.shape}}")
print(f"Variables: {{list(datos_raw.columns)}}")

# ============================================
# ANÁLISIS DESCRIPTIVO
# ============================================

# Estadísticas descriptivas
summary_stats = datos_raw.describe()
summary_stats.to_csv('results/tables/estadisticas_descriptivas.csv')

print("Flujo de trabajo generado exitosamente!")'''

    def update_quality_metrics(self, doc, repro, practices):
        self.doc_progress.value = doc
        self.repro_progress.value = repro
        self.practices_progress.value = practices

    def show_practice_section(self):
        title = ft.Text("Práctica Guiada: Análisis de Hipertensión", 
                       size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)

        # Dataset
        dataset_table = self.create_dataset_table()

        # Pasos de práctica
        steps = self.create_practice_steps()

        # Gráficos de resultados
        charts = self.create_results_charts()

        # Botón continuar
        continue_btn = ft.Container(
            content=ft.ElevatedButton(
                text="Ir a Evaluación",
                icon=ft.Icons.ASSIGNMENT_TURNED_IN,
                on_click=lambda e: self.show_section("evaluation"),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.RED_500,
                    color=ft.Colors.WHITE,
                    padding=ft.padding.symmetric(horizontal=30, vertical=15)
                )
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=20)
        )

        # Agregar contenido
        self.content_container.content.controls.extend([
            self.create_card(title),
            self.create_card(dataset_table),
            self.create_card(steps),
            self.create_card(charts),
            continue_btn
        ])

    def create_dataset_table(self):
        # Crear tabla de datos
        headers = ["ID", "Edad", "Sexo", "PAS", "PAD", "IMC", "Tratamiento"]
        
        table_rows = [ft.DataRow(cells=[
            ft.DataCell(ft.Text("ID", weight=ft.FontWeight.BOLD)),
            ft.DataCell(ft.Text("Edad", weight=ft.FontWeight.BOLD)),
            ft.DataCell(ft.Text("Sexo", weight=ft.FontWeight.BOLD)),
            ft.DataCell(ft.Text("PAS", weight=ft.FontWeight.BOLD)),
            ft.DataCell(ft.Text("PAD", weight=ft.FontWeight.BOLD)),
            ft.DataCell(ft.Text("IMC", weight=ft.FontWeight.BOLD)),
            ft.DataCell(ft.Text("Tratamiento", weight=ft.FontWeight.BOLD))
        ])]

        for row in self.hypertension_data:
            table_rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(row["id"]))),
                ft.DataCell(ft.Text(str(row["edad"]))),
                ft.DataCell(ft.Text(row["sexo"])),
                ft.DataCell(ft.Text(str(row["pas"]))),
                ft.DataCell(ft.Text(str(row["pad"]))),
                ft.DataCell(ft.Text(str(row["imc"]))),
                ft.DataCell(ft.Text(row["tratamiento"]))
            ]))

        return ft.Column([
            ft.Text("Dataset: Pacientes con Hipertensión", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.DataTable(
                    columns=[ft.DataColumn(ft.Text(h)) for h in headers],
                    rows=table_rows[1:]  # Excluir header row
                ),
                bgcolor=ft.Colors.GREY_50,
                padding=ft.padding.all(15),
                border_radius=8
            )
        ])

    def create_practice_steps(self):
        steps = [
            ("Configuración del Entorno", self.get_step1_code(), ft.Colors.BLUE_500),
            ("Carga y Limpieza de Datos", self.get_step2_code(), ft.Colors.GREEN_500),
            ("Análisis Descriptivo", self.get_step3_code(), ft.Colors.YELLOW_600),
            ("Visualización y Documentación", self.get_step4_code(), ft.Colors.PURPLE_500)
        ]

        step_widgets = []
        for i, (title, code, color) in enumerate(steps):
            step_widget = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text(f"Paso {i+1}", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            bgcolor=color,
                            padding=ft.padding.all(8),
                            border_radius=20
                        ),
                        ft.Text(title, size=16, weight=ft.FontWeight.BOLD, expand=True)
                    ]),
                    ft.Container(
                        content=ft.Text(code, font_family="Courier New", size=10, color=ft.Colors.GREEN_400),
                        bgcolor=ft.Colors.GREY_900,
                        padding=ft.padding.all(15),
                        border_radius=8,
                        height=200
                    ),
                    ft.ElevatedButton(
                        text=f"Ejecutar Paso {i+1}",
                        icon=ft.Icons.PLAY_ARROW,
                        on_click=lambda e, step=i+1: self.execute_practice_step(step),
                        style=ft.ButtonStyle(bgcolor=color, color=ft.Colors.WHITE)
                    )
                ], spacing=10),
                border=ft.border.only(left=ft.border.BorderSide(4, color)),
                padding=ft.padding.only(left=20, top=10, bottom=10, right=10),
                margin=ft.margin.only(bottom=20)
            )
            step_widgets.append(step_widget)

        return ft.Column([
            ft.Text("Pasos de la Práctica", size=18, weight=ft.FontWeight.BOLD),
            ft.Column(step_widgets)
        ])

    def get_step1_code(self):
        return """# Configuración inicial del proyecto
# Autor: [Tu nombre]
# Fecha: 2024-01-15
# Proyecto: Análisis de Hipertensión

# Cargar librerías necesarias
library(tidyverse)
library(here)

# Configurar semilla para reproducibilidad
set.seed(123)

# Crear estructura de carpetas
dir.create("data", showWarnings = FALSE)
dir.create("scripts", showWarnings = FALSE)
dir.create("results", showWarnings = FALSE)
dir.create("figures", showWarnings = FALSE)"""

    def get_step2_code(self):
        return """# Cargar datos
datos <- read.csv(here("data", "hipertension.csv"))

# Documentar la estructura de los datos
cat("Dimensiones del dataset:", dim(datos), "\\n")
cat("Variables:", names(datos), "\\n")

# Verificar valores faltantes
missing_data <- sapply(datos, function(x) sum(is.na(x)))
print(missing_data)

# Limpieza básica
datos_limpios <- datos %>%
  filter(!is.na(PAS), !is.na(PAD)) %>%
  mutate(
    IMC_categoria = case_when(
      IMC < 18.5 ~ "Bajo peso",
      IMC < 25 ~ "Normal",
      IMC < 30 ~ "Sobrepeso",
      TRUE ~ "Obesidad"
    )
  )"""

    def get_step3_code(self):
        return """# Análisis descriptivo
resumen_estadistico <- datos_limpios %>%
  summarise(
    n = n(),
    edad_media = mean(Edad, na.rm = TRUE),
    edad_sd = sd(Edad, na.rm = TRUE),
    pas_media = mean(PAS, na.rm = TRUE),
    pas_sd = sd(PAS, na.rm = TRUE),
    pad_media = mean(PAD, na.rm = TRUE),
    pad_sd = sd(PAD, na.rm = TRUE)
  )

# Análisis por sexo
resumen_por_sexo <- datos_limpios %>%
  group_by(Sexo) %>%
  summarise(
    n = n(),
    pas_media = mean(PAS, na.rm = TRUE),
    pad_media = mean(PAD, na.rm = TRUE)
  )"""

    def get_step4_code(self):
        return """# Crear visualizaciones
library(ggplot2)

# Gráfico de distribución de PAS
p1 <- ggplot(datos_limpios, aes(x = PAS)) +
  geom_histogram(bins = 30, fill = "steelblue", alpha = 0.7) +
  labs(title = "Distribución de Presión Arterial Sistólica",
       x = "PAS (mmHg)", y = "Frecuencia") +
  theme_minimal()

# Crear reporte final
reporte <- paste(
  "# Reporte de Análisis de Hipertensión",
  "## Resumen Ejecutivo",
  paste("- Muestra analizada:", nrow(datos_limpios), "pacientes"),
  paste("- PAS promedio:", round(mean(datos_limpios$PAS), 1), "mmHg"),
  sep = "\\n"
)"""

    def execute_practice_step(self, step):
        # Simular ejecución del paso
        results = {
            1: "✅ Paso 1 Completado\n• Librerías cargadas correctamente\n• Semilla establecida: 123\n• Estructura de carpetas creada",
            2: "✅ Paso 2 Completado\n• Dataset cargado: 1000 observaciones, 7 variables\n• Datos faltantes: 0\n• Variable IMC_categoria creada",
            3: "✅ Paso 3 Completado\n• PAS promedio: 142.3 mmHg (SD: 12.8)\n• PAD promedio: 89.7 mmHg (SD: 8.4)\n• Edad promedio: 48.6 años",
            4: "✅ Paso 4 Completado\n• Gráficos generados y guardados\n• Reporte final creado\n• Proyecto listo para compartir"
        }
        
        # Mostrar resultado en un diálogo
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(f"Resultado Paso {step}"),
            content=ft.Text(results[step]),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()

    def create_results_charts(self):
        # Crear gráfico simple usando matplotlib
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Gráfico 1: Distribución de PAS
        pas_ranges = ['120-129', '130-139', '140-149', '150-159', '160+']
        frequencies = [45, 180, 320, 280, 175]
        ax1.bar(pas_ranges, frequencies, color='steelblue', alpha=0.7)
        ax1.set_title('Distribución de PAS (mmHg)')
        ax1.set_ylabel('Número de pacientes')
        
        # Gráfico 2: Comparación por sexo
        sexes = ['Masculino', 'Femenino']
        pas_means = [144.2, 140.8]
        colors = ['green', 'pink']
        ax2.bar(sexes, pas_means, color=colors, alpha=0.7)
        ax2.set_title('PAS Promedio por Sexo')
        ax2.set_ylabel('PAS (mmHg)')
        ax2.set_ylim(135, 150)
        
        plt.tight_layout()
        
        # Convertir a imagen base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return ft.Column([
            ft.Text("Resultados del Análisis", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Image(src_base64=img_base64, width=600, height=300),
                alignment=ft.alignment.center
            )
        ])

    def show_evaluation_section(self):
        title = ft.Text("Evaluación Automatizada", 
                       size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)

        # Quiz
        quiz_section = self.create_quiz_section()
        
        # Ejercicio práctico
        practical_exercise = self.create_practical_exercise()
        
        # Checklist
        checklist_section = self.create_checklist_section()

        # Botón continuar
        continue_btn = ft.Container(
            content=ft.ElevatedButton(
                text="Acceder a Recursos",
                icon=ft.Icons.DOWNLOAD,
                on_click=lambda e: self.show_section("resources"),
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.ORANGE_500,
                    color=ft.Colors.WHITE,
                    padding=ft.padding.symmetric(horizontal=30, vertical=15)
                )
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=20)
        )

        # Agregar contenido
        self.content_container.content.controls.extend([
            self.create_card(title),
            self.create_card(quiz_section),
            self.create_card(practical_exercise),
            self.create_card(checklist_section),
            continue_btn
        ])

    def create_quiz_section(self):
        questions = [
            {
                "question": "¿Cuál es el propósito principal de establecer una semilla aleatoria en un análisis estadístico?",
                "options": [
                    "Acelerar los cálculos estadísticos",
                    "Garantizar la reproducibilidad de resultados aleatorios",
                    "Mejorar la precisión de las estimaciones",
                    "Reducir el tamaño de los archivos de datos"
                ],
                "correct": 1
            },
            {
                "question": "En el modelo C(H)ANGE, ¿qué componente se relaciona directamente con la organización de archivos y carpetas?",
                "options": ["Álgebra", "Combinatoria", "Geometría", "Números"],
                "correct": 1
            },
            {
                "question": "¿Cuál de las siguientes prácticas NO es esencial para un flujo de trabajo reproducible?",
                "options": [
                    "Documentar todos los pasos del análisis",
                    "Usar siempre el software más reciente disponible",
                    "Mantener un control de versiones del código",
                    "Especificar las versiones de las librerías utilizadas"
                ],
                "correct": 1
            }
        ]

        self.quiz_answers = [None, None, None]
        question_widgets = []

        for i, q in enumerate(questions):
            options_group = ft.RadioGroup(
                content=ft.Column([
                    ft.Radio(value=j, label=option) for j, option in enumerate(q["options"])
                ]),
                on_change=lambda e, idx=i: self.update_quiz_answer(idx, e.control.value)
            )

            question_widget = ft.Container(
                content=ft.Column([
                    ft.Text(f"Pregunta {i+1}: {q['question']}", weight=ft.FontWeight.BOLD, size=14),
                    options_group
                ]),
                bgcolor=ft.Colors.BLUE_50 if i == 0 else ft.Colors.GREEN_50 if i == 1 else ft.Colors.YELLOW_50,
                padding=ft.padding.all(20),
                border_radius=8,
                border=ft.border.only(left=ft.border.BorderSide(4, 
                    ft.Colors.BLUE_500 if i == 0 else ft.Colors.GREEN_500 if i == 1 else ft.Colors.YELLOW_500))
            )
            question_widgets.append(question_widget)

        submit_btn = ft.ElevatedButton(
            text="Enviar Respuestas",
            icon=ft.Icons.CHECK,
            on_click=self.submit_quiz,
            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_500, color=ft.Colors.WHITE)
        )

        self.quiz_results = ft.Container(visible=False)

        return ft.Column([
            ft.Text("Quiz de Conocimientos", size=18, weight=ft.FontWeight.BOLD),
            ft.Column(question_widgets, spacing=15),
            submit_btn,
            self.quiz_results
        ], spacing=15)

    def update_quiz_answer(self, question_idx, answer):
        self.quiz_answers[question_idx] = int(answer) if answer is not None else None

    def submit_quiz(self, e):
        correct_answers = [1, 1, 1]  # Índices de respuestas correctas
        score = sum(1 for i, answer in enumerate(self.quiz_answers) 
                   if answer == correct_answers[i])
        
        percentage = int((score / len(correct_answers)) * 100)
        
        color = ft.Colors.GREEN_50 if score == 3 else ft.Colors.YELLOW_50 if score >= 2 else ft.Colors.RED_50
        border_color = ft.Colors.GREEN_500 if score == 3 else ft.Colors.YELLOW_500 if score >= 2 else ft.Colors.RED_500
        
        feedback = "¡Excelente! Dominas los conceptos de reproducibilidad." if score == 3 else \
                  "Buen trabajo. Revisa los conceptos que fallaste." if score >= 2 else \
                  "Necesitas repasar los conceptos fundamentales."

        self.quiz_results.content = ft.Container(
            content=ft.Column([
                ft.Text(f"Resultado: {percentage}% ({score}/3 correctas)", 
                       weight=ft.FontWeight.BOLD, size=16),
                ft.Text(feedback, size=14, color=ft.Colors.GREY_700)
            ]),
            bgcolor=color,
            padding=ft.padding.all(20),
            border_radius=8,
            border=ft.border.only(left=ft.border.BorderSide(4, border_color))
        )
        self.quiz_results.visible = True
        self.page.update()

    def create_practical_exercise(self):
        self.user_code = ft.TextField(
            label="Tu código:",
            multiline=True,
            min_lines=10,
            max_lines=15,
            hint_text="# Escribe tu script aquí...\n# Incluye: comentarios, semilla, carga de librerías, etc."
        )

        validate_btn = ft.ElevatedButton(
            text="Validar con IA",
            icon=ft.Icons.SMART_TOY,
            on_click=self.validate_user_code,
            style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_500, color=ft.Colors.WHITE)
        )

        self.code_validation_result = ft.Container(visible=False)

        return ft.Column([
            ft.Text("Ejercicio Práctico: Crear Script Reproducible", size=18, weight=ft.FontWeight.BOLD),
            ft.Text("Escribe un script en R o Python que incluya los elementos esenciales para la reproducibilidad:",
                   size=14, color=ft.Colors.GREY_700),
            self.user_code,
            validate_btn,
            self.code_validation_result
        ], spacing=15)

    def validate_user_code(self, e):
        code = self.user_code.value or ""
        score = 0
        feedback = []

        # Verificar elementos clave
        if "set.seed" in code or "np.random.seed" in code:
            score += 20
            feedback.append("✅ Semilla aleatoria establecida")
        else:
            feedback.append("❌ Falta establecer semilla aleatoria")

        if "#" in code or '"""' in code or "'''" in code:
            score += 20
            feedback.append("✅ Código documentado con comentarios")
        else:
            feedback.append("❌ Falta documentación en el código")

        if "library" in code or "import" in code:
            score += 20
            feedback.append("✅ Librerías cargadas correctamente")
        else:
            feedback.append("❌ No se cargan librerías necesarias")

        if any(word in code.lower() for word in ["author", "autor", "fecha", "date"]):
            score += 20
            feedback.append("✅ Metadatos del proyecto incluidos")
        else:
            feedback.append("❌ Faltan metadatos (autor, fecha, etc.)")

        if "dir.create" in code or "mkdir" in code or "Path" in code:
            score += 20
            feedback.append("✅ Estructura de directorios definida")
        else:
            feedback.append("❌ No se define estructura de directorios")

        color = ft.Colors.GREEN_50 if score >= 80 else ft.Colors.YELLOW_50 if score >= 60 else ft.Colors.RED_50
        border_color = ft.Colors.GREEN_500 if score >= 80 else ft.Colors.YELLOW_500 if score >= 60 else ft.Colors.RED_500

        final_feedback = "Excelente código reproducible!" if score >= 80 else \
                        "Buen código, pero puede mejorar." if score >= 60 else \
                        "El código necesita más elementos de reproducibilidad."

        self.code_validation_result.content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SMART_TOY, color=border_color.replace("_50", "_600")),
                    ft.Text(f"Validación IA - Puntuación: {score}/100", weight=ft.FontWeight.BOLD)
                ]),
                ft.Column([ft.Text(f, size=12) for f in feedback]),
                ft.Text(final_feedback, size=14, color=ft.Colors.GREY_700, weight=ft.FontWeight.BOLD)
            ]),
            bgcolor=color,
            padding=ft.padding.all(15),
            border_radius=8,
            border=ft.border.only(left=ft.border.BorderSide(4, border_color))
        )
        self.code_validation_result.visible = True
        self.page.update()

    def create_checklist_section(self):
        checklist_items = [
            "Estructura de carpetas organizada",
            "Código bien documentado", 
            "Semilla aleatoria establecida",
            "Versiones de software especificadas",
            "Datos de entrada documentados",
            "Resultados guardados sistemáticamente",
            "README con instrucciones claras",
            "Control de versiones implementado"
        ]

        self.checklist_checkboxes = []
        checkbox_widgets = []

        for i, item in enumerate(checklist_items):
            checkbox = ft.Checkbox(
                label=item,
                on_change=self.update_checklist_progress
            )
            self.checklist_checkboxes.append(checkbox)
            checkbox_widgets.append(checkbox)

        # Dividir en dos columnas
        col1 = ft.Column(checkbox_widgets[:4], spacing=10)
        col2 = ft.Column(checkbox_widgets[4:], spacing=10)

        self.checklist_score_text = ft.Text("0/8 completado", size=20, weight=ft.FontWeight.BOLD)
        self.checklist_progress_bar = ft.ProgressBar(value=0, color=ft.Colors.GREEN_500)

        return ft.Column([
            ft.Text("Checklist de Verificación", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([
                    ft.Row([col1, col2], spacing=30),
                    ft.Container(
                        content=ft.Column([
                            self.checklist_score_text,
                            self.checklist_progress_bar
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        margin=ft.margin.only(top=20)
                    )
                ]),
                bgcolor=ft.Colors.GREEN_50,
                padding=ft.padding.all(20),
                border_radius=8
            )
        ], spacing=15)

    def update_checklist_progress(self, e):
        completed = sum(1 for cb in self.checklist_checkboxes if cb.value)
        total = len(self.checklist_checkboxes)
        
        self.checklist_score_text.value = f"{completed}/{total} completado"
        self.checklist_progress_bar.value = completed / total
        self.page.update()

    def show_resources_section(self):
        title = ft.Text("Recursos Descargables", 
                       size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)

        # Plantillas y guías
        templates_section = self.create_templates_section()
        
        # Datasets
        datasets_section = self.create_datasets_section()
        
        # Actividad de transferencia
        transfer_activity = self.create_transfer_activity()
        
        # Certificación
        certification = self.create_certification_section()

        # Agregar contenido
        self.content_container.content.controls.extend([
            self.create_card(title),
            self.create_card(ft.Row([templates_section, datasets_section], spacing=20)),
            self.create_card(transfer_activity),
            certification
        ])

    def create_templates_section(self):
        templates = [
            ("Plantilla de Script R", "Estructura básica para análisis reproducible", ft.Colors.BLUE_500, "r-template"),
            ("Plantilla de Script Python", "Estructura básica para análisis con pandas", ft.Colors.GREEN_500, "python-template"),
            ("Checklist de Reproducibilidad", "Lista de verificación completa", ft.Colors.YELLOW_600, "checklist"),
            ("Guía de Estructura de Carpetas", "Organización recomendada para proyectos", ft.Colors.PURPLE_500, "folder-guide")
        ]

        template_widgets = []
        for title, description, color, resource_id in templates:
            widget = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(title, weight=ft.FontWeight.BOLD, size=14),
                        ft.Text(description, size=12, color=ft.Colors.GREY_600)
                    ], expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DOWNLOAD,
                        bgcolor=color,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e, rid=resource_id: self.download_resource(rid)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=color.replace("500", "50").replace("600", "50"),
                padding=ft.padding.all(15),
                border_radius=8,
                border=ft.border.only(left=ft.border.BorderSide(4, color)),
                margin=ft.margin.only(bottom=10)
            )
            template_widgets.append(widget)

        return ft.Column([
            ft.Text("Plantillas y Guías", size=18, weight=ft.FontWeight.BOLD),
            ft.Column(template_widgets)
        ], expand=True)

    def create_datasets_section(self):
        datasets = [
            ("Dataset Hipertensión", "1000 pacientes con variables clínicas", ft.Colors.RED_500, "hypertension-data"),
            ("Dataset Diabetes", "Datos de seguimiento de pacientes diabéticos", ft.Colors.INDIGO_500, "diabetes-data"),
            ("Dataset COVID-19", "Datos epidemiológicos simulados", ft.Colors.PINK_500, "covid-data"),
            ("Diccionario de Datos", "Descripción de todas las variables", ft.Colors.TEAL_500, "data-dictionary")
        ]

        dataset_widgets = []
        for title, description, color, resource_id in datasets:
            widget = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(title, weight=ft.FontWeight.BOLD, size=14),
                        ft.Text(description, size=12, color=ft.Colors.GREY_600)
                    ], expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DOWNLOAD,
                        bgcolor=color,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e, rid=resource_id: self.download_resource(rid)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                bgcolor=color.replace("500", "50"),
                padding=ft.padding.all(15),
                border_radius=8,
                border=ft.border.only(left=ft.border.BorderSide(4, color)),
                margin=ft.margin.only(bottom=10)
            )
            dataset_widgets.append(widget)

        return ft.Column([
            ft.Text("Datasets de Práctica", size=18, weight=ft.FontWeight.BOLD),
            ft.Column(dataset_widgets)
        ], expand=True)

    def download_resource(self, resource_id):
        resources = {
            "r-template": {
                "filename": "template_analysis.R",
                "content": """# Plantilla de Análisis Estadístico en R
# Autor: [Tu nombre]
# Fecha: [Fecha]
# Proyecto: [Nombre del proyecto]

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

# Limpiar entorno
rm(list = ls())

# Cargar librerías
library(tidyverse)
library(here)

# Configurar semilla
set.seed(123)

# ============================================
# CARGA DE DATOS
# ============================================

# Cargar datos
datos <- read.csv(here("data", "raw", "datos.csv"))

# Verificar estructura
str(datos)
summary(datos)

# ============================================
# ANÁLISIS
# ============================================

# Tu análisis aquí...

# ============================================
# RESULTADOS
# ============================================

# Guardar resultados
# write.csv(resultados, here("results", "resultados.csv"))

cat("Análisis completado exitosamente!\\n")"""
            },
            "python-template": {
                "filename": "template_analysis.py",
                "content": '''"""
Plantilla de Análisis Estadístico en Python
Autor: [Tu nombre]
Fecha: [Fecha]
Proyecto: [Nombre del proyecto]
"""

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configurar semilla
np.random.seed(123)

# ============================================
# CARGA DE DATOS
# ============================================

# Cargar datos
datos = pd.read_csv('data/raw/datos.csv')

# Verificar estructura
print(datos.info())
print(datos.describe())

# ============================================
# ANÁLISIS
# ============================================

# Tu análisis aquí...

# ============================================
# RESULTADOS
# ============================================

# Guardar resultados
# datos.to_csv('results/resultados.csv', index=False)

print("Análisis completado exitosamente!")'''
            }
        }

        resource = resources.get(resource_id)
        if resource:
            # Crear archivo y guardarlo
            try:
                with open(resource["filename"], "w", encoding="utf-8") as f:
                    f.write(resource["content"])
                
                # Mostrar confirmación
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Archivo {resource['filename']} descargado exitosamente"),
                    bgcolor=ft.Colors.GREEN_500
                )
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as e:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Error al descargar: {str(e)}"),
                    bgcolor=ft.Colors.RED_500
                )
                self.page.snack_bar.open = True
                self.page.update()

    def create_transfer_activity(self):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ROCKET_LAUNCH, color=ft.Colors.ORANGE_600),
                    ft.Text("Proyecto Final: Miniinforme Reproducible", 
                           size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800)
                ]),
                ft.Row([
                    ft.Column([
                        ft.Text("Instrucciones:", weight=ft.FontWeight.BOLD, size=14),
                        ft.Text("• Selecciona uno de los datasets proporcionados", size=12),
                        ft.Text("• Crea un flujo de trabajo reproducible completo", size=12),
                        ft.Text("• Incluye análisis descriptivo y visualizaciones", size=12),
                        ft.Text("• Documenta todo el proceso paso a paso", size=12),
                        ft.Text("• Genera un informe final con interpretación clínica", size=12)
                    ], expand=True),
                    ft.Column([
                        ft.Text("Criterios de Evaluación:", weight=ft.FontWeight.BOLD, size=14),
                        ft.Text("• Reproducibilidad (25%)", size=12),
                        ft.Text("• Documentación (25%)", size=12),
                        ft.Text("• Análisis estadístico (25%)", size=12),
                        ft.Text("• Interpretación clínica (25%)", size=12)
                    ], expand=True)
                ], spacing=30),
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Iniciar Proyecto Final",
                        icon=ft.Icons.ROCKET_LAUNCH,
                        on_click=self.start_transfer_activity,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.ORANGE_500,
                            color=ft.Colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=15)
                        )
                    ),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(top=20)
                )
            ]),
            bgcolor=ft.Colors.ORANGE_50,
            padding=ft.padding.all(20),
            border_radius=8,
            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.ORANGE_500))
        )

    def start_transfer_activity(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Proyecto Final"),
            content=ft.Text("¡Excelente! La actividad de transferencia te permitirá aplicar todo lo aprendido en un proyecto real. Selecciona un dataset y crea tu flujo de trabajo reproducible completo."),
            actions=[ft.TextButton("Entendido", on_click=lambda e: self.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()

    def create_certification_section(self):
        return ft.Container(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.WORKSPACE_PREMIUM, size=60, color=ft.Colors.GREEN_600),
                    ft.Text("¡Felicitaciones!", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Has completado la OVA 16: Flujo de Trabajo Reproducible", 
                           text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton(
                        text="Generar Certificado",
                        icon=ft.Icons.WORKSPACE_PREMIUM,
                        on_click=self.generate_certificate,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_500,
                            color=ft.Colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=15)
                        )
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                bgcolor=ft.Colors.GREEN_50,
                padding=ft.padding.all(40),
                border_radius=12,
                border=ft.border.all(2, ft.Colors.GREEN_300)
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=30)
        )

    def generate_certificate(self, e):
        # Crear certificado simple
        certificate_content = f"""
CERTIFICADO DE COMPLETACIÓN

OVA 16: Flujo de Trabajo Reproducible
Estadística para Ciencias de la Salud

[Tu Nombre]

Ha completado exitosamente el módulo de aprendizaje sobre
flujo de trabajo reproducible en estadística aplicada
a las ciencias de la salud usando el modelo C(H)ANGE

Fecha: {datetime.now().strftime('%Y-%m-%d')}

Universidad Antonio Nariño
"""
        
        try:
            with open("certificado_ova16.txt", "w", encoding="utf-8") as f:
                f.write(certificate_content)
            
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Certificado generado: certificado_ova16.txt"),
                bgcolor=ft.Colors.GREEN_500
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error al generar certificado: {str(e)}"),
                bgcolor=ft.Colors.RED_500
            )
            self.page.snack_bar.open = True
            self.page.update()

def main(page: ft.Page):
    app = OVAApp()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
