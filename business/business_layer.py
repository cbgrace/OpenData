from abc import ABC, abstractmethod
import dal
from datetime import datetime
import db_service
import presentation_layer
from exceptions import DalException, BusinessLogicException
from logging_config import get_logger

"""
This module contains classes and methods to act as an intermediary between the data access layer and the 
presentation layer. 

Methods:
--------
    check_current_files(report_name: str, agency_name: str, date: str):
        Searches for a report in the search_log.db
    evaluate_file_name(bundle: dict):
        Creates either a NewDataFactory or a ExistingDataFactory class, based on weather there is a file name in 
        bundle['file_name'], or if it is set to false.
    bundle_to_dict(report_name: str, agency_name: str, date: str, file_name) -> dict:
        Creates a dict with report_name, agency_name, date and file_name inside
    build_date_params(date: str) -> dict:
        Builds date params for the API query, using today as the 'before' param and the date the user is searching for as 
        the 'after'
    use_factory(factory, bundle: dict):
        Calls the get_data method for the given factory type (either NewData or ExistingData) 
    
Classes:
--------
    DataFactory(ABC):
        Abstract class representing a data factory
    NewDataFactory(DataFactory):
        Class to instantiate a NewData class
    ExistingDataFactory(DataFactory):
        Class to instantiate a ExistingData class
    Data(ABC):
        Abstract class representing data
    NewData(Data):
        Class to hold methods that execute when the user is searching for data that is not already in our database
    ExistingData(Data):
        Class that holds methods that execute when the user is searching for data that is already in our database
            
"""

logger = get_logger(__name__)


def check_current_files(report_name: str, agency_name: str, date: str):
    """
    Searches for a report in the search_log.db
    :param report_name: report name to search for
    :param agency_name: agency name to search for
    :param date: date to search for
    :return: returns False if no match, returns file name of previous search if match is found.
    """
    try:
        file_name = db_service.search_for_match(report_name, agency_name, date)
        bundle = bundle_to_dict(report_name, agency_name, date, file_name)
        return evaluate_file_name(bundle)
    except DalException:
        logger.error("Encountered error, raising exception...")
        raise BusinessLogicException


def evaluate_file_name(bundle: dict):
    """
    Creates either a NewDataFactory or a ExistingDataFactory class, based on weather there is a file name in
        bundle['file_name'], or if it is set to false.
    :param bundle: a dict containing report_name, agency_name, date & file_name
    :return: calls use_factory
    """
    if not bundle['file_name']:  # no file exists
        presentation_layer.on_new_data()
        new_data = NewDataFactory()
        return use_factory(new_data, bundle)
    else:  # data has already been retrieved from api
        existing_data = ExistingDataFactory()
        return use_factory(existing_data, bundle)


def bundle_to_dict(report_name: str, agency_name: str, date: str, file_name) -> dict:
    """
    Creates a dict with report_name, agency_name, date and file_name inside
    :param report_name: the report name the user is searching for
    :param agency_name: the agency name the user is searching for
    :param date: the date the user is searching for
    :param file_name: the file name (either false if there is no file or the file name if data already exists)
    :return: the dict that has been created out of the above params.
    """
    return {'report_name': report_name,
            'agency_name': agency_name,
            'date': date,
            'file_name': file_name}


def build_date_params(date: str) -> dict:
    """
    Builds date params for the API query, using today as the 'before' param and the date the user is searching for as
        the 'after'
    :param date: the date the user is searching for
    :return: the params dict
    """
    today = datetime.today().date()
    params = {'before': f"{today}", 'after': f"{date}"}
    return params


def use_factory(factory, bundle: dict):
    """
    Calls the get_data method for the given factory type (either NewData or ExistingData)
    :param factory: the factory class that needs to be instantiated
    :param bundle: the bundle of search params from the command line
    :return: calls get_data method
    """
    data = factory.set_data_type()
    return data.get_data(bundle)


# Factory Classes
class DataFactory(ABC):
    @abstractmethod
    def set_data_type(self):
        pass


class NewDataFactory(DataFactory):
    def set_data_type(self):
        """
        Instantiates NewData()
        :return: NewData()
        """
        return NewData()


class ExistingDataFactory(DataFactory):
    def set_data_type(self):
        """
        Instantiates ExistingData()
        :return: ExistingData()
        """
        return ExistingData()


class Data(ABC):
    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass


class NewData(Data):
    def get_data(self, bundle: dict):
        """
        Retrieves API response from the dal, calls log_data_to_db, passes response to parse_response
        :param bundle: dict of search parameters from the command line
        :return: calls self.parse_response
        """
        try:
            params = build_date_params(bundle['date'])
            response = dal.make_request(bundle['report_name'], bundle['agency_name'], params=params)
            self.log_data_to_db(bundle)
            return self.parse_response(bundle, response.json())
        except DalException:
            logger.error("Ran into exception (already logged)")
            raise BusinessLogicException

    def log_data_to_db(self, bundle: dict):
        """
        Upon new data being received from the API, logs the search parameters and file name to search_log.db
        :param bundle: dict of search params from the user
        :return: n/a
        """
        try:
            return db_service.insert_search_data(bundle['report_name'], bundle['agency_name'], bundle['date'])
        except DalException:
            logger.error("Ran into exception (already logged)")
            raise BusinessLogicException

    def parse_response(self, bundle: dict, response):
        """
        Parses the response to only include items in which the user's searched for date matches the item's date. Also
            calls a method from the dal to write this data to a txt file.
        :param bundle: dict of search params from the user
        :param response: response from the API to write to txt file
        :return: calls self.return_response
        """
        try:
            parsed_response = []
            for line in response:
                if line['date'] == bundle['date']:
                    parsed_response.append(line)
            file_name = dal.save_json_to_txt(bundle['report_name'], bundle['agency_name'], bundle['date'],
                                             parsed_response)
            return self.return_response(file_name)
        except DalException:
            logger.error("Ran into exception (already logged)")
            raise BusinessLogicException

    def return_response(self, file_name):
        """
        Reads the data we have just loaded from its newly created txt file to the console.
        :param file_name: name of txt file to read from
        :return: n/a
        """
        try:
            data_list = dal.read_from_txt(file_name)
            return presentation_layer.on_new_data(file_name, data_list)
        except DalException as dal_err:
            logger.error("Ran into exception (already logged)")
            presentation_layer.on_error(f"{dal_err}")
            raise BusinessLogicException


class ExistingData(Data):
    def get_data(self, bundle: dict):
        """
        Reads data from txt file to the console.
        :param bundle: dict of search parameters from the
        :return: n/a
        """
        try:
            data_list = dal.read_from_txt(bundle['file_name'])
            return presentation_layer.on_old_data(bundle['file_name'], data_list)
        except DalException as dal_err:
            logger.error("Ran into exception (already logged)")
            presentation_layer.on_error(f"{dal_err}")
            raise BusinessLogicException
