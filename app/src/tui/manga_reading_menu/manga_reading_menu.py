from textual.app import ComposeResult
from textual.widgets import Footer, Header, OptionList, Button
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static
from textual_image.renderable import Image
from PIL import Image as PILImage  # Import Pillow for image processing

from controllers import MangaController
import asyncio

from pathlib import Path
from natsort import natsorted  # Ensure natural sorting of image files

class MangaReader(Screen):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("right", "next_image", "Next Image"),  # Bind the right arrow key to go to the next image
        ("left", "previous_image", "Previous Image"),  # Bind the left arrow key to go to the previous image
    ]

    def __init__(self, manga_pointer: list[dict], chapter_pointer: dict, manga_name: str):
        super().__init__()
        self.manga_pointer = manga_pointer
        self.chapter_pointer = chapter_pointer
        self.manga_name = manga_name
        self.image_paths = []  # List to store image file paths
        self.image_index = 0  # Current image index

    async def on_mount(self) -> None:
        """Called when the screen is mounted."""
        # Start downloading the chapter asynchronously
        save_path = Path(f"manga/chapters/{self.manga_name}/{self.chapter_pointer['chapter_number']}")
        chapter_url = self.chapter_pointer["url"]

        # Log the start of the download
        self.app.log(f"Starting download for chapter: {chapter_url}")
        self.app.log(f"Save path: {save_path}")

        # Run the download asynchronously
        try:
            await MangaController().download_chapter(chapter_url, str(save_path))
            self.app.log("Download completed successfully.")
        except Exception as e:
            self.app.log(f"Error during chapter download: {e}")

        # Load image paths from the save_path directory
        if save_path.exists() and save_path.is_dir():
            self.image_paths = natsorted(
                [str(p) for p in save_path.iterdir() if p.suffix.lower() in [".png", ".jpg", ".jpeg"]]
            )
            if self.image_paths:
                self.update_image()  # Display the first image
            else:
                self.app.log("No images found in the chapter directory.")
        else:
            self.app.log("Chapter directory does not exist.")

    def compose(self) -> ComposeResult:
        """Compose the layout of the screen."""

        yield Vertical(
            Horizontal(
                Vertical(
                    Static(id="image-display"),
                    id="manga_image_container",  # Wrap all in a single container
                ),
                Vertical(
                    Button("Go Back", id="go-back-button"),  # Add a "Go Back" button
                ),
            ),
        )

    def update_image(self):
        """Update the displayed image."""
        if self.image_paths:
            image_path = self.image_paths[self.image_index]
            image_widget = self.query_one("#image-display", Static)

            # Open the image to get its dimensions
            with PILImage.open(image_path) as img:
                original_width, original_height = img.size

            # Get the terminal's dimensions
            terminal_width, terminal_height = self.app.size.width, self.app.size.height

            # Adjust the terminal's height to account for the character cell aspect ratio (2:1)
            adjusted_terminal_height = terminal_height * 2

            # Calculate the scaling factor to fit the image within the terminal
            width_ratio = terminal_width / original_width
            height_ratio = adjusted_terminal_height / original_height
            scaling_factor = min(width_ratio, height_ratio)

            # Calculate the new dimensions while maintaining the aspect ratio
            new_width = int(original_width * scaling_factor)
            new_height = int(original_height * scaling_factor / 2)  # Divide by 2 to adjust for the aspect ratio

            # Update the image widget with the resized image
            image_widget.update(Image(image_path, width=new_width, height=new_height))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "go-back-button":
            self.app.pop_screen()  # Go back to the previous screen (MainMenu)

    def action_next_image(self) -> None:
        """Go to the next image."""
        if self.image_paths:
            self.image_index = (self.image_index + 1) % len(self.image_paths)
            self.update_image()

    def action_previous_image(self) -> None:
        """Go to the previous image."""
        if self.image_paths:
            self.image_index = (self.image_index - 1) % len(self.image_paths)
            self.update_image()