import os
import zipfile
from logger_setup import setup_logger

# Setup the logger
logger = setup_logger(__name__)


def compress_html_responses(zip_file_path):
    """Function to compress the individual .html files to a single .zip file

    :param zip_file_path: name for the zip file
    :type zip_file_path: str
    """
    try:
        logger.info(f"Starting the file compression...")
        with zipfile.ZipFile(zip_file_path, "w") as zip:
            for foldername, subfolder, files in os.walk("../results"):
                for filename in files:
                    if filename.endswith(".html"):
                        file_path = os.path.join(foldername, filename)
                        try:
                            zip.write(file_path, os.path.basename(file_path))
                            # logger.info(f"Compressed the folder path - {file_path}")
                        except Exception as e:
                            logger.error(f"Error compressing the folder path - {file_path} - {str(e)}")
        logger.info(f"File compression completed...")
    except Exception as e:
        logger.error(f"Failed to create zip file - {str(e)}")