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
                        control.border = ft.border.all(3, ft.Colors.AMBER)
                    else:
                        control.border = ft.border.all(1, ft.Colors.GREY_600)
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
        
        # Contenedor principal con imagen y botón
        fondo_container = ft.Column([
            # Imagen de fondo reducida
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Image(
                    src="https://i.postimg.cc/02sy0XKB/portada-Estadistica-6.png",
                    width=page.window_width * 0.9,
                    height=page.window_height * 0.75,
                    fit=ft.ImageFit.CONTAIN,
                )
            ),
            # Espacio entre imagen y botón
            ft.Container(height=20),
            # Botón de ingreso en la parte inferior derecha
            ft.Container(
                alignment=ft.alignment.center_right,
                margin=ft.margin.only(right=50),
                content=ft.ElevatedButton(
                    "INGRESAR",
                    width=200,
                    height=60,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_700,
                        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
                    ),
                    on_click=ir_a_seleccion_avatar
                )
            )
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        page.add(fondo_container)
        page.update()
    
    def mostrar_seleccion_avatar():
        """Crear la pantalla de selección de avatar"""
        
        nonlocal avatar_container
        
        # Datos de los avatares
        avatares = [
            {"nombre": "Medicina", "icono": ft.Icons.SHIELD, "color": ft.Colors.RED_700},
            {"nombre": "Enfermería", "icono": ft.Icons.AUTO_FIX_HIGH, "color": ft.Colors.PURPLE_700},
            {"nombre": "Fisioterapia", "icono": ft.Icons.NATURE_PEOPLE, "color": ft.Colors.GREEN_700},
            {"nombre": "Odontología", "icono": ft.Icons.PSYCHOLOGY, "color": ft.Colors.BLUE_GREY_700},
        ]
        
        # Crear contenedores de avatares
        avatar_controls = []
        for avatar in avatares:
            avatar_control = ft.Container(
                width=80,
                height=100,
                bgcolor="#2d3748",
                border_radius=8,
                border=ft.border.all(1, ft.Colors.GREY_600),
                data=avatar["nombre"],
                content=ft.Column([
                    ft.Container(height=8),
                    ft.Container(
                        width=50,
                        height=50,
                        bgcolor=avatar["color"],
                        border_radius=25,
                        content=ft.Icon(
                            avatar["icono"],
                            size=25,
                            color=ft.Colors.WHITE
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(height=3),
                    ft.Text(
                        avatar["nombre"],
                        size=10,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                on_click=seleccionar_avatar(avatar["nombre"])
            )
            avatar_controls.append(avatar_control)
        
        avatar_container = ft.Row(
            avatar_controls,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        
        # Contenedor principal
        contenido = ft.Container(
            width=page.window_width,
            height=page.window_height,
            bgcolor="#0a0a0a",
            content=ft.Column([
                ft.Container(height=40),
                
                # Título principal
                ft.Text(
                    "Curso de Estadística",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#4169E1",
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Container(height=15),
                
                # Subtítulo
                ft.Text(
                    "¡Selecciona tu avatar y comienza la aventura!",
                    size=14,
                    color=ft.Colors.WHITE70,
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Container(height=30),
                
                # Título de selección
                ft.Text(
                    "Elige tu avatar de Aventurero:",
                    size=18,
                    color=ft.Colors.LIGHT_BLUE_300,
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Container(height=25),
                
                # Contenedor de avatares
                avatar_container,
                
                ft.Container(height=30),
                
                # Botones
                ft.Row([
                    ft.ElevatedButton(
                        "◀ Volver",
                        width=120,
                        height=40,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.GREY_700,
                        ),
                        on_click=volver_inicio
                    ),
                    
                    ft.Container(width=50),
                    
                    ft.ElevatedButton(
                        "▶ Comenzar Aventura",
                        width=200,
                        height=50,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_700,
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
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.GREY_600,
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
