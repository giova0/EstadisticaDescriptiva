
import flet as ft
import math
import random
import time
from datetime import datetime

class OVAApp:
    def __init__(self):
        self.current_module = "intro"
        self.progress = 0
        self.quiz_answers = {}
        self.chat_messages = []
        
    def main(self, page: ft.Page):
        page.title = "OVA: Tablas de Frecuencias y Resúmenes Categóricos"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1200
        page.window_height = 800
        page.window_resizable = True
        page.scroll = ft.ScrollMode.AUTO
        
        # Colores del tema
        self.colors = {
            'primary': ft.colors.BLUE_900,
            'secondary': ft.colors.BLUE_600,
            'success': ft.colors.GREEN_600,
            'warning': ft.colors.ORANGE_600,
            'danger': ft.colors.RED_600,
            'info': ft.colors.CYAN_600,
            'light': ft.colors.GREY_100,
            'dark': ft.colors.GREY_800
        }
        
        # Barra de progreso
        self.progress_bar = ft.ProgressBar(
            width=200,
            color=ft.colors.GREEN_400,
            bgcolor=ft.colors.BLUE_700,
            value=0
        )
        
        self.progress_text = ft.Text("0% completado", size=12, color=ft.colors.WHITE)
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(
                        "OVA: Tablas de Frecuencias y Resúmenes Categóricos",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE
                    ),
                    ft.Text(
                        "Estadística Descriptiva para Ciencias de la Salud - Modelo C(H)ANGE",
                        size=14,
                        color=ft.colors.BLUE_200
                    )
                ], expand=True),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Progreso del OVA", size=12, color=ft.colors.WHITE),
                        self.progress_bar,
                        self.progress_text
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.BLUE_800,
                    padding=10,
                    border_radius=8
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=self.colors['primary'],
            padding=20,
            margin=ft.margin.only(bottom=10)
        )
        
        # Navegación
        self.nav_buttons = []
        nav_items = [
            ("intro", "Introducción", ft.icons.PLAY_CIRCLE),
            ("theory", "Teoría", ft.icons.BOOK),
            ("practice", "Práctica", ft.icons.CALCULATE),
            ("ai_assistant", "Asistente IA", ft.icons.SMART_TOY),
            ("evaluation", "Evaluación", ft.icons.QUIZ),
            ("resources", "Recursos", ft.icons.DOWNLOAD)
        ]
        
        for module_id, title, icon in nav_items:
            btn = ft.ElevatedButton(
                text=title,
                icon=icon,
                on_click=lambda e, mid=module_id: self.show_module(page, mid),
                style=ft.ButtonStyle(
                    bgcolor=self.colors['secondary'] if module_id == "intro" else ft.colors.GREY_200,
                    color=ft.colors.WHITE if module_id == "intro" else ft.colors.GREY_700
                )
            )
            self.nav_buttons.append((module_id, btn))
        
        navigation = ft.Container(
            content=ft.Row(
                [btn for _, btn in self.nav_buttons],
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True
            ),
            bgcolor=ft.colors.WHITE,
            padding=10,
            margin=ft.margin.only(bottom=10),
            border_radius=8,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.GREY_300)
        )
        
        # Contenedor principal para módulos
        self.main_content = ft.Container(
            content=self.create_intro_module(page),
            expand=True
        )
        
        # Layout principal
        page.add(
            ft.Column([
                header,
                navigation,
                self.main_content
            ], expand=True)
        )
        
        self.update_progress(page)
    
    def show_module(self, page, module_id):
        self.current_module = module_id
        
        # Actualizar botones de navegación
        for mid, btn in self.nav_buttons:
            if mid == module_id:
                btn.style = ft.ButtonStyle(
                    bgcolor=self.colors['secondary'],
                    color=ft.colors.WHITE
                )
            else:
                btn.style = ft.ButtonStyle(
                    bgcolor=ft.colors.GREY_200,
                    color=ft.colors.GREY_700
                )
        
        # Mostrar módulo correspondiente
        if module_id == "intro":
            self.main_content.content = self.create_intro_module(page)
        elif module_id == "theory":
            self.main_content.content = self.create_theory_module(page)
        elif module_id == "practice":
            self.main_content.content = self.create_practice_module(page)
        elif module_id == "ai_assistant":
            self.main_content.content = self.create_ai_module(page)
        elif module_id == "evaluation":
            self.main_content.content = self.create_evaluation_module(page)
        elif module_id == "resources":
            self.main_content.content = self.create_resources_module(page)
        
        self.update_progress(page)
        page.update()
    
    def update_progress(self, page):
        modules = ["intro", "theory", "practice", "ai_assistant", "evaluation", "resources"]
        current_index = modules.index(self.current_module)
        self.progress = (current_index + 1) / len(modules)
        
        self.progress_bar.value = self.progress
        self.progress_text.value = f"{int(self.progress * 100)}% completado"
        page.update()
    
    def create_intro_module(self, page):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(ft.icons.BAR_CHART, size=60, color=self.colors['secondary']),
                            bgcolor=ft.colors.BLUE_50,
                            width=80,
                            height=80,
                            border_radius=40,
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(bottom=20)
                        ),
                        ft.Text(
                            "Bienvenido al OVA",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "Aprende a construir y analizar tablas de frecuencias para variables categóricas en el contexto de las ciencias de la salud, utilizando el modelo pedagógico C(H)ANGE e inteligencia artificial.",
                            size=16,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.colors.GREY_600
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    margin=ft.margin.only(bottom=30)
                ),
                
                ft.Row([
                    # Objetivos de Aprendizaje
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.icons.TARGET_OUTLINED, color=self.colors['secondary']),
                                ft.Text("Objetivos de Aprendizaje", size=18, weight=ft.FontWeight.BOLD)
                            ]),
                            ft.Column([
                                self.create_objective_item("Construir tablas de frecuencias claras para variables cualitativas"),
                                self.create_objective_item("Calcular proporciones, tasas e intervalos de confianza simples"),
                                self.create_objective_item("Aplicar buenas prácticas de presentación de datos categóricos"),
                                self.create_objective_item("Interpretar resultados en contextos clínicos y epidemiológicos")
                            ])
                        ]),
                        bgcolor=ft.colors.BLUE_50,
                        padding=20,
                        border_radius=10,
                        expand=True
                    ),
                    
                    # Modelo C(H)ANGE
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.icons.EXTENSION, color=ft.colors.PURPLE_600),
                                ft.Text("Modelo C(H)ANGE", size=18, weight=ft.FontWeight.BOLD)
                            ]),
                            ft.Column([
                                ft.Text("Combinatoria: Conteo y clasificación de casos", size=12),
                                ft.Text("Herramientas: IA para análisis automatizado", size=12),
                                ft.Text("Algebra: Cálculos de proporciones y tasas", size=12),
                                ft.Text("Números: Interpretación numérica de frecuencias", size=12),
                                ft.Text("Geometría: Visualización gráfica de datos", size=12),
                                ft.Text("Estadística: Análisis descriptivo categórico", size=12)
                            ])
                        ]),
                        bgcolor=ft.colors.PURPLE_50,
                        padding=20,
                        border_radius=10,
                        expand=True
                    )
                ], spacing=20),
                
                # Caso Clínico
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.LIGHTBULB, color=ft.colors.ORANGE_600),
                            ft.Text("Caso Clínico Motivador", size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        ft.Text(
                            "El Hospital San Rafael necesita analizar los tipos de consulta en urgencias durante el último mes. De 1,250 pacientes atendidos, se registraron diferentes categorías diagnósticas. ¿Cómo organizarías esta información para presentarla al comité médico?",
                            size=14
                        )
                    ]),
                    bgcolor=ft.colors.YELLOW_50,
                    padding=20,
                    border_radius=10,
                    border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400)),
                    margin=ft.margin.only(top=20, bottom=20)
                ),
                
                # Botón continuar
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Comenzar con la Teoría",
                        icon=ft.icons.ARROW_FORWARD,
                        on_click=lambda e: self.show_module(page, "theory"),
                        style=ft.ButtonStyle(
                            bgcolor=self.colors['secondary'],
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=15)
                        )
                    ),
                    alignment=ft.alignment.center
                )
            ], scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_300)
        )
    
    def create_objective_item(self, text):
        return ft.Row([
            ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN_500, size=16),
            ft.Text(text, size=12, expand=True)
        ], spacing=5)
    
    def create_theory_module(self, page):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.BOOK, color=self.colors['secondary'], size=30),
                    ft.Text("Fundamentos Teóricos", size=28, weight=ft.FontWeight.BOLD)
                ]),
                
                # Variables Categóricas
                ft.Container(
                    content=ft.Column([
                        ft.Text("1. Variables Categóricas en Salud", size=20, weight=ft.FontWeight.BOLD, color=self.colors['secondary']),
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Variables Nominales", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Text("• Tipo sanguíneo (A, B, AB, O)", size=12),
                                    ft.Text("• Diagnóstico principal", size=12),
                                    ft.Text("• Método anticonceptivo", size=12),
                                    ft.Text("• Región anatómica afectada", size=12)
                                ]),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Variables Ordinales", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Text("• Grado de dolor (leve, moderado, severo)", size=12),
                                    ft.Text("• Estadio del cáncer (I, II, III, IV)", size=12),
                                    ft.Text("• Nivel socioeconómico", size=12),
                                    ft.Text("• Grado de satisfacción del paciente", size=12)
                                ]),
                                expand=True
                            )
                        ])
                    ]),
                    bgcolor=ft.colors.BLUE_50,
                    padding=20,
                    border_radius=10,
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Tabla de Frecuencias
                ft.Container(
                    content=ft.Column([
                        ft.Text("2. Construcción de Tablas de Frecuencias", size=20, weight=ft.FontWeight.BOLD, color=self.colors['success']),
                        ft.Text("Ejemplo: Tipos de Consulta en Urgencias", size=16, weight=ft.FontWeight.BOLD),
                        
                        # Tabla ejemplo
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("Tipo de Consulta", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Frecuencia (n)", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Proporción (%)", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("IC 95%", weight=ft.FontWeight.BOLD))
                            ],
                            rows=[
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text("Trauma")),
                                    ft.DataCell(ft.Text("425")),
                                    ft.DataCell(ft.Text("34.0%")),
                                    ft.DataCell(ft.Text("(31.4% - 36.7%)"))
                                ]),
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text("Cardiovascular")),
                                    ft.DataCell(ft.Text("313")),
                                    ft.DataCell(ft.Text("25.0%")),
                                    ft.DataCell(ft.Text("(22.7% - 27.5%)"))
                                ]),
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text("Respiratorio")),
                                    ft.DataCell(ft.Text("250")),
                                    ft.DataCell(ft.Text("20.0%")),
                                    ft.DataCell(ft.Text("(17.9% - 22.3%)"))
                                ]),
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text("Gastrointestinal")),
                                    ft.DataCell(ft.Text("138")),
                                    ft.DataCell(ft.Text("11.0%")),
                                    ft.DataCell(ft.Text("(9.4% - 12.9%)"))
                                ]),
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text("Otros")),
                                    ft.DataCell(ft.Text("124")),
                                    ft.DataCell(ft.Text("10.0%")),
                                    ft.DataCell(ft.Text("(8.4% - 11.8%)"))
                                ]),
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text("Total", weight=ft.FontWeight.BOLD)),
                                    ft.DataCell(ft.Text("1,250", weight=ft.FontWeight.BOLD)),
                                    ft.DataCell(ft.Text("100.0%", weight=ft.FontWeight.BOLD)),
                                    ft.DataCell(ft.Text("-", weight=ft.FontWeight.BOLD))
                                ])
                            ]
                        ),
                        
                        # Conceptos clave
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Frecuencia Absoluta", weight=ft.FontWeight.BOLD, color=self.colors['secondary']),
                                    ft.Text("Número de casos en cada categoría", size=12),
                                    ft.Text("Ejemplo: 425 casos de trauma", size=10, color=ft.colors.GREY_600)
                                ]),
                                bgcolor=ft.colors.BLUE_100,
                                padding=15,
                                border_radius=8,
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Proporción", weight=ft.FontWeight.BOLD, color=self.colors['success']),
                                    ft.Text("Frecuencia relativa expresada como porcentaje", size=12),
                                    ft.Text("Fórmula: (n/N) × 100", size=10, color=ft.colors.GREY_600)
                                ]),
                                bgcolor=ft.colors.GREEN_100,
                                padding=15,
                                border_radius=8,
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Intervalo de Confianza", weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                                    ft.Text("Rango de valores plausibles para la proporción", size=12),
                                    ft.Text("IC 95% = p ± 1.96√(p(1-p)/n)", size=10, color=ft.colors.GREY_600)
                                ]),
                                bgcolor=ft.colors.PURPLE_100,
                                padding=15,
                                border_radius=8,
                                expand=True
                            )
                        ], spacing=10)
                    ]),
                    bgcolor=ft.colors.GREEN_50,
                    padding=20,
                    border_radius=10,
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Buenas Prácticas
                ft.Container(
                    content=ft.Column([
                        ft.Text("3. Buenas Prácticas de Presentación", size=20, weight=ft.FontWeight.BOLD, color=self.colors['warning']),
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("✓ Recomendaciones", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700),
                                    ft.Text("• Ordenar categorías lógicamente", size=12),
                                    ft.Text("• Incluir totales y verificar suma 100%", size=12),
                                    ft.Text("• Reportar intervalos de confianza", size=12),
                                    ft.Text("• Usar títulos descriptivos", size=12),
                                    ft.Text("• Especificar criterios de inclusión", size=12),
                                    ft.Text("• Manejar valores perdidos apropiadamente", size=12)
                                ]),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("✗ Errores Comunes", weight=ft.FontWeight.BOLD, color=ft.colors.RED_700),
                                    ft.Text("• Categorías superpuestas o ambiguas", size=12),
                                    ft.Text("• Omitir información sobre datos faltantes", size=12),
                                    ft.Text("• Usar demasiadas categorías pequeñas", size=12),
                                    ft.Text("• No especificar el período de estudio", size=12),
                                    ft.Text("• Presentar solo frecuencias absolutas", size=12),
                                    ft.Text("• Ignorar la precisión de las estimaciones", size=12)
                                ]),
                                expand=True
                            )
                        ])
                    ]),
                    bgcolor=ft.colors.ORANGE_50,
                    padding=20,
                    border_radius=10,
                    margin=ft.margin.only(bottom=20)
                ),
                
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Continuar con la Práctica",
                        icon=ft.icons.ARROW_FORWARD,
                        on_click=lambda e: self.show_module(page, "practice"),
                        style=ft.ButtonStyle(
                            bgcolor=self.colors['success'],
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=15)
                        )
                    ),
                    alignment=ft.alignment.center
                )
            ], scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_300)
        )
    
    def create_practice_module(self, page):
        # Campos para la calculadora
        self.variable_name_field = ft.TextField(
            label="Nombre de la Variable",
            hint_text="Ej: Tipo de Diagnóstico",
            width=300
        )
        
        self.data_input_field = ft.TextField(
            label="Categorías y Frecuencias",
            hint_text="Formato: Categoría,Frecuencia\nDiabetes,45\nHipertensión,67",
            multiline=True,
            min_lines=6,
            max_lines=10,
            width=300
        )
        
        self.result_container = ft.Container(
            content=ft.Text("Los resultados aparecerán aquí...", color=ft.colors.GREY_500),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_300),
            width=400,
            height=300
        )
        
        # Campos para el ejercicio
        self.hypertension_field = ft.TextField(
            label="Proporción de hipertensión (%)",
            hint_text="Ej: 57.0",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.most_frequent_dropdown = ft.Dropdown(
            label="Comorbilidad más frecuente",
            width=200,
            options=[
                ft.dropdown.Option("hipertension", "Hipertensión"),
                ft.dropdown.Option("dislipidemia", "Dislipidemia"),
                ft.dropdown.Option("nefropatia", "Nefropatía"),
                ft.dropdown.Option("retinopatia", "Retinopatía")
            ]
        )
        
        self.exercise_feedback = ft.Container(visible=False)
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.CALCULATE, color=self.colors['success'], size=30),
                    ft.Text("Práctica Interactiva", size=28, weight=ft.FontWeight.BOLD)
                ]),
                
                # Calculadora de Tablas de Frecuencias
                ft.Container(
                    content=ft.Column([
                        ft.Text("Calculadora de Tablas de Frecuencias", size=20, weight=ft.FontWeight.BOLD, color=self.colors['secondary']),
                        ft.Row([
                            ft.Column([
                                ft.Text("Ingresa los Datos", size=16, weight=ft.FontWeight.BOLD),
                                self.variable_name_field,
                                self.data_input_field,
                                ft.ElevatedButton(
                                    text="Calcular Tabla",
                                    icon=ft.icons.CALCULATE,
                                    on_click=lambda e: self.calculate_frequency_table(page),
                                    style=ft.ButtonStyle(
                                        bgcolor=self.colors['secondary'],
                                        color=ft.colors.WHITE
                                    )
                                )
                            ]),
                            ft.Column([
                                ft.Text("Resultado", size=16, weight=ft.FontWeight.BOLD),
                                self.result_container
                            ])
                        ])
                    ]),
                    bgcolor=ft.colors.BLUE_50,
                    padding=20,
                    border_radius=10,
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Ejercicio Interactivo
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ejercicio: Análisis de Comorbilidades", size=20, weight=ft.FontWeight.BOLD, color=self.colors['success']),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Escenario Clínico", size=16, weight=ft.FontWeight.BOLD),
                                ft.Text("En un estudio de 500 pacientes diabéticos, se registraron las siguientes comorbilidades principales:", size=14),
                                
                                ft.Row([
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Datos del estudio:", weight=ft.FontWeight.BOLD),
                                            ft.Text("• Hipertensión: 285 pacientes", size=12),
                                            ft.Text("• Dislipidemia: 190 pacientes", size=12),
                                            ft.Text("• Nefropatía: 95 pacientes", size=12),
                                            ft.Text("• Retinopatía: 75 pacientes", size=12),
                                            ft.Text("• Sin comorbilidades: 55 pacientes", size=12)
                                        ]),
                                        bgcolor=ft.colors.GREY_100,
                                        padding=15,
                                        border_radius=8,
                                        expand=True
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Tu tarea:", weight=ft.FontWeight.BOLD),
                                            ft.Text("1. Calcular las proporciones", size=12),
                                            ft.Text("2. Determinar intervalos de confianza", size=12),
                                            ft.Text("3. Interpretar los resultados", size=12),
                                            ft.Text("4. Identificar la comorbilidad más frecuente", size=12)
                                        ]),
                                        bgcolor=ft.colors.BLUE_50,
                                        padding=15,
                                        border_radius=8,
                                        expand=True
                                    )
                                ]),
                                
                                ft.Row([
                                    self.hypertension_field,
                                    self.most_frequent_dropdown
                                ]),
                                
                                ft.ElevatedButton(
                                    text="Verificar Respuestas",
                                    icon=ft.icons.CHECK,
                                    on_click=lambda e: self.check_exercise_answers(page),
                                    style=ft.ButtonStyle(
                                        bgcolor=self.colors['success'],
                                        color=ft.colors.WHITE
                                    )
                                ),
                                
                                self.exercise_feedback
                            ]),
                            bgcolor=ft.colors.WHITE,
                            padding=20,
                            border_radius=8,
                            border=ft.border.all(1, ft.colors.GREY_300)
                        )
                    ]),
                    bgcolor=ft.colors.GREEN_50,
                    padding=20,
                    border_radius=10,
                    margin=ft.margin.only(bottom=20)
                ),
                
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Explorar Asistente IA",
                        icon=ft.icons.ARROW_FORWARD,
                        on_click=lambda e: self.show_module(page, "ai_assistant"),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.PURPLE_600,
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=15)
                        )
                    ),
                    alignment=ft.alignment.center
                )
            ], scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_300)
        )
    
    def calculate_frequency_table(self, page):
        variable_name = self.variable_name_field.value
        data_input = self.data_input_field.value
        
        if not variable_name or not data_input:
            self.result_container.content = ft.Text("Por favor, completa todos los campos.", color=ft.colors.RED_500)
            page.update()
            return
        
        try:
            lines = data_input.strip().split('\n')
            data = []
            total = 0
            
            for line in lines:
                if ',' in line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        category = parts[0].strip()
                        frequency = int(parts[1].strip())
                        data.append({'category': category, 'frequency': frequency})
                        total += frequency
            
            if not data:
                raise ValueError('No se encontraron datos válidos')
            
            # Calcular proporciones e intervalos de confianza
            for item in data:
                item['proportion'] = (item['frequency'] / total) * 100
                p = item['frequency'] / total
                se = math.sqrt(p * (1 - p) / total)
                margin = 1.96 * se
                item['ci_lower'] = max(0, (p - margin) * 100)
                item['ci_upper'] = min(100, (p + margin) * 100)
            
            # Crear tabla de resultados
            table_rows = []
            for item in data:
                table_rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(item['category'])),
                        ft.DataCell(ft.Text(str(item['frequency']))),
                        ft.DataCell(ft.Text(f"{item['proportion']:.1f}%")),
                        ft.DataCell(ft.Text(f"({item['ci_lower']:.1f}% - {item['ci_upper']:.1f}%)"))
                    ])
                )
            
            table_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Total", weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(str(total), weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text("100.0%", weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text("-", weight=ft.FontWeight.BOLD))
                ])
            )
            
            result_table = ft.Column([
                ft.Text(f"Tabla de Frecuencias: {variable_name}", weight=ft.FontWeight.BOLD),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Categoría", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("n", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("%", weight=ft.FontWeight.BOLD)),
                        ft.DataColumn(ft.Text("IC 95%", weight=ft.FontWeight.BOLD))
                    ],
                    rows=table_rows
                )
            ])
            
            self.result_container.content = result_table
            
        except Exception as e:
            self.result_container.content = ft.Text(f"Error: {str(e)}", color=ft.colors.RED_500)
        
        page.update()
    
    def check_exercise_answers(self, page):
        try:
            hypertension_prop = float(self.hypertension_field.value or 0)
            most_frequent = self.most_frequent_dropdown.value
            
            correct = 0
            total = 2
            feedback_items = []
            
            # Verificar proporción de hipertensión
            correct_prop = (285 / 500) * 100  # 57.0%
            if abs(hypertension_prop - correct_prop) < 0.5:
                feedback_items.append(ft.Text("✓ Correcto: La proporción de hipertensión es 57.0%", color=ft.colors.GREEN_600))
                correct += 1
            else:
                feedback_items.append(ft.Text(f"✗ Incorrecto: La proporción correcta es {correct_prop}% (285/500 × 100)", color=ft.colors.RED_600))
            
            # Verificar comorbilidad más frecuente
            if most_frequent == "hipertension":
                feedback_items.append(ft.Text("✓ Correcto: La hipertensión es la comorbilidad más frecuente (285 casos)", color=ft.colors.GREEN_600))
                correct += 1
            else:
                feedback_items.append(ft.Text("✗ Incorrecto: La hipertensión es la comorbilidad más frecuente con 285 casos", color=ft.colors.RED_600))
            
            # Interpretación clínica
            feedback_items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("Interpretación Clínica:", weight=ft.FontWeight.BOLD, color=self.colors['secondary']),
                        ft.Text(
                            "El 57% de los pacientes diabéticos presentan hipertensión como comorbilidad, lo que es consistente con la literatura médica que reporta alta prevalencia de hipertensión en población diabética. Este hallazgo sugiere la necesidad de screening y manejo integral de ambas condiciones.",
                            size=12
                        )
                    ]),
                    bgcolor=ft.colors.BLUE_50,
                    padding=15,
                    border_radius=8,
                    margin=ft.margin.only(top=10)
                )
            )
            
            feedback_items.append(ft.Text(f"Puntuación: {correct}/{total} ({int(correct/total*100)}%)", weight=ft.FontWeight.BOLD))
            
            self.exercise_feedback.content = ft.Container(
                content=ft.Column(feedback_items),
                bgcolor=ft.colors.WHITE,
                padding=20,
                border_radius=8,
                border=ft.border.all(1, ft.colors.GREY_300)
            )
            self.exercise_feedback.visible = True
            
        except ValueError:
            self.exercise_feedback.content = ft.Text("Por favor, ingresa valores válidos.", color=ft.colors.RED_500)
            self.exercise_feedback.visible = True
        
        page.update()
    
    def create_ai_module(self, page):
        # Chat messages container
        self.chat_container = ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.SMART_TOY, color=ft.colors.WHITE),
                        bgcolor=ft.colors.PURPLE_600,
                        width=32,
                        height=32,
                        border_radius=16,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("¡Hola! Soy tu asistente de IA. Puedes preguntarme sobre:", size=12),
                            ft.Text("• Interpretación de tablas de frecuencias", size=10),
                            ft.Text("• Cálculo de intervalos de confianza", size=10),
                            ft.Text("• Recomendaciones de visualización", size=10),
                            ft.Text("• Análisis de significancia clínica", size=10)
                        ]),
                        bgcolor=ft.colors.PURPLE_100,
                        padding=10,
                        border_radius=8,
                        expand=True
                    )
                ], spacing=10),
                margin=ft.margin.only(bottom=10)
            )
        ], scroll=ft.ScrollMode.AUTO, height=300)
        
        # Chat input
        self.chat_input = ft.TextField(
            hint_text="Escribe tu pregunta aquí...",
            expand=True,
            on_submit=lambda e: self.send_message(page)
        )
        
        # Dataset selector
        self.dataset_selector = ft.Dropdown(
            label="Selecciona un dataset",
            width=300,
            options=[
                ft.dropdown.Option("emergency", "Consultas de Urgencias"),
                ft.dropdown.Option("comorbidities", "Comorbilidades Diabéticas"),
                ft.dropdown.Option("medications", "Adherencia a Medicamentos"),
                ft.dropdown.Option("satisfaction", "Satisfacción del Paciente")
            ]
        )
        
        self.analysis_result = ft.Container(
            content=ft.Text("Selecciona un dataset y ejecuta el análisis...", color=ft.colors.GREY_500),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_300),
            width=400,
            height=200
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.SMART_TOY, color=ft.colors.PURPLE_600, size=30),
                    ft.Text("Asistente de IA para Análisis Categórico", size=28, weight=ft.FontWeight.BOLD)
                ]),
                
                # AI Assistant Header
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.icons.PSYCHOLOGY, size=40, color=ft.colors.WHITE),
                            width=60,
                            height=60,
                            bgcolor=ft.colors.WHITE24,
                            border_radius=30,
                            alignment=ft.alignment.center
                        ),
                        ft.Column([
                            ft.Text("CHANGE-AI Assistant", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Text("Especialista en análisis estadístico para ciencias de la salud", color=ft.colors.WHITE70)
                        ], expand=True)
                    ]),
                    bgcolor=ft.colors.PURPLE_600,
                    padding=20,
                    border_radius=10,
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Chat Interface
                ft.Container(
                    content=ft.Column([
                        ft.Text("Chat con el Asistente", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=self.chat_container,
                            bgcolor=ft.colors.WHITE,
                            border_radius=8,
                            border=ft.border.all(1, ft.colors.GREY_300),
                            padding=10
                        ),
                        ft.Row([
                            self.chat_input,
                            ft.ElevatedButton(
                                icon=ft.icons.SEND,
                                on_click=lambda e: self.send_message(page),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.PURPLE_600,
                                    color=ft.colors.WHITE
                                )
                            )
                        ]),
                        ft.Text("Preguntas Sugeridas:", weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.ElevatedButton(
                                text="Intervalos de confianza",
                                on_click=lambda e: self.ask_predefined_question(page, "¿Cómo interpreto un intervalo de confianza del 95%?"),
                                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_100, color=ft.colors.BLUE_800)
                            ),
                            ft.ElevatedButton(
                                text="Tipos de gráficos",
                                on_click=lambda e: self.ask_predefined_question(page, "¿Cuándo usar gráfico de barras vs circular?"),
                                style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_100, color=ft.colors.GREEN_800)
                            ),
                            ft.ElevatedButton(
                                text="Categorías pequeñas",
                                on_click=lambda e: self.ask_predefined_question(page, "¿Cómo manejar categorías con frecuencias muy bajas?"),
                                style=ft.ButtonStyle(bgcolor=ft.colors.ORANGE_100, color=ft.colors.ORANGE_800)
                            )
                        ], wrap=True)
                    ]),
                    bgcolor=ft.colors.GREY_50,
                    padding=20,
                    border_radius=10,
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Automatic Analysis
                ft.Container(
                    content=ft.Column([
                        ft.Text("Análisis Automático de Datos", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.INDIGO_800),
                        ft.Row([
                            ft.Column([
                                ft.Text("Cargar Datos para Análisis", weight=ft.FontWeight.BOLD),
                                self.dataset_selector,
                                ft.ElevatedButton(
                                    text="Ejecutar Análisis IA",
                                    icon=ft.icons.AUTO_AWESOME,
                                    on_click=lambda e: self.run_automatic_analysis(page),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.INDIGO_600,
                                        color=ft.colors.WHITE
                                    )
                                )
                            ]),
                            ft.Column([
                                ft.Text("Resultados del Análisis", weight=ft.FontWeight.BOLD),
                                self.analysis_result
                            ])
                        ])
                    ]),
                    bgcolor=ft.colors.INDIGO_50,
                    padding=20,
                    border_radius=10,
                    margin=ft.margin.only(bottom=20)
                ),
                
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Ir a Evaluación",
                        icon=ft.icons.ARROW_FORWARD,
                        on_click=lambda e: self.show_module(page, "evaluation"),
                        style=ft.ButtonStyle(
                            bgcolor=self.colors['danger'],
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=15)
                        )
                    ),
                    alignment=ft.alignment.center
                )
            ], scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_300)
        )
    
    def send_message(self, page):
        message = self.chat_input.value.strip()
        if not message:
            return
        
        # Add user message
        self.chat_container.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.PERSON, color=ft.colors.WHITE),
                        bgcolor=ft.colors.BLUE_600,
                        width=32,
                        height=32,
                        border_radius=16,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Text(message, size=12),
                        bgcolor=ft.colors.BLUE_100,
                        padding=10,
                        border_radius=8,
                        expand=True
                    )
                ], spacing=10),
                margin=ft.margin.only(bottom=10)
            )
        )
        
        self.chat_input.value = ""
        
        # Generate AI response
        response = self.generate_ai_response(message)
        
        # Add AI response
        self.chat_container.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.icons.SMART_TOY, color=ft.colors.WHITE),
                        bgcolor=ft.colors.PURPLE_600,
                        width=32,
                        height=32,
                        border_radius=16,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Text(response, size=12),
                        bgcolor=ft.colors.PURPLE_100,
                        padding=10,
                        border_radius=8,
                        expand=True
                    )
                ], spacing=10),
                margin=ft.margin.only(bottom=10)
            )
        )
        
        page.update()
    
    def ask_predefined_question(self, page, question):
        self.chat_input.value = question
        self.send_message(page)
    
    def generate_ai_response(self, message):
        responses = {
            'intervalo': 'Un intervalo de confianza del 95% significa que si repitiéramos el estudio 100 veces, en 95 ocasiones el verdadero valor poblacional estaría dentro del rango calculado. Es una medida de la precisión de nuestra estimación.',
            'gráfico': 'Los gráficos de barras son ideales para comparar categorías, mientras que los circulares muestran la proporción del total. Para datos médicos, recomiendo barras cuando hay muchas categorías o cuando se quiere facilitar la comparación.',
            'categorías': 'Las categorías con frecuencias muy bajas (< 5% del total) pueden agruparse en "Otros" para mejorar la interpretación. Sin embargo, en contextos clínicos, algunas categorías raras pueden ser clínicamente importantes y deben reportarse por separado.',
            'default': 'Interesante pregunta. En el contexto de tablas de frecuencias para ciencias de la salud, es importante considerar tanto la significancia estadística como la relevancia clínica. ¿Podrías ser más específico sobre qué aspecto te interesa?'
        }
        
        message_lower = message.lower()
        
        if 'intervalo' in message_lower or 'confianza' in message_lower:
            return responses['intervalo']
        elif 'gráfico' in message_lower or 'barras' in message_lower or 'circular' in message_lower:
            return responses['gráfico']
        elif 'categorías' in message_lower or 'frecuencias' in message_lower or 'bajas' in message_lower:
            return responses['categorías']
        else:
            return responses['default']
    
    def run_automatic_analysis(self, page):
        dataset = self.dataset_selector.value
        if not dataset:
            self.analysis_result.content = ft.Text("Por favor, selecciona un dataset.", color=ft.colors.RED_500)
            page.update()
            return
        
        # Show loading
        self.analysis_result.content = ft.Column([
            ft.ProgressRing(),
            ft.Text("Analizando datos con IA...", size=12)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.update()
        
        # Simulate processing time
        time.sleep(2)
        
        analyses = {
            'emergency': ft.Column([
                ft.Text("Análisis Completado: Consultas de Urgencias", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Hallazgos Principales:", weight=ft.FontWeight.BOLD),
                        ft.Text("• Trauma representa el 34% de consultas (IC 95%: 31.4% - 36.7%)", size=12),
                        ft.Text("• Cardiovascular es la segunda causa (25%, IC 95%: 22.7% - 27.5%)", size=12),
                        ft.Text("• Distribución sugiere necesidad de recursos especializados en trauma", size=12)
                    ]),
                    bgcolor=ft.colors.GREEN_50,
                    padding=10,
                    border_radius=5
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Recomendaciones IA:", weight=ft.FontWeight.BOLD),
                        ft.Text("• Fortalecer servicio de traumatología", size=12),
                        ft.Text("• Implementar protocolos de triaje cardiovascular", size=12),
                        ft.Text("• Monitorear tendencias estacionales", size=12)
                    ]),
                    bgcolor=ft.colors.BLUE_50,
                    padding=10,
                    border_radius=5
                )
            ]),
            'comorbidities': ft.Column([
                ft.Text("Análisis Completado: Comorbilidades Diabéticas", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Hallazgos Principales:", weight=ft.FontWeight.BOLD),
                        ft.Text("• Hipertensión: 57% (IC 95%: 52.6% - 61.4%)", size=12),
                        ft.Text("• Dislipidemia: 38% (IC 95%: 33.8% - 42.2%)", size=12),
                        ft.Text("• Solo 11% sin comorbilidades", size=12)
                    ]),
                    bgcolor=ft.colors.GREEN_50,
                    padding=10,
                    border_radius=5
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Recomendaciones IA:", weight=ft.FontWeight.BOLD),
                        ft.Text("• Screening rutinario de hipertensión", size=12),
                        ft.Text("• Manejo integral diabetes-hipertensión", size=12),
                        ft.Text("• Programas de prevención cardiovascular", size=12)
                    ]),
                    bgcolor=ft.colors.BLUE_50,
                    padding=10,
                    border_radius=5
                )
            ])
        }
        
        self.analysis_result.content = analyses.get(dataset, ft.Text("Análisis no disponible para este dataset.", color=ft.colors.GREY_500))
        page.update()
    
    def create_evaluation_module(self, page):
        # Quiz questions
        self.quiz_questions = [
            {
                'question': 'En un estudio de 800 pacientes, 320 presentaron hipertensión. ¿Cuál es la proporción correcta?',
                'options': ['32%', '40%', '25%', '48%'],
                'correct': 1,
                'explanation': '320/800 = 0.40 = 40%. Es fundamental dominar este cálculo básico.'
            },
            {
                'question': '¿Cuál de las siguientes es una variable categórica ordinal en el contexto clínico?',
                'options': ['Tipo sanguíneo (A, B, AB, O)', 'Grado de dolor (leve, moderado, severo)', 'Género (masculino, femenino)', 'Método anticonceptivo utilizado'],
                'correct': 1,
                'explanation': 'El grado de dolor tiene un orden natural (leve < moderado < severo).'
            },
            {
                'question': 'Un intervalo de confianza del 95% para una proporción de 0.30 es (0.25 - 0.35). ¿Qué significa esto?',
                'options': ['Hay 95% de probabilidad de que la proporción sea exactamente 0.30', 'Estamos 95% seguros de que la proporción poblacional está entre 0.25 y 0.35', 'El 95% de los pacientes tienen valores entre 0.25 y 0.35', 'La proporción puede variar hasta 5% del valor observado'],
                'correct': 1,
                'explanation': 'El IC 95% indica el rango donde probablemente está el valor poblacional.'
            },
            {
                'question': '¿Cuál es la mejor práctica al presentar una tabla de frecuencias?',
                'options': ['Mostrar solo frecuencias absolutas', 'Incluir frecuencias, proporciones e intervalos de confianza', 'Usar tantas categorías como sea posible', 'Omitir los totales para ahorrar espacio'],
                'correct': 1,
                'explanation': 'Una tabla completa debe incluir frecuencias, proporciones e intervalos de confianza.'
            },
            {
                'question': 'En una encuesta de satisfacción a 600 pacientes: Muy satisfecho: 240, Satisfecho: 210, Neutral: 90, Insatisfecho: 45, Muy insatisfecho: 15. ¿Cuál es la interpretación más apropiada?',
                'options': ['El 75% de los pacientes están satisfechos o muy satisfechos (IC 95%: 71.4% - 78.6%)', 'Solo el 40% de los pacientes están muy satisfechos', 'La mayoría de pacientes están neutrales', 'Los resultados no son concluyentes'],
                'correct': 0,
                'explanation': 'Sumando muy satisfecho + satisfecho: (240+210)/600 = 75%.'
            }
        ]
        
        self.quiz_controls = []
        quiz_items = []
        
        for i, q in enumerate(self.quiz_questions):
            radio_group = ft.RadioGroup(
                content=ft.Column([
                    ft.Radio(value=j, label=option) for j, option in enumerate(q['options'])
                ])
            )
            self.quiz_controls.append(radio_group)
            
            quiz_items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{i+1}. {q['question']}", size=16, weight=ft.FontWeight.BOLD),
                        radio_group
                    ]),
                    bgcolor=ft.colors.GREY_50,
                    padding=20,
                    border_radius=8,
                    margin=ft.margin.only(bottom=10)
                )
            )
        
        self.quiz_results = ft.Container(visible=False)
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.QUIZ, color=self.colors['danger'], size=30),
                    ft.Text("Evaluación del Aprendizaje", size=28, weight=ft.FontWeight.BOLD)
                ]),
                
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.INFO, color=ft.colors.YELLOW_600),
                        ft.Text("Instrucciones: Responde todas las preguntas. Al finalizar, recibirás retroalimentación inmediata y recomendaciones personalizadas.", weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW_800, expand=True)
                    ]),
                    bgcolor=ft.colors.YELLOW_50,
                    padding=15,
                    border_radius=8,
                    border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400)),
                    margin=ft.margin.only(bottom=20)
                ),
                
                ft.Column(quiz_items),
                
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Enviar Evaluación",
                        icon=ft.icons.CHECK_CIRCLE,
                        on_click=lambda e: self.submit_quiz(page),
                        style=ft.ButtonStyle(
                            bgcolor=self.colors['danger'],
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=15)
                        )
                    ),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(top=20, bottom=20)
                ),
                
                self.quiz_results
            ], scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_300)
        )
    
    def submit_quiz(self, page):
        score = 0
        total = len(self.quiz_questions)
        
        for i, control in enumerate(self.quiz_controls):
            if control.value is not None and int(control.value) == self.quiz_questions[i]['correct']:
                score += 1
        
        percentage = (score / total) * 100
        
        # Create results
        result_items = [
            ft.Text("Resultados de la Evaluación", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text(str(score), size=36, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_600 if percentage >= 70 else ft.colors.RED_600),
                        width=80,
                        height=80,
                        bgcolor=ft.colors.GREEN_100 if percentage >= 70 else ft.colors.RED_100,
                        border_radius=40,
                        alignment=ft.alignment.center
                    ),
                    ft.Text(f"Puntuación: {score}/{total} ({percentage:.0f}%)", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("¡Excelente trabajo!" if percentage >= 70 else "Necesitas repasar algunos conceptos", color=ft.colors.GREY_600)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                margin=ft.margin.only(bottom=20)
            )
        ]
        
        # Add detailed feedback
        result_items.append(ft.Text("Retroalimentación Detallada:", size=16, weight=ft.FontWeight.BOLD))
        
        for i, q in enumerate(self.quiz_questions):
            user_answer = self.quiz_controls[i].value
            is_correct = user_answer is not None and int(user_answer) == q['correct']
            
            result_items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Pregunta {i+1}: {'✓ Correcto' if is_correct else '✗ Incorrecto'}", 
                               weight=ft.FontWeight.BOLD, 
                               color=ft.colors.GREEN_800 if is_correct else ft.colors.RED_800),
                        ft.Text(q['explanation'], size=12)
                    ]),
                    bgcolor=ft.colors.GREEN_50 if is_correct else ft.colors.RED_50,
                    padding=15,
                    border_radius=8,
                    margin=ft.margin.only(bottom=10)
                )
            )
        
        # Add recommendations
        if percentage >= 70:
            result_items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("¡Felicitaciones!", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                        ft.Text("Has demostrado un buen dominio de los conceptos de tablas de frecuencias. Estás listo para aplicar estos conocimientos en contextos clínicos reales.", size=12)
                    ]),
                    bgcolor=ft.colors.GREEN_50,
                    padding=15,
                    border_radius=8,
                    margin=ft.margin.only(top=20)
                )
            )
        else:
            result_items.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("Recomendaciones de Estudio", weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_800),
                        ft.Text("• Repasa el módulo de teoría, especialmente el cálculo de proporciones", size=12),
                        ft.Text("• Practica más con la calculadora interactiva", size=12),
                        ft.Text("• Consulta con el asistente de IA sobre conceptos específicos", size=12),
                        ft.Text("• Revisa los recursos descargables para reforzar el aprendizaje", size=12)
                    ]),
                    bgcolor=ft.colors.ORANGE_50,
                    padding=15,
                    border_radius=8,
                    margin=ft.margin.only(top=20)
                )
            )
        
        self.quiz_results.content = ft.Container(
            content=ft.Column(result_items),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_300)
        )
        self.quiz_results.visible = True
        page.update()
    
    def create_resources_module(self, page):
        resources = [
            ("Plantillas de Tablas", ft.icons.TABLE_CHART, ft.colors.BLUE_600, "Tabla de frecuencias estándar\nFormato para publicación\nPlantilla con intervalos de confianza\nTabla de contingencia 2x2"),
            ("Guías Metodológicas", ft.icons.BOOK_OUTLINED, ft.colors.GREEN_600, "Guía paso a paso\nChecklist de verificación\nInterpretación clínica\nErrores comunes a evitar"),
            ("Datasets de Práctica", ft.icons.DATABASE, ft.colors.PURPLE_600, "Datos de urgencias hospitalarias\nComorbilidades en diabetes\nSatisfacción del paciente\nAdherencia a tratamientos"),
            ("Scripts en R", ft.icons.CODE, ft.colors.ORANGE_600, "Análisis de frecuencias\nCálculo de intervalos de confianza\nVisualizaciones automáticas\nReportes reproducibles"),
            ("Infografías", ft.icons.PIE_CHART, ft.colors.TEAL_600, "Tipos de variables categóricas\nProceso de análisis\nInterpretación de resultados\nBuenas prácticas visuales"),
            ("Certificado", ft.icons.WORKSPACE_PREMIUM, ft.colors.YELLOW_600, "Certificado de finalización\nCompetencias adquiridas\nHoras de estudio\nCódigo de verificación")
        ]
        
        resource_cards = []
        for title, icon, color, description in resources:
            resource_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(icon, size=40, color=color),
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(bottom=10)
                        ),
                        ft.Text(title, size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text(description, size=12, text_align=ft.TextAlign.CENTER, color=ft.colors.GREY_600),
                        ft.ElevatedButton(
                            text="Descargar" if title != "Certificado" else "Generar",
                            icon=ft.icons.DOWNLOAD if title != "Certificado" else ft.icons.WORKSPACE_PREMIUM,
                            on_click=lambda e, t=title: self.download_resource(page, t),
                            style=ft.ButtonStyle(
                                bgcolor=color,
                                color=ft.colors.WHITE
                            )
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.WHITE,
                    padding=20,
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.GREY_300),
                    width=200,
                    height=250
                )
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.DOWNLOAD, color=self.colors['success'], size=30),
                    ft.Text("Recursos Descargables", size=28, weight=ft.FontWeight.BOLD)
                ]),
                
                ft.Container(
                    content=ft.Row(resource_cards[:3], alignment=ft.MainAxisAlignment.SPACE_EVENLY, wrap=True),
                    margin=ft.margin.only(bottom=20)
                ),
                
                ft.Container(
                    content=ft.Row(resource_cards[3:], alignment=ft.MainAxisAlignment.SPACE_EVENLY, wrap=True),
                    margin=ft.margin.only(bottom=30)
                ),
                
                # Referencias Bibliográficas
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.BOOK, color=ft.colors.GREY_800),
                            ft.Text("Referencias Bibliográficas", size=20, weight=ft.FontWeight.BOLD)
                        ]),
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Libros de Texto", weight=ft.FontWeight.BOLD),
                                    ft.Text("• Pagano, M. & Gauvreau, K. (2018). Principles of Biostatistics. 2nd ed.", size=12),
                                    ft.Text("• Rosner, B. (2015). Fundamentals of Biostatistics. 8th ed.", size=12),
                                    ft.Text("• Kirkwood, B. R. & Sterne, J. A. (2003). Essential Medical Statistics. 2nd ed.", size=12),
                                    ft.Text("• Altman, D. G. (1991). Practical Statistics for Medical Research.", size=12)
                                ]),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Artículos de Referencia", weight=ft.FontWeight.BOLD),
                                    ft.Text("• Altman, D. G. et al. (2000). Statistical guidelines for contributors to medical journals. BMJ, 321(7266), 1559-1561.", size=12),
                                    ft.Text("• Lang, T. A. & Secic, M. (2006). How to report statistics in medicine. 2nd ed.", size=12),
                                    ft.Text("• Newcombe, R. G. (1998). Two-sided confidence intervals for the single proportion. Statistics in Medicine, 17(8), 857-872.", size=12)
                                ]),
                                expand=True
                            )
                        ])
                    ]),
                    bgcolor=ft.colors.GREY_50,
                    padding=20,
                    border_radius=10,
                    margin=ft.margin.only(bottom=20)
                ),
                
                # Enlaces Útiles
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.LINK, color=self.colors['secondary']),
                            ft.Text("Enlaces Útiles", size=20, weight=ft.FontWeight.BOLD)
                        ]),
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Software Estadístico", weight=ft.FontWeight.BOLD, color=self.colors['secondary']),
                                    ft.Text("• R Project", size=12, color=self.colors['secondary']),
                                    ft.Text("• RStudio", size=12, color=self.colors['secondary']),
                                    ft.Text("• PSPP (libre)", size=12, color=self.colors['secondary']),
                                    ft.Text("• Jamovi", size=12, color=self.colors['secondary'])
                                ]),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Datos Abiertos", weight=ft.FontWeight.BOLD, color=self.colors['secondary']),
                                    ft.Text("• DANE Colombia", size=12, color=self.colors['secondary']),
                                    ft.Text("• INS Colombia", size=12, color=self.colors['secondary']),
                                    ft.Text("• WHO Global Health Observatory", size=12, color=self.colors['secondary']),
                                    ft.Text("• CDC Wonder", size=12, color=self.colors['secondary'])
                                ]),
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Herramientas Online", weight=ft.FontWeight.BOLD, color=self.colors['secondary']),
                                    ft.Text("• Calculadora de IC", size=12, color=self.colors['secondary']),
                                    ft.Text("• Generador de gráficos", size=12, color=self.colors['secondary']),
                                    ft.Text("• Validador de tablas", size=12, color=self.colors['secondary']),
                                    ft.Text("• Conversor de formatos", size=12, color=self.colors['secondary'])
                                ]),
                                expand=True
                            )
                        ])
                    ]),
                    bgcolor=ft.colors.BLUE_50,
                    padding=20,
                    border_radius=10
                )
            ], scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.colors.WHITE,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_300)
        )
    
    def download_resource(self, page, resource_type):
        messages = {
            "Plantillas de Tablas": "Plantillas de tablas de frecuencias descargadas. Incluye formatos en Excel y Word.",
            "Guías Metodológicas": "Guías metodológicas descargadas. Incluye checklist y mejores prácticas.",
            "Datasets de Práctica": "Datasets de práctica descargados. Incluye datos de urgencias, comorbilidades y más.",
            "Scripts en R": "Scripts de R descargados. Incluye código para análisis completo.",
            "Infografías": "Infografías descargadas. Incluye resúmenes visuales de conceptos clave.",
            "Certificado": "¡Certificado generado! Has completado exitosamente el OVA 'Tablas de Frecuencias y Resúmenes Categóricos'. El certificado incluye las competencias adquiridas y puede ser verificado con el código: OVA-TF-2024-001"
        }
        
        # Show snackbar with download message
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(messages.get(resource_type, "Recurso descargado exitosamente.")),
                action="OK"
            )
        )

def main(page: ft.Page):
    app = OVAApp()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)
