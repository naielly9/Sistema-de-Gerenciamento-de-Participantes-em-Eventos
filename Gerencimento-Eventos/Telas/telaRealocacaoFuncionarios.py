import flet as ft
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .telaBase import TelaBase

class TelaRealocacaoFuncionarios(TelaBase):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.page = page
        self.usuario = {"nome": "Naielly Moura", "empresa": "Empresa Exemplo"}
        self.arquivo_lido = False
        self.funcionarios = []
        self.realocacoes_escolhidas = {}
        self.pagina_atual = 1
        self.funcionarios_por_pagina = 1

        self.altura_janela = 800
        self.page.on_resize = self.ao_redimensionar

        # Cria e adiciona o FilePicker para downloads
        self.file_picker = ft.FilePicker(on_result=self.on_file_save)
        self.page.overlay.append(self.file_picker)

    def ao_redimensionar(self, e):
        self.altura_janela = e.data['height']

    def carregar_planilha_mock(self):
        self.funcionarios = [
            {
                "nome": "João da Silva",
                "filial_atual": "Filial A",
                "distancia_atual": 5,
                "custo_atual": 10,
                "realocacoes": [
                    {"empresa": "Filial B", "distancia_km": 8, "custo": 14},
                    {"empresa": "Filial C", "distancia_km": 12, "custo": 20},
                    {"empresa": "Filial D", "distancia_km": 15, "custo": 25}
                ]
            },
            {
                "nome": "Maria Oliveira",
                "filial_atual": "Filial B",
                "distancia_atual": 6,
                "custo_atual": 12,
                "realocacoes": [
                    {"empresa": "Filial A", "distancia_km": 7, "custo": 11},
                    {"empresa": "Filial C", "distancia_km": 10, "custo": 15},
                    {"empresa": "Filial D", "distancia_km": 20, "custo": 30}
                ]
            },
        ]
        self.arquivo_lido = True
        self.pagina_atual = 1
        self.mostrar()

    def calcular_funcionarios_por_pagina(self):
        altura_disponivel = self.altura_janela or 800
        altura_por_funcionario = 180
        self.funcionarios_por_pagina = max(1, altura_disponivel // altura_por_funcionario)

    def selecionar_realocacao(self, funcionario_nome, nova_realocacao):
        self.realocacoes_escolhidas[funcionario_nome] = nova_realocacao
        self.page.snack_bar = ft.SnackBar(ft.Text(f"{funcionario_nome} realocado para {nova_realocacao['empresa']}"), open=True)
        self.page.update()

    def proxima_pagina(self, e):
        total_paginas = (len(self.funcionarios) - 1) // self.funcionarios_por_pagina + 1
        if self.pagina_atual < total_paginas:
            self.pagina_atual += 1
            self.mostrar()

    def pagina_anterior(self, e):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.mostrar()

    def exportar_excel(self, e):
        if not self.realocacoes_escolhidas:
            self.page.snack_bar = ft.SnackBar(ft.Text("Nenhuma realocação selecionada."), open=True)
            self.page.update()
            return

        dados = [
            {
                "Funcionário": nome,
                "Nova Empresa": realoc["empresa"],
                "Distância (km)": realoc["distancia_km"],
                "Custo (R$)": realoc["custo"]
            }
            for nome, realoc in self.realocacoes_escolhidas.items()
        ]
        df = pd.DataFrame(dados)
        caminho_temp = "realocacoes_escolhidas.xlsx"
        df.to_excel(caminho_temp, index=False)

        # Abrir diálogo para salvar o arquivo no navegador
        self.file_picker.save_file(file_name=caminho_temp, file_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def exportar_pdf(self, e):
        if not self.realocacoes_escolhidas:
            self.page.snack_bar = ft.SnackBar(ft.Text("Nenhuma realocação selecionada."), open=True)
            self.page.update()
            return

        caminho_temp = "realocacoes_escolhidas.pdf"
        c = canvas.Canvas(caminho_temp, pagesize=letter)
        width, height = letter
        y = height - 50
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Relatório de Realocações")
        y -= 30
        c.setFont("Helvetica", 12)

        for nome, realoc in self.realocacoes_escolhidas.items():
            texto = f"{nome} → {realoc['empresa']} | Distância: {realoc['distancia_km']} km | Custo: R$ {realoc['custo']:.2f}"
            c.drawString(50, y, texto)
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50
        c.save()

        self.file_picker.save_file(file_name=caminho_temp, file_type="application/pdf")

    def on_file_save(self, e: ft.FilePickerResultEvent):
        if e.file_path:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Arquivo salvo: {e.file_path}"), open=True)
            self.page.update()

    def mostrar(self):
        self.page.clean()
        self.calcular_funcionarios_por_pagina()

        painel_topo = ft.Container(
            content=ft.Row([
                ft.Text(f"Usuário: {self.usuario['nome']}", size=16),
                ft.Text(f"Empresa: {self.usuario['empresa']}", size=16),
                ft.ElevatedButton("Upload Planilha", on_click=lambda e: self.carregar_planilha_mock())
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.BLUE_50,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_200),
            margin=ft.margin.only(bottom=20)
        )

        lista_funcionarios = ft.Column(spacing=15)

        if self.arquivo_lido:
            inicio = (self.pagina_atual - 1) * self.funcionarios_por_pagina
            fim = inicio + self.funcionarios_por_pagina
            funcionarios_pagina = self.funcionarios[inicio:fim]

            for funcionario in funcionarios_pagina:
                titulo = f"{funcionario['nome']} está na {funcionario['filial_atual']} atualmente. Distância: {funcionario['distancia_atual']}km | Custo: R$ {funcionario['custo_atual']:.2f}"
                opcoes = []
                for r in funcionario["realocacoes"]:
                    opcoes.append(
                        ft.Row([
                            ft.Text(f"→ {r['empresa']}"),
                            ft.Text(f"Distância: {r['distancia_km']} km"),
                            ft.Text(f"Custo: R$ {r['custo']:.2f}"),
                            ft.TextButton("Selecionar", on_click=lambda e, r=r, nome=funcionario["nome"]: self.selecionar_realocacao(nome, r))
                        ], spacing=20)
                    )
                lista_funcionarios.controls.append(
                    ft.ExpansionTile(
                        title=ft.Text(titulo),
                        controls=opcoes
                    )
                )

        botoes_exportar = ft.Row([
            ft.ElevatedButton("Baixar Excel", on_click=self.exportar_excel),
            ft.ElevatedButton("Baixar PDF", on_click=self.exportar_pdf)
        ], alignment=ft.MainAxisAlignment.END)

        paginacao = ft.Row([
            ft.ElevatedButton("<", on_click=self.pagina_anterior),
            ft.Text(f"Página {self.pagina_atual}"),
            ft.ElevatedButton(">", on_click=self.proxima_pagina)
        ], alignment=ft.MainAxisAlignment.CENTER)

        painel_grid = ft.Container(
            content=ft.Column([
                lista_funcionarios,
                paginacao,
                botoes_exportar
            ], spacing=20),
            bgcolor=ft.Colors.GREY_100,
            padding=20,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.GREY_300)
        )

        layout_principal = ft.Column([
            painel_topo,
            painel_grid
        ], scroll=ft.ScrollMode.AUTO)

        self.page.add(layout_principal)
        self.page.update()
