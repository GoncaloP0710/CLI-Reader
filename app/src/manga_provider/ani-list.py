import requests

def get_manga_info(manga_title):
    url = f"https://api.jikan.moe/v4/manga"
    params = {"q": manga_title, "limit": 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            return data["data"][0]  # Return the first match
        else:
            raise Exception(f"Manga with title '{manga_title}' not found.")
    else:
        raise Exception(f"Failed to fetch manga info: {response.status_code} - {response.text}")

# Example usage
manga_info = get_manga_info("One Piece")
print(manga_info)
