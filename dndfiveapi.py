import requests

base_url = "https://www.dnd5eapi.co/api"
headers = {
  'Accept': 'application/json'
}

# default request
def get_request(endpoint, params = {}, payload = {}):
    url = base_url + endpoint

    response = requests.request("GET", url, headers=headers)

    return unwrap(response.json())

def unwrap(data):
    if not 'results' in data:
        return {}

    return data['results']