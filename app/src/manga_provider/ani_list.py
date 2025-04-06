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
            "Origin": "https://weebcentral.com",
            "Referer": "https://weebcentral.com",
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

    def search_anime_list(self, search_text):
        url = "https://weebcentral.com/search/simple?location=main"
        data = {"text": search_text}

        # Make the POST request
        response = self.web_session.post(url, data=data)
        if response.status_code == 200:
            # Parse the HTML response
            soup = BeautifulSoup(response.text, "html.parser")
            anime_list = []
            for link in soup.select("a.btn"):
                title = link.select_one("div.flex-1").text.strip()
                img_tag = link.select_one("img")
                img_url = img_tag["src"] if img_tag else None
                anime_list.append({"title": title, "image_url": img_url})
            return anime_list
        else:
            raise Exception(f"Failed to fetch anime list: {response.status_code}")

    def get_latest_chapter(self, url):
        response = self.web_session.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the page: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Locate the first chapter link in the chapter list
        first_chapter = soup.select_one('#chapter-list a[href]')
        if first_chapter:
            # Extract the chapter number using regex
            match = re.search(r'Chapter\s*(\d+)', first_chapter.text, re.IGNORECASE)
            if match:
                return match.group(1)
            else:
                raise Exception("Chapter number not found in the first chapter link.")
        else:
            raise Exception("No chapters found on the page.")
