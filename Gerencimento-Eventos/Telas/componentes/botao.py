import flet as ft
from .identidadeVisual import COR_PRIMARIA

def Botao(rotulo: str, acao, primario: bool = False):
    if primario:
        return ft.ElevatedButton(
            rotulo,
            on_click=acao,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=COR_PRIMARIA,
                shape=ft.RoundedRectangleBorder(radius=5),
            )
        )
    else:
        return ft.ElevatedButton(
            rotulo,
            on_click=acao
        )

def BotaoTexto(rotulo: str, acao):
    return ft.TextButton(
        rotulo,
        on_click=acao,
        style=ft.ButtonStyle(color=COR_PRIMARIA)
    )
