import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import imagehash
from urllib.parse import urljoin

# Base URL to scrape from
URL = "https://www.example.com/"
# A hash to match images against; images close to this hash will be flagged
REFERENCE_HASH = None
# Keep track of URLs we've already visited to avoid cycles
visited_urls = set()
# Directory to save downloaded images
SAVE_FOLDER = "downloaded-img"
# Location of the reference image to compare other images with
IMG_LOCATION = "image/reference.jpg"

# Create the save directory if it doesn't exist
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def is_valid_image(img_data):
    """Check if the provided bytes represent a valid image."""
    try:
        Image.open(io.BytesIO(img_data))
        return True
    except:
        return False

def download_images_from_page(url, reference_hash):
    """Recursively download images from a page and its linked pages."""
    # Avoid revisiting URLs or processing external links
    if url in visited_urls or not url.startswith(URL):
        return
    visited_urls.add(url)
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Locate all image tags on the page
        images = soup.find_all("img")
        for i, img in enumerate(images):
            src = img.get("src")
            if src:
                # Convert relative URLs to absolute
                if not src.startswith(("http", "www")):
                    src = urljoin(URL, src).split("?")[0]  # Clean up the URL by removing parameters
                
                # Fetch the image data
                img_data = requests.get(src).content
                
                if is_valid_image(img_data):
                    # Determine the image extension from the original URL
                    img_extension = os.path.splitext(src)[1]
                    
                    # Add the origin URL as metadata in the filename, ensuring it's not too long
                    img_name_suffix = "-from-" + url.replace("https://", "").replace("www.", "").replace("/", "-").replace(".", "-")
                    if len(img_name_suffix) > 50:
                        img_name_suffix = img_name_suffix[:50] + "..."
                    
                    # Construct the filename using the original extension
                    img_name = os.path.join(SAVE_FOLDER, os.path.basename(src).split('.')[0] + img_name_suffix + img_extension)
                    with open(img_name, "wb") as f:
                        f.write(img_data)
                    
                    # Check if the image matches or is similar to our reference image
                    current_img = Image.open(io.BytesIO(img_data))
                    current_hash = imagehash.average_hash(current_img)
                    if current_hash - reference_hash < 10:
                        print(f"Similar image found at URL: {url}")
                        print(f"Image saved as: {img_name}")

        # Recursively fetch images from linked pages
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                # Convert relative URLs to absolute
                if not href.startswith(("http", "www")):
                    href = urljoin(URL, href)
                download_images_from_page(href, reference_hash)
    except Exception as e:
        print(f"Failed for URL {url}. Reason: {str(e)}")


if __name__ == "__main__":
    # Compute the hash for our reference image
    reference_image = Image.open(IMG_LOCATION)
    REFERENCE_HASH = imagehash.average_hash(reference_image)

    # Start the scraping process
    download_images_from_page(URL, REFERENCE_HASH)
