# FootyRenders Image Downloader

This Python script allows you to download HD images of football players from the FootyRenders website (https://www.footyrenders.com/premier-league/). The script utilizes concurrent processing to efficiently retrieve player details from multiple pages and then download the corresponding high-resolution images concurrently.

## Prerequisites

Make sure you have the following libraries installed:

- `requests`
- `concurrent.futures`
- `bs4` (BeautifulSoup)

You can install these libraries using the following command:

```bash
pip install requests beautifulsoup4
```

## Usage

1. Clone this repository to your local machine or download the script directly.

2. Run the script using Python:

```bash
python footyrenders_downloader.py
```

## How It Works

1. The script starts by defining the `base_url` for the FootyRenders Premier League pages.

2. The `process_page()` function processes each page by extracting the URLs of individual player pages. It utilizes BeautifulSoup to parse the HTML and retrieve relevant information.

3. The `download_image()` function downloads HD images from the player's page. It saves the images to the `downloaded_images` directory. Concurrent processing is used to speed up image downloading.

4. The `process_url()` function processes each player's page to extract and download the HD images using the `download_image()` function.

5. In the main section of the script, the `concurrent.futures.ThreadPoolExecutor()` is used to concurrently process the Premier League pages and player pages. This significantly improves performance by utilizing multiple threads.

6. After execution, the script will have downloaded all the HD images of football players to the `downloaded_images` directory.

## Customization

- You can modify the `max_pages` variable to control the number of Premier League pages to process.
- Adjust the script as needed for your specific requirements.

**Note:** Please be respectful of the website's terms of use and do not misuse this script.

## Disclaimer

This script is intended for educational purposes only. Use it responsibly and ensure compliance with the website's terms of use.

**Happy image downloading!**
