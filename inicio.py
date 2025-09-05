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
                        control.border = ft.border.all(3, ft.Colors.BLUE_700)
                    else:
                        control.border = ft.border.all(2, ft.Colors.GREY_400)
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
        """Crear la pantalla de inicio con imagen de fondo completa"""
        
        # Contenedor principal con imagen de fondo completa y botón superpuesto
        fondo_container = ft.Stack([
            # Imagen de fondo que ocupa toda la pantalla
            ft.Image(
                src="https://i.postimg.cc/rw0Q9BF2/portada1-6.png",
                width=page.window_width,
                height=page.window_height,
                fit=ft.ImageFit.COVER,
            ),
            # Botón superpuesto en la esquina inferior derecha
            ft.Container(
                width=page.window_width,
                height=page.window_height,
                alignment=ft.alignment.bottom_right,
                padding=ft.padding.only(right=50, bottom=50),
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
        ])
        
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
            # Usar imágenes reales para todas las carreras
            if avatar["nombre"] == "Medicina":
                contenido_imagen = ft.Container(
                    width=50,
                    height=50,
                    border_radius=25,
                    content=ft.Image(
                        src="https://i.postimg.cc/0QCSDVYg/estudiante-medicina.png",
                        width=50,
                        height=50,
                        fit=ft.ImageFit.COVER,
                        border_radius=25
                    ),
                    alignment=ft.alignment.center
                )
            elif avatar["nombre"] == "Enfermería":
                contenido_imagen = ft.Container(
                    width=50,
                    height=50,
                    border_radius=25,
                    content=ft.Image(
                        src="https://i.postimg.cc/bvkkNydw/estudiante-enfermeria.png",
                        width=50,
                        height=50,
                        fit=ft.ImageFit.COVER,
                        border_radius=25
                    ),
                    alignment=ft.alignment.center
                )
            elif avatar["nombre"] == "Fisioterapia":
                contenido_imagen = ft.Container(
                    width=50,
                    height=50,
                    border_radius=25,
                    content=ft.Image(
                        src="https://i.postimg.cc/13fztHRz/fisioterapia-2.png",
                        width=50,
                        height=50,
                        fit=ft.ImageFit.COVER,
                        border_radius=25
                    ),
                    alignment=ft.alignment.center
                )
            elif avatar["nombre"] == "Odontología":
                contenido_imagen = ft.Container(
                    width=50,
                    height=50,
                    border_radius=25,
                    content=ft.Image(
                        src="https://i.postimg.cc/G3gw214k/odontologo-1.png",
                        width=50,
                        height=50,
                        fit=ft.ImageFit.COVER,
                        border_radius=25
                    ),
                    alignment=ft.alignment.center
                )
            
            avatar_control = ft.Container(
                width=90,
                height=120,
                bgcolor=ft.Colors.GREY_100,
                border_radius=8,
                border=ft.border.all(2, ft.Colors.GREY_400),
                data=avatar["nombre"],
                content=ft.Column([
                    ft.Container(height=10),
                    contenido_imagen,
                    ft.Container(height=8),
                    ft.Text(
                        avatar["nombre"],
                        size=12,
                        color=ft.Colors.GREY_800,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_500
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
            bgcolor=ft.Colors.WHITE,
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
                    color=ft.Colors.GREY_700,
                    text_align=ft.TextAlign.CENTER
                ),
                
                ft.Container(height=30),
                
                # Título de selección
                ft.Text(
                    "Elige tu avatar de Aventurero:",
                    size=18,
                    color=ft.Colors.BLUE_700,
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
