import json
from req import *

def execute_migration():
    # print(self.all_requests)
    req_data = []
    with open('data.json', 'r') as fd:
        req_data = json.load(fd)

    for distribution in req_data:
        for i,data_element in enumerate(distribution['fields']['data_elements']):
            valueDomain = request_get(model="valuedomain",name= data_element['data_element']['fields']['valueDomain']['fields']['name'],app="aristotle_mdr")
            if not valueDomain:
                valueDomain = request_post(payload=data_element['data_element']['fields']['valueDomain'])
            data_element['data_element']['fields']['valueDomain'] = valueDomain
            distribution['fields']['data_elements'][i]['data_element'] = request_post(payload=data_element['data_element'])
        request_post(payload=distribution)
        # print(dist)


if __name__ == '__main__':
    execute_migration()