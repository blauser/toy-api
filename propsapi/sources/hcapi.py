import json
import housecanary
import requests_mock


def get_sewer(address):
    details, error = get_details(address)
    if not error:
        return details['sewer'], None
    else:
        return None, error


def get_details(address):
    if address.find('error') > -1:
        return None, 'error in source'
    response = get_response(address)
    if response['property/details']['api_code'] == 0:
        return response['property/details']['result']['property'], None
    else:
        return None, response['property/details']['api_code_description']


@requests_mock.Mocker()
def get_response(address, mock):
    mock_details(mock, address)
    client = housecanary.ApiClient()
    response = client.property.details(address)
    return response.json()


def mock_details(mock, address):
    endpoint = '/v2/property/details'
    headers = {'content-type': 'application/json'}
    response = mock_response(address)
    mock.register_uri("GET", endpoint, headers=headers, json=response)


def mock_response(address):
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


def get_response_json(case):
    path_prefix = './propsapi/sources/'
    path = path_prefix + case + '.json'
    with open(path, 'r') as json_file:
        return json.load(json_file)
