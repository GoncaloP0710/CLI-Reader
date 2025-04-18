from textual.app import ComposeResult
from textual.widgets import Footer, Header, OptionList, Button
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static
from textual_image.renderable import Image
import asyncio

from controllers import MangaController

from tui.manga_reading_menu.manga_reading_menu import MangaReader

cover = None

from textual.app import App, ComposeResult
from textual.widgets import LoadingIndicator

class LoadingApp(Screen):
    def __init__(self, load_screen_coro):
        super().__init__()
        self.load_screen_coro = load_screen_coro

    async def on_mount(self) -> None:
        asyncio.create_task(self.do_loading())

    async def do_loading(self) -> None:
        next_screen = await self.load_screen_coro()

        # Ensure the next screen is valid
        if next_screen is not None:
            self.app.pop_screen()  # Remove the LoadingApp screen
            self.app.push_screen(next_screen)  # Push the next screen
        else:
            self.app.log("Error: load_screen_coro returned None.")
            self.app.pop_screen()  # Close the LoadingApp screen
            # Optionally, you can show an error message or return to the previous screen

    def compose(self) -> ComposeResult:
        """Compose the layout of the LoadingApp screen."""
        yield Static("Downloading chapter...", id="loading-message")

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
        self.manga_preview = MangaController().load_manga_preview(self.manga_pointer["title"])
        self.cover = self.manga_preview[1]  # Assuming the cover image is the second element in the tuple
        self.chapter_list = MangaController().list_chapters(self.manga_pointer["url"])

    def compose(self) -> ComposeResult:
        """Compose the layout of the screen."""
        yield Vertical(
            Horizontal(
                Vertical(
                    DescriptionWidget(self.manga_preview[0]),  # Display the manga description
                    OptionList(
                        *[f"Chapter {chapter['chapter_number']}" for chapter in self.chapter_list],
                        id="chapter-list",
                    ),
  # Add a clickable list of chapters
                    id="content-container",  # Wrap all in a single container
                ),
                Vertical(
                    Static(
                        Image(self.cover, width=30, height=20),  # Display the manga cover image
                        id="logo-widget",
                    ),
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

    async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle selection of an option in the chapter list."""
        selected_index = event.option_index
        selected_result = self.chapter_list[selected_index]

        async def load_manga_reader():
            # Perform the actual work in a separate thread to avoid blocking the event loop
            def create_manga_reader():
                # Simulate real work (e.g., fetching data or creating the screen)
                return MangaReader(self.chapter_list, selected_result, self.manga_pointer["title"])

            # Run the blocking work in a separate thread
            return await asyncio.to_thread(create_manga_reader)

        # Push the LoadingApp screen with the coroutine to load the MangaReader screen
        self.app.push_screen(LoadingApp(load_manga_reader))
        
