from textual.app import ComposeResult
from textual.widgets import Footer, Header, OptionList, Button
from textual.containers import Vertical
from textual.screen import Screen

class MangaPreview(Screen):
    CSS_PATH = "styles.tcss"

    def __init__(self, manga_pointer: list[dict]):
        super().__init__()
        self.manga_pointer = manga_pointer 
