from exceptions import DalException
from logging_config import get_logger
import os


logger = get_logger(__name__)


def save_json_to_txt(report_name: str, agency_name: str, date: str, json_data):
    file_name = build_file_name(report_name, agency_name, date)
    if not check_if_file_exists(file_name):
        try:
            logger.info(f"Attempting to write data to a new file: {file_name}")
            with open(file_name, 'w', newline='') as file:
                for line in json_data:
                    file.write(f"{line}\n")
            logger.info(f"It seems data has been successfully written to database/{file_name}")
        except Exception as e:
            logger.error(f"Ran into some exception: {e}")
            raise DalException
    else:
        logger.error(f"{file_name} somehow already exists!")
        raise DalException


def read_from_txt(report_name: str, agency_name: str, date: str):
    file_name = build_file_name(report_name, agency_name, date)
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
    return f"database/{report_name}_{agency_name}_{date}.txt"


def check_if_file_exists(file_path: str) -> bool:
    if not os.path.exists(file_path):
        return False
    else:
        return True