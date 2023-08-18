import requests
import concurrent.futures
from bs4 import BeautifulSoup
import os 
base_url = "https://www.footyrenders.com/premier-league/page/{}"

'''
Website to process all pages. Sample url: https://www.footyrenders.com/premier-league/page/2

Sample HTML Tag:
<ul class="rendersList">
    	<li class="renderBox">
        <div class="renderDetails">
            <a href="https://www.footyrenders.com/premier-league/chelsea/raheem-sterling-123/">
                <span class="newRender">NEW</span><img src="https://www.footyrenders.com/render/raheem-sterling-81-51x180.png" class="render" alt="Raheem Sterling football render" loading="lazy">                <div class="renderMeta">
                    <span class="bottomAlign">
                        <h3 title="Raheem Sterling render">Raheem Sterling</h3>
                        <span class="renderCreators">
                            Cut by:&nbsp;crisssnw                        </span>
                    </span>
                </div>
            </a>
        </div>
    </li>
    <li> ..... </li>
    <li> ..... </li>

	</ul>

Goal: <a> tag contains link of individual players where we can find full hd resolution various images of players. 
Extract <a href> tag url and append to page_list for all pages using process_page() function
'''

def process_page(page_number):
    url = base_url.format(page_number)
    response = session.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    render_list = soup.find_all("ul", class_="rendersList")

    if render_list:
        page_details = []
        for ul in render_list:
            li_list = ul.find_all("li", class_="renderBox")
            for li in li_list:
                a = li.find("a")
                if a:
                    href = a.get("href")
                    page_details.append(href)
        print(f"Page {page_number} processed.")
        return page_details
    else:
        print(f"No render details found on page {page_number}.")
        return []


def download_image(img_url, img_path):
    img_response = session.get(img_url)
    if img_response.status_code == 200:
        with open(img_path, "wb") as img_file:
            img_file.write(img_response.content)
        print(f"Image downloaded and saved as {os.path.basename(img_path)}")
    else:
        print(f"Failed to download image from {img_url}")


'''
Process_url() returns url of all players in a list. Eg: https://www.footyrenders.com/premier-league/chelsea/raheem-sterling-123/

Sample HTML Tags to download HD Images after clicking the thumbnail of the players.

 <a href="https://www.footyrenders.com/render/raheem-sterling-82.png"
    id="renderDL" download="Raheem Sterling - FootyRenders.png">
    <img
        src="https://www.footyrenders.com/render/raheem-sterling-82-281x540.png"
        loading="lazy" alt="Raheem Sterling"> <button id="downloadRender"
        data-tooltip="Don't forget to leave a rating!"><svg
            class="svg-icon render-download-icon" viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"><path
                d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z"
                fill-rule="evenodd"></path></svg> Download</button>
</a>
 
Goal: Take <a href> tag and download the HD images using threading concept.
'''


def process_url(url):
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        a_tags = soup.find_all("a", id="renderDL")

        if a_tags:
            for a in a_tags:
                img_url = a.get("href")
                img_name = img_url.split("/")[-1]
                img_path = os.path.join("downloaded_images", img_name)
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.submit(download_image, img_url, img_path)
        else:
            print(f"No image <a href> tags found on {url}")
    else:
        print(f"Failed to access URL: {url}")


if __name__ == "__main__":

    '''
    session = requests.Session() creates a persistent session object using the requests library. 
    A session object allows you to persist certain parameters across multiple HTTP requests, such as cookies, headers, and connection pooling. 
    This can be particularly useful when making multiple requests to the same website, as it can improve performance and maintain state between requests.
    '''

    session = requests.Session()

    combined_details = []
    max_pages = 100

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_page, page_number) for page_number in range(1, max_pages + 1)]

        for future in concurrent.futures.as_completed(futures):
            combined_details.extend(future.result())

    if not os.path.exists("downloaded_images"):
        os.makedirs("downloaded_images")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_url, combined_details)

    # Now combined_details contains all the details from all pages
    print("All pages processed and image downloaded.")
