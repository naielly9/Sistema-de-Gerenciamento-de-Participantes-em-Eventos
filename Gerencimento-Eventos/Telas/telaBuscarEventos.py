import flet as ft
from .telaBase import TelaBase
from .componentes.campoTexto import CampoTexto
from .componentes.botao import BotaoTexto
from .componentes.campoDropdown import CampoDropdown
import datetime

class TelaBuscarEventos(TelaBase):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.eventos_por_pagina = 10
        self.pagina_atual = 1
        self.eventos_filtrados = []
        self.data_inicio_value = ""
        self.hora_inicio_value = ""
        self.data_fim_value = ""
        self.hora_fim_value = ""
        
    def pagina_anterior(self, e):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.mostrar()

    def proxima_pagina(self, e):
        self.pagina_atual += 1
        self.mostrar()
        
    def abrir_date_picker_inicio(self, e):
        self.page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2023, month=1, day=1),
                last_date=datetime.datetime(year=2024, month=12, day=31),
                on_change=self.handle_data_inicio_change
            )
        )

    def abrir_time_picker_inicio(self, e):
        self.page.open(
            ft.TimePicker(
                on_change=self.handle_hora_inicio_change
            )
        )

    def abrir_date_picker_fim(self, e):
        self.page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2023, month=1, day=1),
                last_date=datetime.datetime(year=2024, month=12, day=31),
                on_change=self.handle_data_fim_change
            )
        )

    def abrir_time_picker_fim(self, e):
        self.page.open(
            ft.TimePicker(
                on_change=self.handle_hora_fim_change
            )
        )

    def handle_data_inicio_change(self, e):
        self.data_inicio_value = e.control.value.strftime('%Y-%m-%d')
        self.texto_data_inicio.value = f": {self.data_inicio_value}"
        self.page.update() 
        
    def handle_hora_inicio_change(self, e):
        self.hora_inicio_value = e.control.value.strftime('%H:%M')
        self.texto_hora_inicio.value = f": {self.hora_inicio_value}"
        self.page.update() 
        
    def handle_data_fim_change(self, e):
        self.data_fim_value = e.control.value.strftime('%Y-%m-%d')
        self.texto_data_fim.value = f": {self.data_fim_value}"
        self.page.update() 

    def handle_hora_fim_change(self, e):
        self.hora_fim_value = e.control.value.strftime('%H:%M')
        self.texto_hora_fim.value = f": {self.hora_fim_value}"
        self.page.update() 

    def buscar_eventos(self, e):
        print('buscar eventos')

    def mostrar(self):
        self.page.clean()

        self.campo_nome = CampoTexto("Nome do Evento")
        self.campo_local = CampoTexto("Local")
        self.campo_preco = CampoTexto("Preço")
        self.campo_lotacao_max = CampoTexto("Lotação Máxima")
        self.texto_data_inicio = ft.Text(": ")
        self.texto_hora_inicio = ft.Text(": ")
        self.texto_data_fim = ft.Text(": ")
        self.texto_hora_fim = ft.Text(": ")    
        self.campo_categoria = CampoDropdown("Categoria")
        self.campo_data_inicio = ft.Row([ft.Text("Data de Início"), ft.IconButton(ft.icons.CALENDAR_TODAY, on_click=self.abrir_date_picker_inicio)])
        self.campo_hora_inicio = ft.Row([ft.Text("Hora de Início"), ft.IconButton(ft.icons.ACCESS_TIME, on_click=self.abrir_time_picker_inicio)])
        self.campo_data_fim = ft.Row([ft.Text("Data de Fim"), ft.IconButton(ft.icons.CALENDAR_TODAY, on_click=self.abrir_date_picker_fim)])
        self.campo_hora_fim = ft.Row([ft.Text("Hora de Fim"), ft.IconButton(ft.icons.ACCESS_TIME, on_click=self.abrir_time_picker_fim)])

        linha_unica = ft.Row(
            [
                ft.Container(self.campo_nome, padding=ft.padding.only(right=25)),  
                ft.Container(self.campo_local, padding=ft.padding.only(right=25)),
                ft.Container(self.campo_preco, padding=ft.padding.only(right=25)),
                ft.Container(self.campo_lotacao_max, padding=ft.padding.only(right=25)),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

        linha_data_hora = ft.Row(
            [
                ft.Container(self.campo_data_inicio, padding=ft.padding.only(right=25)),
                ft.Container(self.texto_data_inicio, padding=ft.padding.only(right=25)),
                ft.Container(self.campo_hora_inicio, padding=ft.padding.only(right=25)),
                ft.Container(self.texto_hora_inicio, padding=ft.padding.only(right=25)),
                ft.Container(self.campo_data_fim, padding=ft.padding.only(right=25)),
                ft.Container(self.texto_data_fim, padding=ft.padding.only(right=25)),
                ft.Container(self.campo_hora_fim, padding=ft.padding.only(right=25)),
                ft.Container(self.texto_hora_fim, padding=ft.padding.only(right=25)),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

        linha_categoria_botao = ft.Row(
            [
                ft.Container(self.campo_categoria, padding=ft.padding.only(right=25)),
                BotaoTexto("Buscar", self.buscar_eventos),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

        eventos = self.eventos_filtrados[(self.pagina_atual - 1) * self.eventos_por_pagina : self.pagina_atual * self.eventos_por_pagina]

        lista_eventos = ft.Column(
            [ft.Text(f"{evento['nome']} - {evento['data_inicio']} - {evento['local']} - R${evento['preco']:.2f}") for evento in eventos],
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
                linha_unica,
                linha_data_hora,
                linha_categoria_botao,
                lista_eventos,
                ft.Container(expand=True),
                paginacao,
            ],
            spacing=20,
            expand=True
        )

        self.page.add(conteudo_principal)
        self.page.update()
