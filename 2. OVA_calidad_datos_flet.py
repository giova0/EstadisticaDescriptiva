
import flet as ft
import random
import time
from datetime import datetime

class OVAApp:
    def __init__(self):
        self.current_section = "intro"
        self.progress = 0
        self.completed_sections = []
        
        # Datos simulados para el simulador
        self.sample_data = [
            {"id": "001", "edad": "45", "genero": "M", "pas": "140", "pad": "90", "imc": "25.3", "medicamento": "Enalapril", "fecha": "2024-01-15"},
            {"id": "002", "edad": "", "genero": "Femenino", "pas": "320", "pad": "85", "imc": "-10", "medicamento": "Losartan", "fecha": "15/01/2024"},
            {"id": "003", "edad": "999", "genero": "F", "pas": "", "pad": "95", "imc": "28.7", "medicamento": "N/A", "fecha": "2024-01-15"},
            {"id": "004", "edad": "52", "genero": "M", "pas": "155", "pad": "100", "imc": "31.2", "medicamento": "Amlodipino", "fecha": "01-15-2024"},
            {"id": "005", "edad": "38", "genero": "1", "pas": "145", "pad": "88", "imc": "24.1", "medicamento": "Enalapril", "fecha": "2024/01/15"}
        ]
        
        self.cleaned_data = [
            {"id": "001", "edad": "45", "genero": "M", "pas": "140", "pad": "90", "imc": "25.3", "medicamento": "Enalapril", "fecha": "2024-01-15"},
            {"id": "002", "edad": "47", "genero": "F", "pas": "160", "pad": "85", "imc": "28.5", "medicamento": "Losartan", "fecha": "2024-01-15"},
            {"id": "003", "edad": "51", "genero": "F", "pas": "150", "pad": "95", "imc": "28.7", "medicamento": "Amlodipino", "fecha": "2024-01-15"},
            {"id": "004", "edad": "52", "genero": "M", "pas": "155", "pad": "100", "imc": "31.2", "medicamento": "Amlodipino", "fecha": "2024-01-15"},
            {"id": "005", "edad": "38", "genero": "M", "pas": "145", "pad": "88", "imc": "24.1", "medicamento": "Enalapril", "fecha": "2024-01-15"}
        ]
        
        self.data_cleaned = False
        
        # Variables para ejercicios
        self.exercise1_checks = {}
        self.exercise2_solutions = {}
        self.quiz_answers = {}

    def main(self, page: ft.Page):
        page.title = "OVA 2: Calidad y Limpieza de Datos Clínicos"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.scroll = ft.ScrollMode.AUTO
        
        # Barra de progreso
        self.progress_bar = ft.ProgressBar(width=400, color="blue", bgcolor="#eeeeee")
        self.progress_text = ft.Text("0% completado", size=12)
        
        # Navegación
        nav_buttons = ft.Row([
            ft.ElevatedButton("Introducción", icon=ft.icons.PLAY_CIRCLE, on_click=lambda _: self.show_section(page, "intro")),
            ft.ElevatedButton("Teoría", icon=ft.icons.BOOK, on_click=lambda _: self.show_section(page, "theory")),
            ft.ElevatedButton("Simulador IA", icon=ft.icons.SMART_TOY, on_click=lambda _: self.show_section(page, "simulator")),
            ft.ElevatedButton("Práctica", icon=ft.icons.HANDYMAN, on_click=lambda _: self.show_section(page, "practice")),
            ft.ElevatedButton("Evaluación", icon=ft.icons.QUIZ, on_click=lambda _: self.show_section(page, "evaluation")),
            ft.ElevatedButton("Recursos", icon=ft.icons.DOWNLOAD, on_click=lambda _: self.show_section(page, "resources")),
        ], scroll=ft.ScrollMode.AUTO)
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Text("OVA 2: Calidad y Limpieza de Datos Clínicos", 
                       size=28, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text("Estadística Descriptiva para Ciencias de la Salud", 
                       size=16, color="white"),
            ]),
            bgcolor=ft.colors.BLUE_700,
            padding=20,
            margin=ft.margin.only(bottom=10)
        )
        
        # Progress section
        progress_section = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Progreso del OVA", size=14),
                    self.progress_text
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar
            ]),
            padding=10,
            bgcolor="white"
        )
        
        # Navigation section
        nav_section = ft.Container(
            content=nav_buttons,
            padding=10,
            bgcolor="white",
            margin=ft.margin.only(bottom=10)
        )
        
        # Content container
        self.content_container = ft.Container(
            content=self.create_intro_section(page),
            padding=20,
            expand=True
        )
        
        # Main layout
        page.add(
            ft.Column([
                header,
                progress_section,
                nav_section,
                self.content_container
            ], expand=True)
        )

    def show_section(self, page, section_id):
        if section_id != self.current_section:
            if self.current_section not in self.completed_sections:
                self.completed_sections.append(self.current_section)
            
            sections = ["intro", "theory", "simulator", "practice", "evaluation", "resources"]
            current_index = sections.index(section_id)
            self.progress = (current_index + 1) / len(sections)
            
            self.progress_bar.value = self.progress
            self.progress_text.value = f"{int(self.progress * 100)}% completado"
            
            self.current_section = section_id
            
            # Update content
            if section_id == "intro":
                self.content_container.content = self.create_intro_section(page)
            elif section_id == "theory":
                self.content_container.content = self.create_theory_section(page)
            elif section_id == "simulator":
                self.content_container.content = self.create_simulator_section(page)
            elif section_id == "practice":
                self.content_container.content = self.create_practice_section(page)
            elif section_id == "evaluation":
                self.content_container.content = self.create_evaluation_section(page)
            elif section_id == "resources":
                self.content_container.content = self.create_resources_section(page)
            
            page.update()

    def create_intro_section(self, page):
        return ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.DATABASE, size=60, color=ft.colors.BLUE_600),
                            ft.Column([
                                ft.Text("Bienvenido al OVA de Calidad y Limpieza de Datos", 
                                        size=24, weight=ft.FontWeight.BOLD),
                                ft.Text("Aprende a aplicar un flujo básico de depuración de datos clínicos utilizando el modelo pedagógico C(H)ANGE e inteligencia artificial.", 
                                        size=14, color=ft.colors.GREY_700)
                            ], expand=True)
                        ]),
                        
                        ft.Divider(),
                        
                        ft.Row([
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Icon(ft.icons.TARGET, color=ft.colors.BLUE_600),
                                            ft.Text("Objetivo Principal", weight=ft.FontWeight.BOLD)
                                        ]),
                                        ft.Text("Aplicar un flujo básico de depuración de datos clínicos, identificando y corrigiendo valores perdidos, outliers y errores de codificación.", 
                                                size=12)
                                    ]),
                                    padding=15,
                                    bgcolor=ft.colors.BLUE_50
                                ),
                                expand=True
                            ),
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Icon(ft.icons.SCHOOL, color=ft.colors.GREEN_600),
                                            ft.Text("Competencias C(H)ANGE", weight=ft.FontWeight.BOLD)
                                        ]),
                                        ft.Text("C: Combinatoria - Patrones en datos faltantes", size=11),
                                        ft.Text("A: Álgebra - Transformaciones de variables", size=11),
                                        ft.Text("N: Números - Rangos y valores atípicos", size=11),
                                        ft.Text("G: Geometría - Visualización de outliers", size=11),
                                        ft.Text("E: Estadística - Medidas de calidad", size=11),
                                    ]),
                                    padding=15,
                                    bgcolor=ft.colors.GREEN_50
                                ),
                                expand=True
                            )
                        ]),
                        
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Icon(ft.icons.MEDICAL_SERVICES, color=ft.colors.RED_600),
                                        ft.Text("Caso Clínico: Estudio de Hipertensión Arterial", 
                                                weight=ft.FontWeight.BOLD)
                                    ]),
                                    ft.Text("El Hospital San Rafael ha recolectado datos de 500 pacientes con hipertensión arterial durante 6 meses. Sin embargo, la base de datos presenta múltiples problemas de calidad:", 
                                            size=12),
                                    ft.Row([
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Text("Valores perdidos:", weight=ft.FontWeight.BOLD, size=11),
                                                ft.Text("15% de datos faltantes en presión arterial sistólica", size=10)
                                            ]),
                                            padding=10,
                                            bgcolor="white",
                                            border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.RED_400)),
                                            expand=True
                                        ),
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Text("Outliers:", weight=ft.FontWeight.BOLD, size=11),
                                                ft.Text("Presiones arteriales de 300/200 mmHg registradas", size=10)
                                            ]),
                                            padding=10,
                                            bgcolor="white",
                                            border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400)),
                                            expand=True
                                        ),
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Text("Codificación:", weight=ft.FontWeight.BOLD, size=11),
                                                ft.Text("Género registrado como M/F, Masculino/Femenino, 1/2", size=10)
                                            ]),
                                            padding=10,
                                            bgcolor="white",
                                            border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.BLUE_400)),
                                            expand=True
                                        )
                                    ])
                                ]),
                                padding=15,
                                bgcolor=ft.colors.RED_50
                            )
                        ),
                        
                        ft.Container(
                            content=ft.ElevatedButton(
                                "Comenzar con la Teoría",
                                icon=ft.icons.ARROW_FORWARD,
                                on_click=lambda _: self.show_section(page, "theory"),
                                bgcolor=ft.colors.BLUE_600,
                                color="white"
                            ),
                            alignment=ft.alignment.center,
                            padding=20
                        )
                    ]),
                    padding=20
                )
            )
        ], scroll=ft.ScrollMode.AUTO)

    def create_theory_section(self, page):
        return ft.Column([
            ft.Text("Fundamentos Teóricos", size=28, weight=ft.FontWeight.BOLD),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("1. Tipos de Problemas en Datos Clínicos", 
                                size=20, weight=ft.FontWeight.BOLD),
                        
                        ft.Row([
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Icon(ft.icons.HELP, color=ft.colors.RED_600),
                                            ft.Text("Valores Perdidos", weight=ft.FontWeight.BOLD)
                                        ]),
                                        ft.Text("• MCAR (Missing Completely at Random)", size=12),
                                        ft.Text("• MAR (Missing at Random)", size=12),
                                        ft.Text("• MNAR (Missing Not at Random)", size=12),
                                        ft.Text("• Impacto en análisis estadísticos", size=12),
                                    ]),
                                    padding=15,
                                    bgcolor=ft.colors.RED_50
                                ),
                                expand=True
                            ),
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Icon(ft.icons.WARNING, color=ft.colors.YELLOW_600),
                                            ft.Text("Valores Atípicos", weight=ft.FontWeight.BOLD)
                                        ]),
                                        ft.Text("• Outliers univariados", size=12),
                                        ft.Text("• Outliers multivariados", size=12),
                                        ft.Text("• Errores de digitación vs. valores reales", size=12),
                                        ft.Text("• Métodos de detección", size=12),
                                    ]),
                                    padding=15,
                                    bgcolor=ft.colors.YELLOW_50
                                ),
                                expand=True
                            ),
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Icon(ft.icons.CODE, color=ft.colors.BLUE_600),
                                            ft.Text("Errores de Codificación", weight=ft.FontWeight.BOLD)
                                        ]),
                                        ft.Text("• Inconsistencias en categorías", size=12),
                                        ft.Text("• Formatos de fecha incorrectos", size=12),
                                        ft.Text("• Unidades de medida mixtas", size=12),
                                        ft.Text("• Caracteres especiales", size=12),
                                    ]),
                                    padding=15,
                                    bgcolor=ft.colors.BLUE_50
                                ),
                                expand=True
                            )
                        ])
                    ]),
                    padding=20
                )
            ),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("2. Flujo Sistemático de Limpieza de Datos", 
                                size=20, weight=ft.FontWeight.BOLD),
                        
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Container(
                                        content=ft.Text("1", color="white", weight=ft.FontWeight.BOLD),
                                        width=40, height=40,
                                        bgcolor=ft.colors.BLUE_600,
                                        border_radius=20,
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Text("Exploración\nInicial", size=12, text_align=ft.TextAlign.CENTER)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                expand=True
                            ),
                            ft.Icon(ft.icons.ARROW_FORWARD, color=ft.colors.GREY_400),
                            ft.Container(
                                content=ft.Column([
                                    ft.Container(
                                        content=ft.Text("2", color="white", weight=ft.FontWeight.BOLD),
                                        width=40, height=40,
                                        bgcolor=ft.colors.GREEN_600,
                                        border_radius=20,
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Text("Identificación\nde Problemas", size=12, text_align=ft.TextAlign.CENTER)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                expand=True
                            ),
                            ft.Icon(ft.icons.ARROW_FORWARD, color=ft.colors.GREY_400),
                            ft.Container(
                                content=ft.Column([
                                    ft.Container(
                                        content=ft.Text("3", color="white", weight=ft.FontWeight.BOLD),
                                        width=40, height=40,
                                        bgcolor=ft.colors.YELLOW_600,
                                        border_radius=20,
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Text("Corrección\ny Limpieza", size=12, text_align=ft.TextAlign.CENTER)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                expand=True
                            ),
                            ft.Icon(ft.icons.ARROW_FORWARD, color=ft.colors.GREY_400),
                            ft.Container(
                                content=ft.Column([
                                    ft.Container(
                                        content=ft.Text("4", color="white", weight=ft.FontWeight.BOLD),
                                        width=40, height=40,
                                        bgcolor=ft.colors.PURPLE_600,
                                        border_radius=20,
                                        alignment=ft.alignment.center
                                    ),
                                    ft.Text("Validación y\nDocumentación", size=12, text_align=ft.TextAlign.CENTER)
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                expand=True
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ]),
                    padding=20,
                    bgcolor=ft.colors.GREEN_50
                )
            ),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("3. Herramientas y Técnicas de IA para Limpieza", 
                                size=20, weight=ft.FontWeight.BOLD),
                        
                        ft.Row([
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Icon(ft.icons.SMART_TOY, color=ft.colors.PURPLE_600),
                                            ft.Text("Algoritmos de IA Aplicados", weight=ft.FontWeight.BOLD)
                                        ]),
                                        ft.Text("✓ Machine Learning: Detección automática de outliers usando Isolation Forest", size=11),
                                        ft.Text("✓ NLP: Estandarización de texto en variables categóricas", size=11),
                                        ft.Text("✓ Redes Neuronales: Imputación inteligente de valores faltantes", size=11),
                                        ft.Text("✓ Clustering: Identificación de patrones anómalos", size=11),
                                    ]),
                                    padding=15,
                                    bgcolor=ft.colors.PURPLE_50
                                ),
                                expand=True
                            ),
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Icon(ft.icons.BUILD, color=ft.colors.ORANGE_600),
                                            ft.Text("Herramientas Prácticas", weight=ft.FontWeight.BOLD)
                                        ]),
                                        ft.Text("⚙ OpenRefine: Limpieza interactiva de datos", size=11),
                                        ft.Text("⚙ Python/Pandas: Automatización de procesos", size=11),
                                        ft.Text("⚙ R/tidyverse: Análisis exploratorio y limpieza", size=11),
                                        ft.Text("⚙ Trifacta/Alteryx: Plataformas de preparación de datos", size=11),
                                    ]),
                                    padding=15,
                                    bgcolor=ft.colors.ORANGE_50
                                ),
                                expand=True
                            )
                        ])
                    ]),
                    padding=20
                )
            ),
            
            ft.Container(
                content=ft.ElevatedButton(
                    "Continuar al Simulador IA",
                    icon=ft.icons.ARROW_FORWARD,
                    on_click=lambda _: self.show_section(page, "simulator"),
                    bgcolor=ft.colors.GREEN_600,
                    color="white"
                ),
                alignment=ft.alignment.center,
                padding=20
            )
        ], scroll=ft.ScrollMode.AUTO)

    def create_simulator_section(self, page):
        # Estadísticas de calidad
        self.missing_count = ft.Text("3", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600)
        self.outlier_count = ft.Text("2", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW_600)
        self.quality_score = ft.Text("73%", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_600)
        
        # Resultados del IA
        self.ai_results = ft.Container(
            content=ft.Column([
                ft.Text("Análisis IA Completado:", weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                ft.Row([ft.Icon(ft.icons.ERROR, color=ft.colors.RED_600), ft.Text("Detectados 3 valores faltantes en variables críticas", size=12)]),
                ft.Row([ft.Icon(ft.icons.WARNING, color=ft.colors.YELLOW_600), ft.Text("Identificados 2 outliers potenciales en presión arterial", size=12)]),
                ft.Row([ft.Icon(ft.icons.CODE, color=ft.colors.ORANGE_600), ft.Text("Encontradas 4 inconsistencias en codificación de variables", size=12)]),
                ft.Row([ft.Icon(ft.icons.INFO, color=ft.colors.BLUE_600), ft.Text("Sugerencia: Estandarizar formato de fechas", size=12)]),
            ]),
            padding=15,
            bgcolor="white",
            border=ft.border.all(2, ft.colors.PURPLE_200),
            border_radius=10,
            visible=False
        )
        
        # Tabla de datos
        self.data_table = self.create_data_table()
        
        return ft.Column([
            ft.Text("Simulador IA de Limpieza de Datos", size=28, weight=ft.FontWeight.BOLD),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.PSYCHOLOGY, color=ft.colors.PURPLE_600),
                            ft.Text("Asistente IA para Limpieza de Datos", size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "Análisis Automático",
                                icon=ft.icons.SEARCH,
                                on_click=lambda _: self.run_ai_analysis(page),
                                bgcolor=ft.colors.PURPLE_600,
                                color="white"
                            ),
                            ft.ElevatedButton(
                                "Sugerir Limpieza",
                                icon=ft.icons.LIGHTBULB,
                                on_click=lambda _: self.suggest_cleaning(page),
                                bgcolor=ft.colors.BLUE_600,
                                color="white"
                            ),
                            ft.ElevatedButton(
                                "Validar Resultados",
                                icon=ft.icons.CHECK_CIRCLE,
                                on_click=lambda _: self.validate_data(page),
                                bgcolor=ft.colors.GREEN_600,
                                color="white"
                            )
                        ]),
                        
                        self.ai_results
                    ]),
                    padding=20,
                    bgcolor=ft.colors.PURPLE_50
                )
            ),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.TABLE_CHART, color=ft.colors.BLUE_600),
                            ft.Text("Base de Datos: Pacientes con Hipertensión", size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "Resaltar Faltantes",
                                icon=ft.icons.HELP,
                                on_click=lambda _: self.highlight_missing(page),
                                bgcolor=ft.colors.RED_100,
                                color=ft.colors.RED_800
                            ),
                            ft.ElevatedButton(
                                "Detectar Outliers",
                                icon=ft.icons.WARNING,
                                on_click=lambda _: self.highlight_outliers(page),
                                bgcolor=ft.colors.YELLOW_100,
                                color=ft.colors.YELLOW_800
                            ),
                            ft.ElevatedButton(
                                "Inconsistencias",
                                icon=ft.icons.CODE,
                                on_click=lambda _: self.highlight_inconsistent(page),
                                bgcolor=ft.colors.ORANGE_100,
                                color=ft.colors.ORANGE_800
                            ),
                            ft.ElevatedButton(
                                "Limpiar Datos",
                                icon=ft.icons.CLEANING_SERVICES,
                                on_click=lambda _: self.clean_data(page),
                                bgcolor=ft.colors.GREEN_100,
                                color=ft.colors.GREEN_800
                            )
                        ], wrap=True),
                        
                        ft.Container(
                            content=self.data_table,
                            padding=10,
                            bgcolor=ft.colors.GREY_50,
                            border_radius=10
                        )
                    ]),
                    padding=20
                )
            ),
            
            ft.Row([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Valores Faltantes", weight=ft.FontWeight.BOLD, color=ft.colors.RED_800),
                            self.missing_count,
                            ft.Text("registros afectados", size=12, color=ft.colors.RED_600)
                        ]),
                        padding=20,
                        bgcolor=ft.colors.RED_50
                    ),
                    expand=True
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Outliers Detectados", weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW_800),
                            self.outlier_count,
                            ft.Text("valores atípicos", size=12, color=ft.colors.YELLOW_600)
                        ]),
                        padding=20,
                        bgcolor=ft.colors.YELLOW_50
                    ),
                    expand=True
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Calidad General", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                            self.quality_score,
                            ft.Text("datos limpios", size=12, color=ft.colors.GREEN_600)
                        ]),
                        padding=20,
                        bgcolor=ft.colors.GREEN_50
                    ),
                    expand=True
                )
            ]),
            
            ft.Container(
                content=ft.ElevatedButton(
                    "Continuar a la Práctica Guiada",
                    icon=ft.icons.ARROW_FORWARD,
                    on_click=lambda _: self.show_section(page, "practice"),
                    bgcolor=ft.colors.BLUE_600,
                    color="white"
                ),
                alignment=ft.alignment.center,
                padding=20
            )
        ], scroll=ft.ScrollMode.AUTO)

    def create_data_table(self):
        data_to_show = self.cleaned_data if self.data_cleaned else self.sample_data
        
        rows = []
        for item in data_to_show:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["id"], size=12)),
                        ft.DataCell(ft.Text(item["edad"], size=12)),
                        ft.DataCell(ft.Text(item["genero"], size=12)),
                        ft.DataCell(ft.Text(item["pas"], size=12)),
                        ft.DataCell(ft.Text(item["pad"], size=12)),
                        ft.DataCell(ft.Text(item["imc"], size=12)),
                        ft.DataCell(ft.Text(item["medicamento"], size=12)),
                        ft.DataCell(ft.Text(item["fecha"], size=12)),
                    ]
                )
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Edad", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Género", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("PAS (mmHg)", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("PAD (mmHg)", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("IMC", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Medicamento", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD)),
            ],
            rows=rows,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
        )

    def run_ai_analysis(self, page):
        self.ai_results.visible = True
        page.update()

    def suggest_cleaning(self, page):
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("IA sugiere:\n1. Imputar edad faltante con mediana del grupo\n2. Verificar PAS=320 con expediente clínico\n3. Estandarizar género como M/F\n4. Convertir todas las fechas a formato YYYY-MM-DD"),
                action="OK"
            )
        )

    def validate_data(self, page):
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Validación IA completada:\n✓ Estructura de datos correcta\n✓ Tipos de variables apropiados\n⚠ Requiere limpieza adicional\n📊 Calidad actual: 73%"),
                action="OK"
            )
        )

    def highlight_missing(self, page):
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Resaltando valores faltantes..."), action="OK"))

    def highlight_outliers(self, page):
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Detectando outliers..."), action="OK"))

    def highlight_inconsistent(self, page):
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Identificando inconsistencias..."), action="OK"))

    def clean_data(self, page):
        self.data_cleaned = True
        # Actualizar tabla
        new_table = self.create_data_table()
        # Encontrar el contenedor de la tabla y actualizarlo
        for control in self.content_container.content.controls:
            if isinstance(control, ft.Card):
                for card_control in control.content.content.controls:
                    if isinstance(card_control, ft.Container) and hasattr(card_control, 'content') and isinstance(card_control.content, ft.DataTable):
                        card_control.content = new_table
                        break
        
        # Actualizar estadísticas
        self.missing_count.value = "0"
        self.outlier_count.value = "0"
        self.quality_score.value = "100%"
        
        page.show_snack_bar(ft.SnackBar(content=ft.Text("¡Datos limpiados exitosamente!"), action="OK"))
        page.update()

    def create_practice_section(self, page):
        # Variables para ejercicios
        self.exercise1_feedback = ft.Container(visible=False)
        self.exercise2_feedback = ft.Container(visible=False)
        self.exercise3_feedback = ft.Container(visible=False)
        
        return ft.Column([
            ft.Text("Práctica Guiada Paso a Paso", size=28, weight=ft.FontWeight.BOLD),
            
            # Ejercicio 1
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.SEARCH, color=ft.colors.BLUE_600),
                            ft.Text("Ejercicio 1: Identificación de Problemas de Calidad", 
                                    size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        ft.Text("Analiza el siguiente conjunto de datos y identifica todos los problemas de calidad que encuentres.", 
                                size=14),
                        
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("Paciente", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Edad", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Sexo", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Presión Sistólica", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Peso (kg)", weight=ft.FontWeight.BOLD)),
                            ],
                            rows=[
                                ft.DataRow(cells=[ft.DataCell(ft.Text("001")), ft.DataCell(ft.Text("45")), ft.DataCell(ft.Text("M")), ft.DataCell(ft.Text("140")), ft.DataCell(ft.Text("75"))]),
                                ft.DataRow(cells=[ft.DataCell(ft.Text("002")), ft.DataCell(ft.Text("")), ft.DataCell(ft.Text("Femenino")), ft.DataCell(ft.Text("320")), ft.DataCell(ft.Text("-10"))]),
                                ft.DataRow(cells=[ft.DataCell(ft.Text("003")), ft.DataCell(ft.Text("999")), ft.DataCell(ft.Text("F")), ft.DataCell(ft.Text("N/A")), ft.DataCell(ft.Text("68.5"))]),
                            ],
                            border=ft.border.all(1, ft.colors.GREY_400),
                        ),
                        
                        ft.Column([
                            ft.Checkbox(label="Valores faltantes en edad (Paciente 002)", value=False, 
                                       on_change=lambda e: self.update_exercise1_check("problem1", e.control.value)),
                            ft.Checkbox(label="Inconsistencia en codificación de sexo (M/F vs Femenino)", value=False,
                                       on_change=lambda e: self.update_exercise1_check("problem2", e.control.value)),
                            ft.Checkbox(label="Outlier en presión sistólica (320 mmHg)", value=False,
                                       on_change=lambda e: self.update_exercise1_check("problem3", e.control.value)),
                            ft.Checkbox(label="Valor imposible en peso (-10 kg)", value=False,
                                       on_change=lambda e: self.update_exercise1_check("problem4", e.control.value)),
                            ft.Checkbox(label="Edad codificada como valor perdido (999)", value=False,
                                       on_change=lambda e: self.update_exercise1_check("problem5", e.control.value)),
                        ]),
                        
                        ft.ElevatedButton(
                            "Verificar Respuestas",
                            icon=ft.icons.CHECK,
                            on_click=lambda _: self.check_exercise1(page),
                            bgcolor=ft.colors.BLUE_600,
                            color="white"
                        ),
                        
                        self.exercise1_feedback
                    ]),
                    padding=20,
                    bgcolor=ft.colors.BLUE_50
                )
            ),
            
            # Ejercicio 2
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.CLEANING_SERVICES, color=ft.colors.GREEN_600),
                            ft.Text("Ejercicio 2: Aplicación de Técnicas de Limpieza", 
                                    size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        ft.Text("Selecciona la técnica más apropiada para cada problema identificado:", size=14),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Problema: Valor faltante en edad del Paciente 002", weight=ft.FontWeight.BOLD),
                                ft.RadioGroup(
                                    content=ft.Column([
                                        ft.Radio(value="delete", label="Eliminar el registro completo"),
                                        ft.Radio(value="mean", label="Imputar con la media de edad"),
                                        ft.Radio(value="contact", label="Contactar al paciente para obtener el dato"),
                                    ]),
                                    on_change=lambda e: self.update_exercise2_solution("solution1", e.control.value)
                                )
                            ]),
                            padding=15,
                            bgcolor="white",
                            border=ft.border.all(2, ft.colors.GREEN_200),
                            border_radius=10
                        ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Problema: Presión arterial de 320 mmHg", weight=ft.FontWeight.BOLD),
                                ft.RadioGroup(
                                    content=ft.Column([
                                        ft.Radio(value="keep", label="Mantener el valor (podría ser real)"),
                                        ft.Radio(value="verify", label="Verificar con el expediente clínico"),
                                        ft.Radio(value="delete", label="Eliminar automáticamente"),
                                    ]),
                                    on_change=lambda e: self.update_exercise2_solution("solution2", e.control.value)
                                )
                            ]),
                            padding=15,
                            bgcolor="white",
                            border=ft.border.all(2, ft.colors.GREEN_200),
                            border_radius=10
                        ),
                        
                        ft.ElevatedButton(
                            "Verificar Soluciones",
                            icon=ft.icons.CHECK,
                            on_click=lambda _: self.check_exercise2(page),
                            bgcolor=ft.colors.GREEN_600,
                            color="white"
                        ),
                        
                        self.exercise2_feedback
                    ]),
                    padding=20,
                    bgcolor=ft.colors.GREEN_50
                )
            ),
            
            # Ejercicio 3
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.BOOK, color=ft.colors.PURPLE_600),
                            ft.Text("Ejercicio 3: Creación de Diccionario de Datos", 
                                    size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        ft.Text("Completa el diccionario de datos para la variable 'Estado Civil':", size=14),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Column([
                                        ft.Text("Nombre de la Variable:", weight=ft.FontWeight.BOLD, size=12),
                                        self.var_name_field := ft.TextField(hint_text="estado_civil", width=200)
                                    ], expand=True),
                                    ft.Column([
                                        ft.Text("Tipo de Variable:", weight=ft.FontWeight.BOLD, size=12),
                                        self.var_type_dropdown := ft.Dropdown(
                                            width=200,
                                            options=[
                                                ft.dropdown.Option("categorical", "Categórica"),
                                                ft.dropdown.Option("numerical", "Numérica"),
                                                ft.dropdown.Option("date", "Fecha"),
                                            ]
                                        )
                                    ], expand=True)
                                ]),
                                ft.Column([
                                    ft.Text("Valores Válidos:", weight=ft.FontWeight.BOLD, size=12),
                                    self.var_values_field := ft.TextField(
                                        hint_text="1 = Soltero, 2 = Casado, 3 = Divorciado, 4 = Viudo",
                                        multiline=True,
                                        min_lines=2,
                                        max_lines=3
                                    )
                                ]),
                                ft.Column([
                                    ft.Text("Descripción:", weight=ft.FontWeight.BOLD, size=12),
                                    self.var_description_field := ft.TextField(
                                        hint_text="Estado civil del paciente al momento del ingreso",
                                        multiline=True,
                                        min_lines=2,
                                        max_lines=3
                                    )
                                ])
                            ]),
                            padding=15,
                            bgcolor="white",
                            border=ft.border.all(2, ft.colors.PURPLE_200),
                            border_radius=10
                        ),
                        
                        ft.ElevatedButton(
                            "Validar Diccionario",
                            icon=ft.icons.CHECK,
                            on_click=lambda _: self.check_exercise3(page),
                            bgcolor=ft.colors.PURPLE_600,
                            color="white"
                        ),
                        
                        self.exercise3_feedback
                    ]),
                    padding=20,
                    bgcolor=ft.colors.PURPLE_50
                )
            ),
            
            ft.Container(
                content=ft.ElevatedButton(
                    "Continuar a la Evaluación",
                    icon=ft.icons.ARROW_FORWARD,
                    on_click=lambda _: self.show_section(page, "evaluation"),
                    bgcolor=ft.colors.ORANGE_600,
                    color="white"
                ),
                alignment=ft.alignment.center,
                padding=20
            )
        ], scroll=ft.ScrollMode.AUTO)

    def update_exercise1_check(self, problem, value):
        self.exercise1_checks[problem] = value

    def update_exercise2_solution(self, solution, value):
        self.exercise2_solutions[solution] = value

    def check_exercise1(self, page):
        correct_count = sum(1 for checked in self.exercise1_checks.values() if checked)
        
        if correct_count == 5:
            self.exercise1_feedback.content = ft.Container(
                content=ft.Column([
                    ft.Text("¡Excelente!", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                    ft.Text("Has identificado correctamente todos los problemas de calidad en los datos.", 
                            color=ft.colors.GREEN_700)
                ]),
                padding=15,
                bgcolor=ft.colors.GREEN_50,
                border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.GREEN_400)),
                border_radius=10
            )
        else:
            self.exercise1_feedback.content = ft.Container(
                content=ft.Column([
                    ft.Text("Revisa tu respuesta", weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW_800),
                    ft.Text(f"Has identificado {correct_count} de 5 problemas. Revisa los datos nuevamente.", 
                            color=ft.colors.YELLOW_700)
                ]),
                padding=15,
                bgcolor=ft.colors.YELLOW_50,
                border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400)),
                border_radius=10
            )
        
        self.exercise1_feedback.visible = True
        page.update()

    def check_exercise2(self, page):
        solution1 = self.exercise2_solutions.get("solution1")
        solution2 = self.exercise2_solutions.get("solution2")
        
        score = 0
        if solution1 == "contact":
            score += 1
        if solution2 == "verify":
            score += 1
        
        if score == 2:
            self.exercise2_feedback.content = ft.Container(
                content=ft.Column([
                    ft.Text("¡Perfecto!", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                    ft.Text("Has seleccionado las mejores estrategias de limpieza para cada problema.", 
                            color=ft.colors.GREEN_700)
                ]),
                padding=15,
                bgcolor=ft.colors.GREEN_50,
                border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.GREEN_400)),
                border_radius=10
            )
        else:
            self.exercise2_feedback.content = ft.Container(
                content=ft.Column([
                    ft.Text("Buena aproximación", weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_800),
                    ft.Text("Considera siempre verificar con fuentes primarias antes de eliminar o imputar datos.", 
                            color=ft.colors.ORANGE_700)
                ]),
                padding=15,
                bgcolor=ft.colors.ORANGE_50,
                border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.ORANGE_400)),
                border_radius=10
            )
        
        self.exercise2_feedback.visible = True
        page.update()

    def check_exercise3(self, page):
        var_name = self.var_name_field.value
        var_type = self.var_type_dropdown.value
        var_values = self.var_values_field.value
        var_description = self.var_description_field.value
        
        if var_name and var_type == "categorical" and var_values and var_description:
            self.exercise3_feedback.content = ft.Container(
                content=ft.Column([
                    ft.Text("¡Diccionario completo!", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                    ft.Text("Has creado un diccionario de datos completo y bien estructurado.", 
                            color=ft.colors.GREEN_700)
                ]),
                padding=15,
                bgcolor=ft.colors.GREEN_50,
                border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.GREEN_400)),
                border_radius=10
            )
        else:
            self.exercise3_feedback.content = ft.Container(
                content=ft.Column([
                    ft.Text("Información incompleta", weight=ft.FontWeight.BOLD, color=ft.colors.RED_800),
                    ft.Text("Completa todos los campos para crear un diccionario de datos válido.", 
                            color=ft.colors.RED_700)
                ]),
                padding=15,
                bgcolor=ft.colors.RED_50,
                border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.RED_400)),
                border_radius=10
            )
        
        self.exercise3_feedback.visible = True
        page.update()

    def create_evaluation_section(self, page):
        self.quiz_results = ft.Container(visible=False)
        
        return ft.Column([
            ft.Text("Evaluación Automatizada", size=28, weight=ft.FontWeight.BOLD),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.QUIZ, color=ft.colors.ORANGE_600),
                            ft.Text("Quiz: Calidad y Limpieza de Datos (3 preguntas)", 
                                    size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        # Pregunta 1
                        ft.Container(
                            content=ft.Column([
                                ft.Text("1. ¿Cuál es la diferencia entre MCAR y MAR?", 
                                        weight=ft.FontWeight.BOLD, size=14),
                                ft.RadioGroup(
                                    content=ft.Column([
                                        ft.Radio(value="a", label="MCAR significa que los datos faltantes son completamente aleatorios, MAR que dependen de variables observadas"),
                                        ft.Radio(value="b", label="No hay diferencia, ambos términos son sinónimos"),
                                        ft.Radio(value="c", label="MCAR es para variables categóricas, MAR para numéricas"),
                                    ]),
                                    on_change=lambda e: self.update_quiz_answer("q1", e.control.value)
                                )
                            ]),
                            padding=15,
                            bgcolor="white",
                            border=ft.border.all(2, ft.colors.ORANGE_200),
                            border_radius=10,
                            margin=ft.margin.only(bottom=10)
                        ),
                        
                        # Pregunta 2
                        ft.Container(
                            content=ft.Column([
                                ft.Text("2. ¿Cuál es el método más apropiado para detectar outliers univariados?", 
                                        weight=ft.FontWeight.BOLD, size=14),
                                ft.RadioGroup(
                                    content=ft.Column([
                                        ft.Radio(value="a", label="Regla del rango intercuartílico (IQR)"),
                                        ft.Radio(value="b", label="Análisis de componentes principales"),
                                        ft.Radio(value="c", label="Regresión lineal"),
                                    ]),
                                    on_change=lambda e: self.update_quiz_answer("q2", e.control.value)
                                )
                            ]),
                            padding=15,
                            bgcolor="white",
                            border=ft.border.all(2, ft.colors.ORANGE_200),
                            border_radius=10,
                            margin=ft.margin.only(bottom=10)
                        ),
                        
                        # Pregunta 3
                        ft.Container(
                            content=ft.Column([
                                ft.Text("3. En el contexto del modelo C(H)ANGE, ¿qué componente se relaciona más con la visualización de outliers?", 
                                        weight=ft.FontWeight.BOLD, size=14),
                                ft.RadioGroup(
                                    content=ft.Column([
                                        ft.Radio(value="a", label="Combinatoria (C)"),
                                        ft.Radio(value="b", label="Geometría (G)"),
                                        ft.Radio(value="c", label="Álgebra (A)"),
                                    ]),
                                    on_change=lambda e: self.update_quiz_answer("q3", e.control.value)
                                )
                            ]),
                            padding=15,
                            bgcolor="white",
                            border=ft.border.all(2, ft.colors.ORANGE_200),
                            border_radius=10,
                            margin=ft.margin.only(bottom=10)
                        ),
                        
                        ft.ElevatedButton(
                            "Enviar Quiz",
                            icon=ft.icons.SEND,
                            on_click=lambda _: self.submit_quiz(page),
                            bgcolor=ft.colors.ORANGE_600,
                            color="white"
                        ),
                        
                        self.quiz_results
                    ]),
                    padding=20,
                    bgcolor=ft.colors.ORANGE_50
                )
            ),
            
            # Ejercicio Práctico Final
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.LAPTOP, color=ft.colors.BLUE_600),
                            ft.Text("Ejercicio Práctico Final: Limpieza Completa de Dataset", 
                                    size=18, weight=ft.FontWeight.BOLD)
                        ]),
                        
                        ft.Text("Aplica todo lo aprendido para limpiar completamente el siguiente dataset de pacientes diabéticos:", 
                                size=14),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Dataset: Pacientes con Diabetes Tipo 2", weight=ft.FontWeight.BOLD),
                                ft.Text("Problemas identificados: 23 valores faltantes, 8 outliers, 15 inconsistencias de codificación", 
                                        size=12, color=ft.colors.GREY_600),
                                
                                ft.Row([
                                    ft.Column([
                                        ft.Text("Tareas a Realizar:", weight=ft.FontWeight.BOLD),
                                        ft.Checkbox(label="Identificar patrones de datos faltantes"),
                                        ft.Checkbox(label="Detectar y validar outliers"),
                                        ft.Checkbox(label="Estandarizar codificación"),
                                        ft.Checkbox(label="Crear diccionario de datos"),
                                        ft.Checkbox(label="Documentar proceso de limpieza"),
                                    ], expand=True),
                                    ft.Column([
                                        ft.Text("Criterios de Evaluación:", weight=ft.FontWeight.BOLD),
                                        ft.Text("• Correcta identificación de problemas (25%)", size=11),
                                        ft.Text("• Aplicación apropiada de técnicas (30%)", size=11),
                                        ft.Text("• Calidad del diccionario de datos (20%)", size=11),
                                        ft.Text("• Documentación del proceso (15%)", size=11),
                                        ft.Text("• Interpretación clínica (10%)", size=11),
                                    ], expand=True)
                                ])
                            ]),
                            padding=15,
                            bgcolor="white",
                            border=ft.border.all(2, ft.colors.BLUE_200),
                            border_radius=10
                        ),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                "Descargar Dataset",
                                icon=ft.icons.DOWNLOAD,
                                on_click=lambda _: self.download_dataset(page),
                                bgcolor=ft.colors.BLUE_600,
                                color="white"
                            ),
                            ft.ElevatedButton(
                                "Subir Solución",
                                icon=ft.icons.UPLOAD,
                                on_click=lambda _: self.submit_final_exercise(page),
                                bgcolor=ft.colors.GREEN_600,
                                color="white"
                            )
                        ])
                    ]),
                    padding=20,
                    bgcolor=ft.colors.BLUE_50
                )
            ),
            
            ft.Container(
                content=ft.ElevatedButton(
                    "Ver Recursos Descargables",
                    icon=ft.icons.ARROW_FORWARD,
                    on_click=lambda _: self.show_section(page, "resources"),
                    bgcolor=ft.colors.PURPLE_600,
                    color="white"
                ),
                alignment=ft.alignment.center,
                padding=20
            )
        ], scroll=ft.ScrollMode.AUTO)

    def update_quiz_answer(self, question, value):
        self.quiz_answers[question] = value

    def submit_quiz(self, page):
        correct_answers = {"q1": "a", "q2": "a", "q3": "b"}
        score = sum(1 for q, answer in self.quiz_answers.items() if answer == correct_answers.get(q))
        percentage = int((score / 3) * 100)
        
        feedback_text = []
        feedback_text.append(f"Pregunta 1: {'✓ Correcto' if self.quiz_answers.get('q1') == 'a' else '✗ Incorrecto - MCAR significa completamente aleatorio'}")
        feedback_text.append(f"Pregunta 2: {'✓ Correcto' if self.quiz_answers.get('q2') == 'a' else '✗ Incorrecto - La regla IQR es el método estándar'}")
        feedback_text.append(f"Pregunta 3: {'✓ Correcto' if self.quiz_answers.get('q3') == 'b' else '✗ Incorrecto - Geometría se relaciona con visualización'}")
        
        self.quiz_results.content = ft.Container(
            content=ft.Column([
                ft.Text("Resultados del Quiz", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                ft.Text(f"Puntuación: {score}/3 ({percentage}%)", color=ft.colors.GREEN_700),
                ft.Column([ft.Text(feedback, size=12) for feedback in feedback_text])
            ]),
            padding=15,
            bgcolor=ft.colors.GREEN_50,
            border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.GREEN_400)),
            border_radius=10
        )
        
        self.quiz_results.visible = True
        page.update()

    def download_dataset(self, page):
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Descargando dataset de práctica...\nArchivo: diabetes_dataset_dirty.csv\nTamaño: 2.3 MB"),
                action="OK"
            )
        )

    def submit_final_exercise(self, page):
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Función de envío de ejercicio final.\nEn un entorno real, esto subiría el archivo y lo evaluaría automáticamente."),
                action="OK"
            )
        )

    def create_resources_section(self, page):
        return ft.Column([
            ft.Text("Recursos Descargables", size=28, weight=ft.FontWeight.BOLD),
            
            ft.Row([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.icons.DESCRIPTION, color=ft.colors.BLUE_600),
                                ft.Text("Plantillas y Formularios", weight=ft.FontWeight.BOLD)
                            ]),
                            
                            ft.Container(
                                content=ft.Row([
                                    ft.Column([
                                        ft.Text("Plantilla de Diccionario de Datos", weight=ft.FontWeight.BOLD, size=12),
                                        ft.Text("Excel/CSV - Estructura estándar", size=10, color=ft.colors.GREY_600)
                                    ], expand=True),
                                    ft.ElevatedButton("Descargar", icon=ft.icons.DOWNLOAD, 
                                                    bgcolor=ft.colors.BLUE_600, color="white",
                                                    on_click=lambda _: page.show_snack_bar(ft.SnackBar(content=ft.Text("Descargando plantilla..."), action="OK")))
                                ]),
                                padding=10,
                                bgcolor="white",
                                border=ft.border.all(1, ft.colors.GREY_300),
                                border_radius=5,
                                margin=ft.margin.only(bottom=5)
                            ),
                            
                            ft.Container(
                                content=ft.Row([
                                    ft.Column([
                                        ft.Text("Checklist de Calidad de Datos", weight=ft.FontWeight.BOLD, size=12),
                                        ft.Text("PDF - Lista de verificación", size=10, color=ft.colors.GREY_600)
                                    ], expand=True),
                                    ft.ElevatedButton("Descargar", icon=ft.icons.DOWNLOAD, 
                                                    bgcolor=ft.colors.BLUE_600, color="white",
                                                    on_click=lambda _: page.show_snack_bar(ft.SnackBar(content=ft.Text("Descargando checklist..."), action="OK")))
                                ]),
                                padding=10,
                                bgcolor="white",
                                border=ft.border.all(1, ft.colors.GREY_300),
                                border_radius=5,
                                margin=ft.margin.only(bottom=5)
                            ),
                            
                            ft.Container(
                                content=ft.Row([
                                    ft.Column([
                                        ft.Text("Formulario de Reporte de Limpieza", weight=ft.FontWeight.BOLD, size=12),
                                        ft.Text("Word - Documentación estándar", size=10, color=ft.colors.GREY_600)
                                    ], expand=True),
                                    ft.ElevatedButton("Descargar", icon=ft.icons.DOWNLOAD, 
                                                    bgcolor=ft.colors.BLUE_600, color="white",
                                                    on_click=lambda _: page.show_snack_bar(ft.SnackBar(content=ft.Text("Descargando formulario..."), action="OK")))
                                ]),
                                padding=10,
                                bgcolor="white",
                                border=ft.border.all(1, ft.colors.GREY_300),
                                border_radius=5
                            )
                        ]),
                        padding=20,
                        bgcolor=ft.colors.BLUE_50
                    ),
                    expand=True
                ),
                
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.icons.CODE, color=ft.colors.GREEN_600),
                                ft.Text("Scripts y Códigos", weight=ft.FontWeight.BOLD)
                            ]),
                            
                            ft.Container(
                                content=ft.Row([
                                    ft.Column([
                                        ft.Text("Script Python - Detección de Outliers", weight=ft.FontWeight.BOLD, size=12),
                                        ft.Text("Python - Usando pandas y scipy", size=10, color=ft.colors.GREY_600)
                                    ], expand=True),
                                    ft.ElevatedButton("Descargar", icon=ft.icons.DOWNLOAD, 
                                                    bgcolor=ft.colors.GREEN_600, color="white",
                                                    on_click=lambda _: page.show_snack_bar(ft.SnackBar(content=ft.Text("Descargando script Python..."), action="OK")))
                                ]),
                                padding=10,
                                bgcolor="white",
                                border=ft.border.all(1, ft.colors.GREY_300),
                                border_radius=5,
                                margin=ft.margin.only(bottom=5)
                            ),
                            
                            ft.Container(
                                content=ft.Row([
                                    ft.Column([
                                        ft.Text("Script R - Análisis de Datos Faltantes", weight=ft.FontWeight.BOLD, size=12),
                                        ft.Text("R - Usando VIM y mice", size=10, color=ft.colors.GREY_600)
                                    ], expand=True),
                                    ft.ElevatedButton("Descargar", icon=ft.icons.DOWNLOAD, 
                                                    bgcolor=ft.colors.GREEN_600, color="white",
                                                    on_click=lambda _: page.show_snack_bar(ft.SnackBar(content=ft.Text("Descargando script R..."), action="OK")))
                                ]),
                                padding=10,
                                bgcolor="white",
                                border=ft.border.all(1, ft.colors.GREY_300),
                                border_radius=5,
                                margin=ft.margin.only(bottom=5)
                            ),
                            
                            ft.Container(
                                content=ft.Row([
                                    ft.Column([
                                        ft.Text("Notebook Jupyter - Flujo Completo", weight=ft.FontWeight.BOLD, size=12),
                                        ft.Text("Jupyter - Ejemplo paso a paso", size=10, color=ft.colors.GREY_600)
                                    ], expand=True),
                                    ft.ElevatedButton("Descargar", icon=ft.icons.DOWNLOAD, 
                                                    bgcolor=ft.colors.GREEN_600, color="white",
                                                    on_click=lambda _: page.show_snack_bar(ft.SnackBar(content=ft.Text("Descargando notebook..."), action="OK")))
                                ]),
                                padding=10,
                                bgcolor="white",
                                border=ft.border.all(1, ft.colors.GREY_300),
                                border_radius=5
                            )
                        ]),
                        padding=20,
                        bgcolor=ft.colors.GREEN_50
                    ),
                    expand=True
                )
            ]),
            
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.STORAGE, color=ft.colors.ORANGE_600),
                            ft.Text("Datasets de Práctica", weight=ft.FontWeight.BOLD)
                        ]),
                        
                        ft.Row([
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Text("Dataset Básico", weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_800),
                                        ft.Text("100 registros con problemas simples de calidad", size=12),
                                        ft.ElevatedButton("Descargar CSV", icon=ft.icons.DOWNLOAD, 
                                                        bgcolor=ft.colors.ORANGE_600, color="white",
                                                        on_click=lambda _: page.show_snack_bar(ft.SnackBar(content=ft.Text("Descargando dataset básico..."), action="OK")))
                                    ]),
                                    padding=15,
                                    bgcolor=ft.colors.ORANGE_50
                                ),
                                expand=True
                            ),
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Text("Dataset Intermedio", weight=ft.FontWeight.BOLD, color=ft.colors.RED_800),
                                        ft.Text("500 registros con múltiples tipos de problemas", size=12),
                                        ft.ElevatedButton("Descargar CSV", icon=ft.icons.DOWNLOAD, 
                                                        bgcolor=ft.colors.RED_600, color="white",
                                                        on_click=lambda _: page.show_snack_bar(ft.SnackBar(content=ft.Text("Descargando dataset intermedio..."), action="OK")))
                                    ]),
                                    padding=15,
                                    bgcolor=ft.colors.RED_50
                                ),
                                expand=True
                            ),
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column([
                                        ft.Text("Dataset Avanzado", weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_800),
                                        ft.Text("1000+ registros con problemas complejos", size=12),
                                        ft.ElevatedButton("Descargar CSV", icon=ft.icons.DOWNLOAD, 
                                                        bgcolor=ft.colors.PURPLE_600, color="white",
                                                        on_click=lambda _: page.show_snack_bar(ft.SnackBar(content=ft.Text("Descargando dataset avanzado..."), action="OK")))
                                    ]),
                                    padding=15,
                                    bgcolor=ft.colors.PURPLE_50
                                ),
                                expand=True
                            )
                        ])
                    ]),
                    padding=20
                )
            ),
            
            # Certificado de Finalización
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.icons.EMOJI_EVENTS, color=ft.colors.YELLOW_600, size=40),
                            ft.Column([
                                ft.Text("Certificado de Finalización", size=20, weight=ft.FontWeight.BOLD),
                                ft.Text("¡Felicitaciones! Has completado exitosamente el OVA de Calidad y Limpieza de Datos Clínicos.", 
                                        size=14)
                            ], expand=True)
                        ]),
                        
                        ft.Container(
                            content=ft.ElevatedButton(
                                "Generar Certificado",
                                icon=ft.icons.CARD_MEMBERSHIP,
                                on_click=lambda _: self.generate_certificate(page),
                                bgcolor=ft.colors.YELLOW_600,
                                color="white"
                            ),
                            alignment=ft.alignment.center,
                            padding=20
                        )
                    ]),
                    padding=20,
                    bgcolor=ft.colors.YELLOW_50
                )
            )
        ], scroll=ft.ScrollMode.AUTO)

    def generate_certificate(self, page):
        current_date = datetime.now().strftime("%d/%m/%Y")
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(f"Generando certificado de finalización...\n\nCertificado digital generado exitosamente.\nNombre: [Nombre del estudiante]\nCurso: Calidad y Limpieza de Datos Clínicos\nFecha: {current_date}"),
                action="OK"
            )
        )

def main(page: ft.Page):
    app = OVAApp()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)
