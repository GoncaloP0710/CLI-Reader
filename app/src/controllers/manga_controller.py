import os

from manga_provider import get_manga_info
from manga_downloader import download_image
from utils import create_directory

# ========== manga_controller.py ==========

def load_manga(manga_title):
    try:
        print(f"Loading manga: {manga_title}")
        manga_info = get_manga_info(manga_title)
        if manga_info:
            manga_title = manga_info.get("title")
            print (f"Title: {manga_title}")
            image_url = manga_info.get("images", {}).get("jpg", {}).get("image_url")
            
            # Define the full directory path
            directory = f"../../manga/covers/{manga_title}"
            
            create_directory(directory)
                
            download_image(image_url, "../../manga/covers/" + manga_title, manga_title + ".jpg")
            return manga_info
        else:
            raise Exception(f"Manga with title '{manga_title}' not found.")
    except Exception as e:
        print(f"Error: {e}")
        return None
