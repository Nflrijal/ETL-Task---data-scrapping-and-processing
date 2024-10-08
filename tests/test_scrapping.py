import os
import sys
import pytest
import requests
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.scrapping import save_table_response, get_total_pages


@patch("src.scrapping.requests.get")
@patch("src.scrapping.BeautifulSoup")
def test_get_total_pages_success(mock_soup, mock_get):

    # mock setup
    url = "http://example.com"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # mocking the pagination in the BeautifulSoup object
    mock_soup_obj = MagicMock()
    mock_soup.return_value = mock_soup_obj
    pagination = MagicMock()
    mock_soup_obj.find.return_value = pagination
    pagination.find_all.return_value = [
        MagicMock(text="1"),
        MagicMock(text="2"),
        MagicMock(text="3"),
    ]

    # function call
    total_pages = get_total_pages(url)

    # assertion
    assert total_pages == 3
    mock_get.assert_called_once_with(url)
    mock_soup.assert_called_once()


@patch("src.scrapping.requests.get")
@patch("src.scrapping.BeautifulSoup")
def test_get_total_pages_no_pagination(mock_soup, mock_get):

    # mock setup
    url = "http://example.com"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # mocking no pagination in the BeautifulSoup object
    mock_soup_obj = MagicMock()
    mock_soup.return_value = mock_soup_obj
    mock_soup_obj.find.return_value = None

    # function call
    total_pages = get_total_pages(url)

    # Assert
    assert total_pages == 0
    mock_get.assert_called_once_with(url)


@patch("src.scrapping.requests.get")
def test_get_total_pages_request_exception(mock_get):

    # mock setup
    url = "http://example.com"
    mock_get.side_effect = requests.RequestException("Error")

    # function call
    total_pages = get_total_pages(url)

    # assertion
    assert total_pages == 0
    mock_get.assert_called_once_with(url)


@patch("src.scrapping.requests.get")
@patch("src.scrapping.BeautifulSoup")
@patch("builtins.open", new_callable=MagicMock)
@patch("os.path.join")
def test_save_table_response_success(mock_path_join, mock_open, mock_soup, mock_get):

    # mock setup
    base_url = "https://example.com/forms/."
    page_value = "?page_num={}"
    total_pages = 3
    response_folder = "./results"

    # mocking get request to return a valid response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # mocking BeautifulSoup to return a table
    mock_soup_obj = MagicMock()
    mock_soup.return_value = mock_soup_obj
    table = MagicMock()
    mock_soup_obj.find.return_value = table

    # mocking os.path.join to return valid file paths
    mock_path_join.side_effect = lambda folder, filename: f"{folder}/{filename}"

    # function call
    save_table_response(base_url, page_value, total_pages, response_folder)

    # assertion
    assert mock_get.call_count == total_pages
    mock_soup.assert_called()


@patch("src.scrapping.requests.get")
@patch("src.scrapping.BeautifulSoup")
@patch("builtins.open", new_callable=MagicMock)
@patch("os.path.join")
def test_save_table_response_no_table(mock_path_join, mock_open, mock_soup, mock_get):

    # mock setup
    base_url = "https://example.com/forms/."
    page_value = "?page_num={}"
    total_pages = 3
    response_folder = "./results"

    # mocking get request to return a valid response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # mocking BeautifulSoup to return no table
    mock_soup_obj = MagicMock()
    mock_soup.return_value = mock_soup_obj
    mock_soup_obj.find.return_value = None  # No table found

    # function call
    save_table_response(base_url, page_value, total_pages, response_folder)

    # assertion
    mock_open.assert_not_called()  # No file should be written
    mock_soup.assert_called()


@patch("src.scrapping.requests.get")
@patch("src.scrapping.BeautifulSoup")
@patch("builtins.open", new_callable=MagicMock)
def test_save_table_response_request_exception(mock_open, mock_soup, mock_get):

    # mock setupe
    base_url = "https://example.com/forms/."
    page_value = "?page_num={}"
    total_pages = 3
    response_folder = "./results"

    # mocking get request to raise an exception
    mock_get.side_effect = requests.RequestException("Error")

    # function call
    save_table_response(base_url, page_value, total_pages, response_folder)

    # assertion
    mock_open.assert_not_called()  # No file should be written
    assert mock_get.call_count == total_pages
