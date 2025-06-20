import flet as ft

class inputForm(ft.TextField):
    def __init__(self, label: str, icon: str, ):
        super().__init__()
        self.label = label
        self.icon = icon
        self.width = 300
        if label == "descripcion":
            self.multiline = True
            self.min_lines = 3
            self.max_lines = 5
            
def equipment_form(page: ft.Page):
    
    container_form = ft.Container(
        width= 400,
        height= 400,
        bgcolor= ft.Colors.WHITE,
        border_radius= 20,
        content= ft.Column(
            alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            controls= [
                ft.Text("Agregar equipo", 
                        size= 30,
                        weight= ft.FontWeight.BOLD,
                        color= ft.Colors.GREY_700
                        ),
                inputForm("codigo", ft.Icons.QR_CODE_2),
                inputForm("nombre", ft.Icons.AIRPORT_SHUTTLE),
                inputForm("descripcion", ft.Icons.ASSIGNMENT),
                inputForm("proveedor", ft.Icons.STORE)
            ],
        )
    )
    
    return ft.Container(
        content= container_form,
        alignment=ft.alignment.center,
        expand=True
    )

