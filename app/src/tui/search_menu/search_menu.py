from textual.app import ComposeResult
from textual.widgets import Footer, Header, OptionList, Button
from textual.containers import Vertical
from textual.screen import Screen

class OptionListApp(Screen):
    CSS_PATH = "styles.tcss"

    def __init__(self, search_results: list[dict]):
        """
        Initialize the OptionListApp with a list of search results.

        Args:
            search_results (list[dict]): A list of dictionaries containing 'title' and 'url'.
        """
        super().__init__()
        self.search_results = search_results  # Store the search results

    def compose(self) -> ComposeResult:
        """Compose the layout of the screen."""
        yield Vertical(
            OptionList(
                *[result["title"] for result in self.search_results],  # Display only the titles
                id="option-list",
            ),
            Button("Go Back", id="go-back-button"),  # Add a "Go Back" button
            id="content-container",  # Wrap both in a single container
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "go-back-button":
            # Lazy import to avoid circular dependency
            from tui.start_menu.start_menu import MainMenu
            self.app.pop_screen()  # Go back to the previous screen (MainMenu)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle selection of an option."""
        selected_index = event.option_index
        selected_result = self.search_results[selected_index]
        print(f"Selected option: {selected_result['title']} - {selected_result['url']}")