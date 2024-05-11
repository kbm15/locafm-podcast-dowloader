# Podcast Crawler

## Overview
This Python program crawls a radio website to download podcast MP3 files. It extracts podcast URLs from pagination and downloads the MP3 files from each podcast page.

## Requirements
- Python 3.x
- BeautifulSoup (`pip install beautifulsoup4`)
- Requests (`pip install requests`)

## Usage
1. Clone this repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run `python podcast_crawler.py`.

## Description
- `podcast_crawler.py`: Main script to crawl the radio website, extract podcast URLs, and download MP3 files.
- `download_file.py`: Function to download MP3 files from URLs.
- `README.md`: Instructions and overview of the program.

## Configuration
- Adjust the `start_url` variable in `podcast_crawler.py` to specify the starting URL.
- Modify the `download_folder` variable to specify the folder to save downloaded files.

## Limitations
- Assumes specific HTML structure of the radio website.
- May require adjustments for different website structures or formats.


## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
