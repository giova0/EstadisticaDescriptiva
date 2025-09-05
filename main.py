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

    # Lista básica de OVAs disponibles
    ovas = [
        ("1", "OVA 1: Bioestadística esencial para salud"),
        ("2", "OVA 2: Calidad y limpieza de datos clínicos"),
        ("3", "OVA 3: Tablas de frecuencias y resúmenes categóricos"),
        ("4", "OVA 4: Medidas de tendencia central y posición"),
        ("6", "OVA 6: Asimetría, curtosis y normalidad práctica"),
        ("12", "OVA 12: Curvas epidémicas y series de tiempo"),
        ("18", "OVA 18: Dashboard descriptivo básico"),
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
            ova = load_module_by_filename("1. OVA_bioestadistica_flet.py", "ova1")
            if not run_module_main(ova):
                # Fallback explícito
                app = ova.OVABioestadistica()
                app.main(page)
            return
        if clave == "2":
            ova = load_module_by_filename("2. OVA_calidad_datos_flet.py", "ova2")
            if not run_module_main(ova):
                app = ova.OVAApp()
                app.main(page)
            return
        if clave == "3":
            ova = load_module_by_filename("3. OVA_tablas_frecuencias_flet.py", "ova3")
            if not run_module_main(ova):
                app = ova.OVAApp()
                app.main(page)
            return
        if clave == "4":
            ova = load_module_by_filename("4. OVA_medidas_tendencia_central_flet.py", "ova4")
            if not run_module_main(ova):
                app = ova.OVAApp()
                app.main(page)
            return
        if clave == "6":
            ova = load_module_by_filename("6. OVA_asimetria_curtosis_flet.py", "ova6")
            if not run_module_main(ova):
                app = ova.OVAAsimetriaCurtosis()
                app.main(page)
            return
        if clave == "12":
            ova = load_module_by_filename("12. OVA_curvas_epidemicas_flet.py", "ova12")
            # Esta OVA construye UI en su __init__(page)
            if not run_module_main(ova):
                ova.OVAEpidemicCurves(page)
            return
        if clave == "18":
            ova = load_module_by_filename("18. OVA_dashboard_flet.py", "ova18")
            if not run_module_main(ova):
                ova.main(page)
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
    ft.app(target=app_main)
