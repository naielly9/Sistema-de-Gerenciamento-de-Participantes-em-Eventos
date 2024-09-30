import flet as ft
from database import Database
from .telaPrincipal import TelaPrincipal
from .telaCadastro import TelaCadastro
from .telaBase import TelaBase
from .componentes.campoTexto import CampoTexto
from .componentes.identidadeVisual import ALINHAMENTO_COLUNA, FUNDO_QUADRADO
from .componentes.botao import Botao, BotaoTexto

class TelaLogin(TelaBase):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.db = Database()
        self.page.snack_bar = ft.SnackBar(content=ft.Text(""))
        
    def ao_clicar_login(self, e):
        username = self.username_field.value
        senha = self.password_field.value
        
        participantes = self.db.validate_user(username, senha)
        if participantes:
            identificador = participantes[0]
            self.page.clean()
            principal_screen = TelaPrincipal(self.page, identificador)
            principal_screen.mostrar()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Usuário ou senha inválidos"), open=True)
            self.page.update()

    def ao_clicar_registro(self, e):
        self.page.clean()
        tela_cadastro = TelaCadastro(self.page,True,None)
        tela_cadastro.mostrar()
        
    def mostrar(self):
        self.page.title = "Eventos"
        self.username_field = CampoTexto("Usuário")
        self.password_field = CampoTexto("Senha", senha=True)
        
        conteudo_login = ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=FUNDO_QUADRADO(
                ft.Column(
                    [
                        ft.Container(height=20),  
                        self.username_field,
                        self.password_field,
                        Botao("Login", self.ao_clicar_login, primario=True),
                        BotaoTexto("Não tem cadastro? Cadastre-se", self.ao_clicar_registro)
                    ],
                    **ALINHAMENTO_COLUNA
                )
            )
        )

        self.page.add(conteudo_login)
        self.page.update()

        
