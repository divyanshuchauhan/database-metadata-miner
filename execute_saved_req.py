import json
from req import *

def execute_migration():
    # print(self.all_requests)
    req_data = []
    dataset = ''
    extra_information_distribution = {"data_elements": [], "dataset": dataset}
    extra_information_dataelement = {"valueDomain": ""}
    with open('data.json', 'r') as fd:
        req_data = json.load(fd)
        print(req_data[0]['concept_type']['model'])
    for payload in req_data:
        if payload['concept_type']['model'] == 'dataset':
            extra_information_distribution['dataset'] = request_post(payload=payload)
        if payload['concept_type']['model'] == 'valuedomain':
            valueDomain = request_get(model="valuedomain",name= payload['fields']['name'],app="aristotle_mdr")
            if not valueDomain:
                valueDomain = request_post(payload=payload)
            extra_information_dataelement = {"valueDomain": valueDomain}
        if payload['concept_type']['model'] == 'dataelement':
            data_element = request_post(payload=payload,other_field_data=extra_information_dataelement)
            extra_information_distribution['data_elements'].append({'data_element' : data_element, "logical_path": "."+payload['fields']['name']})
        if payload['concept_type']['model'] == 'distribution':
            for data_element in extra_information_distribution['data_elements']:
                data_element['logical_path'] = payload['fields']['name']+data_element['logical_path']
            request_post(payload=payload,other_field_data=extra_information_distribution)
            extra_information_distribution['data_elements']=[]

if __name__ == '__main__':
    execute_migration()