from textual.app import ComposeResult
from textual.widgets import Footer, Header, OptionList, Button
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static
from textual_image.renderable import Image

from controllers import MangaController

class MangaReader(Screen):
    CSS_PATH = "styles.tcss"

    def __init__(self, manga_pointer: list[dict], chapter_pointer: int):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Manga Reader Placeholder", id="manga-reader-placeholder")
        )

