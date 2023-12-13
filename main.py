"""
import requests
from config import API_KEY


url = "https://api.gsa.gov/analytics/dap/v1.1"
endpoint_one = "/reports/<report name>/data"
endpoint_two = "/agencies/<agency name>/reports/<report name>/data"
endpoint_three = "/domain/<domain>/reports/<report name>/data"

headers = {
	'x-api-key': 'API_KEY' }

-> response = requests.get(url, headers=headers) <-

"""
