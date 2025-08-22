import flet as ft

def main(page: ft.Page):
    page.title = "Curso de Estadística"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1a1a1a"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 1024
    page.window_height = 768
    
    def ir_a_seleccion_avatar(e):
        """Función para cambiar a la pantalla de selección de avatar"""
        page.clean()
        mostrar_seleccion_avatar()
    
    def volver_inicio(e):
        """Función para volver a la pantalla de inicio"""
        page.clean()
        mostrar_pantalla_inicio()
    
    def seleccionar_avatar(avatar_tipo):
        """Función para manejar la selección de avatar"""
        def on_click(e):
            # Aquí puedes agregar la lógica para seleccionar el avatar
            print(f"Avatar seleccionado: {avatar_tipo}")
            # Por ejemplo, cambiar el color del contenedor seleccionado
            for control in avatar_container.controls:
                if isinstance(control, ft.Container):
                    if control.data == avatar_tipo:
                        control.border = ft.border.all(3, ft.colors.AMBER)
                    else:
                        control.border = ft.border.all(1, ft.colors.GREY_600)
            page.update()
        return on_click
    
    def comenzar_aventura(e):
        """Función para comenzar la aventura"""
        page.go("/estadistica")
    
    def mostrar_ayuda(e):
        """Función para mostrar ayuda"""
        print("Mostrando ayuda...")
        # Aquí agregarías la lógica para mostrar la ayuda
    
    def mostrar_pantalla_inicio():
        """Crear la pantalla de inicio con el libro"""
        
        # Contenedor principal con fondo de piedra simulado
        fondo_container = ft.Container(
            width=page.window_width,
            height=page.window_height,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#2d1810", "#1a0f08", "#3d2415"]
            ),
            content=ft.Stack([
                # Elementos decorativos (antorchas simuladas)
                ft.Container(
                    left=50,
                    top=100,
                    width=20,
                    height=60,
                    bgcolor=ft.colors.ORANGE_800,
                    border_radius=10,
                ),
                ft.Container(
                    right=50,
                    top=150,
                    width=20,
                    height=60,
                    bgcolor=ft.colors.ORANGE_800,
                    border_radius=10,
                ),
                
                # Contenedor principal centrado
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Row([
                        # Libro central
                        ft.Container(
                            width=300,
                            height=400,
                            bgcolor="#7FFFD4",
                            border_radius=15,
                            border=ft.border.all(3, "#654321"),
                            content=ft.Column([
                                ft.Container(height=40),
                                ft.Text(
                                    "CURSO DE ESTADÍSTICA",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color="#4169E1",
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Container(height=20),
                                # Escudo con corona y cruz
                                ft.Container(
                                    width=120,
                                    height=140,
                                    bgcolor=ft.colors.BLUE_800,
                                    border_radius=60,
                                    border=ft.border.all(3, ft.colors.AMBER_700),
                                    content=ft.Column([
                                        ft.Container(height=20),
                                        ft.Icon(
                                            ft.icons.CASTLE,
                                            size=40,
                                            color=ft.colors.AMBER_700
                                        ),
                                        ft.Icon(
                                            ft.icons.ADD,
                                            size=30,
                                            color=ft.colors.AMBER_700
                                        ),
                                    ], alignment=ft.MainAxisAlignment.CENTER)
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                        ),
                        
                        ft.Container(width=100),
                        
                        # Texto de bienvenida y botón
                        ft.Column([
                            ft.Text(
                                "Bienvenido al Curso",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color="#4169E1",
                            ),
                            ft.Container(height=50),
                            ft.ElevatedButton(
                                "INGRESAR",
                                width=150,
                                height=50,
                                style=ft.ButtonStyle(
                                    color=ft.colors.WHITE,
                                    bgcolor=ft.colors.BLUE_700,
                                    text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                                ),
                                on_click=ir_a_seleccion_avatar
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.CENTER)
                )
            ])
        )
        
        page.add(fondo_container)
        page.update()
    
    def mostrar_seleccion_avatar():
        """Crear la pantalla de selección de avatar"""
        
        nonlocal avatar_container
        
        # Datos de los avatares
        avatares = [
            {"nombre": "Medicina", "icono": ft.icons.SHIELD, "color": ft.colors.RED_700},
            {"nombre": "Enfermería", "icono": ft.icons.AUTO_FIX_HIGH, "color": ft.colors.PURPLE_700},
            {"nombre": "Fisioterapia", "icono": ft.icons.NATURE_PEOPLE, "color": ft.colors.GREEN_700},
            {"nombre": "Odontología", "icono": ft.icons.PSYCHOLOGY, "color": ft.colors.BLUE_GREY_700},
        ]
        
        # Crear contenedores de avatares
        avatar_controls = []
        for avatar in avatares:
            avatar_control = ft.Container(
                width=100,
                height=120,
                bgcolor="#2d3748",
                border_radius=10,
                border=ft.border.all(1, ft.colors.GREY_600),
                data=avatar["nombre"],
                content=ft.Column([
                    ft.Container(height=10),
                    ft.Container(
                        width=60,
                        height=60,
                        bgcolor=avatar["color"],
                        border_radius=30,
                        content=ft.Icon(
                            avatar["icono"],
                            size=30,
                            color=ft.colors.WHITE
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=5),
                    ft.Text(
                        avatar["nombre"],
                        size=12,
                        color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                on_click=seleccionar_avatar(avatar["nombre"])
            )
            avatar_controls.append(avatar_control)
        
        avatar_container = ft.Row(
            avatar_controls,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30
        )
        
        # Contenedor principal
        contenido = ft.Container(
            width=page.window_width,
            height=page.window_height,
            bgcolor="#0a0a0a",
            content=ft.Column([
                ft.Container(height=80),
                
                # Título principal
                ft.Text(
                    "Curso de Estadística",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color="#4169E1",
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Container(height=20),
                
                # Subtítulo
                ft.Text(
                    "¡Selecciona tu avatar y comienza la aventura!",
                    size=16,
                    color=ft.colors.WHITE70,
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Container(height=60),
                
                # Título de selección
                ft.Text(
                    "Elige tu avatar de Aventurero:",
                    size=20,
                    color=ft.colors.LIGHT_BLUE_300,
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Container(height=40),
                
                # Contenedor de avatares
                avatar_container,
                
                ft.Container(height=60),
                
                # Botones
                ft.Row([
                    ft.ElevatedButton(
                        "◀ Volver",
                        width=120,
                        height=40,
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.GREY_700,
                        ),
                        on_click=volver_inicio
                    ),
                    
                    ft.Container(width=50),
                    
                    ft.ElevatedButton(
                        "▶ Comenzar Aventura",
                        width=200,
                        height=50,
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE_700,
                            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                        ),
                        on_click=comenzar_aventura
                    ),
                    
                    ft.Container(width=50),
                    
                    ft.ElevatedButton(
                        "❓ Ayuda",
                        width=100,
                        height=40,
                        style=ft.ButtonStyle(
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.GREY_600,
                        ),
                        on_click=mostrar_ayuda
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
                
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        
        page.add(contenido)
        page.update()
    
    # Variable global para el contenedor de avatares
    avatar_container = None
    
    # Mostrar la pantalla inicial
    mostrar_pantalla_inicio()

if __name__ == "__main__":
    ft.app(target=main)
