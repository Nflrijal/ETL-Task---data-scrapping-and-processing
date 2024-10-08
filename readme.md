# ETL Task - data scrapping and processing

This project provides a framework for scrapping the data from websites, processes the data and stores them in various formats.
It uses Python libraries such as BeautifulSoup for web scraping and OpenPyXL for handling Excel files.

# Features 

1. Gets the total number of pages available on the webpage.
2. Scrapes the data from each page and saves them as individual HTML files based on the page number.
3. Compresses the individual .html files into a single zip file.
4. Combines the data from individual .html files sequentially and creates an Excel sheet.
5. Performs a transformation over the data inside the Excel sheet and saves the summary inside a new sheet.
6. Creates an intermediate SQLite table using the data available in the Excel sheet for performing transformations.
7. Runs the transformation query against the table and saves the result back to a new sheet in the Excel file.

# Folder Structure 

```text
results/               # Folder where scraped HTML files, zip file and final excel sheet are saved
src/
├── __init__.py
├── compress_file.py    # Handles file compression
├── database.py         # Database interaction logic
├── excel_processing.py # Functions for processing and saving Excel files
├── logger_setup.py     # Logger configuration
├── main.py             # Main entry point of the application
|── query.sql           # The transformation sql script
└── scrapping.py        # Web scraping logic
tests/
├── __init__.py
├── test_compress_file.py # Tests for the compress_file module
└── test_scrapping.py     # Tests for the scrapping module
requirements.txt      # Python dependencies
README.md             # Project documentation
```

# Installation

```text
git clone https://your_repository_url.git
cd your_repository_directory
pip install -r requirements.txt
```

# Usage

To execute the entire ETL process, run the following command:

```text
python src/main.py
```

## File description

1. main.py : The main entry point of the application that orchestrates the entire ETL process.
2. scrapping.py : Contains the web scraping logic to extract data from the specified webpage and save it as HTML files.
3. compress_file.py : Reads the individual .html files and compress them into a single .zip file.
4. database.py : Contains logic for interacting with the sqlite database, including creating tables and executing queries.
5. excel_processing.py : Provides functions for - 
    1. Saving the scrapped data in sequence to the excel sheet
    2. Saving the transformed data to the new sheet
6. logger_setup.py : Configures the logger used throughout the project to log important information and errors.
7. query.sql : SQL query for performing the transformation over the scrapped data.

# Running Tests
To run the tests for the project, use the following command:

```text
pytest tests/
```

