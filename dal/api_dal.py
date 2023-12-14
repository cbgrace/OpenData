import requests
from config import API_KEY
from exceptions import DalException
from logging_config import get_logger
from abc import ABC, abstractmethod


"""


Methods:
--------


Constants:
-----------

    
"""
logger = get_logger(__name__)


# Factory classes
class ConnectionFactory(ABC):
    @abstractmethod
    def create_connection(self, *args, **kwargs):
        pass


class RestAPIConnectionFactory(ConnectionFactory):
    def create_connection(self, base_url: str):
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
        endpoint = self.AGENCIES_ENDPOINT.replace('1', agency_name)
        return endpoint.replace('2', report_name)

    def send_request(self, url: str, headers: dict, params=None):
        return requests.get(url, headers=headers, params=params)

    def get_data(self, report_name: str, agency_name: str, header: dict, params=None):
        url = f"{self.connection.base_url}{self.fix_endpoint(report_name, agency_name)}"
        return self.send_request(url, headers=header, params=params)


def make_request(report_name: str, agency_name: str, params=None):
    try:
        factory = RestAPIConnectionFactory()
        connection = factory.create_connection(OpenDataAPIAdapter.BASE_URL)
        adapter = OpenDataAPIAdapter(connection)
        headers = {'x-api-key': API_KEY}
        response = adapter.get_data(report_name, agency_name, headers, params)
        return response
    except Exception as e:
        logger.error(f"Ran into an error trying to make API request: {e}")
        raise DalException

