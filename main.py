import requests
from bs4 import BeautifulSoup
import os

# Function to download MP3 files
def download_file(url, folder):
    filename = os.path.join(folder, url.split('/')[-1])
    with open(filename, 'wb') as f:
        response = requests.get(url)
        f.write(response.content)

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
    pages = [a['href'] for a in pagination.find_all('a')]

    # Iterate through pagination
    for page in pages:
        page_url = base_url + page
        page_soup = fetch_and_parse(page_url)

        # Find podcast URLs
        podcast_items = page_soup.find_all('div', class_='programa-item')
        for item in podcast_items:
            podcast_url = base_url + item.find('a')['href']
            podcast_soup = fetch_and_parse(podcast_url)

            # Find MP3 download link
            download_link = podcast_soup.find('div', class_='jp-download').find('a')['href']
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
