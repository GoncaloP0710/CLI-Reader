
import requests
from bs4 import BeautifulSoup
import re


def get_latest_chapter(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
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

# Example usage
url = 'https://weebcentral.com/series/01J76XY7E9FNDZ1DBBM6PBJPFK/One-Piece'
latest_chapter = get_latest_chapter(url)
print(f"The latest One Piece chapter is: {latest_chapter}")


def get_all_chapters(self, url):
    response = self.web_session.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # Locate all chapter links in the chapter list
    chapter_links = soup.select('#chapter-list a[href]')
    if chapter_links:
        chapters = []
        for link in chapter_links:
            # Extract the chapter number using regex
            match = re.search(r'Chapter\s*(\d+)', link.text, re.IGNORECASE)
            if match:
                chapter_number = match.group(1)
                chapter_url = link['href']
                chapters.append({"chapter_number": chapter_number, "url": chapter_url})
        return chapters
    else:
        raise Exception("No chapters found on the page.")
    
# Example: Get all chapters
url = "https://weebcentral.com/series/01J76XY7E9FNDZ1DBBM6PBJPFK/One-Piece"
all_chapters = provider.get_all_chapters(url)
for chapter in all_chapters:
    print(f"Chapter {chapter['chapter_number']}: {chapter['url']}")