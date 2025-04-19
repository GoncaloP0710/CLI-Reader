from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Input, ProgressBar
from textual_image.renderable import Image
from natsort import natsorted
import os
from textual.screen import Screen

from tui.search_menu.search_menu import OptionListApp
from controllers import MangaController

class DescriptionWidget(Static):
    def compose(self) -> ComposeResult:
        yield Static(
            "Read manga right from your terminal with a sleek, minimalist interface.\n"
            "Use the search function to find titles, and enjoy fast navigation with keyboard shortcuts."
        )

class MainMenu(Screen):
    CSS_PATH = "styles.css"
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        # Dynamically load all image files from the directory
        image_directory = "app/files/main_menu/Chapter 1"
        self.image_paths = [
            os.path.join(image_directory, file)
            for file in natsorted(os.listdir(image_directory))  # Use natsorted for natural sorting
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        self.image_index = 0

    def compose(self) -> ComposeResult:
        print("MainMenu is mounted")
        """Compose the main menu layout."""
        yield Horizontal(
            Vertical(
                Static(
                    Image("app/files/main_menu/logo_clean.png", width=20, height=10),
                    id="logo-widget",
                ),
                DescriptionWidget(id="description", expand=True),
                Input(placeholder="Search manga...", id="search-input"),
                id="left-panel",
            ),
            Vertical(
                Static(id="image-cycler-widget"),
                ProgressBar(total=100, id="progress-bar"),
                id="right-panel",
            ),
        )

    async def on_mount(self) -> None:
        """Start image cycling and progress bar updates."""
        self.image_widget = self.query_one("#image-cycler-widget", Static)
        self.progress_bar = self.query_one("#progress-bar", ProgressBar)

        # Display the first image immediately
        if self.image_paths:
            first_image_path = self.image_paths[self.image_index]
            self.image_widget.update(Image(first_image_path, width=40, height=30))
            self.progress_bar.progress = int((self.image_index + 1) / len(self.image_paths) * 100)

        # Start a repeating task every 2 seconds
        self.set_interval(4.0, self.update_image)

    def update_image(self):
        """Update image and progress bar."""
        # Update image
        image_path = self.image_paths[self.image_index]
        self.image_widget.update(Image(image_path, width=40, height=30))

        # Update progress bar
        progress = int((self.image_index + 1) / len(self.image_paths) * 100)
        self.progress_bar.progress = progress

        # Move to next image
        self.image_index = (self.image_index + 1) % len(self.image_paths)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle search input submission."""
        query = event.value.strip()  # Get the user input
        input_widget = self.query_one("#search-input", Input)
        if query:  # Ensure the input is not empty
            print(f"Search submitted: {query}")
            # Search for the manga
            animes_search_results = MangaController().search_manga(query)

            if not animes_search_results:
                print("No results found.")
                
                input_widget.value = ""
                input_widget.placeholder = "No mangas found with that name."
            else:
                # Push the OptionListApp screen with the search results
                self.app.push_screen(OptionListApp(animes_search_results))
            
if __name__ == "__main__":
    MainMenu().run()
