from abc import ABC, abstractmethod
import dal
from datetime import datetime
import db_service
import presentation_layer
from exceptions import DalException, BusinessLogicException
from logging_config import get_logger

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
    if bundle['file_name'] == False:  # no file exists
        presentation_layer.on_new_data()
        new_data = NewDataFactory()
        return use_factory(new_data, bundle)
    else:  # data has already been retrieved from api
        existing_data = ExistingDataFactory()
        return use_factory(existing_data, bundle)


def bundle_to_dict(report_name: str, agency_name: str, date: str, file_name) -> dict:
    return {'report_name': report_name,
            'agency_name': agency_name,
            'date': date,
            'file_name': file_name}


def build_date_params(date: str) -> dict:
    today = datetime.today().date()
    params = {'before': f"{today}", 'after': f"{date}"}
    return params


def use_factory(factory, bundle: dict):
    data = factory.set_data_type()
    return data.get_data(bundle)


# Factory Classes
class DataFactory(ABC):
    @abstractmethod
    def set_data_type(self):
        pass


class NewDataFactory(DataFactory):
    def set_data_type(self):
        return NewData()


class ExistingDataFactory(DataFactory):
    def set_data_type(self):
        return ExistingData()


class Data(ABC):
    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass


class NewData(Data):
    def get_data(self, bundle: dict):
        try:
            params = build_date_params(bundle['date'])
            response = dal.make_request(bundle['report_name'], bundle['agency_name'], params=params)
            self.log_data_to_db(bundle)
            return self.parse_response(bundle, response.json())
        except DalException:
            logger.error("Ran into exception (already logged)")
            raise BusinessLogicException

    def log_data_to_db(self, bundle: dict):
        try:
            return db_service.insert_search_data(bundle['report_name'], bundle['agency_name'], bundle['date'])
        except DalException:
            logger.error("Ran into exception (already logged)")
            raise BusinessLogicException

    def parse_response(self, bundle: dict, response):
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
        try:
            data_list = dal.read_from_txt(file_name)
            return presentation_layer.on_new_data(file_name, data_list)
        except DalException as dal_err:
            logger.error("Ran into exception (already logged)")
            presentation_layer.on_error(f"{dal_err}")
            raise BusinessLogicException


class ExistingData(Data):
    def get_data(self, bundle: dict):
        try:
            data_list = dal.read_from_txt(bundle['file_name'])
            return presentation_layer.on_old_data(bundle['file_name'], data_list)
        except DalException as dal_err:
            logger.error("Ran into exception (already logged)")
            presentation_layer.on_error(f"{dal_err}")
            raise BusinessLogicException
