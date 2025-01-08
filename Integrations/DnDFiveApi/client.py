import requests
from . import utils

base_url = "https://www.dnd5eapi.co/api"
headers = {
  'Accept': 'application/json'
}

# default request
def get_request(endpoint):
    url = base_url + endpoint

    response = requests.request("GET", url, headers=headers)

    return utils.unwrap(response.json())