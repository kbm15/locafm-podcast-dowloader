import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os

# Function to download MP3 files
def download_file(url, folder):
    # Parse podcast name and date from URL
    parts = url.split('/')[-1].split('__')
    podcast_name = parts[0].replace('-', ' ').title()
    
    # Find the date in the parts
    date_str = None
    for part in parts[1].split('_'):
        try:
            date = datetime.strptime(part, "%Y-%m-%d")
            date_str = part
            break
        except ValueError:
            pass

    if date_str is None:
        print(f"Date not found in URL {url}. Skipping...")
        return
    
    filename = date_str + '.mp3'

    # Create folder for podcast if it doesn't exist
    podcast_folder = os.path.join(folder, podcast_name)
    if not os.path.exists(podcast_folder):
        os.makedirs(podcast_folder)

    # Check if the file already exists
    filepath = os.path.join(podcast_folder, filename)
    if os.path.exists(filepath):
        print(f"File {filename} for podcast {podcast_name} already exists. Skipping...")
        return

    # Download the file
    with open(filepath, 'wb') as f:
        response = requests.get(url)
        f.write(response.content)

    print(f"Downloaded {filename} for podcast {podcast_name}")


# Base URL
base_url = "https://www.locafm.com"

# Function to fetch and parse HTML content
def fetch_and_parse(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Main function to crawl podcast URLs
def crawl_podcasts(start_url, download_folder):
    # Fetch HTML content
    soup = fetch_and_parse(start_url)

    # Find pagination links
    pagination = soup.find('ul', class_='pagination')
    pagination_items = pagination.find_all('li', class_='hidden-xs')
    pages = []
    for item in pagination_items:
        page_number = int(item.contents[1].string)  # Extract the page number
        pages.append(f"/podcast.html?pagina={page_number}")  # Construct the URL with page number

    # Iterate through pagination
    for page_url in pages:
        print(f"Scraping page: {base_url}{page_url}")
        page_soup = fetch_and_parse(base_url + page_url)

        # Find podcast URLs
        podcast_items = page_soup.find_all('div', class_='programa-item')
        for i, item in enumerate(podcast_items, start=1):
            podcast_url = base_url + item.find('a')['href']
            print(f"Downloading podcast {i}/{len(podcast_items)} from {podcast_url}")
            podcast_soup = fetch_and_parse(podcast_url)

            # Find MP3 download link
            download_divs = podcast_soup.find_all('div', class_='jp-download')
            for div in download_divs:
                download_link = div.find('a')['href']
                mp3_url = base_url + download_link

                # Download MP3 file
                download_file(mp3_url, download_folder)


# Start URL
start_url = "https://www.locafm.com/podcast.html?pagina=1"
# Folder to save downloaded files
download_folder = "podcasts"

# Create folder if it doesn't exist
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Start crawling
crawl_podcasts(start_url, download_folder)
