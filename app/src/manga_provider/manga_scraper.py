import requests
import time
from bs4 import BeautifulSoup
import re

class MangaProvider:
    def __init__(self):
        # Initialize two sessions
        self.api_session = requests.Session()  # For AniList API (get_manga_info)
        self.api_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        self.web_session = requests.Session()  # For web scraping (search_anime_list, get_latest_chapter)
        self.web_session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://mangapill.com",
            "Referer": "https://mangapill.com",
        })

    def get_manga_info(self, manga_title):
        print("get_manga_info title: ", manga_title)
        url = "https://api.jikan.moe/v4/manga"
        params = {"q": manga_title, "limit": 1, "timestamp": int(time.time())}
        response = self.api_session.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                return data["data"][0]  # Return the first match
            else:
                raise Exception(f"Manga with title '{manga_title}' not found.")
        else:
            raise Exception(f"Failed to fetch manga info: {response.status_code} - {response.text}")

    def search_manga(self, search_text):
        url = f"https://mangapill.com/search?q={search_text}&type=&status="
        
        # Make the GET request
        response = self.web_session.get(url)
        if response.status_code == 200:
            # Parse the HTML response
            soup = BeautifulSoup(response.text, "html.parser")
            manga_list = []
            
            # Select all anime/manga blocks
            manga_blocks = soup.select("div.grid > div")
            for block in manga_blocks:
                # Extract the title
                title_tag = block.select_one("a > div.mt-3.font-black")
                title = title_tag.text.strip() if title_tag else None
                
                # Extract the URL
                link_tag = block.select_one("a")
                link = f"https://mangapill.com{link_tag['href']}" if link_tag else None
                
                if title and link:
                    manga_list.append({"title": title, "url": link})
            
            return manga_list[:20]  # Return the first 20 results
        else:
            raise Exception(f"Failed to fetch anime list: {response.status_code}")

    def get_chapters(self, url):
        # Make a GET request to the provided URL
        response = self.web_session.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the page: {response.status_code}")
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate all chapter links in the chapter list
        chapter_links = soup.select('#chapters a[href]')
        if not chapter_links:
            raise Exception("No chapters found on the page. Verify the selector or check if the content is dynamically loaded.")
        
        chapters = []
        for link in chapter_links:
            # Extract the chapter number using regex
            match = re.search(r'Chapter\s*(\d+)', link.text, re.IGNORECASE)
            if match:
                chapter_number = match.group(1)
                chapter_url = f"https://mangapill.com{link['href']}"
                chapters.append({"chapter_number": chapter_number, "url": chapter_url})
            else:
                print(f"Skipping link without chapter number: {link.text}")  # Debugging
        
        if not chapters:
            raise Exception("No valid chapters were extracted from the page.")
        
        print(f"Found {len(chapters)} chapters.")
        return chapters

    def get_chapter_pages(self, chapter_url):
        
        # Make a GET request to the chapter URL
        response = requests.get(chapter_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the chapter page: {response.status_code}")
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <picture> elements containing the images
        picture_elements = soup.select('picture img.js-page')
        if not picture_elements:
            raise Exception("No pages found in the chapter.")
        
        # Extract page numbers and image URLs
        pages = {}
        for img in picture_elements:
            # Extract the page number from the "alt" attribute
            alt_text = img.get('alt', '')
            page_number = None
            if "Page" in alt_text:
                page_number = int(alt_text.split("Page")[-1].strip())
            
            # Extract the image URL from the "data-src" attribute
            image_url = img.get('data-src')
            
            if page_number and image_url:
                pages[page_number] = image_url
        
        return pages
