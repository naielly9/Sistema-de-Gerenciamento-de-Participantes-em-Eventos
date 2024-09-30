import flet as ft

class TelaBase:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.window_resizable = False 
        self.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#4a044e"
    
    def mostrar(self):
        raise NotImplementedError("A subclasse deve implementar este método")
