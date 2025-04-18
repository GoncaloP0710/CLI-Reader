import os
import asyncio
import aiohttp

from manga_provider import MangaProvider
from manga_downloader import download_all_images, download_image
from utils import create_directory

class MangaController:

    def __init__(self, manga_provider=None):
        self.manga_provider = manga_provider or MangaProvider()

    def load_manga_preview(self, manga_title):
        try:
            manga_info = self.manga_provider.get_manga_info(manga_title) # Get manga information
            if manga_info: # Get the manga cover image
                manga_title = manga_info.get("title")
                image_url = manga_info.get("images", {}).get("jpg", {}).get("image_url")
                cover_path = create_directory(f"../../manga/covers/{manga_title}")
                if cover_path == 1:
                    download_image(image_url, "../../manga/covers/" + manga_title, manga_title + ".jpg")
                elif cover_path == -1:
                    print(f"Error creating directory for the cover from {manga_title}.")
                    return None
                return manga_info, f"../../manga/covers/{manga_title}/" + manga_title + ".jpg"    
            else:
                raise Exception(f"Manga with title '{manga_title}' not found.")
                return manga_info, None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def search_manga(self, manga_title):
        """
            Search for a manga by title.

            :param manga_title: The title of the manga to search for.
        """

        try:
            results = self.manga_provider.search_manga(manga_title) # Search for the manga
            if results:
                return results
            else:
                raise Exception(f"No results found for '{manga_title}'.")
        except Exception as e:
            print(f"Error: {e}")
            return None


    def list_chapters(self, manga_link):
        """
            List all chapters of a manga.

            :param manga_link: The link of the manga page.
        """

        try:
            chapters = self.manga_provider.get_chapters(manga_link) # Get the latest chapter
            return chapters
        except Exception as e:
            print(f"Error: {e}")
            return None

    async def download_chapter(self, chapter_url, save_path):
        """
        Download all pages of a chapter using asyncio.

        :param chapter_url: The URL of the chapter to download.
        :param save_path: The path where the images will be saved.
        """
        try:
            if not os.path.exists(save_path):
                # Get all pages of the chapter
                pages = self.manga_provider.get_chapter_pages(chapter_url)
                if not pages:
                    raise Exception("No pages found in the chapter.")

                # Run the asynchronous download
                referer_url = chapter_url  # Use the chapter URL as the Referer
                await download_all_images(pages, save_path, referer_url)
        except Exception as e:
            print(f"Error during chapter download: {e}")