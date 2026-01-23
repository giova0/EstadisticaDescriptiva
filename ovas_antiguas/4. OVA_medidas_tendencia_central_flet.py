
import flet as ft
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import numpy as np
import statistics
import random
import io
import base64
from typing import List, Dict, Any

class EstadisticasCalculator:
    """Clase para cálculos estadísticos"""
    
    @staticmethod
    def calcular_media(datos: List[float]) -> float:
        return sum(datos) / len(datos)
    
    @staticmethod
    def calcular_mediana(datos: List[float]) -> float:
        return statistics.median(datos)
    
    @staticmethod
    def calcular_moda(datos: List[float]) -> str:
        try:
            moda = statistics.mode(datos)
            return str(moda)
        except statistics.StatisticsError:
            # Si no hay moda única, encontrar las más frecuentes
            frecuencias = {}
            for dato in datos:
                frecuencias[dato] = frecuencias.get(dato, 0) + 1
            
            max_freq = max(frecuencias.values())
            if max_freq == 1:
                return "No hay moda"
            
            modas = [k for k, v in frecuencias.items() if v == max_freq]
            return ", ".join(map(str, modas))

class GraficosGenerator:
    """Clase para generar gráficos"""
    
    @staticmethod
    def crear_histograma(datos: List[float], titulo: str, color: str = 'blue') -> str:
        """Crea un histograma y retorna la imagen como base64"""
        plt.figure(figsize=(8, 6))
        plt.hist(datos, bins=min(10, len(set(datos))), alpha=0.7, color=color, edgecolor='black')
        plt.title(titulo, fontsize=14, fontweight='bold')
        plt.xlabel('Valores')
        plt.ylabel('Frecuencia')
        plt.grid(True, alpha=0.3)
        
        # Agregar líneas para media y mediana
        media = EstadisticasCalculator.calcular_media(datos)
        mediana = EstadisticasCalculator.calcular_mediana(datos)
        
        plt.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media: {media:.1f}')
        plt.axvline(mediana, color='green', linestyle='--', linewidth=2, label=f'Mediana: {mediana:.1f}')
        plt.legend()
        
        # Convertir a base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"

class SimuladorDatos:
    """Clase para simular datos clínicos"""
    
    VARIABLES_CLINICAS = {
        'presion': {'nombre': 'Presión Arterial', 'unidad': 'mmHg', 'min': 90, 'max': 180},
        'glucosa': {'nombre': 'Glucosa en Sangre', 'unidad': 'mg/dL', 'min': 70, 'max': 200},
        'colesterol': {'nombre': 'Colesterol Total', 'unidad': 'mg/dL', 'min': 150, 'max': 300},
        'frecuencia': {'nombre': 'Frecuencia Cardíaca', 'unidad': 'bpm', 'min': 60, 'max': 120},
        'temperatura': {'nombre': 'Temperatura Corporal', 'unidad': '°C', 'min': 36.0, 'max': 39.5}
    }
    
    @staticmethod
    def generar_datos(tipo_variable: str, num_pacientes: int, distribucion: str) -> List[float]:
        """Genera datos simulados según los parámetros"""
        config = SimuladorDatos.VARIABLES_CLINICAS[tipo_variable]
        datos = []
        
        for _ in range(num_pacientes):
            if distribucion == 'normal':
                media = (config['min'] + config['max']) / 2
                desviacion = (config['max'] - config['min']) / 6
                valor = np.random.normal(media, desviacion)
            elif distribucion == 'asimetrica':
                valor = config['min'] + np.random.exponential(2) * (config['max'] - config['min']) / 10
            else:  # bimodal
                if random.random() < 0.5:
                    valor = np.random.normal(config['min'] + (config['max'] - config['min']) * 0.25, 
                                          (config['max'] - config['min']) * 0.1)
                else:
                    valor = np.random.normal(config['min'] + (config['max'] - config['min']) * 0.75, 
                                          (config['max'] - config['min']) * 0.1)
            
            # Ajustar a los límites
            valor = max(config['min'], min(config['max'], valor))
            
            # Redondear según el tipo
            if tipo_variable == 'temperatura':
                valor = round(valor, 1)
            else:
                valor = round(valor)
            
            datos.append(valor)
        
        return datos

class OVAApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "OVA: Medidas de Tendencia Central en Ciencias de la Salud"
        self.page.window_width = 1200
        self.page.window_height = 800
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # Estado de la aplicación
        self.datos_simulador = None
        self.respuestas_quiz = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Crear pestañas
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="🎯 Introducción", content=self.crear_introduccion()),
                ft.Tab(text="📚 Teoría", content=self.crear_teoria()),
                ft.Tab(text="🏥 Casos Clínicos", content=self.crear_casos_clinicos()),
                ft.Tab(text="🔬 Simulador", content=self.crear_simulador()),
                ft.Tab(text="📝 Evaluación", content=self.crear_evaluacion()),
            ],
            expand=1,
        )
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Text("📊 Medidas de Tendencia Central", 
                       size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("Aplicadas a Ciencias de la Salud", 
                       size=20, color=ft.Colors.WHITE),
                ft.Text("Objeto Virtual de Aprendizaje - Modelo Pedagógico C(H)ANGE", 
                       size=14, color=ft.Colors.WHITE70),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE_700,
            padding=20,
            margin=ft.margin.only(bottom=10)
        )
        
        # Layout principal
        self.page.add(
            ft.Column([
                header,
                tabs
            ], expand=True)
        )
    
    def crear_introduccion(self) -> ft.Container:
        """Crea la pestaña de introducción"""
        return ft.Container(
            content=ft.Column([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("🎯 Objetivos de Aprendizaje", 
                                   size=24, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.Row([
                                ft.Container(
                                    content=ft.Column([
                                        self.crear_objetivo("1", "Comprender los conceptos fundamentales de media, mediana y moda en contextos de salud"),
                                        self.crear_objetivo("2", "Aplicar medidas de tendencia central en análisis de datos clínicos y epidemiológicos"),
                                        self.crear_objetivo("3", "Interpretar resultados estadísticos para la toma de decisiones en salud"),
                                    ]),
                                    expand=1
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("💡 ¿Por qué es importante?", 
                                               size=18, weight=ft.FontWeight.BOLD),
                                        ft.Text(
                                            "Las medidas de tendencia central son fundamentales en ciencias de la salud para resumir y describir datos de pacientes, evaluar la efectividad de tratamientos, y tomar decisiones clínicas basadas en evidencia.",
                                            size=14
                                        )
                                    ]),
                                    bgcolor=ft.Colors.BLUE_50,
                                    padding=15,
                                    border_radius=10,
                                    expand=1
                                )
                            ])
                        ]),
                        padding=20
                    )
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("🔄 Modelo Pedagógico C(H)ANGE", 
                                   size=24, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.Row([
                                self.crear_componente_change("🔢", "Combinatoria", "Organización de datos", ft.Colors.RED_100),
                                self.crear_componente_change("📐", "Álgebra", "Fórmulas y cálculos", ft.Colors.BLUE_100),
                                self.crear_componente_change("🔢", "Números", "Interpretación numérica", ft.Colors.GREEN_100),
                                self.crear_componente_change("📊", "Geometría", "Visualización gráfica", ft.Colors.YELLOW_100),
                                self.crear_componente_change("📈", "Estadística", "Análisis de datos", ft.Colors.PURPLE_100),
                            ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                        ]),
                        padding=20
                    )
                )
            ], scroll=ft.ScrollMode.AUTO),
            padding=10
        )
    
    def crear_objetivo(self, numero: str, texto: str) -> ft.Row:
        """Crea un objetivo de aprendizaje"""
        return ft.Row([
            ft.Container(
                content=ft.Text(numero, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.BLUE_500,
                width=30,
                height=30,
                border_radius=15,
                alignment=ft.alignment.center
            ),
            ft.Text(texto, size=14, expand=True)
        ], spacing=10)
    
    def crear_componente_change(self, icono: str, titulo: str, descripcion: str, color: str) -> ft.Container:
        """Crea un componente del modelo C(H)ANGE"""
        return ft.Container(
            content=ft.Column([
                ft.Text(icono, size=24),
                ft.Text(titulo, weight=ft.FontWeight.BOLD, size=14),
                ft.Text(descripcion, size=12, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=color,
            padding=15,
            border_radius=10,
            width=200
        )
    
    def crear_teoria(self) -> ft.Container:
        """Crea la pestaña de teoría"""
        return ft.Container(
            content=ft.Column([
                ft.Text("📚 Fundamentos Teóricos", size=28, weight=ft.FontWeight.BOLD),
                
                # Media Aritmética
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("➕ Media Aritmética", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                            ft.Row([
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("La media es el promedio de todos los valores. Se calcula sumando todos los datos y dividiendo entre el número total de observaciones.", size=14),
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Text("Fórmula:", weight=ft.FontWeight.BOLD),
                                                ft.Text("x̄ = Σx / n", size=18, weight=ft.FontWeight.BOLD),
                                                ft.Text("Donde x̄ es la media, Σx es la suma de todos los valores, y n es el número de observaciones", size=12)
                                            ]),
                                            bgcolor=ft.Colors.WHITE,
                                            padding=10,
                                            border_radius=5,
                                            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.BLUE_500))
                                        )
                                    ]),
                                    expand=1
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Ejemplo en Salud:", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                                        ft.Text("Presión arterial sistólica de 5 pacientes:", size=14),
                                        ft.Row([
                                            ft.Container(ft.Text("120"), bgcolor=ft.Colors.BLUE_100, padding=5, border_radius=3),
                                            ft.Container(ft.Text("130"), bgcolor=ft.Colors.BLUE_100, padding=5, border_radius=3),
                                            ft.Container(ft.Text("125"), bgcolor=ft.Colors.BLUE_100, padding=5, border_radius=3),
                                            ft.Container(ft.Text("135"), bgcolor=ft.Colors.BLUE_100, padding=5, border_radius=3),
                                            ft.Container(ft.Text("140"), bgcolor=ft.Colors.BLUE_100, padding=5, border_radius=3),
                                        ]),
                                        ft.Text("Media = (120+130+125+135+140)/5 = 130 mmHg", weight=ft.FontWeight.BOLD)
                                    ]),
                                    bgcolor=ft.Colors.WHITE,
                                    padding=10,
                                    border_radius=5,
                                    expand=1
                                )
                            ])
                        ]),
                        padding=15
                    ),
                    color=ft.Colors.BLUE_50
                ),
                
                # Mediana
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("📍 Mediana", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                            ft.Row([
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("La mediana es el valor central cuando los datos están ordenados. Divide el conjunto de datos en dos mitades iguales.", size=14),
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Text("Características:", weight=ft.FontWeight.BOLD),
                                                ft.Text("• No se ve afectada por valores extremos"),
                                                ft.Text("• Útil en distribuciones asimétricas"),
                                                ft.Text("• Representa el percentil 50"),
                                            ]),
                                            bgcolor=ft.Colors.WHITE,
                                            padding=10,
                                            border_radius=5,
                                            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.GREEN_500))
                                        )
                                    ]),
                                    expand=1
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Ejemplo en Salud:", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                                        ft.Text("Tiempo de espera en urgencias (minutos):", size=14),
                                        ft.Row([
                                            ft.Container(ft.Text("15"), bgcolor=ft.Colors.GREEN_100, padding=5, border_radius=3),
                                            ft.Container(ft.Text("20"), bgcolor=ft.Colors.GREEN_100, padding=5, border_radius=3),
                                            ft.Container(ft.Text("25"), bgcolor=ft.Colors.GREEN_200, padding=5, border_radius=3, border=ft.border.all(2, ft.Colors.GREEN_700)),
                                            ft.Container(ft.Text("30"), bgcolor=ft.Colors.GREEN_100, padding=5, border_radius=3),
                                            ft.Container(ft.Text("45"), bgcolor=ft.Colors.GREEN_100, padding=5, border_radius=3),
                                        ]),
                                        ft.Text("Mediana = 25 minutos", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
                                    ]),
                                    bgcolor=ft.Colors.WHITE,
                                    padding=10,
                                    border_radius=5,
                                    expand=1
                                )
                            ])
                        ]),
                        padding=15
                    ),
                    color=ft.Colors.GREEN_50
                ),
                
                # Moda
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("🎯 Moda", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                            ft.Row([
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("La moda es el valor que aparece con mayor frecuencia en el conjunto de datos. Puede haber una, varias o ninguna moda.", size=14),
                                        ft.Container(
                                            content=ft.Column([
                                                ft.Text("Tipos:", weight=ft.FontWeight.BOLD),
                                                ft.Text("• Unimodal: Una sola moda"),
                                                ft.Text("• Bimodal: Dos modas"),
                                                ft.Text("• Multimodal: Más de dos modas"),
                                            ]),
                                            bgcolor=ft.Colors.WHITE,
                                            padding=10,
                                            border_radius=5,
                                            border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.PURPLE_500))
                                        )
                                    ]),
                                    expand=1
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text("Ejemplo en Salud:", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                                        ft.Text("Grupo sanguíneo de pacientes:", size=14),
                                        ft.Column([
                                            ft.Row([
                                                ft.Container(ft.Text("A"), bgcolor=ft.Colors.PURPLE_100, padding=5, border_radius=3),
                                                ft.Container(ft.Text("O"), bgcolor=ft.Colors.PURPLE_200, padding=5, border_radius=3, border=ft.border.all(2, ft.Colors.PURPLE_700)),
                                            ]),
                                            ft.Row([
                                                ft.Container(ft.Text("B"), bgcolor=ft.Colors.PURPLE_100, padding=5, border_radius=3),
                                                ft.Container(ft.Text("O"), bgcolor=ft.Colors.PURPLE_200, padding=5, border_radius=3, border=ft.border.all(2, ft.Colors.PURPLE_700)),
                                            ]),
                                            ft.Row([
                                                ft.Container(ft.Text("O"), bgcolor=ft.Colors.PURPLE_200, padding=5, border_radius=3, border=ft.border.all(2, ft.Colors.PURPLE_700)),
                                                ft.Container(ft.Text("AB"), bgcolor=ft.Colors.PURPLE_100, padding=5, border_radius=3),
                                            ])
                                        ]),
                                        ft.Text("Moda = Grupo O (3 veces)", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700)
                                    ]),
                                    bgcolor=ft.Colors.WHITE,
                                    padding=10,
                                    border_radius=5,
                                    expand=1
                                )
                            ])
                        ]),
                        padding=15
                    ),
                    color=ft.Colors.PURPLE_50
                )
            ], scroll=ft.ScrollMode.AUTO),
            padding=10
        )
    
    def crear_casos_clinicos(self) -> ft.Container:
        """Crea la pestaña de casos clínicos"""
        # Contenedores para resultados
        self.caso1_resultados = ft.Column(visible=False)
        self.caso2_resultados = ft.Column(visible=False)
        self.caso3_resultados = ft.Column(visible=False)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("🏥 Casos Clínicos Interactivos", size=28, weight=ft.FontWeight.BOLD),
                
                # Caso 1: Presión Arterial
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Caso 1: Análisis de Presión Arterial", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                            ft.Text("Un cardiólogo registró la presión arterial sistólica de 10 pacientes hipertensos durante su consulta matutina:", size=14),
                            ft.Row([
                                ft.Container(ft.Text("145"), bgcolor=ft.Colors.RED_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("150"), bgcolor=ft.Colors.RED_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("138"), bgcolor=ft.Colors.RED_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("162"), bgcolor=ft.Colors.RED_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("155"), bgcolor=ft.Colors.RED_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("148"), bgcolor=ft.Colors.RED_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("142"), bgcolor=ft.Colors.RED_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("158"), bgcolor=ft.Colors.RED_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("151"), bgcolor=ft.Colors.RED_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("149"), bgcolor=ft.Colors.RED_100, padding=8, border_radius=5),
                            ], wrap=True),
                            ft.ElevatedButton(
                                "Calcular Medidas",
                                on_click=lambda _: self.calcular_caso1(),
                                bgcolor=ft.Colors.RED_600,
                                color=ft.Colors.WHITE
                            ),
                            self.caso1_resultados
                        ]),
                        padding=15
                    ),
                    color=ft.Colors.RED_50
                ),
                
                # Caso 2: IMC
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Caso 2: Índice de Masa Corporal (IMC)", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                            ft.Text("Una nutricionista evaluó el IMC de 12 pacientes en una consulta de control nutricional:", size=14),
                            ft.Row([
                                ft.Container(ft.Text("22.5"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("28.3"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("31.2"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("24.8"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("26.7"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("29.1"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("23.4"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("27.9"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("25.6"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("30.5"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("24.2"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("26.8"), bgcolor=ft.Colors.GREEN_100, padding=8, border_radius=5),
                            ], wrap=True),
                            ft.ElevatedButton(
                                "Analizar IMC",
                                on_click=lambda _: self.calcular_caso2(),
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE
                            ),
                            self.caso2_resultados
                        ]),
                        padding=15
                    ),
                    color=ft.Colors.GREEN_50
                ),
                
                # Caso 3: Tiempo de Recuperación
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Caso 3: Tiempo de Recuperación Post-Cirugía", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                            ft.Text("Un cirujano registró los días de recuperación de 15 pacientes después de una apendicectomía:", size=14),
                            ft.Row([
                                ft.Container(ft.Text("3"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("5"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("4"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("7"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("4"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("6"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("5"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("4"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("8"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("5"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("6"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("4"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("5"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("7"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                                ft.Container(ft.Text("5"), bgcolor=ft.Colors.BLUE_100, padding=8, border_radius=5),
                            ], wrap=True),
                            ft.ElevatedButton(
                                "Analizar Recuperación",
                                on_click=lambda _: self.calcular_caso3(),
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE
                            ),
                            self.caso3_resultados
                        ]),
                        padding=15
                    ),
                    color=ft.Colors.BLUE_50
                )
            ], scroll=ft.ScrollMode.AUTO),
            padding=10
        )
    
    def calcular_caso1(self):
        """Calcula las medidas para el caso 1"""
        datos = [145, 150, 138, 162, 155, 148, 142, 158, 151, 149]
        media = EstadisticasCalculator.calcular_media(datos)
        mediana = EstadisticasCalculator.calcular_mediana(datos)
        moda = EstadisticasCalculator.calcular_moda(datos)
        
        # Crear gráfico
        imagen_base64 = GraficosGenerator.crear_histograma(datos, "Presión Arterial Sistólica", "red")
        
        self.caso1_resultados.controls = [
            ft.Divider(),
            ft.Text("Resultados:", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{media:.1f}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                        ft.Text("Media (mmHg)", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.BLUE_100,
                    padding=15,
                    border_radius=10,
                    expand=1
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{mediana}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                        ft.Text("Mediana (mmHg)", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.GREEN_100,
                    padding=15,
                    border_radius=10,
                    expand=1
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{moda}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                        ft.Text("Moda (mmHg)", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.PURPLE_100,
                    padding=15,
                    border_radius=10,
                    expand=1
                )
            ]),
            ft.Container(
                content=ft.Text(
                    f"Interpretación: La media de {media:.1f} mmHg indica hipertensión arterial en este grupo de pacientes. La mediana ({mediana} mmHg) confirma que al menos la mitad de los pacientes tienen valores elevados.",
                    size=14
                ),
                bgcolor=ft.Colors.YELLOW_50,
                padding=10,
                border_radius=5,
                border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.YELLOW_600))
            ),
            ft.Image(src=imagen_base64, width=600, height=400)
        ]
        self.caso1_resultados.visible = True
        self.page.update()
    
    def calcular_caso2(self):
        """Calcula las medidas para el caso 2"""
        datos = [22.5, 28.3, 31.2, 24.8, 26.7, 29.1, 23.4, 27.9, 25.6, 30.5, 24.2, 26.8]
        media = EstadisticasCalculator.calcular_media(datos)
        mediana = EstadisticasCalculator.calcular_mediana(datos)
        moda = EstadisticasCalculator.calcular_moda(datos)
        
        # Clasificar IMC
        clasificacion = []
        for imc in datos:
            if imc < 18.5:
                clasificacion.append('Bajo peso')
            elif imc < 25:
                clasificacion.append('Normal')
            elif imc < 30:
                clasificacion.append('Sobrepeso')
            else:
                clasificacion.append('Obesidad')
        
        conteo_clasif = {}
        for c in clasificacion:
            conteo_clasif[c] = conteo_clasif.get(c, 0) + 1
        
        # Crear gráfico
        imagen_base64 = GraficosGenerator.crear_histograma(datos, "Índice de Masa Corporal", "green")
        
        self.caso2_resultados.controls = [
            ft.Divider(),
            ft.Text("Análisis Nutricional:", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{media:.1f}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                        ft.Text("Media IMC", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.BLUE_100,
                    padding=15,
                    border_radius=10,
                    expand=1
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{mediana:.1f}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                        ft.Text("Mediana IMC", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.GREEN_100,
                    padding=15,
                    border_radius=10,
                    expand=1
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{moda}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                        ft.Text("Moda IMC", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.PURPLE_100,
                    padding=15,
                    border_radius=10,
                    expand=1
                )
            ]),
            ft.Container(
                content=ft.Column([
                    ft.Text("Distribución por Categorías:", weight=ft.FontWeight.BOLD),
                    *[ft.Row([
                        ft.Text(f"{cat}:", expand=1),
                        ft.Text(f"{count} pacientes", weight=ft.FontWeight.BOLD)
                    ]) for cat, count in conteo_clasif.items()]
                ]),
                bgcolor=ft.Colors.GREY_50,
                padding=10,
                border_radius=5
            ),
            ft.Container(
                content=ft.Text(
                    f"Interpretación: El IMC promedio de {media:.1f} indica sobrepeso en el grupo. Se recomienda intervención nutricional para {conteo_clasif.get('Sobrepeso', 0)} pacientes con sobrepeso y {conteo_clasif.get('Obesidad', 0)} con obesidad.",
                    size=14
                ),
                bgcolor=ft.Colors.GREEN_50,
                padding=10,
                border_radius=5,
                border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.GREEN_600))
            ),
            ft.Image(src=imagen_base64, width=600, height=400)
        ]
        self.caso2_resultados.visible = True
        self.page.update()
    
    def calcular_caso3(self):
        """Calcula las medidas para el caso 3"""
        datos = [3, 5, 4, 7, 4, 6, 5, 4, 8, 5, 6, 4, 5, 7, 5]
        media = EstadisticasCalculator.calcular_media(datos)
        mediana = EstadisticasCalculator.calcular_mediana(datos)
        moda = EstadisticasCalculator.calcular_moda(datos)
        
        # Crear gráfico
        imagen_base64 = GraficosGenerator.crear_histograma(datos, "Días de Recuperación", "blue")
        
        self.caso3_resultados.controls = [
            ft.Divider(),
            ft.Text("Análisis de Recuperación:", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{media:.1f}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                        ft.Text("Media (días)", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.BLUE_100,
                    padding=15,
                    border_radius=10,
                    expand=1
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{mediana}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                        ft.Text("Mediana (días)", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.GREEN_100,
                    padding=15,
                    border_radius=10,
                    expand=1
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{moda}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                        ft.Text("Moda (días)", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.PURPLE_100,
                    padding=15,
                    border_radius=10,
                    expand=1
                )
            ]),
            ft.Container(
                content=ft.Text(
                    f"Interpretación: El tiempo promedio de recuperación es {media:.1f} días. La moda de {moda} días indica que estos son los tiempos más frecuentes de recuperación. Esto ayuda a planificar la capacidad hospitalaria y expectativas del paciente.",
                    size=14
                ),
                bgcolor=ft.Colors.BLUE_50,
                padding=10,
                border_radius=5,
                border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.BLUE_600))
            ),
            ft.Image(src=imagen_base64, width=600, height=400)
        ]
        self.caso3_resultados.visible = True
        self.page.update()
    
    def crear_simulador(self) -> ft.Container:
        """Crea la pestaña del simulador"""
        # Controles del simulador
        self.tipo_variable = ft.Dropdown(
            label="Tipo de Variable Clínica",
            options=[
                ft.dropdown.Option("presion", "Presión Arterial (mmHg)"),
                ft.dropdown.Option("glucosa", "Glucosa en Sangre (mg/dL)"),
                ft.dropdown.Option("colesterol", "Colesterol Total (mg/dL)"),
                ft.dropdown.Option("frecuencia", "Frecuencia Cardíaca (bpm)"),
                ft.dropdown.Option("temperatura", "Temperatura Corporal (°C)"),
            ],
            value="presion",
            width=300
        )
        
        self.num_pacientes = ft.Slider(
            min=5,
            max=50,
            value=20,
            divisions=45,
            label="{value}",
            width=300
        )
        
        self.distribucion = ft.Dropdown(
            label="Distribución",
            options=[
                ft.dropdown.Option("normal", "Normal"),
                ft.dropdown.Option("asimetrica", "Asimétrica"),
                ft.dropdown.Option("bimodal", "Bimodal"),
            ],
            value="normal",
            width=300
        )
        
        self.datos_generados = ft.Column(visible=False)
        self.resultados_simulador = ft.Column(visible=False)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("🔬 Simulador Interactivo", size=28, weight=ft.FontWeight.BOLD),
                
                ft.Row([
                    # Panel de Control
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text("Configuración del Simulador", size=18, weight=ft.FontWeight.BOLD),
                                self.tipo_variable,
                                ft.Column([
                                    ft.Text("Número de Pacientes:", size=14),
                                    self.num_pacientes,
                                ]),
                                self.distribucion,
                                ft.ElevatedButton(
                                    "🎲 Generar Datos Simulados",
                                    on_click=lambda _: self.generar_datos_simulador(),
                                    bgcolor=ft.Colors.BLUE_600,
                                    color=ft.Colors.WHITE,
                                    width=280
                                ),
                                self.datos_generados
                            ]),
                            padding=20,
                            width=350
                        )
                    ),
                    
                    # Resultados
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text("Resultados del Análisis", size=18, weight=ft.FontWeight.BOLD),
                                self.resultados_simulador
                            ]),
                            padding=20,
                            width=700
                        ),
                        expand=1
                    )
                ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START)
            ], scroll=ft.ScrollMode.AUTO),
            padding=10
        )
    
    def generar_datos_simulador(self):
        """Genera datos para el simulador"""
        tipo = self.tipo_variable.value
        num = int(self.num_pacientes.value)
        dist = self.distribucion.value
        
        datos = SimuladorDatos.generar_datos(tipo, num, dist)
        config = SimuladorDatos.VARIABLES_CLINICAS[tipo]
        
        # Mostrar datos generados
        datos_texto = [ft.Container(
            ft.Text(f"{d}{config['unidad']}"),
            bgcolor=ft.Colors.BLUE_100,
            padding=5,
            border_radius=3
        ) for d in datos[:20]]  # Mostrar solo los primeros 20
        
        if len(datos) > 20:
            datos_texto.append(ft.Text(f"... y {len(datos) - 20} más"))
        
        self.datos_generados.controls = [
            ft.Divider(),
            ft.Text("Datos Generados:", weight=ft.FontWeight.BOLD),
            ft.Row(datos_texto, wrap=True),
            ft.ElevatedButton(
                "📊 Calcular Medidas",
                on_click=lambda _: self.calcular_simulador(datos, config),
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE
            )
        ]
        self.datos_generados.visible = True
        self.page.update()
    
    def calcular_simulador(self, datos: List[float], config: Dict[str, Any]):
        """Calcula las medidas del simulador"""
        media = EstadisticasCalculator.calcular_media(datos)
        mediana = EstadisticasCalculator.calcular_mediana(datos)
        moda = EstadisticasCalculator.calcular_moda(datos)
        
        # Generar interpretación
        interpretacion = self.generar_interpretacion_clinica(self.tipo_variable.value, media, mediana, datos)
        
        # Crear gráfico
        imagen_base64 = GraficosGenerator.crear_histograma(
            datos, 
            f"Distribución de {config['nombre']}", 
            "blue"
        )
        
        self.resultados_simulador.controls = [
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{media:.1f}", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                        ft.Text(f"Media {config['unidad']}", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.BLUE_100,
                    padding=20,
                    border_radius=10,
                    expand=1
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{mediana}", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                        ft.Text(f"Mediana {config['unidad']}", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.GREEN_100,
                    padding=20,
                    border_radius=10,
                    expand=1
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"{moda}", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700),
                        ft.Text(f"Moda {config['unidad']}", size=12)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.PURPLE_100,
                    padding=20,
                    border_radius=10,
                    expand=1
                )
            ]),
            ft.Container(
                content=ft.Column([
                    ft.Text("💡 Interpretación Clínica:", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                    ft.Text(interpretacion, size=14)
                ]),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=5,
                border=ft.border.only(left=ft.border.BorderSide(4, ft.Colors.BLUE_500))
            ),
            ft.Image(src=imagen_base64, width=650, height=450)
        ]
        self.resultados_simulador.visible = True
        self.page.update()
    
    def generar_interpretacion_clinica(self, tipo: str, media: float, mediana: float, datos: List[float]) -> str:
        """Genera interpretación clínica según el tipo de variable"""
        if tipo == 'presion':
            if media > 140:
                return f"La presión arterial promedio de {media:.1f} mmHg indica hipertensión en el grupo. Se recomienda seguimiento y posible tratamiento antihipertensivo."
            elif media > 120:
                return f"La presión arterial promedio de {media:.1f} mmHg está en rango de prehipertensión. Se sugieren cambios en el estilo de vida."
            else:
                return f"La presión arterial promedio de {media:.1f} mmHg está en rango normal."
        
        elif tipo == 'glucosa':
            if media > 126:
                return f"La glucosa promedio de {media:.1f} mg/dL sugiere diabetes. Se requiere confirmación diagnóstica y manejo especializado."
            elif media > 100:
                return f"La glucosa promedio de {media:.1f} mg/dL indica prediabetes. Se recomienda intervención preventiva."
            else:
                return f"La glucosa promedio de {media:.1f} mg/dL está en rango normal."
        
        elif tipo == 'colesterol':
            if media > 240:
                return f"El colesterol promedio de {media:.1f} mg/dL es alto. Se requiere intervención dietética y posible tratamiento farmacológico."
            elif media > 200:
                return f"El colesterol promedio de {media:.1f} mg/dL está en el límite superior. Se recomienda modificación dietética."
            else:
                return f"El colesterol promedio de {media:.1f} mg/dL está en rango deseable."
        
        else:
            diferencia = abs(media - mediana)
            if diferencia > media * 0.1:
                return f"Los valores muestran una distribución con media de {media:.1f} y mediana de {mediana}. La diferencia entre media y mediana sugiere asimetría en los datos."
            else:
                return f"Los valores muestran una distribución con media de {media:.1f} y mediana de {mediana}. La similitud entre media y mediana sugiere una distribución simétrica."
    
    def crear_evaluacion(self) -> ft.Container:
        """Crea la pestaña de evaluación"""
        # Preguntas del quiz
        preguntas = [
            {
                "pregunta": "Un médico registró los siguientes valores de glucosa en ayunas (mg/dL) de 7 pacientes: 85, 92, 88, 95, 90, 87, 91. ¿Cuál es la media?",
                "opciones": ["88.3 mg/dL", "89.7 mg/dL", "90.0 mg/dL", "91.2 mg/dL"],
                "correcta": 1,
                "explicacion": "Media = (85+92+88+95+90+87+91)/7 = 628/7 = 89.7 mg/dL"
            },
            {
                "pregunta": "Los tiempos de espera en urgencias (en minutos) fueron: 15, 20, 25, 30, 45, 60, 120. ¿Qué medida de tendencia central es más apropiada para representar estos datos?",
                "opciones": ["Media, porque incluye todos los valores", "Mediana, porque no se ve afectada por el valor extremo (120)", "Moda, porque es la más fácil de calcular"],
                "correcta": 1,
                "explicacion": "La mediana es más apropiada porque el valor extremo (120 minutos) distorsiona la media, mientras que la mediana representa mejor el tiempo típico de espera."
            },
            {
                "pregunta": "En un estudio sobre grupos sanguíneos se encontró: A(5), B(3), AB(1), O(8). ¿Cuál es la moda?",
                "opciones": ["Grupo A", "Grupo O", "Grupo B", "Grupo AB"],
                "correcta": 1,
                "explicacion": "El grupo O aparece 8 veces, más que cualquier otro grupo sanguíneo, por lo que es la moda."
            },
            {
                "pregunta": "Las edades de pacientes en una consulta geriátrica son: 65, 68, 70, 72, 75, 78, 80. ¿Cuál es la mediana?",
                "opciones": ["70 años", "72 años", "73 años", "75 años"],
                "correcta": 1,
                "explicacion": "Con 7 valores ordenados (65,68,70,72,75,78,80), la mediana es el valor central (posición 4): 72 años."
            },
            {
                "pregunta": "¿En qué situación clínica sería más apropiado usar la mediana en lugar de la media?",
                "opciones": ["Cuando los datos tienen una distribución perfectamente simétrica", "Cuando hay valores extremos que pueden distorsionar la media", "Cuando tenemos muy pocos datos", "Cuando trabajamos con datos categóricos"],
                "correcta": 1,
                "explicacion": "La mediana es más robusta ante valores extremos (outliers) que pueden distorsionar la media, siendo más representativa del valor central típico."
            }
        ]
        
        # Crear controles para las preguntas
        self.radio_groups = []
        preguntas_controles = []
        
        for i, pregunta in enumerate(preguntas):
            radio_group = ft.RadioGroup(
                content=ft.Column([
                    ft.Radio(value=j, label=opcion) for j, opcion in enumerate(pregunta["opciones"])
                ])
            )
            self.radio_groups.append(radio_group)
            
            pregunta_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"Pregunta {i+1} de {len(preguntas)}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                        ft.Text(pregunta["pregunta"], size=14),
                        radio_group
                    ]),
                    padding=15
                ),
                color=ft.Colors.BLUE_50
            )
            preguntas_controles.append(pregunta_card)
        
        self.resultados_quiz = ft.Column(visible=False)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📝 Evaluación Interactiva", size=28, weight=ft.FontWeight.BOLD),
                *preguntas_controles,
                ft.Container(
                    content=ft.ElevatedButton(
                        "📊 Evaluar Respuestas",
                        on_click=lambda _: self.evaluar_quiz(preguntas),
                        bgcolor=ft.Colors.GREEN_600,
                        color=ft.Colors.WHITE,
                        width=200
                    ),
                    alignment=ft.alignment.center
                ),
                self.resultados_quiz
            ], scroll=ft.ScrollMode.AUTO),
            padding=10
        )
    
    def evaluar_quiz(self, preguntas: List[Dict]):
        """Evalúa el quiz y muestra resultados"""
        puntuacion = 0
        total_preguntas = len(preguntas)
        retroalimentacion = []
        
        for i, (pregunta, radio_group) in enumerate(zip(preguntas, self.radio_groups)):
            respuesta_seleccionada = radio_group.value
            es_correcta = respuesta_seleccionada is not None and int(respuesta_seleccionada) == pregunta["correcta"]
            
            if es_correcta:
                puntuacion += 1
            
            color = ft.Colors.GREEN_50 if es_correcta else ft.Colors.RED_50
            border_color = ft.Colors.GREEN_400 if es_correcta else ft.Colors.RED_400
            text_color = ft.Colors.GREEN_800 if es_correcta else ft.Colors.RED_800
            
            retroalimentacion.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Pregunta {i+1}: {'✅ Correcta' if es_correcta else '❌ Incorrecta'}", 
                               weight=ft.FontWeight.BOLD, color=text_color),
                        ft.Text(pregunta["explicacion"], size=12, color=text_color)
                    ]),
                    bgcolor=color,
                    padding=15,
                    border_radius=5,
                    border=ft.border.only(left=ft.border.BorderSide(4, border_color))
                )
            )
        
        porcentaje = (puntuacion / total_preguntas) * 100
        
        if porcentaje >= 80:
            mensaje = "¡Excelente! Dominas muy bien los conceptos de medidas de tendencia central."
            color_resultado = ft.Colors.GREEN_600
        elif porcentaje >= 60:
            mensaje = "Buen trabajo. Tienes una comprensión sólida, pero puedes mejorar algunos aspectos."
            color_resultado = ft.Colors.BLUE_600
        else:
            mensaje = "Necesitas repasar los conceptos. Te recomendamos revisar la teoría y los casos clínicos."
            color_resultado = ft.Colors.RED_600
        
        self.resultados_quiz.controls = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("🎯 Resultados de la Evaluación", size=20, weight=ft.FontWeight.BOLD),
                        ft.Column([
                            ft.Text(f"{puntuacion}/{total_preguntas}", size=48, weight=ft.FontWeight.BOLD, color=color_resultado),
                            ft.Text(f"{porcentaje:.0f}%", size=24, weight=ft.FontWeight.BOLD, color=color_resultado),
                            ft.Text(mensaje, color=color_resultado, text_align=ft.TextAlign.CENTER)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Divider(),
                        ft.Column(retroalimentacion, spacing=10),
                        ft.ElevatedButton(
                            "🔄 Intentar de Nuevo",
                            on_click=lambda _: self.reiniciar_quiz(),
                            bgcolor=ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE
                        )
                    ]),
                    padding=20
                ),
                color=ft.Colors.BLUE_50
            )
        ]
        self.resultados_quiz.visible = True
        self.page.update()
    
    def reiniciar_quiz(self):
        """Reinicia el quiz"""
        for radio_group in self.radio_groups:
            radio_group.value = None
        self.resultados_quiz.visible = False
        self.page.update()

def main(page: ft.Page):
    app = OVAApp(page)

if __name__ == "__main__":
    ft.app(target=main)
