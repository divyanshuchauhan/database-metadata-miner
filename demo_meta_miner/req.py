import requests
import json

def request_post(auth,payload={},other_field_data={}):
    headers = {'Authorization':'Token  '+auth, 'Content-Type': 'application/json'}
    for key, value in other_field_data.items():
        payload["fields"][key] = value
    # print(json.dumps(payload))
    response = requests.post('http://localhost:8080/api/v3/metadata/',data=json.dumps(payload), headers=headers)
    print(response.json())
    print('Your UUID is {0}'.format(response.json()['created'][0]['uuid']))
    return response.json()['created'][0]['uuid']

def request_get(auth,model="valuedomain",name="Test1",app="aristotle_mdr"):
    headers = {'Authorization':'Token  '+auth}
    payload = {
        'name__icontains' : name,
        'type' : app+':'+model }
    response = requests.get('http://localhost:8080/api/v3/metadata/',params=(payload), headers=headers)
    # print(response.json())
    if response.json()['count'] > 0:
        return response.json()['results'][0]['uuid']
    else:
        False

if __name__ == '__main__':
    request_post()