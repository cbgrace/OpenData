from config import DATABASE_PATH
from dal import execute
from exceptions import DalException
from logging_config import get_logger
import os
from dal import build_file_name

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
    try:
        logger.info("checking to see if database exists...")  # TODO remove this logging
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
        # since this will run first every time, I suppose it is at least necessary to also check for db/table here
        # it would probably be ok to only check if file exists here, and not in the above method...
        # but I will have to think on it.
        if not check_if_file_exists(DATABASE_PATH):
            # if there is no db file, then no searches have been made...
            return False
        if not check_if_table_exists('search_history'):
            # same here, if not table, no searches, return false
            return False
        file_name = execute(SEARCH_DB, (report_name, agency_name, date))
        return file_name
    except DalException:
        raise
    except Exception as e:
        logger.error(f"Ran into an unexpected error, {e}")
        raise DalException


def check_if_file_exists(file_path: str):
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


def check_if_table_exists(table_name):
    logger.info("Checking if table exists...")  # TODO remove some of these logs
    try:
        count = execute(f"SELECT COUNT(*) FROM {table_name};")
        if count > 0:
            logger.info(f'Table "{table_name}" exists')
            return True
        else:
            logger.info(f"Table '{table_name}' did not exist")
            return False
    except Exception as e:
        logger.error(f"Ran into an error trying to check if table {table_name} exists: {e}")
        return False