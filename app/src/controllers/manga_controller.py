import os

from manga_provider import MangaProvider
from manga_downloader import download_image
from utils import create_directory

# ========== manga_controller.py ==========

# Instantiate the MangaProvider class
manga_provider = MangaProvider()

def load_manga_preview(manga_title):
    try:
        print(f"Loading manga: {manga_title}")
        manga_info = manga_provider.get_manga_info(manga_title) # Get manga information
        print(manga_info)
        if manga_info: # Get the manga cover image
            manga_title = manga_info.get("title")
            image_url = manga_info.get("images", {}).get("jpg", {}).get("image_url")
            cover_path = create_directory(f"../../manga/covers/{manga_title}")
            if cover_path == 1:
                download_image(image_url, "../../manga/covers/" + manga_title, manga_title + ".jpg")
            elif cover_path == -1:
                print(f"Error creating directory for the cover from {manga_title}.")
                return None
            return manga_info, f"../../manga/covers/{manga_title}"        
        else:
            raise Exception(f"Manga with title '{manga_title}' not found.")
            return manga_info, None
    except Exception as e:
        print(f"Error: {e}")
        return None
