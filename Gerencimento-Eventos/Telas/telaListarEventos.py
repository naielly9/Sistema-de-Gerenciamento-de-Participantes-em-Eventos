import flet as ft
from .telaBase import TelaBase
from .componentes.botao import BotaoTexto
from database import Database 

class TelaHistoricoEventos(TelaBase):
    def __init__(self, page: ft.Page, participante):
        super().__init__(page)
        self.db = Database() 
        self.participante = participante
        self.eventos_por_pagina = 20
        self.pagina_atual = 1

    def obter_eventos(self):
        total_eventos = self.db.get_eventos()
        inicio = (self.pagina_atual - 1) * self.eventos_por_pagina
        fim = inicio + self.eventos_por_pagina
        return self.db.get_eventos_paginados(inicio, fim) 

    def proxima_pagina(self, e):
        self.pagina_atual += 1
        self.mostrar()

    def pagina_anterior(self, e):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
        self.mostrar()

    def editar_evento(self, e, evento):
        self.page.clean()
        from .telaEventos import TelaCadastroEvento
        editar_evento = TelaCadastroEvento(self.page,self.participante,False,evento)
        editar_evento.mostrar()
        self.page.update()

    def remover_evento(self, evento_id):
        self.db.delete_evento(evento_id)
        self.page.snack_bar = ft.SnackBar(ft.Text('Evento deletado com sucesso.'), open=True)
        self.mostrar()  
        
    def vincular_evento(self, evento_id):
        self.db.relacionar_participante_evento(self.participante[0], evento_id)
        self.page.snack_bar = ft.SnackBar(ft.Text('Participante vinculado ao evento com sucesso.'), open=True)
        self.mostrar() 

    def mostrar(self):
        self.page.clean()
        eventos = self.obter_eventos()
        
        lista_eventos = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(f"{evento[1]} - {evento[2]}"),
                        BotaoTexto("Editar", lambda e, evento=evento: self.editar_evento(e, evento)),
                        BotaoTexto("Remover", lambda e, evento_id=evento[0]: self.remover_evento(evento_id)),
                        BotaoTexto("Vincular", lambda e, evento_id=evento[0]: self.vincular_evento(evento_id)),
                    ],
                    spacing=10
                ) for evento in eventos
            ],
            spacing=10
        )

        paginacao = ft.Row(
            [
                ft.Container(BotaoTexto("Página Anterior", self.pagina_anterior), expand=False),
                ft.Text(f"Página {self.pagina_atual}", expand=True, text_align="center"),
                ft.Container(BotaoTexto("Próxima Página", self.proxima_pagina), expand=False)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        conteudo_principal = ft.Column(
            [
                lista_eventos,
                ft.Container(expand=True), 
                paginacao
            ],
            spacing=20,
            expand=True
        )

        self.page.add(conteudo_principal)
        self.page.update()
