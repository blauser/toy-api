"""
Use the official HouseCanary API python client, but mock the requests for property details since
we do not have access the live API
"""
import json
from typing import Optional, Tuple
import housecanary
import requests_mock


def get_sewer(address: str) -> Tuple[Optional[str], Optional[str]]:
    """Gets the sewer type from the details provided by the HouseCanary API."""
    details, error = get_details(address)
    if not error:
        return details['sewer'], None
    else:
        return None, error


def get_details(address: str) -> Tuple[Optional[dict], Optional[str]]:
    """Gets the details for a property from the HouseCanary API."""
    if address.find('error') > -1:
        return None, 'error in source'
    response = get_response(address)
    if response['property/details']['api_code'] == 0:
        return response['property/details']['result']['property'], None
    else:
        return None, response['property/details']['api_code_description']


@requests_mock.Mocker()
def get_response(address: str, mock: requests_mock.Mocker) -> dict:
    """Gets the (mocked) response for a property from the HouseCanary API."""
    mock_details(mock, address)
    client = housecanary.ApiClient()
    response = client.property.details(address)
    return response.json()


def mock_details(mock: requests_mock.Mocker, address: str) -> None:
    """Creates mock response for /v2/property/details endpoint."""
    endpoint = '/v2/property/details'
    headers = {'content-type': 'application/json'}
    response = mock_response(address)
    mock.register_uri("GET", endpoint, headers=headers, json=response)


def mock_response(address: str) -> dict:
    """Loads json file corresponding to address type."""
    if address.find('null') > -1:
        return get_response_json('null')
    elif address.find('unknown') > -1:
        return get_response_json('unknown')
    elif address.find('septic') > -1:
        return get_response_json('septic')
    elif address.find('noinfo') > -1:
        return get_response_json('noinfo')
    else:
        return get_response_json('noseptic')


def get_response_json(case: str) -> dict:
    """Loads json file for the given case."""
    path_prefix = './propsapi/sources/'
    path = path_prefix + case + '.json'
    with open(path, 'r') as json_file:
        return json.load(json_file)
