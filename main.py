import flet as ft
import inicio
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import inspect
import traceback


def mostrar_inicio(page: ft.Page) -> None:
    page.clean()
    page.title = "Bioestadística para Ciencias de la Salud UAN"
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
        page.go("/inicio_cover")

    contenido_botones = ft.Column(
        [
            ft.Text(
                "Bioestadística para Ciencias de la Salud UAN",
                size=26,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=30),
            ft.Column(
                [
                    ft.ElevatedButton("FASES DEL CURSO DE BIOESTADÍSTICA", style=button_style, on_click=lambda e: page.go("/fases")),
                    ft.ElevatedButton("AMBIENTES VIRTUALES", style=button_style, on_click=lambda e: page.go("/ovas_principal")),
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

    contenido_stack = ft.Stack([
        ft.Image(
            src="https://i.postimg.cc/fLFk4sSL/bioestadistica1.png",
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        ft.Container(
            content=contenido_botones,
            alignment=ft.alignment.center,
            expand=True
        ),
    ])

    page.add(contenido_stack)
    page.update()


def app_main(page: ft.Page):
    page.on_route_change = lambda e: route_change(page)
    # Primera carga
    page.go("/inicio_cover")


def mostrar_menu_ovas(page: ft.Page) -> None:
    page.clean()
    page.title = "Fase I - Estadística Descriptiva - Bioestadística para Ciencias de la Salud UAN"
    page.bgcolor = "#f8f9fa"

    def volver(e):
        page.go("/fases")

    # Lista de OVAs para FASE I - Bioestadística para Ciencias de la Salud UAN
    ovas = [
        ("1", "OVA 1. Bienvenida y Fundamentos"),
        ("2", "OVA 2. Población, Muestra y Variables"),
        ("3", "OVA 3. Clasificación de Variables"),
        ("4", "OVA 4. Organización de Datos Clínicos"),
        ("5", "OVA 5. Visualización Avanzada de Datos"),
        ("6", "OVA 6. Estadísticas Descriptivas Básicas"),
        ("7", "OVA 7. Integración y Evaluación Parcial I"),
    ]

    botones = [
        ft.ElevatedButton(texto, on_click=lambda e, k=clave: page.go(f"/ova/{k}"), width=520)
        for clave, texto in ovas
    ]

    page.add(
        ft.Column(
            [
                ft.Text("Fase I - Estadística Descriptiva - Selecciona un módulo", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
        if clave == "historia_bioestadistica":
            # Abrir la URL de la historia de la bioestadística en el navegador del sistema
            import webbrowser

            url = "https://mgx.dev/chat/20e285a3d5a14931ad2495ddd8dcd3d1"
            webbrowser.open(url)

            # Mostrar mensaje de confirmación en la aplicación
            page.add(
                ft.Column([
                    ft.Row([
                        ft.ElevatedButton(
                            "◀ Volver a Salas de Hospitalización",
                            on_click=lambda e: page.go("/unidades_especializadas"),
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
                                "Historia de la Bioestadística",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.INDIGO,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=20),
                            ft.Text(
                                "La página se ha abierto en tu navegador predeterminado.",
                                size=16,
                                color=ft.Colors.GREY_700,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=30),
                            ft.ElevatedButton(
                                "🔄 Abrir nuevamente",
                                on_click=lambda e: webbrowser.open(url),
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
            
            page.update()
            return
        if clave == "19":
            # Cargar página HTML para OVA 19 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova_19_aplicaciones_integradas.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a FASE III",
                                on_click=lambda e: page.go("/fase3"),
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
                                    "OVA 19: Aplicaciones Integradas",
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
                                "◀ Volver a FASE III",
                                on_click=lambda e: page.go("/fase3"),
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
            
            html_path = str(base_dir / "Población_muestra2.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
        if clave == "17":
            # Cargar página HTML para OVA 17 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova_17_pruebas_hipotesis.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a FASE I",
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
                                    "OVA 17: Fundamentos de Pruebas de Hipótesis",
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
                                "◀ Volver a FASE I",
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
        if clave == "20":
            # Cargar página HTML para OVA 20 en el navegador del sistema
            import webbrowser
            import os
            
            html_path = str(base_dir / "ova_20_cierre_proyeccion_profesional.html")
            
            # Verificar que el archivo existe
            if os.path.exists(html_path):
                # Abrir el archivo HTML en el navegador predeterminado
                webbrowser.open(f"file:///{html_path}")
                
                # Mostrar mensaje de confirmación en la aplicación
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a FASE I",
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
                                    "OVA 20: Cierre y Proyección Profesional",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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
                                "◀ Volver a FASE I",
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

def abrir_juego(page: ft.Page, clave: str) -> None:
    page.clean()
    try:
        base_dir = Path(__file__).resolve().parent

        if clave == "1":
            import webbrowser
            import os
            
            html_path = str(base_dir / "Muestras1.html")
            
            if os.path.exists(html_path):
                webbrowser.open(f"file:///{html_path}")
                
                page.add(
                    ft.Column([
                        ft.Row([
                            ft.ElevatedButton(
                                "◀ Volver a Juegos",
                                on_click=lambda e: page.go("/clasificacion_variables"),
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
                                    "Juego 1: Triage de Variables",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                ft.Text(
                                    "El juego se ha abierto en tu navegador predeterminado.",
                                    size=16,
                                    color=ft.Colors.GREY_700,
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
                                "◀ Volver a Juegos",
                                on_click=lambda e: page.go("/clasificacion_variables"),
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
        
    except Exception as err:
        traceback.print_exc()
        page.add(ft.Text(f"Error al cargar el juego: {err}", color=ft.Colors.RED))
        page.update()

def mostrar_fases(page: ft.Page) -> None:
    page.clean()
    page.title = "Fases - Bioestadística para Ciencias de la Salud UAN"
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
        page.go("/")

    contenido = ft.Column(
        [
            ft.Text(
                "Fases del curso",
                size=26,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=30),
            ft.Column(
                [
                    ft.ElevatedButton("Fase I - Estadística Descriptiva - 7 OVAs", style=button_style, on_click=lambda e: page.go("/ovas")),
                    ft.ElevatedButton("Fase II - Probabilidad - 8 OVA", style=button_style, on_click=lambda e: page.go("/fase2")),
                    ft.ElevatedButton("Fase III - Inferencia Estadística - 4 OVAs", style=button_style, on_click=lambda e: page.go("/fase3")),
                    ft.ElevatedButton("Fase IV - Síntesis e Integración - 1 OVA", style=button_style, on_click=lambda e: page.go("/fase4")),
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
            bgcolor="#f8f9fa",
            content=contenido,
            alignment=ft.alignment.center,
        )
    )
    page.update()

def mostrar_ovas_principal(page: ft.Page) -> None:
    page.clean()
    page.title = "OVAs - Bioestadística para Ciencias de la Salud UAN"
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
        page.go("/")

    contenido_botones = ft.Column(
            [
                ft.Text(
                    "OVAs",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_800,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=30),
                ft.Column(
                    [
                        ft.ElevatedButton("Hospital", style=button_style, on_click=lambda e: page.go("/hospital")),
                        ft.ElevatedButton("Farmacia", style=button_style, on_click=lambda e: page.go("/farmacia")),
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

    contenido = ft.Stack([
        ft.Image(
            src="https://i.postimg.cc/nrR2fCYm/descanso1.png",
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        ft.Container(
            content=contenido_botones,
            alignment=ft.alignment.center,
            expand=True
            ),
    ])

    page.add(contenido)
    page.update()

def mostrar_hospital(page: ft.Page) -> None:
    page.clean()
    page.title = "Hospital"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f0f0"

    button_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=6),
        elevation=2,
    )

    def volver_ovas(e):
        page.go("/ovas_principal")

    contenido = ft.Stack([
        ft.Image(
            src="https://i.postimg.cc/Px6b7zhs/hospital1.png",
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        ft.Column(
            [
                ft.ElevatedButton("Ingresar al Hospital", style=button_style, on_click=lambda e: page.go("/pizarra")),
                ft.ElevatedButton("◀ Volver", on_click=volver_ovas, style=button_style),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    ])

    page.add(contenido)
    page.update()

def mostrar_farmacia(page: ft.Page) -> None:
    page.clean()
    page.title = "Farmacia"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f0f0"

    button_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=6),
        elevation=2,
    )

    def volver_ovas(e):
        page.go("/ovas_principal")

    contenido = ft.Stack([
        ft.Image(
            src="https://i.postimg.cc/nh7z6NnV/Farmacia2.jpg",
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        ft.Column(
            [
                ft.Text(
                    "Farmacia",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_800,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=30),
                ft.ElevatedButton("Farmacia_1", style=button_style, on_click=lambda e: page.go("/farmacia_1")),
                ft.ElevatedButton("Farmacia_2", style=button_style, on_click=None),
                ft.ElevatedButton("◀ Volver", on_click=volver_ovas, style=button_style),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    ])

    page.add(contenido)
    page.update()

def mostrar_farmacia_1(page: ft.Page) -> None:
    page.clean()
    page.title = "Farmacia 1"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f0f0"

    button_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=6),
        elevation=2,
    )

    def volver_farmacia(e):
        page.go("/farmacia")

    contenido = ft.Stack([
        ft.Image(
            src="https://i.postimg.cc/cJBJJYKV/Farmacia3.png",
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        ft.Column(
            [
                ft.Text(
                    "Farmacia 1",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_800,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=30),
                ft.ElevatedButton("Farmacia_A", style=button_style, on_click=None),
                ft.ElevatedButton("Farmacia_B", style=button_style, on_click=None),
                ft.ElevatedButton("◀ Volver", on_click=volver_farmacia, style=button_style),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    ])

    page.add(contenido)
    page.update()

def mostrar_pizarra(page: ft.Page) -> None:
    page.clean()
    page.title = "Pizarra"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f0f0"

    button_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=6),
        elevation=2,
    )

    def volver_hospital(e):
        page.go("/hospital")

    contenido = ft.Stack([
        ft.Image(
            src="https://i.postimg.cc/85PBTPnx/pizarra1.jpg",
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        ft.Column(
            [
                ft.Text(
                    "Recepción / admisiones",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=30),
                ft.ElevatedButton("Unidades especializadas", style=button_style, on_click=lambda e: page.go("/unidades_especializadas")),
                ft.ElevatedButton("Investigación", style=button_style, on_click=lambda e: page.go("/investigacion")),
                ft.ElevatedButton("◀ Volver", on_click=volver_hospital, style=button_style),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    ])

    page.add(contenido)
    page.update()

def mostrar_unidades_especializadas(page: ft.Page) -> None:
    page.clean()
    page.title = "Unidades Especializadas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f0f0"

    button_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=6),
        elevation=2,
    )

    def volver_pizarra(e):
        page.go("/pizarra")

    contenido = ft.Stack([
        ft.Image(
            src="https://i.postimg.cc/z3mgHJ0z/uci2.png",
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        ft.Column(
            [
                ft.Text(
                    "Salas de hospitalización",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=30),
                ft.ElevatedButton("Historia de la BioEstadística", style=button_style, on_click=lambda e: page.go("/ova/historia_bioestadistica")),
                ft.ElevatedButton("Población, Muestra y Variables", style=button_style, on_click=lambda e: page.go("/ova/2")),
                ft.ElevatedButton("Clasificación de Variables", style=button_style, on_click=lambda e: page.go("/clasificacion_variables")),
                ft.ElevatedButton("◀ Volver", on_click=volver_pizarra, style=button_style),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    ])

    page.add(contenido)
    page.update()

def mostrar_clasificacion_variables_juegos(page: ft.Page) -> None:
    page.clean()
    page.title = "Clasificación de Variables - Juegos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f0f0"

    button_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=6),
        elevation=2,
    )

    def volver_unidades(e):
        page.go("/unidades_especializadas")

    contenido_botones = ft.Column(
        [
            ft.Text(
                "Juegos de Clasificación de Variables",
                size=26,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=30),
            ft.Column(
                [
                    ft.ElevatedButton("Juego 1", style=button_style, on_click=lambda e: page.go("/juego/1")),
                    ft.ElevatedButton(
                        "Juego 2", 
                        style=button_style, 
                        on_click=lambda e: page.launch_url("https://mgx.dev/chat/bae3ed154bab4e128c6c4bc25d5ffe1c")),
                    ft.ElevatedButton(
                        "Juego 3", 
                        style=button_style, 
                        on_click=lambda e: page.launch_url("https://mgx.dev/chat/076f9e14545546918293a391646bef9f")),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=40),
            ft.ElevatedButton("◀ Volver", on_click=volver_unidades, style=button_style),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    contenido_stack = ft.Stack([
        ft.Image(
            src="https://i.postimg.cc/L6mnZmKc/clasificacion-Variables1.png",
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        ft.Container(
            content=contenido_botones,
            alignment=ft.alignment.center,
            expand=True
        ),
    ])

    page.add(contenido_stack)
    page.update()

def mostrar_investigacion(page: ft.Page) -> None:
    page.clean()
    page.title = "Investigación"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f0f0"

    button_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=6),
        elevation=2,
    )

    def volver_pizarra(e):
        page.go("/pizarra")

    contenido = ft.Stack([
        ft.Image(
            src="https://i.postimg.cc/prpQMhX9/laboratorios1.png",
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER,
        ),
        ft.Column(
            [
                ft.ElevatedButton("Programa_1", style=button_style, on_click=None),
                ft.ElevatedButton("Programa_2", style=button_style, on_click=None),
                ft.ElevatedButton("Programa_3", style=button_style, on_click=None),
                ft.ElevatedButton("◀ Volver", on_click=volver_pizarra, style=button_style),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    ])

    page.add(contenido)
    page.update()

def mostrar_fase4(page: ft.Page) -> None:
    page.clean()
    page.title = "Fase IV - Síntesis e Integración - Selecciona un módulo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f0f0"

    button_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=6),
        elevation=2,
    )

    def volver_fases(e):
        page.go("/fases")

    contenido = ft.Column(
        [
            ft.Text(
                "Fase IV - Síntesis e Integración - Selecciona un módulo",
                size=26,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=30),
            ft.Column(
                [
                    ft.ElevatedButton(
                        "OVA 20. Cierre y Proyección Profesional", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/20")
                    ),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=40),
            ft.ElevatedButton("◀ Volver", on_click=volver_fases, style=button_style),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(
        ft.Container(
            bgcolor="#f8f9fa",
            content=contenido,
            alignment=ft.alignment.center,
        )
    )
    page.update()


def mostrar_fase3(page: ft.Page) -> None:
    page.clean()
    page.title = "Fase III - Inferencia Estadística - Selecciona un módulo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f0f0"

    button_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=6),
        elevation=2,
    )

    def volver_fases(e):
        page.go("/fases")

    contenido = ft.Column(
        [
            ft.Text(
                "Fase III - Inferencia Estadística - Selecciona un módulo",
                size=26,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=30),
            ft.Column(
                [
                    ft.ElevatedButton(
                        "OVA 16. Intervalos para Diferencias", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/16")
                    ),
                    ft.ElevatedButton(
                        "OVA 17. Fundamentos de Pruebas de Hipótesis", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/17")
                    ),
                    ft.ElevatedButton(
                        "OVA 18. Pruebas Específicas para Ciencias de la Salud", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/18")
                    ),
                    ft.ElevatedButton(
                        "OVA 19. Aplicaciones Integradas", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/19")
                    ),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=40),
            ft.ElevatedButton("◀ Volver", on_click=volver_fases, style=button_style),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(
        ft.Container(
            bgcolor="#f8f9fa",
            content=contenido,
            alignment=ft.alignment.center,
        )
    )
    page.update()


def mostrar_fase2(page: ft.Page) -> None:
    page.clean()
    page.title = "Fase II - Probabilidad - Selecciona un módulo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f0f0"

    button_style = ft.ButtonStyle(
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_700,
        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=6),
        elevation=2,
    )

    def volver_fases(e):
        page.go("/fases")

    contenido = ft.Column(
        [
            ft.Text(
                "Fase II - Probabilidad - Selecciona un módulo",
                size=26,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=30),
            ft.Column(
                [
                    ft.ElevatedButton(
                        "OVA 8. Teoría de Conjuntos y Probabilidad Básica", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/8")
                    ),
                    ft.ElevatedButton(
                        "OVA 9. Probabilidad Condicional y Bayes", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/9")
                    ),
                    ft.ElevatedButton(
                        "OVA 10. Integración y Evaluación Parcial II", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/10")
                    ),
                    ft.ElevatedButton(
                        "OVA 11. Distribuciones Discretas en Medicina", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/11")
                    ),
                    ft.ElevatedButton(
                        "OVA 12. Distribución Binomial y Poisson", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/12")
                    ),
                    ft.ElevatedButton(
                        "OVA 13. Distribución Normal en Biomedicina", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/13")
                    ),
                    ft.ElevatedButton(
                        "OVA 14. Integración y Evaluación Parcial III", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/14")
                    ),
                    ft.ElevatedButton(
                        "OVA 15. Inferencia Estadística Básica", 
                        style=button_style, 
                        on_click=lambda e: page.go("/ova/15")
                    ),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=40),
            ft.ElevatedButton("◀ Volver", on_click=volver_fases, style=button_style),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(
        ft.Container(
            bgcolor="#f8f9fa",
            content=contenido,
            alignment=ft.alignment.center,
        )
    )
    page.update()


def route_change(page: ft.Page):
    if page.route == "/inicio_cover":
        inicio.main(page)
    elif page.route == "/":
        mostrar_inicio(page)
    elif page.route == "/fases":
        mostrar_fases(page)
    elif page.route == "/ovas_principal":
        mostrar_ovas_principal(page)
    elif page.route == "/hospital":
        mostrar_hospital(page)
    elif page.route == "/farmacia":
        mostrar_farmacia(page)
    elif page.route == "/farmacia_1":
        mostrar_farmacia_1(page)
    elif page.route == "/pizarra":
        mostrar_pizarra(page)
    elif page.route == "/unidades_especializadas":
        mostrar_unidades_especializadas(page)
    elif page.route == "/investigacion":
        mostrar_investigacion(page)
    elif page.route == "/clasificacion_variables":
        mostrar_clasificacion_variables_juegos(page)
    elif page.route == "/ovas":
        mostrar_menu_ovas(page)
    elif page.route == "/fase2":
        mostrar_fase2(page)
    elif page.route == "/fase3":
        mostrar_fase3(page)
    elif page.route == "/fase4":
        mostrar_fase4(page)
    elif page.route.startswith("/ova/"):
        clave = page.route.split("/ova/")[-1]
        abrir_ova(page, clave)
    elif page.route.startswith("/juego/"):
        clave = page.route.split("/juego/")[-1]
        abrir_juego(page, clave)
    else:
        # Ruta por defecto: cargar la pantalla de inicio desde inicio.py
        page.clean()
        inicio.main(page)
        page.update()



if __name__ == "__main__":
    ft.app(target=app_main, view=ft.AppView.WEB_BROWSER, port=8083)