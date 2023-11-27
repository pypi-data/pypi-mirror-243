import argparse
import os
import threading
from queue import Queue

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve

from pygments.lexer import default

# Set to store visited URLs
visited_urls = set()


# Function to create directories based on URL structure
def create_directories(url, base_url):
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Remove leading and trailing slashes
    path = path.strip('/')

    # Replace slashes with the OS-specific separator
    path = path.replace('/', os.path.sep)

    # Create the directory structure relative to the base URL
    full_path = os.path.join('pdf_files', path)
    os.makedirs(full_path, exist_ok=True)

    return full_path


# Function to download PDF files with the correct folder structure
def download_pdf(pdf_url, full_path):
    pdf_filename = pdf_url.split("/")[-1]
    pdf_path = os.path.join(full_path, pdf_filename)

    # Check if the PDF file already exists
    if not os.path.exists(pdf_path):
        urlretrieve(pdf_url, pdf_path)
        print(f'Downloaded: {pdf_filename}')
    else:
        print(f'Skipped: {pdf_filename} (already exists)')


# Function to crawl a URL and its links recursively
def crawl_url(base_url, url, domain):
    try:
        # Check if the URL starts with the base URL and if it has not been visited before
        if not url.startswith(base_url) or url in visited_urls:
            return

        visited_urls.add(url)  # Add the URL to the set of visited URLs

        print("Crawling:" + url)

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            full_path = create_directories(url, base_url)

            for link in soup.find_all('a'):
                link_url = urljoin(url, link.get('href'))

                # Check if the link points to a PDF file
                if link_url.endswith('.pdf'):
                    download_pdf(link_url, full_path)
                else:
                    # Check if the link is within the same domain and is an HTML page
                    parsed_link_url = urlparse(link_url)
                    if parsed_link_url.netloc == domain and link_url.endswith(('.html', '.htm')):
                        crawl_url(base_url, link_url, domain)

    except Exception as e:
        print(f'Error while crawling {url}: {e}')


# Function to manage crawling threads
def crawl_thread(url_queue, domain):
    while True:
        url = url_queue.get()
        crawl_url(url, domain, url_queue)
        url_queue.task_done()


def main():
    parser = argparse.ArgumentParser(description='Recursively Crawl website for PDFs')
    parser.add_argument('--base', required=True,
                        help='the base URL. Crawling will not go up this base.')
    parser.add_argument('--start', required=True,
                        help='the start page')
    parser.add_argument('--threads', required=False,
                        help='Number of threads to use', default=4)
    args = parser.parse_args()

    # Replace with the URL of the webpage you want to crawl
    # base_url = "https://www.jpx.co.jp/english/markets"
    # start_url = base_url + '/equities/alerts/index.html'
    base_url = args.base
    start_url = base_url + args.start
    print("Start parameters:" + base_url + " > " + start_url)

    # Create a directory to save the PDF files
    if not os.path.exists('pdf_files'):
        os.makedirs('pdf_files')

    # Extract the domain from the starting URL
    parsed_start_url = urlparse(start_url)
    domain = parsed_start_url.netloc

    # Start crawling from the starting URL
    crawl_url(base_url, start_url, domain)


if __name__ == '__main__':
    main()
