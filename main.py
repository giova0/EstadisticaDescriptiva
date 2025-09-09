import flet as ft
import inicio
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import inspect
import traceback


def mostrar_estadistica_descriptiva(page: ft.Page) -> None:
    page.clean()
    page.title = "Estadística Descriptiva"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f0f0"

    button_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=6),
        elevation=2,
    )

    def volver_inicio(e):
        page.go("/inicio")

    contenido = ft.Column(
        [
            ft.Text(
                "ESTADÍSTICA DESCRIPTIVA",
                size=26,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=30),
            ft.Column(
                [
                    ft.ElevatedButton("OVAS", style=button_style, on_click=lambda e: page.go("/ovas")),
                    ft.ElevatedButton("Análisis de Datos", style=button_style),
                    ft.ElevatedButton("Gráficos", style=button_style),
                    ft.ElevatedButton("Reportes", style=button_style),
                    ft.ElevatedButton("Configuración", style=button_style),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=40),
            ft.ElevatedButton("◀ Volver", on_click=volver_inicio, style=button_style),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(
        ft.Container(
            width=page.window_width,
            height=page.window_height,
            bgcolor="#f8f9fa",
            content=contenido,
            alignment=ft.alignment.center,
        )
    )
    page.update()


def app_main(page: ft.Page):
    page.on_route_change = lambda e: route_change(page)
    # Primera carga
    page.go("/inicio")


def mostrar_menu_ovas(page: ft.Page) -> None:
    page.clean()
    page.title = "OVAS - Estadística Descriptiva"
    page.bgcolor = "#f8f9fa"

    def volver(e):
        page.go("/estadistica")

    # Lista completa de OVAs disponibles
    ovas = [
        ("1", "OVA 1. Bienvenida y Fundamentos"),
        ("2", "OVA 2. Población, Muestra y Variables"),
        ("3", "OVA 3. Clasificación de Variables"),
        ("4", "OVA 4. Organización de Datos Clínicos"),
        ("5", "OVA 5. Visualización Avanzada de Datos"),
        ("6", "OVA 6. Estadísticas Descriptivas Básicas"),
        ("7", "OVA 7. Integración y Evaluación Parcial I"),
        ("8", "OVA 8. Teoría de Conjuntos y Probabilidad Básica"),
        ("9", "OVA 9. Probabilidad Condicional y Bayes"),
        ("10", "OVA 10. Integración y Evaluación Parcial II"),
        ("11", "OVA 11. Distribuciones Discretas en Medicina"),
        ("12", "OVA 12. Distribución Binomial y Poisson"),
        ("13", "OVA 13. Distribución Normal en Biomedicina"),
        ("14", "OVA 14. Integración y Evaluación Parcial III"),
        ("15", "OVA 15. Inferencia Estadística Básica"),
        ("16", "OVA 16. Intervalos para Diferencias"),
        ("17", "OVA 17. Fundamentos de Pruebas de Hipótesis"),
        ("18", "OVA 18. Pruebas Específicas para Ciencias de la Salud"),
        ("19", "OVA 19. Aplicaciones Integradas"),
        ("20", "OVA 20. Cierre y Proyección Profesional"),
    ]

    botones = [
        ft.ElevatedButton(texto, on_click=lambda e, k=clave: page.go(f"/ova/{k}"), width=520)
        for clave, texto in ovas
    ]

    page.add(
        ft.Column(
            [
                ft.Text("OVAS - Selecciona un módulo", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                ft.Container(height=20),
                ft.Column(botones, spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=30),
                ft.ElevatedButton("◀ Volver", on_click=volver),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    page.update()


def abrir_ova(page: ft.Page, clave: str) -> None:
    page.clean()
    try:
        base_dir = Path(__file__).resolve().parent

        def load_module_by_filename(filename: str, module_name: str):
            spec = spec_from_file_location(module_name, str(base_dir / filename))
            if spec is None or spec.loader is None:
                raise ImportError(f"No se pudo crear el spec para {filename}")
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        def run_module_main(mod):
            # 1) Si hay función main(page)
            if hasattr(mod, "main") and callable(getattr(mod, "main")):
                mod.main(page)
                return True
            # 2) Buscar clase con método main(self, page)
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if isinstance(attr, type):
                    if hasattr(attr, "main") and callable(getattr(attr, "main")):
                        needs_page = False
                        try:
                            sig = inspect.signature(attr.__init__)
                            needs_page = "page" in sig.parameters and len(sig.parameters) >= 2
                        except (ValueError, TypeError):
                            needs_page = False
                        instance = attr(page) if needs_page else attr()
                        instance.main(page)  # type: ignore
                        return True
            return False

        if clave == "1":
            # Cargar página HTML para OVA 1 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova1_bienvenida_fundamentos.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.INDIGO
                                ),
                                ft.Text(
                                    "OVA 1: Bienvenida y Fundamentos",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.INDIGO,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.INDIGO_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "2":
            # Cargar página HTML para OVA 2 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova2_poblacion_muestra_variables.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.BLUE
                                ),
                                ft.Text(
                                    "OVA 2: Población, Muestra y Variables",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.BLUE_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "3":
            # Cargar página HTML para OVA 3 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova3_clasificacion_variables.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.GREEN
                                ),
                                ft.Text(
                                    "OVA 3: Clasificación de Variables",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.GREEN,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.GREEN_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "4":
            # Cargar página HTML para OVA 4 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova4_organizacion_datos_clinicos.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.PURPLE
                                ),
                                ft.Text(
                                    "OVA 4: Organización de Datos Clínicos",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.PURPLE,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.PURPLE_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "5":
            # Cargar página HTML para OVA 5 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova5_visualizacion_datos.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.ORANGE
                                ),
                                ft.Text(
                                    "OVA 5: Visualización Avanzada de Datos",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.ORANGE,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.ORANGE_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "7":
            # Cargar página HTML para OVA 7 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova7_bioestadistica.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.TEAL
                                ),
                                ft.Text(
                                    "OVA 7: Integración y Evaluación Parcial I",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.TEAL,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.TEAL_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "6":
            # Cargar página HTML para OVA 6 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova6_estadisticas_descriptivas.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "OVA 6: Estadísticas Descriptivas Básicas",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.RED_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "8":
            # Cargar página HTML para OVA 8 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova_8_teoria_conjuntos_probabilidad.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.BLUE_GREY
                                ),
                                ft.Text(
                                    "OVA 8: Teoría de Conjuntos y Probabilidad Básica",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_GREY,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.BLUE_GREY_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "9":
            # Cargar página HTML para OVA 9 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova_9_probabilidad_condicional_bayes.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.LIGHT_GREEN
                                ),
                                ft.Text(
                                    "OVA 9: Probabilidad Condicional y Bayes",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.LIGHT_GREEN,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.LIGHT_GREEN_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "11":
            # Cargar página HTML para OVA 11 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova_11_distribuciones_discretas.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.CYAN
                                ),
                                ft.Text(
                                    "OVA 11: Distribuciones Discretas en Medicina",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.CYAN,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.CYAN_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "12":
            # Cargar página HTML para OVA 12 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova12_binomial_poisson.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.LIME
                                ),
                                ft.Text(
                                    "OVA 12: Distribución Binomial y Poisson",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.LIME,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.LIME_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "13":
            # Cargar página HTML para OVA 13 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova13_distribucion_normal.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.AMBER
                                ),
                                ft.Text(
                                    "OVA 13: Distribución Normal en Biomedicina",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.AMBER,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.AMBER_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "14":
            # Cargar página HTML para OVA 14 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova14_integracion_evaluacion.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.DEEP_ORANGE
                                ),
                                ft.Text(
                                    "OVA 14: Integración y Evaluación Parcial III",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.DEEP_ORANGE,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.DEEP_ORANGE_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "15":
            # Cargar página HTML para OVA 15 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova15_inferencia_estadistica.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.BROWN
                                ),
                                ft.Text(
                                    "OVA 15: Inferencia Estadística Básica",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BROWN,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.BROWN_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "16":
            # Cargar página HTML para OVA 16 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova16_intervalos_diferencias.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.DEEP_PURPLE
                                ),
                                ft.Text(
                                    "OVA 16: Intervalos para Diferencias",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.DEEP_PURPLE,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.DEEP_PURPLE_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "18":
            # Cargar página HTML para OVA 18 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova18_pruebas_especificas_salud.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.LIGHT_BLUE
                                ),
                                ft.Text(
                                    "OVA 18: Pruebas Específicas para Ciencias de la Salud",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.LIGHT_BLUE,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.LIGHT_BLUE_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        if clave == "10":
            # Cargar página HTML para OVA 10 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova_10_html.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.OPEN_IN_BROWSER,
                                    size=80,
                                    color=ft.Colors.PINK
                                ),
                                ft.Text(
                                    "OVA 10: Integración y Evaluación Parcial II",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.PINK,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "La OVA se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Si no se abrió automáticamente, verifica que el archivo HTML existe en la carpeta del proyecto.",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "🔄 Abrir nuevamente",
                                    on_click=lambda e: webbrowser.open(f"file:///{html_path}"),
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.PINK_700,
                                    )
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            else:
                # Mostrar error si el archivo no existe
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a OVAS",
                                on_click=lambda e: page.go("/ovas"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.GREY_700,
                                )
                            )
                        ], alignment=ft.MainAxisAlignment.START),
                        ft.Container(height=50),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(
                                    ft.Icons.ERROR,
                                    size=80,
                                    color=ft.Colors.RED
                                ),
                                ft.Text(
                                    "Error: Archivo no encontrado",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.RED,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    f"No se pudo encontrar el archivo: {html_path}",
                                    size=14,
                                    color=ft.Colors.GREY_600,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    ])
                )
            
            page.update()
            return
        # Si no está mapeada
        page.add(ft.Text("OVA no disponible", color=ft.Colors.RED))
        page.update()
    except Exception as err:
        # Registrar traza en consola y mostrar mensaje en UI
        traceback.print_exc()
        page.add(ft.Text(f"Error al cargar la OVA: {err}", color=ft.Colors.RED))
        page.update()


def route_change(page: ft.Page):
    if page.route == "/estadistica":
        mostrar_estadistica_descriptiva(page)
    elif page.route == "/ovas":
        mostrar_menu_ovas(page)
    elif page.route.startswith("/ova/"):
        clave = page.route.split("/ova/")[-1]
        abrir_ova(page, clave)
    else:
        # Ruta por defecto: cargar la pantalla de inicio desde inicio.py
        page.clean()
        inicio.main(page)
        page.update()



if __name__ == "__main__":
    ft.app(target=app_main, view=ft.AppView.WEB_BROWSER, port=8080)