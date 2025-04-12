from controllers import MangaController
from tui.start_menu import MainMenu  # Explicit import

from textual.app import App, ComposeResult

class App(App):

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        
    def on_mount(self):
        self.push_screen(MainMenu())
            
if __name__ == "__main__":
    App().run()
