
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
                           size=24, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800),
                    ft.Text("Estadística Descriptiva para Ciencias de la Salud", 
                           size=16, color=ft.colors.GREY_600)
                ], expand=True),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Modelo C(H)ANGE", size=12, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                        ft.Text("Duración: 2-4 horas", size=10, color=ft.colors.BLUE_600)
                    ]),
                    bgcolor=ft.colors.BLUE_100,
                    padding=10,
                    border_radius=8
                )
            ]),
            bgcolor=ft.colors.WHITE,
            padding=20,
            border=ft.border.only(bottom=ft.border.BorderSide(4, ft.colors.BLUE_500))
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
                    bgcolor=ft.colors.BLUE_600 if section == self.current_section else ft.colors.BLUE_400,
                    color=ft.colors.WHITE
                ) for section, label in nav_buttons
            ], scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.colors.BLUE_600,
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
                    bgcolor=ft.colors.BLUE_GREY_50
                )
            ], expand=True)
        )
    
    def show_section(self, section):
        self.current_section = section
        
        # Update navigation buttons
        nav_container = self.page.controls[0].controls[1]
        for i, (sect, _) in enumerate([("intro", "Introducción"), ("theory", "Teoría"), 
                                      ("practice", "Práctica"), ("simulation", "Simulación"), 
                                      ("evaluation", "Evaluación"), ("resources", "Recursos")]):
            nav_container.content.controls[i].bgcolor = ft.colors.BLUE_600 if sect == section else ft.colors.BLUE_400
        
        # Update main content
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
        return ft.Container(
            content=ft.Column([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("1", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                                    bgcolor=ft.colors.BLUE_500,
                                    width=32,
                                    height=32,
                                    border_radius=16,
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("Introducción y Objetivos", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800)
                            ]),
                            ft.Divider(),
                            ft.Row([
                                ft.Column([
                                    ft.Text("¿Por qué comparar grupos en salud?", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_700),
                                    ft.Text(
                                        "En ciencias de la salud, constantemente necesitamos comparar diferentes grupos de pacientes, "
                                        "tratamientos, o poblaciones para entender patrones, identificar diferencias y tomar decisiones "
                                        "clínicas informadas.",
                                        color=ft.colors.GREY_600
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Ejemplos clínicos:", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                            ft.Text("• Comparar presión arterial entre hombres y mujeres", color=ft.colors.BLUE_700),
                                            ft.Text("• Analizar tiempo de recuperación por grupos de edad", color=ft.colors.BLUE_700),
                                            ft.Text("• Evaluar efectividad de diferentes tratamientos", color=ft.colors.BLUE_700),
                                            ft.Text("• Estudiar prevalencia de enfermedades por región", color=ft.colors.BLUE_700)
                                        ]),
                                        bgcolor=ft.colors.BLUE_50,
                                        padding=15,
                                        border_radius=8
                                    )
                                ], expand=True),
                                ft.Column([
                                    ft.Text("Objetivos de Aprendizaje", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_700),
                                    ft.Column([
                                        self.create_objective_item("Contrastar perfiles de dos o más cohortes sin inferencia estadística"),
                                        self.create_objective_item("Calcular resúmenes descriptivos por grupo"),
                                        self.create_objective_item("Interpretar diferencias absolutas entre grupos"),
                                        self.create_objective_item("Calcular tamaños de efecto descriptivos")
                                    ])
                                ], expand=True)
                            ]),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.icons.WARNING, color=ft.colors.YELLOW_600),
                                    ft.Column([
                                        ft.Text("Importante:", weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW_700),
                                        ft.Text(
                                            "En esta OVA nos enfocamos en análisis descriptivo. "
                                            "No realizaremos pruebas de significancia estadística ni inferencias causales.",
                                            color=ft.colors.YELLOW_700
                                        )
                                    ], expand=True)
                                ]),
                                bgcolor=ft.colors.YELLOW_50,
                                padding=15,
                                border_radius=8,
                                border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.YELLOW_400))
                            )
                        ]),
                        padding=20
                    )
                )
            ], scroll=ft.ScrollMode.AUTO),
            expand=True
        )
    
    def create_objective_item(self, text):
        return ft.Row([
            ft.Container(
                content=ft.Text("✓", color=ft.colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
                bgcolor=ft.colors.GREEN_500,
                width=24,
                height=24,
                border_radius=12,
                alignment=ft.alignment.center
            ),
            ft.Text(text, color=ft.colors.GREY_600, expand=True)
        ])
    
    def create_theory_section(self):
        return ft.Container(
            content=ft.Column([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("2", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                                    bgcolor=ft.colors.BLUE_500,
                                    width=32,
                                    height=32,
                                    border_radius=16,
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("Fundamentos Teóricos", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800)
                            ]),
                            ft.Divider(),
                            ft.Row([
                                self.create_theory_card(
                                    "Resúmenes por Grupo",
                                    "Calculamos medidas de tendencia central y dispersión para cada grupo por separado.",
                                    "• Media, mediana, moda\n• Desviación estándar\n• Rango intercuartílico\n• Percentiles",
                                    ft.colors.BLUE_50
                                ),
                                self.create_theory_card(
                                    "Diferencias Absolutas",
                                    "Calculamos la diferencia directa entre las medidas de los grupos.",
                                    "Diferencia = Grupo A - Grupo B\n\nEjemplo:\nMedia PA Hombres: 130 mmHg\nMedia PA Mujeres: 125 mmHg\nDiferencia: 5 mmHg",
                                    ft.colors.GREEN_50
                                ),
                                self.create_theory_card(
                                    "Tamaño del Efecto",
                                    "Medida estandarizada que permite comparar diferencias independientemente de las unidades.",
                                    "d de Cohen:\nd = (Media₁ - Media₂) / DE_pooled\n\nInterpretación:\n• 0.2: Pequeño\n• 0.5: Mediano\n• 0.8: Grande",
                                    ft.colors.PURPLE_50
                                )
                            ]),
                            ft.Divider(),
                            ft.Text("Caso de Estudio: Presión Arterial por Sexo", size=18, weight=ft.FontWeight.BOLD),
                            ft.Row([
                                ft.Column([
                                    ft.Text("Datos Simulados", weight=ft.FontWeight.BOLD),
                                    ft.DataTable(
                                        columns=[
                                            ft.DataColumn(ft.Text("Grupo")),
                                            ft.DataColumn(ft.Text("n")),
                                            ft.DataColumn(ft.Text("Media")),
                                            ft.DataColumn(ft.Text("DE"))
                                        ],
                                        rows=[
                                            ft.DataRow(cells=[
                                                ft.DataCell(ft.Text("Hombres")),
                                                ft.DataCell(ft.Text("150")),
                                                ft.DataCell(ft.Text("132.5")),
                                                ft.DataCell(ft.Text("15.2"))
                                            ]),
                                            ft.DataRow(cells=[
                                                ft.DataCell(ft.Text("Mujeres")),
                                                ft.DataCell(ft.Text("180")),
                                                ft.DataCell(ft.Text("127.8")),
                                                ft.DataCell(ft.Text("14.8"))
                                            ])
                                        ]
                                    )
                                ], expand=True),
                                ft.Column([
                                    ft.Text("Análisis Descriptivo", weight=ft.FontWeight.BOLD),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Diferencia absoluta: 132.5 - 127.8 = 4.7 mmHg", weight=ft.FontWeight.BOLD),
                                            ft.Text("Diferencia relativa: (4.7/127.8) × 100 = 3.7%"),
                                            ft.Text("d de Cohen: 4.7/15.0 = 0.31 (efecto pequeño-mediano)"),
                                            ft.Text(
                                                "Interpretación clínica: Los hombres muestran una presión arterial sistólica "
                                                "promedio 4.7 mmHg mayor que las mujeres en esta muestra.",
                                                color=ft.colors.BLUE_600
                                            )
                                        ]),
                                        bgcolor=ft.colors.WHITE,
                                        padding=15,
                                        border_radius=8,
                                        border=ft.border.all(1, ft.colors.GREY_300)
                                    )
                                ], expand=True)
                            ])
                        ]),
                        padding=20
                    )
                )
            ], scroll=ft.ScrollMode.AUTO),
            expand=True
        )
    
    def create_theory_card(self, title, description, details, bg_color):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD),
                ft.Text(description, size=12),
                ft.Container(
                    content=ft.Text(details, size=10),
                    bgcolor=ft.colors.WHITE,
                    padding=10,
                    border_radius=5
                )
            ]),
            bgcolor=bg_color,
            padding=15,
            border_radius=8,
            expand=True
        )
    
    def create_practice_section(self):
        # Controles para mostrar resultados
        self.stats_results = ft.Column(visible=False)
        self.diff_results = ft.Column(visible=False)
        self.clinical_interpretation = ft.Text("Complete los cálculos para ver la interpretación clínica de los resultados.")
        
        return ft.Container(
            content=ft.Column([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("3", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                                    bgcolor=ft.colors.BLUE_500,
                                    width=32,
                                    height=32,
                                    border_radius=16,
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("Práctica Guiada", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800)
                            ]),
                            ft.Divider(),
                            ft.Text("Ejercicio: Tiempo de Recuperación por Grupo de Edad", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text("Analicemos el tiempo de recuperación (en días) después de una cirugía en dos grupos de edad diferentes."),
                            ft.Row([
                                ft.Column([
                                    ft.Text("Datos del Estudio", weight=ft.FontWeight.BOLD),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Grupo Joven (18-40 años):", weight=ft.FontWeight.BOLD),
                                            ft.Text("8, 7, 9, 6, 8, 7, 10, 8, 9, 7, 8, 6, 9, 8, 7", 
                                                   style=ft.TextStyle(font_family="monospace")),
                                            ft.Text("Grupo Mayor (60+ años):", weight=ft.FontWeight.BOLD),
                                            ft.Text("12, 14, 11, 13, 15, 12, 16, 13, 14, 12, 15, 13, 14, 11, 13",
                                                   style=ft.TextStyle(font_family="monospace"))
                                        ]),
                                        bgcolor=ft.colors.GREY_100,
                                        padding=15,
                                        border_radius=8
                                    ),
                                    ft.Column([
                                        ft.Text("Paso 1: Calcular estadísticos descriptivos", weight=ft.FontWeight.BOLD),
                                        ft.ElevatedButton(
                                            text="Calcular Estadísticos",
                                            on_click=self.calculate_stats,
                                            bgcolor=ft.colors.BLUE_500,
                                            color=ft.colors.WHITE
                                        ),
                                        self.stats_results,
                                        ft.Text("Paso 2: Calcular diferencias", weight=ft.FontWeight.BOLD),
                                        ft.ElevatedButton(
                                            text="Calcular Diferencias",
                                            on_click=self.calculate_differences,
                                            bgcolor=ft.colors.GREEN_500,
                                            color=ft.colors.WHITE
                                        ),
                                        self.diff_results
                                    ])
                                ], expand=True),
                                ft.Column([
                                    ft.Text("Visualización", weight=ft.FontWeight.BOLD),
                                    ft.Container(
                                        content=ft.Text("Los gráficos se mostrarán después de calcular los estadísticos"),
                                        bgcolor=ft.colors.WHITE,
                                        padding=20,
                                        border_radius=8,
                                        border=ft.border.all(1, ft.colors.GREY_300),
                                        height=200
                                    ),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Interpretación Clínica", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                            self.clinical_interpretation
                                        ]),
                                        bgcolor=ft.colors.BLUE_50,
                                        padding=15,
                                        border_radius=8
                                    )
                                ], expand=True)
                            ])
                        ]),
                        padding=20
                    )
                )
            ], scroll=ft.ScrollMode.AUTO),
            expand=True
        )
    
    def calculate_stats(self, e):
        young_stats = self.calculate_descriptive_stats(self.young_group)
        older_stats = self.calculate_descriptive_stats(self.older_group)
        
        stats_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Estadístico")),
                ft.DataColumn(ft.Text("Grupo Joven")),
                ft.DataColumn(ft.Text("Grupo Mayor"))
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("n")),
                    ft.DataCell(ft.Text(str(len(self.young_group)))),
                    ft.DataCell(ft.Text(str(len(self.older_group))))
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Media")),
                    ft.DataCell(ft.Text(f"{young_stats['mean']:.1f}")),
                    ft.DataCell(ft.Text(f"{older_stats['mean']:.1f}"))
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Mediana")),
                    ft.DataCell(ft.Text(f"{young_stats['median']:.1f}")),
                    ft.DataCell(ft.Text(f"{older_stats['median']:.1f}"))
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("DE")),
                    ft.DataCell(ft.Text(f"{young_stats['sd']:.1f}")),
                    ft.DataCell(ft.Text(f"{older_stats['sd']:.1f}"))
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Mín")),
                    ft.DataCell(ft.Text(str(young_stats['min']))),
                    ft.DataCell(ft.Text(str(older_stats['min'])))
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Máx")),
                    ft.DataCell(ft.Text(str(young_stats['max']))),
                    ft.DataCell(ft.Text(str(older_stats['max'])))
                ])
            ]
        )
        
        self.stats_results.controls = [
            ft.Text("Resultados:", weight=ft.FontWeight.BOLD),
            stats_table
        ]
        self.stats_results.visible = True
        self.page.update()
    
    def calculate_differences(self, e):
        young_mean = 7.7
        older_mean = 13.1
        young_sd = 1.2
        older_sd = 1.5
        
        absolute_diff = older_mean - young_mean
        relative_diff = (absolute_diff / young_mean) * 100
        pooled_sd = math.sqrt(((young_sd ** 2) + (older_sd ** 2)) / 2)
        cohen_d = absolute_diff / pooled_sd
        
        diff_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Medida")),
                ft.DataColumn(ft.Text("Valor"))
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Diferencia absoluta")),
                    ft.DataCell(ft.Text(f"{absolute_diff:.1f} días", weight=ft.FontWeight.BOLD))
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Diferencia relativa")),
                    ft.DataCell(ft.Text(f"{relative_diff:.1f}%"))
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("d de Cohen")),
                    ft.DataCell(ft.Text(f"{cohen_d:.2f} (efecto muy grande)"))
                ])
            ]
        )
        
        self.diff_results.controls = [
            ft.Text("Análisis de Diferencias:", weight=ft.FontWeight.BOLD),
            diff_table
        ]
        self.diff_results.visible = True
        
        # Actualizar interpretación clínica
        interpretation = (
            f"Interpretación: Los pacientes del grupo mayor (60+ años) requieren en promedio "
            f"{absolute_diff:.1f} días adicionales de recuperación comparado con el grupo joven (18-40 años). "
            f"Esta diferencia representa un {relative_diff:.1f}% más de tiempo de recuperación. "
            f"El tamaño del efecto (d = {cohen_d:.2f}) indica una diferencia muy grande y clínicamente significativa, "
            f"lo que sugiere que la edad es un factor importante a considerar en la planificación del alta hospitalaria."
        )
        
        self.clinical_interpretation.value = interpretation
        self.clinical_interpretation.color = ft.colors.BLUE_700
        
        self.page.update()
    
    def calculate_descriptive_stats(self, data):
        sorted_data = sorted(data)
        n = len(data)
        mean = sum(data) / n
        median = statistics.median(data)
        variance = sum((x - mean) ** 2 for x in data) / (n - 1)
        sd = math.sqrt(variance)
        
        return {
            'mean': mean,
            'median': median,
            'sd': sd,
            'min': min(data),
            'max': max(data)
        }
    
    def create_simulation_section(self):
        # Controles para la simulación
        self.mean1_slider = ft.Slider(min=50, max=150, value=100, divisions=100, label="{value}")
        self.sd1_slider = ft.Slider(min=5, max=30, value=15, divisions=25, label="{value}")
        self.mean2_slider = ft.Slider(min=50, max=150, value=110, divisions=100, label="{value}")
        self.sd2_slider = ft.Slider(min=5, max=30, value=15, divisions=25, label="{value}")
        self.sample_size_slider = ft.Slider(min=20, max=200, value=50, divisions=180, label="{value}")
        
        self.sim_stats = ft.Text("Ejecute la simulación para ver los resultados.")
        self.sim_differences = ft.Text("Ejecute la simulación para ver el análisis.")
        
        return ft.Container(
            content=ft.Column([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("4", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                                    bgcolor=ft.colors.BLUE_500,
                                    width=32,
                                    height=32,
                                    border_radius=16,
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("Simulación Interactiva", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800)
                            ]),
                            ft.Divider(),
                            ft.Text("Simulador de Comparaciones entre Grupos", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text("Explore cómo diferentes parámetros afectan las comparaciones entre grupos usando datos simulados."),
                            ft.Row([
                                ft.Column([
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Parámetros de Simulación", weight=ft.FontWeight.BOLD),
                                            ft.Text("Grupo 1 - Media:"),
                                            self.mean1_slider,
                                            ft.Text("Grupo 1 - Desviación Estándar:"),
                                            self.sd1_slider,
                                            ft.Text("Grupo 2 - Media:"),
                                            self.mean2_slider,
                                            ft.Text("Grupo 2 - Desviación Estándar:"),
                                            self.sd2_slider,
                                            ft.Text("Tamaño de muestra (cada grupo):"),
                                            self.sample_size_slider,
                                            ft.ElevatedButton(
                                                text="Ejecutar Simulación",
                                                on_click=self.run_simulation,
                                                bgcolor=ft.colors.PURPLE_500,
                                                color=ft.colors.WHITE
                                            )
                                        ]),
                                        bgcolor=ft.colors.GREY_100,
                                        padding=20,
                                        border_radius=8
                                    )
                                ], expand=1),
                                ft.Column([
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Distribuciones Simuladas", weight=ft.FontWeight.BOLD),
                                            ft.Container(
                                                content=ft.Text("Ejecute la simulación para ver los gráficos"),
                                                height=200,
                                                bgcolor=ft.colors.WHITE,
                                                border_radius=8,
                                                padding=20
                                            )
                                        ]),
                                        bgcolor=ft.colors.WHITE,
                                        padding=15,
                                        border_radius=8,
                                        border=ft.border.all(1, ft.colors.GREY_300)
                                    ),
                                    ft.Row([
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Text("Estadísticos Descriptivos", weight=ft.FontWeight.BOLD),
                                                self.sim_stats
                                            ]),
                                            bgcolor=ft.colors.WHITE,
                                            padding=15,
                                            border_radius=8,
                                            border=ft.border.all(1, ft.colors.GREY_300),
                                            expand=True
                                        ),
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Text("Análisis de Diferencias", weight=ft.FontWeight.BOLD),
                                                self.sim_differences
                                            ]),
                                            bgcolor=ft.colors.WHITE,
                                            padding=15,
                                            border_radius=8,
                                            border=ft.border.all(1, ft.colors.GREY_300),
                                            expand=True
                                        )
                                    ])
                                ], expand=2)
                            ])
                        ]),
                        padding=20
                    )
                )
            ], scroll=ft.ScrollMode.AUTO),
            expand=True
        )
    
    def run_simulation(self, e):
        mean1 = self.mean1_slider.value
        sd1 = self.sd1_slider.value
        mean2 = self.mean2_slider.value
        sd2 = self.sd2_slider.value
        n = int(self.sample_size_slider.value)
        
        # Generar datos simulados
        group1 = np.random.normal(mean1, sd1, n)
        group2 = np.random.normal(mean2, sd2, n)
        
        # Calcular estadísticos
        stats1 = self.calculate_descriptive_stats(group1.tolist())
        stats2 = self.calculate_descriptive_stats(group2.tolist())
        
        # Mostrar estadísticos
        stats_text = f"""Grupo 1:
Media: {stats1['mean']:.1f}
DE: {stats1['sd']:.1f}
Mediana: {stats1['median']:.1f}

Grupo 2:
Media: {stats2['mean']:.1f}
DE: {stats2['sd']:.1f}
Mediana: {stats2['median']:.1f}"""
        
        self.sim_stats.value = stats_text
        
        # Calcular diferencias
        absolute_diff = stats2['mean'] - stats1['mean']
        relative_diff = (absolute_diff / stats1['mean']) * 100
        pooled_sd = math.sqrt(((stats1['sd'] ** 2) + (stats2['sd'] ** 2)) / 2)
        cohen_d = absolute_diff / pooled_sd
        
        effect_size = 'pequeño'
        if abs(cohen_d) >= 0.8:
            effect_size = 'grande'
        elif abs(cohen_d) >= 0.5:
            effect_size = 'mediano'
        
        diff_text = f"""Diferencia absoluta: {absolute_diff:.1f}
Diferencia relativa: {relative_diff:.1f}%
d de Cohen: {cohen_d:.2f}
Tamaño del efecto: {effect_size}"""
        
        self.sim_differences.value = diff_text
        
        self.page.update()
    
    def create_evaluation_section(self):
        # Controles para evaluación
        self.q1_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="a", label="60 mg/dL"),
                ft.Radio(value="b", label="70 mg/dL"),
                ft.Radio(value="c", label="80 mg/dL")
            ])
        )
        
        self.q2_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="a", label="Es una diferencia pequeña y clínicamente irrelevante"),
                ft.Radio(value="b", label="Es una diferencia grande y clínicamente significativa"),
                ft.Radio(value="c", label="No se puede interpretar sin más información")
            ])
        )
        
        self.q3_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="a", label="d ≈ 3.5 (efecto muy grande)"),
                ft.Radio(value="b", label="d ≈ 1.2 (efecto grande)"),
                ft.Radio(value="c", label="d ≈ 0.8 (efecto mediano)")
            ])
        )
        
        self.feedback_q1 = ft.Text(visible=False)
        self.feedback_q2 = ft.Text(visible=False)
        self.feedback_q3 = ft.Text(visible=False)
        
        # Ejercicio práctico
        self.diff_calc = ft.TextField(label="Diferencia absoluta", width=200)
        self.rel_diff_calc = ft.TextField(label="Diferencia relativa (%)", width=200)
        self.cohen_calc = ft.TextField(label="d de Cohen (aproximada)", width=200)
        self.interpretation = ft.TextField(
            label="Interpretación clínica",
            multiline=True,
            min_lines=4,
            max_lines=6
        )
        self.practical_feedback = ft.Text(visible=False)
        
        self.final_score = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
        
        return ft.Container(
            content=ft.Column([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("5", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                                    bgcolor=ft.colors.BLUE_500,
                                    width=32,
                                    height=32,
                                    border_radius=16,
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("Evaluación Automatizada", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800)
                            ]),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Text(
                                    "Instrucciones: Responda las siguientes preguntas basadas en el caso clínico presentado. "
                                    "Recibirá retroalimentación inmediata para cada respuesta.",
                                    color=ft.colors.BLUE_700
                                ),
                                bgcolor=ft.colors.BLUE_50,
                                padding=15,
                                border_radius=8,
                                border=ft.border.only(left=ft.border.BorderSide(4, ft.colors.BLUE_400))
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Caso Clínico: Niveles de Glucosa", weight=ft.FontWeight.BOLD),
                                    ft.Text("Un estudio comparó los niveles de glucosa en sangre (mg/dL) entre pacientes diabéticos y no diabéticos:"),
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Column([
                                                ft.Text("No Diabéticos (n=100):", weight=ft.FontWeight.BOLD),
                                                ft.Text("Media: 95 mg/dL"),
                                                ft.Text("DE: 12 mg/dL")
                                            ], expand=True),
                                            ft.Column([
                                                ft.Text("Diabéticos (n=80):", weight=ft.FontWeight.BOLD),
                                                ft.Text("Media: 165 mg/dL"),
                                                ft.Text("DE: 25 mg/dL")
                                            ], expand=True)
                                        ]),
                                        bgcolor=ft.colors.WHITE,
                                        padding=15,
                                        border_radius=8,
                                        border=ft.border.all(1, ft.colors.GREY_300)
                                    ),
                                    ft.Text("1. ¿Cuál es la diferencia absoluta en los niveles promedio de glucosa?", weight=ft.FontWeight.BOLD),
                                    self.q1_group,
                                    ft.ElevatedButton(
                                        text="Verificar Respuesta",
                                        on_click=lambda e: self.check_answer('q1', 'b', '70 mg/dL es correcto. Se calcula: 165 - 95 = 70 mg/dL'),
                                        bgcolor=ft.colors.BLUE_500,
                                        color=ft.colors.WHITE
                                    ),
                                    self.feedback_q1,
                                    ft.Text("2. ¿Cómo interpretaría clínicamente esta diferencia?", weight=ft.FontWeight.BOLD),
                                    self.q2_group,
                                    ft.ElevatedButton(
                                        text="Verificar Respuesta",
                                        on_click=lambda e: self.check_answer('q2', 'b', 'Correcto. Una diferencia de 70 mg/dL en glucosa es clínicamente muy significativa, ya que refleja la diferencia entre niveles normales y diabéticos.'),
                                        bgcolor=ft.colors.BLUE_500,
                                        color=ft.colors.WHITE
                                    ),
                                    self.feedback_q2,
                                    ft.Text("3. Calcule aproximadamente la d de Cohen para este caso:", weight=ft.FontWeight.BOLD),
                                    self.q3_group,
                                    ft.ElevatedButton(
                                        text="Verificar Respuesta",
                                        on_click=lambda e: self.check_answer('q3', 'a', 'Correcto. d = 70/20 ≈ 3.5, donde 20 es aproximadamente la DE pooled. Este es un efecto muy grande.'),
                                        bgcolor=ft.colors.BLUE_500,
                                        color=ft.colors.WHITE
                                    ),
                                    self.feedback_q3
                                ]),
                                bgcolor=ft.colors.GREY_100,
                                padding=20,
                                border_radius=8
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Ejercicio Práctico: Análisis Completo", weight=ft.FontWeight.BOLD),
                                    ft.Text("Complete el siguiente análisis de comparación entre grupos:"),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Datos: Tiempo de espera en urgencias (minutos)", weight=ft.FontWeight.BOLD),
                                            ft.Text("Turno Día (n=50): Media = 45, DE = 12", weight=ft.FontWeight.BOLD),
                                            ft.Text("Turno Noche (n=45): Media = 62, DE = 18", weight=ft.FontWeight.BOLD)
                                        ]),
                                        bgcolor=ft.colors.WHITE,
                                        padding=15,
                                        border_radius=8,
                                        border=ft.border.all(1, ft.colors.GREY_300)
                                    ),
                                    ft.Row([
                                        ft.Column([
                                            ft.Text("Cálculos:", weight=ft.FontWeight.BOLD),
                                            self.diff_calc,
                                            self.rel_diff_calc,
                                            self.cohen_calc
                                        ], expand=True),
                                        ft.Column([
                                            ft.Text("Interpretación:", weight=ft.FontWeight.BOLD),
                                            self.interpretation
                                        ], expand=True)
                                    ]),
                                    ft.ElevatedButton(
                                        text="Verificar Ejercicio",
                                        on_click=self.check_practical_exercise,
                                        bgcolor=ft.colors.GREEN_500,
                                        color=ft.colors.WHITE
                                    ),
                                    self.practical_feedback
                                ]),
                                bgcolor=ft.colors.GREEN_50,
                                padding=20,
                                border_radius=8
                            ),
                            self.final_score
                        ]),
                        padding=20
                    )
                )
            ], scroll=ft.ScrollMode.AUTO),
            expand=True
        )
    
    def check_answer(self, question_id, correct_answer, feedback):
        if question_id == 'q1':
            selected = self.q1_group.value
            feedback_control = self.feedback_q1
        elif question_id == 'q2':
            selected = self.q2_group.value
            feedback_control = self.feedback_q2
        elif question_id == 'q3':
            selected = self.q3_group.value
            feedback_control = self.feedback_q3
        
        if not selected:
            feedback_control.value = "Por favor seleccione una respuesta."
            feedback_control.color = ft.colors.YELLOW_700
            feedback_control.visible = True
            self.page.update()
            return
        
        self.total_questions += 1
        
        if selected == correct_answer:
            self.score += 1
            feedback_control.value = f"✓ Correcto! {feedback}"
            feedback_control.color = ft.colors.GREEN_700
        else:
            feedback_control.value = f"✗ Incorrecto. {feedback}"
            feedback_control.color = ft.colors.RED_700
        
        feedback_control.visible = True
        self.update_final_score()
        self.page.update()
    
    def check_practical_exercise(self, e):
        try:
            diff_calc = float(self.diff_calc.value) if self.diff_calc.value else 0
            rel_diff_calc = float(self.rel_diff_calc.value) if self.rel_diff_calc.value else 0
            cohen_calc = float(self.cohen_calc.value) if self.cohen_calc.value else 0
            interpretation = self.interpretation.value
            
            feedback = "Retroalimentación:\n"
            
            # Verificar cálculos
            correct_diff = 17  # 62 - 45
            correct_rel_diff = 37.8  # (17/45) * 100
            correct_cohen = 1.1  # aproximadamente
            
            if abs(diff_calc - correct_diff) <= 1:
                feedback += "✓ Diferencia absoluta correcta (17 minutos)\n"
            else:
                feedback += "✗ Diferencia absoluta: debería ser 62 - 45 = 17 minutos\n"
            
            if abs(rel_diff_calc - correct_rel_diff) <= 2:
                feedback += "✓ Diferencia relativa correcta (~37.8%)\n"
            else:
                feedback += "✗ Diferencia relativa: (17/45) × 100 = 37.8%\n"
            
            if abs(cohen_calc - correct_cohen) <= 0.2:
                feedback += "✓ d de Cohen aproximadamente correcta (~1.1)\n"
            else:
                feedback += "✗ d de Cohen: aproximadamente 17/15 = 1.1 (efecto grande)\n"
            
            if len(interpretation) > 50:
                feedback += "✓ Interpretación proporcionada"
            else:
                feedback += "✗ La interpretación debe ser más detallada"
            
            self.practical_feedback.value = feedback
            self.practical_feedback.color = ft.colors.BLUE_700
            self.practical_feedback.visible = True
            
        except ValueError:
            self.practical_feedback.value = "Error: Por favor ingrese valores numéricos válidos."
            self.practical_feedback.color = ft.colors.RED_700
            self.practical_feedback.visible = True
        
        self.page.update()
    
    def update_final_score(self):
        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100
            self.final_score.value = f"Puntuación actual: {self.score}/{self.total_questions} ({percentage:.1f}%)"
    
    def create_resources_section(self):
        return ft.Container(
            content=ft.Column([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text("6", color=ft.colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                                    bgcolor=ft.colors.BLUE_500,
                                    width=32,
                                    height=32,
                                    border_radius=16,
                                    alignment=ft.alignment.center
                                ),
                                ft.Text("Recursos y Materiales", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_800)
                            ]),
                            ft.Divider(),
                            ft.Row([
                                ft.Column([
                                    ft.Text("Materiales Descargables", size=16, weight=ft.FontWeight.BOLD),
                                    self.create_download_item(
                                        "Plantilla de Análisis Comparativo",
                                        "Formato estándar para reportar comparaciones entre grupos",
                                        "comparison"
                                    ),
                                    self.create_download_item(
                                        "Checklist de Verificación",
                                        "Lista de verificación para análisis descriptivos",
                                        "checklist"
                                    ),
                                    self.create_download_item(
                                        "Dataset de Práctica",
                                        "Datos simulados para ejercicios adicionales",
                                        "dataset"
                                    ),
                                    ft.Text("Rúbrica de Evaluación", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Container(
                                        content=ft.DataTable(
                                            columns=[
                                                ft.DataColumn(ft.Text("Criterio")),
                                                ft.DataColumn(ft.Text("Excelente")),
                                                ft.DataColumn(ft.Text("Bueno")),
                                                ft.DataColumn(ft.Text("Mejorable"))
                                            ],
                                            rows=[
                                                ft.DataRow(cells=[
                                                    ft.DataCell(ft.Text("Cálculos estadísticos")),
                                                    ft.DataCell(ft.Text("Todos correctos")),
                                                    ft.DataCell(ft.Text("1-2 errores menores")),
                                                    ft.DataCell(ft.Text("Múltiples errores"))
                                                ]),
                                                ft.DataRow(cells=[
                                                    ft.DataCell(ft.Text("Interpretación clínica")),
                                                    ft.DataCell(ft.Text("Clara y precisa")),
                                                    ft.DataCell(ft.Text("Adecuada")),
                                                    ft.DataCell(ft.Text("Confusa o incorrecta"))
                                                ]),
                                                ft.DataRow(cells=[
                                                    ft.DataCell(ft.Text("Presentación de resultados")),
                                                    ft.DataCell(ft.Text("Profesional")),
                                                    ft.DataCell(ft.Text("Organizada")),
                                                    ft.DataCell(ft.Text("Desorganizada"))
                                                ])
                                            ]
                                        ),
                                        bgcolor=ft.colors.GREY_100,
                                        padding=15,
                                        border_radius=8
                                    )
                                ], expand=True),
                                ft.Column([
                                    ft.Text("Actividad de Transferencia", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Miniinforme: Comparación de Tratamientos", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                                            ft.Text(
                                                "Elabore un informe de 1-2 páginas comparando la efectividad de dos tratamientos "
                                                "para hipertensión usando los datos proporcionados.",
                                                color=ft.colors.BLUE_700
                                            ),
                                            ft.Container(
                                                content=ft.Column([
                                                    ft.Text("Estructura sugerida:", weight=ft.FontWeight.BOLD),
                                                    ft.Text("• Introducción y objetivos"),
                                                    ft.Text("• Descripción de los datos"),
                                                    ft.Text("• Análisis descriptivo por grupo"),
                                                    ft.Text("• Comparación entre grupos"),
                                                    ft.Text("• Interpretación clínica"),
                                                    ft.Text("• Limitaciones del análisis")
                                                ]),
                                                bgcolor=ft.colors.WHITE,
                                                padding=15,
                                                border_radius=8,
                                                border=ft.border.all(1, ft.colors.GREY_300)
                                            )
                                        ]),
                                        bgcolor=ft.colors.BLUE_50,
                                        padding=20,
                                        border_radius=8
                                    ),
                                    ft.Text("Referencias y Lecturas", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Column([
                                        self.create_reference_item("Cohen, J. (1988).", "Statistical Power Analysis for the Behavioral Sciences.", "Academic Press."),
                                        self.create_reference_item("Altman, D. G. (1991).", "Practical Statistics for Medical Research.", "Chapman & Hall."),
                                        self.create_reference_item("Kirkwood, B. R., & Sterne, J. A. (2003).", "Essential Medical Statistics.", "Blackwell Science.")
                                    ]),
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Text("Próximos Pasos", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_800),
                                            ft.Text(
                                                "En la siguiente OVA exploraremos las tablas 2x2 y 2xk en epidemiología, "
                                                "donde aprenderemos a analizar asociaciones entre variables categóricas.",
                                                color=ft.colors.GREEN_700
                                            )
                                        ]),
                                        bgcolor=ft.colors.GREEN_50,
                                        padding=15,
                                        border_radius=8
                                    )
                                ], expand=True)
                            ])
                        ]),
                        padding=20
                    )
                )
            ], scroll=ft.ScrollMode.AUTO),
            expand=True
        )
    
    def create_download_item(self, title, description, file_type):
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(title, weight=ft.FontWeight.BOLD),
                    ft.Text(description, size=12, color=ft.colors.GREY_600)
                ], expand=True),
                ft.ElevatedButton(
                    text="Descargar",
                    on_click=lambda e, t=file_type: self.download_template(t),
                    bgcolor=ft.colors.BLUE_500,
                    color=ft.colors.WHITE
                )
            ]),
            bgcolor=ft.colors.WHITE,
            padding=15,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_300),
            margin=ft.margin.only(bottom=10)
        )
    
    def create_reference_item(self, author, title, publisher):
        return ft.Container(
            content=ft.Text(f"{author} {title} {publisher}"),
            bgcolor=ft.colors.WHITE,
            padding=10,
            border_radius=8,
            border=ft.border.all(1, ft.colors.GREY_300),
            margin=ft.margin.only(bottom=5)
        )
    
    def download_template(self, template_type):
        content = ""
        filename = ""
        
        if template_type == "comparison":
            content = self.generate_comparison_template()
            filename = "plantilla_analisis_comparativo.txt"
        elif template_type == "checklist":
            content = self.generate_checklist()
            filename = "checklist_analisis_descriptivo.txt"
        elif template_type == "dataset":
            content = self.generate_dataset()
            filename = "dataset_practica.csv"
        
        # Crear directorio de descargas si no existe
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads", "OVA_Materiales")
        os.makedirs(downloads_dir, exist_ok=True)
        
        # Guardar archivo
        filepath = os.path.join(downloads_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Mostrar mensaje de confirmación
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(f"Archivo descargado: {filepath}"),
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
