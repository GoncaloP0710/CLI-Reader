
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
# url = 'https://weebcentral.com/series/01J76XY7E9FNDZ1DBBM6PBJPFK/One-Piece'
# latest_chapter = get_latest_chapter(url)
# print(f"The latest One Piece chapter is: {latest_chapter}")

def get_all_chapters(url):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0"
    })

    # Step 1: Fetch the initial page
    response = session.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 2: Locate the "Show All Chapters" button and its URL
    show_all_button = soup.select_one('button[hx-get]')
    if not show_all_button:
        raise Exception("Show All Chapters button not found on the page.")
    
    full_chapter_list_url = show_all_button.get('hx-get')
    if not full_chapter_list_url:
        raise Exception("The 'hx-get' attribute is missing in the Show All Chapters button.")
    
    print(f"Fetching full chapter list from: {full_chapter_list_url}")  # Debugging

    # Step 3: Fetch the full chapter list
    response = session.get(full_chapter_list_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the full chapter list: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 4: Extract all chapters
    chapter_links = soup.select('#chapter-list a[href]')
    if not chapter_links:
        raise Exception("No chapters found on the page.")
    
    chapters = []
    for link in chapter_links:
        # Extract the chapter number using regex
        match = re.search(r'Chapter\s*(\d+)', link.text, re.IGNORECASE)
        if match:
            chapter_number = match.group(1)
            chapter_url = link['href']
            chapters.append({"chapter_number": chapter_number, "url": chapter_url})
        else:
            print(f"Skipping link without chapter number: {link.text}")  # Debugging
    
    if not chapters:
        raise Exception("No valid chapters were extracted from the page.")
    
    return chapters

# Example usage
url = "https://weebcentral.com/series/01J76XY7E9FNDZ1DBBM6PBJPFK/One-Piece"
all_chapters = get_all_chapters(url)

# Write the chapters to a text file
output_file_path = "/home/goncalop0710/Desktop/Projects/CLI-Reader/app/src/output.txt"
with open(output_file_path, "w") as file:
    for chapter in all_chapters:
        file.write(f"Chapter {chapter['chapter_number']}: {chapter['url']}\n")

print(f"Chapter list has been written to {output_file_path}")