import flet as ft

class inputForm(ft.TextField):
    def __init__(self, label: str, icon: str, height):
        super().__init__()
        self.label = label
        self.icon = icon
        self.width = 300
        self.height = height
        if label == "descripcion":
            self.multiline = True
            self.min_lines = 3
            self.max_lines = 5
            
def equipment_form(page: ft.Page):
    return ft.Column(
        [
            ft.Text("Agregar equipo", size=50), 
            inputForm("codigo", ft.Icons.QR_CODE_2, 100),
            inputForm("nombre", ft.Icons.AIRPORT_SHUTTLE, 100),
            inputForm("descripcion", ft.Icons.ASSIGNMENT, 500),
            inputForm("proveedor", ft.Icons.STORE, 100)
        ]
    )

