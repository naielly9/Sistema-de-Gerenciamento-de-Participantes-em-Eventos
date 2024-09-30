import flet as ft
from .telaBase import TelaBase
from .componentes.campoTexto import CampoTexto
from .componentes.botao import BotaoTexto

class TelaListarEventoPorParticipante(TelaBase):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.eventos_por_pagina = 15
        self.pagina_atual = 1
        self.participante = None
        self.eventos_filtrados = []

    def obter_eventos_por_participante(self, participante):
        todos_eventos = [
            {"nome": f"Evento {i + 1}", "data": "01/01/2024", "participantes": ["123.456.789-00"]}
            for i in range(100)
        ]
        eventos_participante = [evento for evento in todos_eventos if participante in evento["participantes"]]
        return eventos_participante

    def buscar_eventos(self, e):
        participante = self.campo_busca.value
        self.participante = participante

        if not participante:
            self.page.snack_bar = ft.SnackBar(ft.Text("Informe o nome ou CPF do participante."), open=True)
            self.page.update()
            return

        self.eventos_filtrados = self.obter_eventos_por_participante(participante)
        if not self.eventos_filtrados:
            self.page.snack_bar = ft.SnackBar(ft.Text("Nenhum evento encontrado para o participante."), open=True)
        self.pagina_atual = 1
        self.mostrar()

    def proxima_pagina(self, e):
        self.pagina_atual += 1
        self.mostrar()

    def pagina_anterior(self, e):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
        self.mostrar()

    def mostrar(self):
        self.page.clean()
        self.campo_busca = CampoTexto("Nome ou CPF do Participante")
        eventos = self.eventos_filtrados[(self.pagina_atual - 1) * self.eventos_por_pagina : self.pagina_atual * self.eventos_por_pagina]

        lista_eventos = ft.Column(
            [ft.Text(f"{evento['nome']} - {evento['data']}") for evento in eventos],
            spacing=10
        )

        paginacao = ft.Row(
            [
                ft.Container(BotaoTexto("Página Anterior", self.pagina_anterior), expand=False),
                ft.Text(f"Página {self.pagina_atual}", expand=True, text_align="center"),
                ft.Container(BotaoTexto("Próxima Página", self.proxima_pagina), expand=False),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        conteudo_principal = ft.Column(
            [
                self.campo_busca,
                BotaoTexto("Buscar", self.buscar_eventos),
                lista_eventos,
                ft.Container(expand=True),  
                paginacao,
            ],
            spacing=20,
            expand=True
        )

        self.page.add(conteudo_principal)
        self.page.update()
