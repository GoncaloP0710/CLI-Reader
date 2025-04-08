from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Input
from textual_image.renderable import Image


class DescriptionWidget(Static):
    def compose(self) -> ComposeResult:
        yield Static(
            "Read manga right from your terminal with a sleek, minimalist interface.\n"
            "Use the search function to find titles, and enjoy fast navigation with keyboard shortcuts."
        )


class MainMenu(App):
    CSS_PATH = "styles.css"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        """Compose the main menu layout."""

        # Horizontal layout: Left (DescriptionWidget) and Right (Image)
        yield Horizontal(
            # Left side: Description and search input
            Vertical(
                Static(
                    Image("../../../../files/main_menu/logo_clean.png", width=20, height=10),
                    id="image-widget",
                ),

                DescriptionWidget(id="description", expand=True),
                Input(placeholder="Search manga...", id="search-input"),
                id="left-panel",
            ),
            # Right side: Centered image
            Vertical(
                Static(
                    Image("../../../../files/main_menu/main_menu_img.jpg", width=40, height=30),
                    id="image-widget",
                ),
                id="right-panel",
            ),
        )

        yield Footer()

    def on_mount(self) -> None:
        """Set styles for centering the right panel."""
        right_panel = self.query_one("#right-panel", Vertical)
        right_panel.styles.align = ("center", "middle")  # Center the content horizontally and vertically

    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.value
        print(f"Search submitted: {query}")


if __name__ == "__main__":
    MainMenu().run()
