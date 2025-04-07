import os
import cloudscraper
import asyncio
import aiohttp
from utils import create_directory


    


































def download_image(image_url, save_path, file_name, referer_url=None):
    # Create the directory if it doesn't exist
    create_directory(save_path)
        
    # Define the full file path for the image
    file_path = os.path.join(save_path, file_name)
    
    # Create a CloudScraper session
    scraper = cloudscraper.create_scraper()
    
    # Set headers for the request
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
    }
    headers["Referer"] = "https://mangapill.com/"
    
    # Download the image
    response = scraper.get(image_url, headers=headers, stream=True)
    print(response)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image successfully downloaded to {file_path}")
    else:
        raise Exception(f"Failed to download image: {response.status_code}")


async def download_image_async(session, image_url, save_path, file_name, referer_url=None):
    """
    Asynchronously download a single image.

    :param session: The aiohttp session.
    :param image_url: The URL of the image to download.
    :param save_path: The path where the image will be saved.
    :param file_name: The name of the file to save the image as.
    :param referer_url: The Referer URL for the request.
    """
    try:
        # Create the directory if it doesn't exist
        create_directory(save_path)

        # Define the full file path for the image
        file_path = os.path.join(save_path, file_name)

        # Set headers for the request
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
        }
        headers["Referer"] = "https://mangapill.com/"

        # Asynchronously download the image
        async with session.get(image_url, headers=headers) as response:
            if response.status == 200:
                with open(file_path, "wb") as file:
                    file.write(await response.read())
                print(f"Image successfully downloaded: {file_path}")
            else:
                print(f"Failed to download {image_url}: {response.status}")
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")


async def download_all_images(pages, save_path, referer_url=None):
    """
    Asynchronously download all images for a chapter.

    :param pages: A dictionary of page numbers and their corresponding image URLs.
    :param save_path: The path where the images will be saved.
    :param referer_url: The Referer URL for the requests.
    """
    # Create the directory if it doesn't exist
    create_directory(save_path)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for page_number, image_url in pages.items():
            file_name = f"page_{page_number}.jpg"
            print(f"Queueing download for page {page_number} from {image_url}")
            tasks.append(download_image_async(session, image_url, save_path, file_name, referer_url))
        await asyncio.gather(*tasks)
