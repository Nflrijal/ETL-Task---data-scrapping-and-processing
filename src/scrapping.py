import os
import requests
import logging
from bs4 import BeautifulSoup
from logger_setup import setup_logger

# Setup the logger
logger = setup_logger(__name__)


def get_total_pages(url: str):
    """Function to find the total number of pages available / required to scrap

    :param url: base url from which the number of pages has to be determined
    :type url: str
    :return: max value of the page numbers found
    :rtype: int
    """
    logger.info(f"Fetching the total number of pages from URL : {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching URL : {url} --- {str(e)}")
        return 0

    soup = BeautifulSoup(response.content, "html.parser")

    pagination = soup.find("ul", class_="pagination")

    if not pagination:
        logger.warning(f"No pagination found.")
        return 0

    pages = pagination.find_all("a")

    page_numbers = [
        int(page.text.strip()) for page in pages if page.text.strip().isdigit()
    ]

    return max(page_numbers)


def save_table_response(base_url, page_value, total_pages, response_folder):
    """Function to save the response tables as individual .html files

    :param base_url: base url from which the data has to be extracted
    :type base_url: str
    :param page_value: the url part to fetch the page's data
    :type page_value: str
    :param total_pages: the total number of pages to be extracted
    :type total_pages: int
    :param response_folder: the folder to which the individual files are to be saved
    :type response_folder: str

    """

    for i in range(1, total_pages + 1):
        new_url = base_url + page_value

        try:
            logger.info(f"Fetching data from URL: {new_url.format(i)}")
            response = requests.get(new_url.format(i))
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(
                f"Failed to retreive data from URL : {new_url.format(i)} --- {str(e)}"
            )
            continue
        try:
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")
            table = soup.find("table")

            if not table:
                logger.warning(f"No table found in URL - {new_url.format(i)}")
                continue

            file_path = os.path.join(response_folder, f"{i}.html")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(str(table))
        except Exception as e:
            logger.error(f"Error processing URL - {new_url.format(i)} -- {str(e)}")
