import requests
from config import API_KEY
from exceptions import DalException
from logging_config import get_logger
from abc import ABC, abstractmethod


"""
This module contains classes and methods to query an API and either retrieve the response or handle any errors that 
may occur. 

Methods:
--------
    make_request(report_name: str, agency_name: str, params=None):
            Instantiates the Factory & Adapter, returns the result of the API request or handles errors

Classes:
---------
    ConnectionFactory(ABC):
        Abstract class that models a connection factory
    RestAPIConnectionFactory(ConnectionFactory):
        Instantiates the RestAPIConnection class
    RestAPIConnection:
        Holds base url for our api connection
    APIAdapter(ABC):
        Abstract class that models an API adapter
    OpenDataAPIAdapter(APIAdapter):
    

Constants:
-----------
    GOOD_RESPONSE_CODE: the response code we want from the api (200)
    
"""
logger = get_logger(__name__)
GOOD_RESPONSE_CODE = 200


# Factory classes
class ConnectionFactory(ABC):
    @abstractmethod
    def create_connection(self, *args, **kwargs):
        pass


class RestAPIConnectionFactory(ConnectionFactory):
    def create_connection(self, base_url: str):
        """
        Instantiates the RestAPIConnection class
        :param base_url: base url for the API query
        :return: an instance of the RestAPIConnection class.
        """
        return RestAPIConnection(base_url)


class RestAPIConnection:
    def __init__(self, base_url: str):
        self.base_url = base_url


# Adapter Classes
class APIAdapter(ABC):
    def __init__(self, connection: RestAPIConnection):
        self.connection = connection

    @abstractmethod
    def send_request(self, *args, **kwargs):
        pass


class OpenDataAPIAdapter(APIAdapter):
    BASE_URL = "https://api.gsa.gov/analytics/dap/v1.1"
    AGENCIES_ENDPOINT = "/agencies/1/reports/2/data"  # /agencies/<agency name>/reports/<report name>/data

    def fix_endpoint(self, report_name: str, agency_name: str) -> str:
        """
        Replaces the number '1' and '2' in AGENCIES_ENDPOINT with the user's search parameters
        :param report_name: the report name to search for
        :param agency_name: the agency name to search for
        :return: complete endpoint
        """
        endpoint = self.AGENCIES_ENDPOINT.replace('1', agency_name)
        return endpoint.replace('2', report_name)

    def send_request(self, url: str, headers: dict, params=None):
        """
        Performs the API request
        :param url: base url + endpoint
        :param headers: dict containing the api key
        :param params: dict containing search params
        :return: results for the api request
        """
        return requests.get(url, headers=headers, params=params)

    def get_data(self, report_name: str, agency_name: str, header: dict, params=None):
        """
        Builds the API query and calls self.send_request() to perform the get request.
        :param report_name: report name the user is searching for
        :param agency_name: agency name the user is searching for
        :param header: header containing API key
        :param params: params for the API query
        :return: calls send_request
        """
        url = f"{self.connection.base_url}{self.fix_endpoint(report_name, agency_name)}"
        return self.send_request(url, headers=header, params=params)


def make_request(report_name: str, agency_name: str, params=None):
    """
    Instantiates the Factory & Adapter, returns the result of the API request or handles errors
    :param report_name: report name the user is searching for
    :param agency_name: agency name the user is searching for
    :param params: dict of search parameters.
    :return: response from api
    """
    factory = RestAPIConnectionFactory()
    connection = factory.create_connection(OpenDataAPIAdapter.BASE_URL)
    adapter = OpenDataAPIAdapter(connection)
    headers = {'x-api-key': API_KEY}
    try:
        response = adapter.get_data(report_name, agency_name, headers, params)
        if response.status_code == GOOD_RESPONSE_CODE:
            return response
        else:
            logger.error("Bad response code from API")
            raise DalException
    except requests.Timeout as time_out:
        logger.error(f"Request timed out: {time_out}")
        raise DalException
    except requests.ConnectionError as connection_error:
        logger.error(f"Connection failed: {connection_error}")
        raise DalException
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise DalException

