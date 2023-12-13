import requests
from config import API_KEY, DATABASE_PATH
from exceptions import DalException

"""


Methods:
--------


Constants:
-----------
    URL: holds the 'base' url for the api
    REPORTS_ENDPOINT: 
    AGENCIES_ENDPOINT: 
    DOMAIN_ENDPOINT: 
    
"""

URL = "https://api.gsa.gov/analytics/dap/v1.1"
REPORTS_ENDPOINT = "/reports/1/data"  # /reports/<report name>/data
AGENCIES_ENDPOINT = "/agencies/1/reports/2/data"  # /agencies/<agency name>/reports/<report name>/data
DOMAIN_ENDPOINT = "/domain/1/reports/2/data"  # /domain/<domain>/reports/<report name>/data

