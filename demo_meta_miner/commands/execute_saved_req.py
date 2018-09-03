import json
import demo_meta_miner.utils as utils
import click
from demo_meta_miner.AristotleDbTools import AristotleDbTools


@click.command()
@click.option(
    '--auth',
    default='6da4e3f4d662972428d369a11a5bdf153e202d51',
    help='Authentication token'
    )
@click.option(
    '--file',
    default='data.json',
    help='Spicify the json file name'
    )
@click.option(
    '--dbuuid',
    default='',
    help='Optional database uuid if the upload is incremental'
    )
def execute_saved_req(auth, file, dbuuid):
    """This script consumes the json file to upload the metadata to Aristotle"""
    req_data = utils.read_file(file)
    existing_dataset = {}
    if dbuuid:
        datasetResponse = utils.request_get(
            auth=auth,
            payload = {
            'type': 'aristotle_dse:distribution',
            'dq':'dataset__uuid:'+dbuuid
            })
        if datasetResponse.status_code != 200:
            print("uuid not valid")
            return "uuid not valid"
        else:
            existing_dataset = create_dataset_structure(datasetResponse,auth)
    # import pdb; pdb.set_trace()
    for distribution in req_data:
        distribution_name = distribution['fields']['name']
        if distribution_name in existing_dataset:
            # This updates the distribution
            distribution['fields']['uuid'] = existing_dataset[distribution_name]['uuid']
        data_elements = distribution['fields']['data_elements']
        for i, data_element_payload in enumerate(data_elements):
            data_elements[i]['data_element'] = get_data_element(existing_dataset,data_element_payload,distribution_name,auth)
        utils.request_post(
            auth=auth,
            payload=distribution
            )

def get_data_element(existing_dataset,data_element_payload,distribution_name,auth):
    """ Get the data element id. Either from existing dataset or by creating new"""
    logical_path = data_element_payload['logical_path']
    if (distribution_name in existing_dataset and 
        logical_path in existing_dataset[distribution_name]['tables']):
        data_element_id = existing_dataset[distribution_name]['tables'][logical_path]
    else:
        value_domain_payload = data_element_payload['data_element']['fields']['valueDomain']
        value_domain_id = get_value_domain(value_domain_payload,auth)
        data_element_payload['data_element']['fields']['valueDomain'] = value_domain_id
        data_element_id = utils.request_post(
            auth=auth,
            payload=data_element_payload['data_element']
            )
    return data_element_id

def get_value_domain(value_domain_payload,auth):
    """ Get the value domain id. Either from existing value domain or by creating new"""
    valueDomainResponse = utils.request_get(
        auth=auth,
        payload = {
            'name__icontains': value_domain_payload['fields']['name'],
            'type': 'aristotle_mdr:valuedomain'
        })
    if valueDomainResponse.json()['count'] > 0:
        value_domain_id = valueDomainResponse.json()['results'][0]['uuid']
    else:
        value_domain_id = False
    
    if not value_domain_id:
        value_domain_id = utils.request_post(
            auth=auth,
            payload=value_domain_payload
            )
    return value_domain_id

def create_dataset_structure(datasetResponse,auth):
    import ast
    dataset = {}
    for dist in datasetResponse.json()["results"]:
        dist_data =  utils.request_get(
            auth=auth,
            uuid=dist['uuid']
        )
        dist_slots_name = ''
        for value in dist_data.json()['slots']:
            if value['name'] == 'distribution':
                dist_slots_name = ast.literal_eval(value['value'])[0]

        dataset[dist_slots_name] = {'uuid': dist['uuid'] ,'tables': {}}
        for data_elements in dist_data.json()['fields']['data_elements']:
            dataset[dist_slots_name]['tables'][data_elements['logical_path']] = data_elements["data_element"]
    return dataset

if __name__ == '__main__':
    execute_saved_req()
