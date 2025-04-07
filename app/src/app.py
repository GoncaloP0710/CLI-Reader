from controllers import MangaController

manga_controller = MangaController()

# Search for the manga
search_results = manga_controller.search_manga("K on")
print("Search Results:")
for idx, result in enumerate(search_results):
    print(f"{idx + 1}. {result['title']} - {result['url']}")

# Select the first result (or any specific result you want)
if search_results:
    selected_manga = search_results[0]  # Select the first result
    manga_url = selected_manga["url"]  # Extract the URL

    # Fetch all chapters for the selected manga
    all_chapters = manga_controller.list_chapters(manga_url)[:1]
    chapter_number = None
    chapter_link = None
    for chapter in all_chapters:
        chapter_link = chapter['url']
        chapter_number = chapter['chapter_number']

    # Download the first chapter
    if chapter_link:
        save_path = f"../../manga/chapters/{selected_manga['title']}/Chapter {chapter_number}"
        manga_controller.download_chapter(chapter_link, save_path)

else:
    print("No manga found.")
