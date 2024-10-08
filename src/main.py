import os
import sys
from scrapping import get_total_pages, save_table_response
from database import create_table, execute_query
from excel_processing import combine_tables_to_excel, team_summary
from compress_file import compress_html_responses
from logger_setup import setup_logger

# Setup the logger
logger = setup_logger(__name__)

# Get the path of the current script
current_script_path = os.path.abspath(__file__)

# Get the path of the project root directory
project_root = os.path.abspath(
    os.path.join(os.path.dirname(current_script_path), "..")
)


def get_transformation_query():
    query_path = current_script_path.replace("main.py", "query.sql")

    with open(query_path, "r") as f:
        query = f.read()
    return query


def main():
    base_url = "https://www.scrapethissite.com/pages/forms/."
    page_value = "?page_num={}"

    # output_directory = "../results"
    # response_folder = os.path.join(output_directory, "html_responses")
    # os.makedirs(response_folder, exist_ok=True)
    
    print(project_root)
    output_directory = os.path.join(project_root, "results")
    print("output_directory", output_directory)
    response_folder = os.path.join(output_directory, "html_responses")
    print("response_folder", response_folder)
    
    zip_file_path = os.path.join(output_directory, "web_data.zip")
    print("zip_file_path", zip_file_path)
    excel_file_path = os.path.join(output_directory, "combined_tables.xlsx")
    print("excel_file_path", excel_file_path)
    # exit()
    os.makedirs(response_folder, exist_ok=True)


    column_mapping = {
        "Team Name": "team_name",
        "Year": "year",
        "Wins": "wins",
        "Losses": "losses",
        "OT Losses": "ot_losses",
        "Win %": "win_pct",
        "Goals For (GF)": "goals_for",
        "Goals Against (GA)": "goals_against",
        "+ / -": "goal_difference",
    }

    query = get_transformation_query()

    total_pages = get_total_pages(base_url)

    if total_pages == 0:
        logger.info(f"No pages found or failed to retrieve pages")
    logger.info(f"Total pages to scrap - {total_pages}")

    save_table_response(base_url, page_value, total_pages, response_folder)

    compress_html_responses(zip_file_path)

    combine_tables_to_excel(response_folder, excel_file_path)

    team_summary(excel_file_path, column_mapping, query)


if __name__ == "__main__":
    main()
