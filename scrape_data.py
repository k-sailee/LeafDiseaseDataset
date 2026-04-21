import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin

SAVE_DIR = "scraped_data"

PAGES = {
    "healthy": "https://shwethav-pixel.github.io/Jasmine.LeafData/healtyLeaves.html",
    "stage1": "https://shwethav-pixel.github.io/Jasmine.LeafData/stage1.html",
    "stage2": "https://shwethav-pixel.github.io/Jasmine.LeafData/stage2.html",
    "stage3": "https://shwethav-pixel.github.io/Jasmine.LeafData/stage3.html",
    "stage4": "https://shwethav-pixel.github.io/Jasmine.LeafData/stage4.html"
}

os.makedirs(SAVE_DIR, exist_ok=True)

def scrape_page(class_name, url):
    print(f"\nScraping {class_name}...")

    os.makedirs(os.path.join(SAVE_DIR, class_name), exist_ok=True)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    images = soup.find_all("img")

    count = 0

    for img in tqdm(images):
        img_url = img.get("src")

        if not img_url:
            continue

        full_url = urljoin(url, img_url)

        try:
            img_data = requests.get(full_url).content
            file_path = os.path.join(SAVE_DIR, class_name, f"{count}.jpg")

            with open(file_path, "wb") as f:
                f.write(img_data)

            count += 1

        except:
            continue

    print(f"{class_name}: {count} images downloaded")


def main():
    for cls, url in PAGES.items():
        scrape_page(cls, url)


if __name__ == "__main__":
    main()