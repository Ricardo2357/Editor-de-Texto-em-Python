from textual.app import App
from textual.widgets import Header, TextArea, Footer, Label, Input, Button
from textual.screen import ModalScreen
from textual.containers import Grid
from textual import on

class ModalAbrir(ModalScreen):
    CSS = """
    ModalAbrir {
        align: center middle;
    }

    #modal {
        width: 50;
        height: 20;
        padding: 1;
    }
    """

    def compose(self):
        with Grid(id="modal"):
            self.label = Label("Digite o Nome ou Caminho do Arquivo.",)
            yield self.label
            yield Input(placeholder="Ex.: restrições_alimentares.txt", id="input_abrir")

    def on_input_submitted(self, event: Input.Submitted):
        self.dismiss(event.value)

class ModalSalvarComo(ModalScreen):
    CSS = """
    ModalSalvarComo {
        align: center middle;
    }

    #modal {
        width: 50;
        height: 20;
        padding: 1;
    }
    """

    def compose(self):
        with Grid(id="modal"):
            self.label = Label("Digite o Nome ou Caminho do Arquivo.",)
            yield self.label
            yield Input(placeholder="Ex.: anotações_do_trabalho.txt", id="input_salvar_como")

    def on_input_submitted(self, event: Input.Submitted):
        self.dismiss(event.value)

class ModalSair(ModalScreen):
    CSS = """
    ModalSair {
        align: center middle;
    }

    #modal {
        width: 50;
        height: 20;
        padding: 1;
    }
    """

    def compose(self):
        with Grid(id="modal"):
            self.label = Label("Você tem Alterações não Salvas",)
            yield self.label
            self.label = Label("Deseja Realmente Sair?",)
            yield self.label
            yield Button("Sim", id="sim")
            yield Button("Não", id="nao")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "sim":
            self.dismiss(True)
        else:
            self.dismiss(False)

class EditorDeTexto(App):
    #Arquivo CSS:
    #CSS_PATH = "style.tycss"

    caminho_do_arquivo = None
    editor_de_texto_modificado = False
    carregando_arquivo = False
    
    TITLE = "Editor TUI"
    SUB_TITLE = "Novo Arquivo"

    BINDINGS = [("ctrl+s", "salvar", "Salvar"), ("ctrl+a", "salvar_como", "Salvar Como"), ("ctrl+o", "abrir", "Abrir"), ("ctrl+q", "sair", "Sair"),]

    def compose(self):
        yield Header(show_clock=True)

        yield TextArea(id="text_area")

        yield Footer()

    @on(TextArea.Changed, "#text_area")
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if self.carregando_arquivo:
            return

        if not self.editor_de_texto_modificado:
            self.editor_de_texto_modificado = True

            if self.caminho_do_arquivo:
                self.sub_title = f"{self.caminho_do_arquivo}*"  
            else: 
                self.sub_title = "Novo Arquivo*"

    def action_salvar(self):
        if self.caminho_do_arquivo is None:
            self.action_salvar_como()
        else:
            editor_de_texto = self.query_one("#text_area", TextArea).text

            with open(self.caminho_do_arquivo, "w") as arquivo:
                arquivo.write(editor_de_texto)

            self.editor_de_texto_modificado = False
            self.sub_title = self.caminho_do_arquivo

    def action_salvar_como(self):
        def verificar_input(input):
            if input:
                try:
                    self.caminho_do_arquivo = input
                    self.sub_title = input

                    self.editor_de_texto_modificado = False

                    self.action_salvar()

                except FileNotFoundError:
                    self.notify("Erro: O Arquivo não foi Encontrado.")
                except Exception as e:
                    self.notify("Erro ao Ler o Arquivo")      

        self.push_screen(ModalSalvarComo(), verificar_input)

    def action_abrir(self):
        def verificar_input(input):
            if input: 
                try: 
                    with open(input, "r") as arquivo:
                        conteudo_do_arquivo = arquivo.read()

                    self.carregando_arquivo = True

                    self.query_one("#text_area", TextArea).text = conteudo_do_arquivo

                    self.caminho_do_arquivo = input
                    self.sub_title = input
                    self.editor_de_texto_modificado = False

                    self.carregando_arquivo = False
                except FileNotFoundError:
                    self.notify("Erro: O Arquivo não foi Encontrado.")
                except Exception as e:
                    self.carregando_arquivo = False            
                    self.notify("Erro ao Ler o Arquivo")

        self.push_screen(ModalAbrir(), verificar_input)

    def action_sair(self):
        if self.editor_de_texto_modificado:
            def verificar_button(button):
                if button:
                    self.exit()
                    
            self.push_screen(ModalSair(), verificar_button)
        else:
            self.exit()

if __name__ == "__main__":
    app = EditorDeTexto()
    app.run()
