import os
import sqlite3
from logger_setup import setup_logger

# Setup the logger
logger = setup_logger(__name__)


def create_table(ws, columns):
    """Function to create the sqlite table from the excel sheet for performing the transofmrations.

    :param ws: active worksheet
    :type ws: str
    :param columns: the columns with which table is to be created
    :type columns: list

    """
    try:
        with sqlite3.connect("excel_data.db") as conn:
            cursor = conn.cursor()

            cursor.execute("DROP TABLE IF EXISTS data")

            create_table_query = f"CREATE TABLE data ({', '.join(columns)});"

            logger.info(f"Executing create table query: {create_table_query}")
            cursor.execute(create_table_query)

            # Insert data into the table
            for row in ws.iter_rows(min_row=2, values_only=True):
                placeholders = ", ".join(["?"] * len(row))
                insert_query = f"INSERT INTO data VALUES ({placeholders});"
                logger.info(f"Executing insert query: {insert_query} with values {row}")
                cursor.execute(insert_query, row)

            # Commit the changes
            conn.commit()
    except sqlite3.Error as e:
        logger.error(f"SQLite error: {e}")
    except Exception as e:
        logger.error(f"An error occurred while creating the table or inserting data: {e}")


def execute_query(query):
    """Function to execute the transformation script over the sqlite table and return the response

    :param query: transformation sql query to be executed
    :type query: str
    :return query_result: the transformation sql query result
    :rtype query_result: string
    :return query_columns: the list of column names in the result
    :rtype query_columns: list
    
    """
    try:
        with sqlite3.connect("excel_data.db") as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            query_result = cursor.fetchall()
            query_columns = [description[0] for description in cursor.description]

            conn.commit()
        logger.info("Query executed successfully.")
        return query_result, query_columns
    
    except sqlite3.Error as e:
        logger.error(f"SQLite error occurred: {e}")
        return [], []
    except Exception as e:
        logger.error(f"An error occurred while executing the query: {e}")
        return [], []