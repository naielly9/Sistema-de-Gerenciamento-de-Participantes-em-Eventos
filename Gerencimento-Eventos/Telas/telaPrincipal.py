import flet as ft
from .telaBase import TelaBase
from database import Database

class TelaPrincipal(TelaBase):
    def __init__(self, page: ft.Page, identificador: int):
        super().__init__(page)
        self.db = Database()
        self.identificador = identificador

    def ao_clicar_cadastro_participante(self, e):
        from .telaCadastro import TelaCadastro
        self.page.clean()
        tela_cadastro = TelaCadastro(self.page,False, self.participante)
        tela_cadastro.mostrar()

    def ao_clicar_cadastro_evento(self, e):
        from .telaEventos import TelaCadastroEvento
        self.page.clean()
        tela_cadastroevento = TelaCadastroEvento(self.page,self.participante,True,None)
        tela_cadastroevento.mostrar()

    def ao_clicar_listar_eventos(self, e):
        from .telaListarEventos import TelaHistoricoEventos
        self.page.clean()
        tela_historico= TelaHistoricoEventos(self.page, self.participante)
        tela_historico.mostrar()


    def ao_clicar_eventos_participante(self, e):
        from .telaListarEventosParticipante import TelaListarEventoPorParticipante
        self.page.clean()
        tela_eventoparticipante = TelaListarEventoPorParticipante(self.page)
        tela_eventoparticipante.mostrar()


    def ao_clicar_buscar_eventos(self, e):
       from .telaBuscarEventos import TelaBuscarEventos
       self.page.clean()
       tela_buscarevento = TelaBuscarEventos(self.page)
       tela_buscarevento.mostrar()
       
    def mostrar(self):
        self.page.title = "Sistema de Gerenciamento de Eventos"
        self.page.update()
        participante = self.db.get_participante(self.identificador)
        self.usuario = participante[1]
        self.participante = participante
        self.page.appbar = ft.AppBar(
            leading=ft.PopupMenuButton(
                icon=ft.icons.MENU,
                items=[
                    ft.PopupMenuItem(text="Cadastrar Participante", on_click=self.ao_clicar_cadastro_participante),
                    ft.PopupMenuItem(text="Cadastrar Evento", on_click=self.ao_clicar_cadastro_evento),
                    ft.PopupMenuItem(text="Listar Eventos", on_click=self.ao_clicar_listar_eventos),
                    ft.PopupMenuItem(text="Eventos por Participante", on_click=self.ao_clicar_eventos_participante),
                    ft.PopupMenuItem(text="Buscar Eventos", on_click=self.ao_clicar_buscar_eventos),
                ],
            ),
            title=ft.Text("Sistema de Eventos", style="titleLarge"),
            actions=[
                ft.PopupMenuButton(
                    icon=ft.icons.PERSON,
                    items=[
                       ft.PopupMenuItem(text=f"\nUsuário: {self.usuario}"),
                    ],
                )
            ],
            center_title=True,
        )

       
        conteudo_principal = ft.Container(
            expand=True,
            content=ft.Text("Bem-vindo ao Sistema de Gerenciamento de Eventos!", style="headlineMedium"),
            alignment=ft.alignment.center
        )

        self.page.add(conteudo_principal)
