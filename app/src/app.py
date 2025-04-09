from controllers import MangaController
from tui.start_menu import MainMenu  # Explicit import

MainMenu().run()

"""

manga_controller = MangaController()

# Load manga preview
# manga_info, cover_path = manga_controller.load_manga_preview("K on")

# Search for the manga
search_results = manga_controller.search_manga("One piece")
print("Search Results:")
for idx, result in enumerate(search_results):
    print(f"{idx + 1}. {result['title']} - {result['url']}")

# Select the first result (or any specific result you want)
if search_results:
    selected_manga = search_results[0]  # Select the first result
    manga_url = selected_manga["url"]  # Extract the URL

    # Fetch all chapters for the selected manga
    all_chapters = manga_controller.list_chapters(manga_url)[-1]

    chapter_link = all_chapters['url']
    chapter_number = all_chapters['chapter_number']

    if chapter_link:
        save_path = f"../../manga/chapters/{selected_manga['title']}/Chapter {chapter_number}"
        manga_controller.download_chapter(chapter_link, save_path)

else:
    print("No manga found.")

"""