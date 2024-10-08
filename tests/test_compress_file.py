import sys
import os
import pytest
from unittest.mock import patch, MagicMock, call
import logging


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.compress_file import compress_html_responses


@patch("src.compress_file.os.walk")
@patch("src.compress_file.zipfile.ZipFile")
@patch("src.compress_file.logger")
def test_compress_html_responses_success(mock_logger, mock_zipfile, mock_os_walk):

    zip_file_name = "test.zip"

    mock_os_walk.return_value = [
        ("../results", ["subfolder"], ["file1.html", "file2.html", "file3.txt"])
    ]

    mock_zip = MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zip

    compress_html_responses(zip_file_name)

    mock_os_walk.assert_called_once_with("../results")

    mock_zipfile.assert_called_once_with(zip_file_name, "w")

    expected_calls = [
        call(os.path.join("../results", "file1.html"), "file1.html"),
        call(os.path.join("../results", "file2.html"), "file2.html"),
    ]
    mock_zip.write.assert_has_calls(expected_calls, any_order=True)

    # Ensure .txt file was ignored
    assert mock_zip.write.call_count == 2

    mock_logger.info.assert_any_call("Starting the file compression...")
    mock_logger.info.assert_any_call("File compression completed...")


@patch("src.compress_file.os.walk")
@patch("src.compress_file.zipfile.ZipFile")
@patch("src.compress_file.logger")
def test_compress_html_responses_exception(mock_logger, mock_zipfile, mock_os_walk):

    zip_file_name = "test.zip"

    mock_os_walk.return_value = [("../results", [], ["file1.html", "file2.html"])]

    mock_zip = MagicMock()
    mock_zip.write.side_effect = Exception("Mocked exception")
    mock_zipfile.return_value.__enter__.return_value = mock_zip

    compress_html_responses(zip_file_name)

    mock_logger.error.assert_any_call(
        f"Error compressing the folder path - {os.path.join('../results', 'file1.html')} - Mocked exception"
    )
    mock_logger.error.assert_any_call(
        f"Error compressing the folder path - {os.path.join('../results', 'file2.html')} - Mocked exception"
    )
    mock_zipfile.return_value.__exit__.assert_called()


@patch("src.compress_file.os.walk")
@patch("src.compress_file.zipfile.ZipFile")
@patch("src.compress_file.logger")
def test_compress_html_responses_no_html_files(mock_logger, mock_zipfile, mock_os_walk):

    zip_file_name = "test.zip"

    mock_os_walk.return_value = [("../results", [], ["file1.txt", "file2.doc"])]

    mock_zip = MagicMock()
    mock_zipfile.return_value.__enter__.return_value = mock_zip

    compress_html_responses(zip_file_name)

    mock_zip.write.assert_not_called()

    mock_logger.info.assert_any_call("Starting the file compression...")
    mock_logger.info.assert_any_call("File compression completed...")
