import flet as ft

def CampoDropdown(rotulo: str, opcoes: list = None):
    if opcoes is None:
        opcoes = [
            "Show Musical", 
            "Peça de Teatro", 
            "Exposição de Museu", 
            "Apresentação de Circo", 
            "Baile Dançante", 
            "Mostra de Artes", 
            "Outro"
        ]
    
    return ft.Dropdown(
        label=rotulo,
        options=[ft.dropdown.Option(text=opcao) for opcao in opcoes],
        width=200,  
        border_color='#9ca3af',
        focused_color='#e5e7eb',
        filled=False,
        color='#e5e7eb',  
        label_style=ft.TextStyle(color='#e5e7eb'),  
        focused_bgcolor=ft.colors.WHITE, 
    )
