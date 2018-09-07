import requests
import json


def request_post(auth, payload={}, other_field_data={},url='http://127.0.0.1:8080'):
    """
    Makes a post request to aristotle using the given payload.
    The other_field_data will be appened inside the 'fields' data in payload.
    """
    headers = {
        'Authorization': 'Token  '+auth,
        'Content-Type': 'application/json'
        }
    for key, value in other_field_data.items():
        payload["fields"][key] = value
    response = requests.post(
        url+'/api/v3_1/metadata/',
        data=json.dumps(payload),
        headers=headers
        )
    # print(response.json())
    # print('Your UUID is {0}'.format(response.json()['created'][0]['uuid']))
    return response.json()['created'][0]['uuid']


def request_get(auth, payload={}, uuid = '',url='http://127.0.0.1:8080'):
    """
    Makes a get request to aristotle and fetched the requested data.
    """
    headers = {'Authorization':'Token  '+auth}
    response = requests.get(
        url+'/api/v3/metadata/'+uuid,
        params=(payload),
        headers=headers
        )
    return response


def create_req(model="dataelement", name="Test1", app="aristotle_mdr", other_field_data={}, slots_data=[]):
    """
    Returns a payload for API according to the provided arguments
    """
    payload = {
        "concept_type": {
            "app": app,
            "model": model
        },
        "fields": {
            "name": name,
            "definition": "Placeholder"
        },
        "slots": slots_data
    }
    for key, value in other_field_data.items():
        payload["fields"][key] = value
    return payload


def save_req_file(data, file_name):
    """
    Saves the data in the provided fileName.
    """
    with open(file_name, 'w') as outfile:
        outfile.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))

def read_file(file_name):
    data = []
    with open(file_name, 'r') as fd:
        data = json.load(fd)
    return data

def get_miner_class(command):
    from importlib import import_module
    module = import_module("demo_meta_miner.commands.%s" % command.lower())
    klass = getattr(module, command.lower())
    return klass
