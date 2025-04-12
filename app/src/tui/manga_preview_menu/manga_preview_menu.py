from textual.app import ComposeResult
from textual.widgets import Footer, Header, OptionList, Button
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static
from textual_image.renderable import Image

from controllers import MangaController

cover = None

class DescriptionWidget(Static):

    def __init__(self, manga_info: dict):
        super().__init__()
        self.manga_info = manga_info  # Store the manga information

    def compose(self) -> ComposeResult:
        formatted_info = (
            f"Chapters: {self.manga_info.get('chapters', 'N/A')}\n"
            f"Volumes: {self.manga_info.get('volumes', 'N/A')}\n"
            f"Status: {self.manga_info.get('status', 'N/A')}\n"
            f"Score: {self.manga_info.get('score', 'N/A')}\n"
            f"Synopsis: {self.manga_info.get('synopsis', 'N/A')}\n"
        )
        yield Static(formatted_info)

class MangaPreview(Screen):
    CSS_PATH = "styles.tcss"

    def __init__(self, manga_pointer: list[dict]):
        super().__init__()
        self.manga_pointer = manga_pointer 
        print(self.manga_pointer["title"])

    def compose(self) -> ComposeResult:
        self.manga_preview = MangaController().load_manga_preview(self.manga_pointer["title"])
        cover = self.manga_preview[1]  # Assuming the cover image is the second element in the tuple
        chapter_list = MangaController().list_chapters(self.manga_pointer["url"])

        """Compose the layout of the screen."""
        yield Vertical(
            Horizontal(
                Vertical(
                    DescriptionWidget(self.manga_preview[0]),  # Display the manga description
                    OptionList(
                        *[f"Chapter {chapter['chapter_number']}" for chapter in chapter_list],
                        id="chapter-list"
                    ),  # Add a clickable list of chapters
                    id="content-container",  # Wrap all in a single container
                ),
                Vertical(
                    Static(
                        Image(cover, width=30, height=20),  # Display the manga cover image
                        id="logo-widget",
                    ),
                    Button("Download all", id="download-all-button"),  # Add a "Go Back" button
                    Button("Go Back", id="go-back-button"),  # Add a "Go Back" button
                    id="image-container",  # Add an ID for styling
                ),
            ),
            id="main-container",  # Add an ID for the main container
        )

    def on_option_list_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle chapter selection."""
        selected_chapter_id = event.option.id
        print(f"Selected chapter: {selected_chapter_id}")
        # Add logic to handle chapter selection, e.g., load the chapter content

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "go-back-button":
            self.app.pop_screen()  # Go back to the previous screen (MainMenu)
        elif event.button.id == "download-all-button":
            # TODO: Implement download functionality
            print("Download all chapters functionality not implemented yet.")
