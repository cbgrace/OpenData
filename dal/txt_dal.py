from exceptions import DalException
from logging_config import get_logger
import os

"""
This module contains methods to read/write data to text files.

Methods:
--------
    save_json_to_txt(report_name: str, agency_name: str, date: str, json_data):
        Saves data in JSON format to a txt file
    read_from_txt(file_name) -> list:
        Reads data from a txt file
    build_file_name(report_name: str, agency_name: str, date: str):
        Builds file name in format: "database/reportname_agencyname_YYYY-MM-DD.txt"
    check_if_file_exists(file_path: str) -> bool:
            Checks if a given file name exists

"""

logger = get_logger(__name__)


def save_json_to_txt(report_name: str, agency_name: str, date: str, json_data):
    """
    Saves data in JSON format to a txt file
    :param report_name: report name the user was searching for
    :param agency_name: agency name the user was searching for
    :param date: date the user was searching for
    :param json_data: data to write to the txt file
    :return: returns the name of the file the data has been saved to
    """
    file_name = build_file_name(report_name, agency_name, date)
    if not check_if_file_exists(file_name):
        try:
            logger.info(f"Attempting to write data to a new file: {file_name}")
            with open(file_name, 'w', newline='') as file:
                for line in json_data:
                    file.write(f"{line}\n")
            logger.info(f"It seems data has been successfully written to database/{file_name}")
            return file_name
        except Exception as e:
            logger.error(f"Ran into some exception: {e}")
            raise DalException
    else:
        logger.error(f"{file_name} somehow already exists!")
        raise DalException


def read_from_txt(file_name) -> list:
    """
    Reads data from a txt file
    :param file_name: name of file to read from
    :return: list of data (1 list item = 1 line of data)
    """
    if check_if_file_exists(file_name):
        try:
            data_list = []
            logger.info(f"Reading data from {file_name}")
            with open(file_name, 'r') as file:
                for line in file:
                    if line != '':  # pycharm likes to add a blank line at the end of files...
                        data_list.append(line.rstrip('\n'))
            logger.info(f'successfully read data from {file_name}')
            return data_list
        except Exception as e:
            logger.error(f"Ran into some exception: {e}")
            raise DalException
    else:
        logger.error(f"{file_name} somehow does not exist!")
        raise DalException


def build_file_name(report_name: str, agency_name: str, date: str):
    """
    Builds file name in format: "database/reportname_agencyname_YYYY-MM-DD.txt"
    :param report_name: the report name the user is searching for
    :param agency_name: the agency name the user is searching for
    :param date: the date the user is searching for
    :return: the built file name (as a string)
    """
    return f"database/{report_name}_{agency_name}_{date}.txt"


def check_if_file_exists(file_path: str) -> bool:
    """
    Checks if a given file name exists
    :param file_path: path where the file *should* exist
    :return: false if the file does not exist, true if it does
    """
    if not os.path.exists(file_path):
        return False
    else:
        return True