import os

import requests
from bs4 import BeautifulSoup

base_url = "https://link.springer.com/"
url = "{}search/page/{}?showAll=true&package=mat-covid19_textbooks&facet-content-type=%22Book%22&sortOrder=newestFirst"
pages = 24

download_folder = "books"

# if our download folder doesn't exists, we create the download folder.
if not os.path.exists(download_folder):
    os.mkdir(download_folder)

# we iterate over the pages
for page in range(1, pages + 1):
    print(f"REQUESTING PAGE {page}")
    paged_url = url.format(base_url, page)
    response = requests.get(paged_url)

    # if we fetched the page correctly, we read the links to each book
    if response.status_code == 200:
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        books_links = soup.findAll("a", {"class": "title"})

        # for each book, we visit the concrete book page
        for book_link in books_links:
            book_url = f"{base_url}{book_link['href']}"
            print(f"REQUESTING BOOK URL {book_url}")
            response = requests.get(book_url)

            # if we fetch correctly the book page, we look for the title and the download link
            if response.status_code == 200:
                book_html = response.content
                soup = BeautifulSoup(book_html, 'html.parser')
                title = soup.findAll("h1")[0].text
                download_url = soup.findAll("a", {"class": "test-bookpdf-link"})[0]["href"]
                download_url = f"{base_url}{download_url}"
                print(f"TRYING TO DOWNLOAD FROM {download_url}")
                # once we have the title and the download url, we download the content
                # note that content is not a text string, is a binary string
                response = requests.get(download_url)

                # if we download correctly the book content, we store it in a file called <title>.pdf
                # replacing <title> for each book title.
                if response.status_code == 200:
                    with open(f"{download_folder}/{title}.pdf", "wb") as downloaded_file:
                        downloaded_file.write(response.content)
                        print(f"DOWNLOADED {download_folder}/{title}.pdf")
