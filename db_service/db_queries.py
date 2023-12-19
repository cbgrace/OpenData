from config import DATABASE_PATH
from dal import execute
from exceptions import DalException
from logging_config import get_logger
import os
from dal import build_file_name

"""
This module contains methods to query my sqlite database. 

Methods:
--------
    insert_search_data(report_name: str, agency_name: str, date: str):
        Creates a new entry in the search_history table containing the details for a recently executed search (report name,
        agency name, date & file name)
    search_for_match(report_name: str, agency_name: str, date: str):
        Searches for a report in the search_log.db
    check_if_file_exists(file_path: str) -> bool:
        Checks if a given file at file_path exists
    check_if_table_exists(table_name):
        Checks if a given table exists in my sqlite3 database.

Constants:
----------
    CREATE_TABLE: creates a table called search_history with the listed fields.
    INSERT_DATA: inserts a new row into the search_history table
    SEARCH_DB: searches for a file name in the search_history table given a report_name, agency_name & date

"""

logger = get_logger(__name__)

CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_name TEXT,
    agency_name TEXT,
    date TEXT,
    file_name TEXT)
"""

INSERT_DATA = """
    INSERT INTO search_history (report_name, agency_name, date, file_name)
    VALUES (?, ?, ?, ?)
"""

SEARCH_DB = """
    SELECT file_name FROM search_history
    WHERE report_name = ? AND agency_name = ? AND date = ?
"""

def insert_search_data(report_name: str, agency_name: str, date: str):
    """
    Creates a new entry in the search_history table containing the details for a recently executed search (report name,
        agency name, date & file name)
    :param report_name: the name of the report the user is searching for
    :param agency_name: the name of the agency the user is searching for
    :param date: the date the user is searching for
    :return: n/a
    """
    try:
        # need to build the file name:
        file_name = build_file_name(report_name, agency_name, date)
        # first, test if the database has been created (this function will create the file if not)
        check_if_file_exists(DATABASE_PATH)
        # then check if the table exists
        if not check_if_table_exists('search_history'):
            # if it doesn't exist, create it
            execute(CREATE_TABLE)
        # otherwise (and always), insert the data...
        execute(INSERT_DATA, (report_name, agency_name, date, file_name))
    except DalException:
        raise
    except Exception as e:
        logger.error(f"Ran into an unexpected error, {e}")
        raise DalException


def search_for_match(report_name: str, agency_name: str, date: str):
    """
    Searches for a report in the search_log.db
    :param report_name: report name to search for
    :param agency_name: agency name to search for
    :param date: date to search for
    :return: returns False if no match, returns file name of previous search if match is found.
    """
    try:
        if not check_if_file_exists(DATABASE_PATH):
            logger.info("Determined no database file exists.")
            # if there is no db file, then no searches have been made...
            return False
        if not check_if_table_exists('search_history'):
            logger.info("Determined no table 'search_history' exists w/in db.")
            # same here, if not table, no searches, return false
            return False
        file_name = execute(SEARCH_DB, (report_name, agency_name, date))
        if file_name == []:
            logger.info("File name does not exist in db")
            return False
        else:  # file name was found... I hope!
            logger.info(f"Successfully found file name: {file_name}")
            return file_name[0][0]
    except DalException:
        raise
    except Exception as e:
        logger.error(f"Ran into an unexpected error, {e}")
        raise DalException


def check_if_file_exists(file_path: str) -> bool:
    """
    Checks if a given file at file_path exists
    :param file_path: the path where the file *should* exist
    :return: false if file does not exist, true if it does
    """
    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                logger.info(f"Created new db file at {file_path}")
                pass
            return False
        else:
            return True
    except Exception as e:
        logger.error(f"Ran into an error trying to create db file: {e}")
        raise DalException


def check_if_table_exists(table_name) -> bool:
    """
    Checks if a given table exists in my sqlite3 database.
    :param table_name: table name to check
    :return: true if table exists, false if not
    """
    try:
        count = execute(f"SELECT COUNT(*) FROM {table_name};")
        if len(count) > 0:
            logger.info(f'Table "{table_name}" exists')
            return True
        else:  # this is essentially unreachable code, should I leave it here anyway?
            logger.info(f"Table '{table_name}' did not exist")
            return False
    except Exception as e:
        logger.error(f"Ran into an error trying to check if table {table_name} exists: {e}")
        return False  # this functionality didn't work how I wanted, so I had to return false on error too...
