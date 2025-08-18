import flet as ft
import pandas as pd
import io

def main(page: ft.Page):
    page.title = "OVA 7: Estadística Descriptiva Aplicada a Ciencias de la Salud"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50
    page.window_width = 900
    page.window_height = 800
    page.scroll = "adaptive"

    # --- Data for the chart ---
    data = """
Categoria,Frecuencia
Hipertensión,120
Diabetes,85
Asma,60
Obesidad,75
Covid-19,40
"""
    df = pd.read_csv(io.StringIO(data))

    # --- Chart ---
    chart = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=row["Frecuencia"],
                        width=20,
                        color=ft.colors.BLUE,
                        tooltip=f"{row['Categoria']}: {row['Frecuencia']}",
                        border_radius=0,
                    )
                ],
            )
            for i, row in df.iterrows()
        ],
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=i, label=ft.Text(row["Categoria"], size=10, text_align=ft.TextAlign.CENTER))
                for i, row in df.iterrows()
            ],
            labels_size=40,
        ),
        left_axis=ft.ChartAxis(
            labels_size=40,
            title=ft.Text("Frecuencia"),
            title_size=14,
        ),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=20, color=ft.colors.GREY_300, width=1
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.WHITE),
        max_y=140,
        interactive=True,
        expand=True,
    )

    # --- Interactive Question ---
    feedback_text = ft.Text(value="", visible=False)

    def check_answer(e):
        if e.control.value == "Gráfico de Barras":
            feedback_text.value = "¡Correcto! El gráfico de barras es ideal para comparar frecuencias entre categorías."
            feedback_text.color = ft.colors.GREEN
        else:
            feedback_text.value = "Respuesta incorrecta. El gráfico de barras es el más adecuado para comparar categorías discretas."
            feedback_text.color = ft.colors.RED
        feedback_text.visible = True
        page.update()

    radio_group = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="Gráfico de Líneas", label="Gráfico de Líneas"),
            ft.Radio(value="Gráfico de Dispersión", label="Gráfico de Dispersión"),
            ft.Radio(value="Gráfico de Barras", label="Gráfico de Barras"),
            ft.Radio(value="Histograma", label="Histograma"),
        ]),
        on_change=check_answer,
    )

    # --- App Layout ---
    app_layout = ft.Column(
        controls=[
            ft.Text("OVA 07: Visualización para Salud I - Gráficos Categóricos", size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Text(
                "Bienvenido a la séptima OVA. En esta unidad, exploraremos cómo visualizar datos categóricos de salud utilizando herramientas interactivas para fortalecer el pensamiento estadístico.",
                size=16,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Divider(),
            ft.Text("Gráfico Interactivo: Frecuencia de Condiciones de Salud", size=24, weight=ft.FontWeight.W_500),
            ft.Text("Pasa el cursor sobre las barras para ver los valores exactos."),
            ft.Container(
                content=chart,
                height=350,
                padding=20,
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=ft.border_radius.all(5),
            ),
            ft.Divider(),
            ft.Text("Práctica Interactiva (Modelo C(H)ANGE)", size=24, weight=ft.FontWeight.W_500),
            ft.Text("¿Qué tipo de gráfico es más adecuado para comparar la frecuencia de diagnósticos médicos entre diferentes grupos de pacientes (categorías no ordenadas)?"),
            radio_group,
            feedback_text,
            ft.Divider(),
            ft.Text("Conceptos Clave", size=24, weight=ft.FontWeight.W_500),
            ft.Text(
                "• Variable Categórica: Representa características o cualidades que no pueden ser medidas con números (ej. tipo de diagnóstico).\n"
                "• Gráfico de Barras: Compara valores numéricos (frecuencias) entre diferentes categorías.\n"
                "• Frecuencia: El número de veces que un evento o característica aparece en un conjunto de datos."
            ),
             ft.Divider(),
            ft.Text("Cierre y Siguientes Pasos", size=24, weight=ft.FontWeight.W_500),
            ft.Text(
                "Has aprendido a crear e interpretar un gráfico de barras para datos de salud. En la próxima OVA, exploraremos la visualización de datos numéricos y su distribución."
            ),
        ],
        spacing=20,
        width=800,
    )

    page.add(app_layout)

if __name__ == "__main__":
    ft.app(target=main)
