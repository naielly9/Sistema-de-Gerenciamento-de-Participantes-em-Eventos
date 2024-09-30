import flet as ft
import re
from database import Database
from .componentes.campoTexto import CampoTexto
from .componentes.botao import Botao, BotaoTexto
from .telaBase import TelaBase
from .componentes.identidadeVisual import GRADIENTE
import datetime

class TelaCadastro(TelaBase):
    def __init__(self, page: ft.Page, is_new_user=bool, participante=None):
        super().__init__(page)
        self.db = Database()
        self.is_new_user = is_new_user
        self.participante = participante 
        self.data_nasc_value = ""
        
    def carregar_dados_participante(self):
        if self.participante:   
            self.campo_nome.value = self.participante[1]
            self.campo_cpf.value = self.participante[2]
            self.data_nasc_value = self.participante[3]
            self.campo_endereco.value = self.participante[4]
            self.campo_telefone.value = self.participante[5]
            self.campo_sexo.value = self.participante[6]
            self.campo_senha.value = self.participante[7]
            self.texto_data_nasc.value = f": {self.data_nasc_value}"

    def validar_cpf(self, cpf):
        padrao = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
        if not re.match(padrao, cpf):
            return "CPF inválido"
        return None

    def validar_campos_obrigatorios(self, nome, cpf, data_nasc, endereco, telefone, sexo, senha):
        if not nome or not cpf or not data_nasc or not endereco or not telefone or not sexo or not senha:
            return "Preencha todos os campos"
        return None

    def ao_clicar_registrar(self, e):
        nome = self.campo_nome.value
        cpf = self.campo_cpf.value
        data_nasc = self.data_nasc_value
        endereco = self.campo_endereco.value
        telefone = self.campo_telefone.value
        sexo = self.campo_sexo.value
        senha = self.campo_senha.value

        erro = self.validar_campos_obrigatorios(nome, cpf, data_nasc, endereco, telefone, sexo, senha) or \
               self.validar_cpf(cpf)

        if erro:
            self.page.snack_bar = ft.SnackBar(ft.Text(erro), open=True)
        else:
            if self.is_new_user:
                self.db.add_participante(nome, cpf, data_nasc, endereco, telefone, sexo, senha)
                self.page.snack_bar = ft.SnackBar(ft.Text("Participante cadastrado com sucesso!"), open=True)
                self.page.clean()
                from .telaLogin import TelaLogin
                login_screen = TelaLogin(self.page)
                login_screen.mostrar()
            else:
                self.db.edit_participante(self.participante[0], nome, cpf, data_nasc, endereco, telefone, sexo, senha)
                self.page.snack_bar = ft.SnackBar(ft.Text("Participante atualizado com sucesso!"), open=True)
                self.page.clean()
                from .telaPrincipal import TelaPrincipal
                tela_principal = TelaPrincipal(self.page, self.participante[0])
                tela_principal.mostrar()

        self.page.update()

    def ao_clicar_excluir(self, e):
        if self.participante:
            self.db.delete_participante(self.participante[0])
            self.page.snack_bar = ft.SnackBar(ft.Text("Cadastro excluído com sucesso!"), open=True)
            self.page.clean()
            from .telaLogin import TelaLogin
            login_screen = TelaLogin(self.page)
            login_screen.mostrar()
        self.page.update()

    def ao_clicar_voltar(self, e):
        self.page.clean()
        if self.is_new_user:
            from .telaLogin import TelaLogin
            login_screen = TelaLogin(self.page)
            login_screen.mostrar()
        else:
            from .telaPrincipal import TelaPrincipal
            tela_principal = TelaPrincipal(self.page, self.participante[0])
            tela_principal.mostrar()

    def abrir_date_picker(self, e):
        self.page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=1990, month=1, day=1),
                last_date=datetime.datetime(year=2024, month=12, day=31),
                on_change=self.handle_data_nasc_change
            )
        )

    def handle_data_nasc_change(self, e):
        self.data_nasc_value = e.control.value.strftime('%Y-%m-%d')
        self.texto_data_nasc.value = f": {self.data_nasc_value}"
        self.page.update()

    def mostrar(self):
        self.page.title = "Cadastro de Participante"
        self.campo_nome = CampoTexto("Nome")
        self.campo_cpf = CampoTexto("CPF (Formato: 000.000.000-00)")
        self.campo_endereco = CampoTexto("Endereço")
        self.campo_telefone = CampoTexto("Telefone")
        self.campo_sexo = CampoTexto("Sexo")
        self.campo_senha = CampoTexto("Senha", senha=True)
        self.campo_data_nasc = ft.Row([
            ft.Text("Data de Nascimento"),
            ft.IconButton(ft.icons.CALENDAR_TODAY, on_click=self.abrir_date_picker)
        ])

        self.texto_data_nasc = ft.Text(": ")

        conteudo = ft.Container(
            expand=True,  
            gradient=GRADIENTE,
            content=ft.Column(
                [
                    self.campo_nome,
                    self.campo_cpf,
                    ft.Row(
                        [
                            self.campo_data_nasc,
                            self.texto_data_nasc,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    self.campo_endereco,
                    self.campo_telefone,
                    self.campo_sexo,
                    self.campo_senha,
                    Botao("Registrar" if self.is_new_user else "Salvar", self.ao_clicar_registrar, primario=True),
                    BotaoTexto("Excluir" if not self.is_new_user else "", self.ao_clicar_excluir),
                    BotaoTexto("Voltar", self.ao_clicar_voltar),
                ],
               
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True  
            )
        )

        self.page.add(conteudo)
        if not self.is_new_user:
            self.carregar_dados_participante()
        self.page.update()
