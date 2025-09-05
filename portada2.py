
import flet as ft

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Codédx Dashboard"
    page.bgcolor = "#f0f2f5"
    page.padding = 30
    page.window_width = 1200
    page.window_height = 800
    page.scroll = ft.ScrollMode.AUTO

    # Función para crear tarjetas con estilo consistente
    def create_card(content, width=None, height=None):
        return ft.Container(
            content=content,
            padding=ft.padding.all(20),
            bgcolor=ft.colors.WHITE,
            border_radius=ft.border_radius.all(12),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color=ft.colors.BLACK12,
                offset=ft.Offset(0, 2),
            ),
            width=width,
            height=height,
        )

    # 1. Mensaje del computador (parte superior izquierda)
    computer_message = ft.Row(
        [
            ft.Container(
                content=ft.Icon(
                    name=ft.icons.COMPUTER,
                    size=40,
                    color=ft.colors.BLUE_400
                ),
                width=50,
                height=50,
                bgcolor=ft.colors.BLUE_50,
                border_radius=ft.border_radius.all(8),
                alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.Text(
                    "Hi bestie! Intermediate Python is out now!",
                    size=14,
                    color=ft.colors.BLACK87,
                    weight=ft.FontWeight.W_500,
                ),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                bgcolor=ft.colors.WHITE,
                border_radius=ft.border_radius.all(20),
                border=ft.border.all(1, ft.colors.GREY_300),
                margin=ft.margin.only(left=10),
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # 2. Tarjeta principal de bienvenida
    welcome_card = create_card(
        ft.Column(
            [
                ft.Container(
                    content=ft.Icon(
                        name=ft.icons.PERSON,
                        size=80,
                        color=ft.colors.PURPLE_400,
                    ),
                    width=120,
                    height=120,
                    bgcolor=ft.colors.PURPLE_50,
                    border_radius=ft.border_radius.all(60),
                    alignment=ft.alignment.center,
                ),
                ft.Text(
                    "Welcome to Codédx!",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK87,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Your coding journey awaits—but first let's find something to learn.",
                    size=16,
                    color=ft.colors.GREY_600,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=10),
                ft.ElevatedButton(
                    content=ft.Text(
                        "Get Started",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                    ),
                    bgcolor=ft.colors.BLUE_600,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=32, vertical=16),
                    ),
                    on_click=lambda e: print("Get Started clicked"),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        width=500,
    )

    # 3. Tarjeta de perfil de usuario
    profile_card = create_card(
        ft.Column(
            [
                # Información del usuario
                ft.Row(
                    [
                        ft.CircleAvatar(
                            content=ft.Text("G", size=20, weight=ft.FontWeight.BOLD),
                            radius=25,
                            bgcolor=ft.colors.GREEN_400,
                            color=ft.colors.WHITE,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "giova0294",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLACK87,
                                ),
                                ft.Text(
                                    "Level 1",
                                    size=14,
                                    color=ft.colors.GREY_600,
                                ),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=12,
                ),
                
                ft.Container(height=20),
                
                # Estadísticas - Primera fila
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Icon(
                                    name=ft.icons.STAR,
                                    size=24,
                                    color=ft.colors.AMBER_500,
                                ),
                                ft.Text(
                                    "0",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLACK87,
                                ),
                                ft.Text(
                                    "Total XP",
                                    size=12,
                                    color=ft.colors.GREY_600,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                            expand=True,
                        ),
                        ft.Column(
                            [
                                ft.Icon(
                                    name=ft.icons.MILITARY_TECH,
                                    size=24,
                                    color=ft.colors.BROWN_600,
                                ),
                                ft.Text(
                                    "Bronze",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLACK87,
                                ),
                                ft.Text(
                                    "Rank",
                                    size=12,
                                    color=ft.colors.GREY_600,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                            expand=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                
                ft.Container(height=15),
                
                # Estadísticas - Segunda fila
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Icon(
                                    name=ft.icons.BADGE,
                                    size=24,
                                    color=ft.colors.BLUE_500,
                                ),
                                ft.Text(
                                    "0",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLACK87,
                                ),
                                ft.Text(
                                    "Badges",
                                    size=12,
                                    color=ft.colors.GREY_600,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                            expand=True,
                        ),
                        ft.Column(
                            [
                                ft.Icon(
                                    name=ft.icons.LOCAL_FIRE_DEPARTMENT,
                                    size=24,
                                    color=ft.colors.ORANGE_600,
                                ),
                                ft.Text(
                                    "1",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLACK87,
                                ),
                                ft.Text(
                                    "Day streak",
                                    size=12,
                                    color=ft.colors.GREY_600,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                            expand=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                
                ft.Container(height=20),
                
                # Botón de perfil
                ft.OutlinedButton(
                    content=ft.Text(
                        "View profile",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=ft.colors.BLACK87,
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        side=ft.BorderSide(1, ft.colors.GREY_300),
                        padding=ft.padding.symmetric(vertical=12),
                    ),
                    width=float('inf'),
                    on_click=lambda e: print("View profile clicked"),
                ),
            ],
            spacing=0,
        ),
        width=280,
    )

    # 4. Función para crear elementos de eventos
    def create_event_item(month, day, title, datetime_str, color):
        return ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                month,
                                size=10,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE,
                            ),
                            ft.Text(
                                str(day),
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    width=50,
                    height=50,
                    bgcolor=color,
                    border_radius=ft.border_radius.all(8),
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    [
                        ft.Text(
                            title,
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK87,
                        ),
                        ft.Text(
                            datetime_str,
                            size=12,
                            color=ft.colors.GREY_600,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
            ],
            spacing=12,
        )

    # 5. Tarjeta de eventos próximos
    events_card = create_card(
        ft.Column(
            [
                ft.Text(
                    "Upcoming Events",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK87,
                ),
                ft.Container(height=15),
                create_event_item(
                    "AUG", 27, 
                    "August Rhythm Remixer",
                    "Wed Aug 27th @ 3:00pm ET",
                    ft.colors.ORANGE_400
                ),
                ft.Container(height=15),
                create_event_item(
                    "SEP", 10,
                    "Club LinkedIn Profile Reviews", 
                    "Wed Sep 10th @ 3:00pm ET",
                    ft.colors.GREEN_500
                ),
                ft.Container(height=15),
                create_event_item(
                    "OCT", 1,
                    "Resume Review Workshop",
                    "Wed Oct 1st @ 3:00pm ET", 
                    ft.colors.RED_400
                ),
            ],
            spacing=0,
        ),
        width=280,
    )

    # Layout principal
    main_layout = ft.Row(
        [
            # Columna izquierda - Contenido principal
            ft.Column(
                [
                    computer_message,
                    ft.Container(height=30),
                    welcome_card,
                    ft.Container(height=40),
                    ft.Text(
                        "Explore more",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLACK87,
                    ),
                ],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            
            ft.Container(width=30),  # Espaciado entre columnas
            
            # Columna derecha - Sidebar
            ft.Column(
                [
                    profile_card,
                    ft.Container(height=20),
                    events_card,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

    page.add(main_layout)

# Para ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=main)
