import flet as ft
from database import Database
from .componentes.campoTexto import CampoTexto
from .componentes.botao import Botao, BotaoTexto
from .telaBase import TelaBase
from .componentes.identidadeVisual import GRADIENTE
from .componentes.campoDropdown import CampoDropdown
import datetime

class TelaCadastroEvento(TelaBase):
    def __init__(self, page: ft.Page, participante=None, is_new_evento=bool, evento=None):
        super().__init__(page)
        self.db = Database()
        self.participante = participante
        self.is_new_evento = is_new_evento
        self.evento = evento
      
    def validar_campos_obrigatorios(self, nome, data_inicio, hora_inicio, data_fim, hora_fim, local, preco, lotacao_maxima, categoria):
        if not nome or not data_inicio or not hora_inicio or not data_fim or not hora_fim or not local or not preco or not lotacao_maxima or not categoria:
            return "Preencha todos os campos obrigatórios"
        return None

    def ao_clicar_registrar(self, e):
        nome = self.campo_nome.value
        data_inicio = self.data_inicio_value
        hora_inicio = self.hora_inicio_value
        data_fim = self.data_fim_value
        hora_fim = self.hora_fim_value
        local = self.campo_local.value
        preco = self.campo_preco.value
        lotacao_maxima = self.campo_lotacao_maxima.value
        num_participantes = self.campo_num_participantes.value
        categoria = self.campo_categoria.value

        erro = self.validar_campos_obrigatorios(nome, data_inicio, hora_inicio, data_fim, hora_fim, local, preco, lotacao_maxima, categoria)

        if erro:
            self.page.snack_bar = ft.SnackBar(ft.Text(erro), open=True)
        else:
            if self.is_new_evento:
                self.db.add_evento(nome, data_inicio, hora_inicio, data_fim, hora_fim, local, preco, lotacao_maxima, num_participantes, categoria)
                mensagem = "Evento cadastrado com sucesso!"
            else:
                self.db.edit_evento(self.evento[0], nome, data_inicio, hora_inicio, data_fim, hora_fim, local, preco, lotacao_maxima, num_participantes, categoria)
                mensagem = "Evento atualizado com sucesso!"
            
            self.page.snack_bar = ft.SnackBar(ft.Text(mensagem), open=True)
            self.page.clean()
            from .telaPrincipal import TelaPrincipal
            principal_screen = TelaPrincipal(self.page, self.participante[0])
            principal_screen.mostrar()

        self.page.update()

    def ao_clicar_voltar(self, e):
        self.page.clean()
        from .telaPrincipal import TelaPrincipal
        principal_screen = TelaPrincipal(self.page, self.participante[0])
        principal_screen.mostrar()

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
        
    def carregar_dados_evento(self):
        if self.evento:   
            self.campo_nome.value = self.evento[1]
            self.campo_local.value = self.evento[6]
            self.campo_preco.value = self.evento[7]
            self.campo_lotacao_maxima.value = self.evento[8]
            self.campo_num_participantes.value = self.evento[9]
            self.data_inicio_value = self.evento[2]
            self.hora_inicio_value = self.evento[3]
            self.data_fim_value = self.evento[4]
            self.hora_fim_value = self.evento[5]
            self.texto_data_inicio.value = f": {self.data_inicio_value}"
            self.texto_hora_inicio.value = f": {self.hora_inicio_value}"
            self.texto_data_fim.value = f": {self.data_fim_value}"
            self.texto_hora_fim.value = f": {self.hora_fim_value}"

            self.campo_categoria.value = self.evento[10]
              
    def mostrar(self):
        self.page.title = "Cadastro de Evento"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.campo_nome = CampoTexto("Nome do Evento")
        self.campo_local = CampoTexto("Local")
        self.campo_preco = CampoTexto("Preço")
        self.campo_lotacao_maxima = CampoTexto("Lotação Máxima")
        self.campo_num_participantes = CampoTexto("Número de Participantes")
        self.campo_data_inicio = ft.Row([
            ft.Text("Data de Início"),
            ft.IconButton(ft.icons.CALENDAR_TODAY, on_click=self.abrir_date_picker_inicio)
        ])
        self.campo_hora_inicio = ft.Row([
            ft.Text("Hora de Início"),
            ft.IconButton(ft.icons.ACCESS_TIME, on_click=self.abrir_time_picker_inicio)
        ])
        self.campo_data_fim = ft.Row([
            ft.Text("Data de Fim"),
            ft.IconButton(ft.icons.CALENDAR_TODAY, on_click=self.abrir_date_picker_fim)
        ])
        self.campo_hora_fim = ft.Row([
            ft.Text("Hora de Fim"),
            ft.IconButton(ft.icons.ACCESS_TIME, on_click=self.abrir_time_picker_fim)
        ])

       
        self.texto_data_inicio = ft.Text(": ")
        self.texto_hora_inicio = ft.Text(": ")
        self.texto_data_fim = ft.Text(": ")
        self.texto_hora_fim = ft.Text(": ")      
        self.campo_categoria = CampoDropdown("Categoria")

        conteudo = ft.Container(
            expand=True,
            gradient=GRADIENTE,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            self.campo_nome,
                            self.campo_local,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.Row(
                        [
                            self.campo_data_inicio,
                            self.texto_data_inicio,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.Row(
                        [
                            self.campo_data_fim,
                            self.texto_data_fim,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.Row(
                        [
                            self.campo_hora_inicio,
                            self.texto_hora_inicio,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.Row(
                        [
                            self.campo_hora_fim,
                            self.texto_hora_fim,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.Row(
                        [
                            self.campo_preco,
                            self.campo_lotacao_maxima,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.Row(
                        [
                            self.campo_num_participantes,
                            self.campo_categoria,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    ft.Row(
                        [
                            Botao("Registrar Evento", self.ao_clicar_registrar, primario=True),
                            BotaoTexto("Voltar", self.ao_clicar_voltar),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )
        
        self.page.add(conteudo)
        if not self.is_new_evento:
            self.carregar_dados_evento()
        self.page.update()