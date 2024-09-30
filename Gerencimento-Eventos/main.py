import flet as ft
from Telas.telaLogin import TelaLogin

def main(page: ft.Page):
    tela_login = TelaLogin(page)
    tela_login.mostrar()

ft.app(target=main,  view=ft.WEB_BROWSER)
    