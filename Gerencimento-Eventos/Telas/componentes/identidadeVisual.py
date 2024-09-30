import flet as ft

GRADIENTE = ft.LinearGradient(
    colors=["#4a044e", "#c026d3"],
    begin=ft.Alignment(-1, -1),
    end=ft.Alignment(1, 1)
)

COR_PRIMARIA = '#e879f9'
COR_TEXTO_CLARO = ft.colors.WHITE
COR_TEXTO_ESCURO = ft.colors.BLACK

ESTILO_BOTAO_PRIMARIO = ft.ButtonStyle(
    color=COR_TEXTO_CLARO,
    bgcolor=COR_PRIMARIA,
    shape=ft.RoundedRectangleBorder(radius=5),
)

ESTILO_BOTAO_SECUNDARIO = ft.ButtonStyle(
    color=COR_PRIMARIA,
    shape=ft.RoundedRectangleBorder(radius=5),
)


ALINHAMENTO_COLUNA = {
    "alignment": ft.MainAxisAlignment.CENTER,
    "horizontal_alignment": ft.CrossAxisAlignment.CENTER,
    "spacing": 20
}

ALINHAMENTO_LINHA = {
    "alignment": ft.MainAxisAlignment.CENTER,
    "vertical_alignment": ft.CrossAxisAlignment.CENTER
}

def FUNDO_QUADRADO(conteudo):
   return ft.Container(
        content=conteudo,
        width=300, 
        height=400, 
        padding=20,
        border_radius=10, 
        bgcolor="#701a75", 
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(
            blur_radius=15,
            spread_radius=5,
            color="#f0abfc", 
        )
    )