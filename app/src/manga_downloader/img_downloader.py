import requests
import os
# ========== manga_provider/Image Downloader ==========

def download_image(image_url, save_path, file_name):
        
    # Define the full file path for the image
    file_path = os.path.join(save_path, file_name)
    
    # Download the image
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image successfully downloaded to {file_path}")
    else:
        raise Exception(f"Failed to download image: {response.status_code}")
