import flet as ft
import datetime

from src.widgets.gradient_button import gradient_button
from src.widgets.input_form import input_form
from src.widgets.custom_button import custom_button

from src.consts.colors import gradient_colors, gradient_colors2, gradient_colors3, middle_color

def create_maintenance_view(page: ft.Page, on_success=None):
    title_form = ft.Column(
        controls= [
            # main_img,
            ft.Icon(
                ft.Icons.BUILD,
                size= 80,
                color= middle_color
            ),
            ft.Text(
                value= "Agregar orden de mantenimiento",
                size= 20,
                weight= ft.FontWeight.BOLD,
                color= ft.Colors.GREY_700
            ),
            ft.Divider(height= 15, color= ft.Colors.GREY_300),
        ],
        alignment= ft.MainAxisAlignment.CENTER,
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        spacing=5
    )
    
    date_picker = ft.DatePicker(
        first_date = datetime.datetime.now(),
        on_change= lambda e: print(f"fecha seleccionada: {e.data}"),
        on_dismiss= lambda e: print("fecha no seleccionada")
    )
    
    def open_date_picker(e):
        date_picker.open = True
        page.update()
        
    selected_date = ft.Text(
        value= "Seleccionar fecha",
        size= 15,
        color= ft.Colors.GREY_700
    )
    
    def handle_date_selection(e):
        if date_picker.value:
            selected_date.value = date_picker.value.strftime("%d-%m-%Y")
        else:
            selected_date.value = "Seleccionar fecha"
        
        page.update()
        
    date_picker.on_change = handle_date_selection
    page.overlay.append(date_picker)
    
    container_form = ft.Container(
        width=400,
        height=550,
        border_radius=20,
        bgcolor=ft.Colors.WHITE,
        border = ft.border.all(1, ft.Colors.GREY_300),
        padding=ft.padding.all(20),
        content= ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                title_form,
                ft.Row(
                    controls=[
                        # estos custom buttons son para seleccionar el equipo y tecnico
                        # se abre una pagina, donde dice los ultimos 5 seleccionados, y luego una lista (asi estilo estados de ws).
                        
                        custom_button(
                            text= "Equipo",
                            width=150,
                            height=150,
                            gradient= gradient_colors2,
                            icon= ft.Icons.PRECISION_MANUFACTURING,
                            on_click= lambda e: print("ventana emergente de eleccion de equipo") 
                        ),
                        custom_button(
                            text= "Tecnico",
                            width=150,
                            height=150,
                            gradient= gradient_colors3,
                            icon= ft.Icons.PERSON,
                            on_click= lambda e: print("ventana emergente de eleccion de tecnico")
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                input_form(
                    label ="Descripcion",
                    icon= ft.Icons.ASSIGNMENT
                ),
                ft.ElevatedButton(
                    width=350,
                    height=50,
                    content = ft.Row(
                        controls= [
                            ft.Icon(
                                ft.Icons.DATE_RANGE,
                                color=ft.Colors.GREY_700
                            ),
                            selected_date
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    ),
                    style=ft.ButtonStyle(
                        padding=ft.padding.all(15),
                        bgcolor=ft.Colors.WHITE,
                        side=ft.BorderSide(1, ft.Colors.GREY_300),
                        shape=ft.RoundedRectangleBorder(radius=20),
                    ),
                    on_click= open_date_picker,
                ),
            ]
        )
    )
    
    return ft.Container(
        content= ft.Column(
            controls=[
                container_form,
                gradient_button(
                    text= 'agregar',
                    width=300,
                    height=48,
                    gradient= gradient_colors,
                    on_click= lambda e: print('guardar orden de mantenimiento'),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center,
        expand=True
    )