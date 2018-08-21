import requests
import json


def request_post(auth, payload={}, other_field_data={}):
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
        'http://localhost:8080/api/v3/metadata/',
        data=json.dumps(payload),
        headers=headers
        )
    print(response.json())
    print('Your UUID is {0}'.format(response.json()['created'][0]['uuid']))
    return response.json()['created'][0]['uuid']


def request_get(auth, model="valuedomain", name="Test1", app="aristotle_mdr"):
    """
    Makes a get request to aristotle and fetched the requested data.
    """
    headers = {'Authorization':'Token  '+auth}
    payload = {
        'name__icontains': name,
        'type': '{}:{}'.format(app, model)
        }
    response = requests.get(
        'http://localhost:8080/api/v3/metadata/',
        params=(payload),
        headers=headers
        )
    if response.json()['count'] > 0:
        return response.json()['results'][0]['uuid']
    else:
        False


def create_req(model="dataelement", name="Test1", app="aristotle_mdr", other_field_data={}):
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
        }
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
