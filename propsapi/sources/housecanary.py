import json

def get_sewer(address):
    if address.find('error') > -1:
        return None, 'error in source'
    else:
        details = get_details(address)
        return details['sewer'], None

def get_details(address):
    path = './propsapi/sources/'
    if address.find('null') > -1:
        with open(path + 'null.json','r') as json_file:
            response = json.load(json_file)
    elif address.find('unknown') > -1:
        with open(path + 'unknown.json', 'r') as json_file:
            response = json.load(json_file)
    elif address.find('septic') > -1:
        with open(path + 'septic.json', 'r') as json_file:
            response = json.load(json_file)
    else:
        with open(path + 'noseptic.json', 'r') as json_file:
            response = json.load(json_file)
    return response['property/details']['result']['property']
