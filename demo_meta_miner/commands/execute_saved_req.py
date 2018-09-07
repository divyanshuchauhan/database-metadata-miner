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
@click.option(
    '--aristotleurl',
    default='http://127.0.0.1:8080',
    help='Specify the aristotle url'
    )
def execute_saved_req(auth, file, dbuuid, aristotleurl):
    """This script consumes the json file to upload the metadata to Aristotle"""
    json_data = utils.read_file(file)
    existing_dataset = {}
    if dbuuid:
        try:
            existing_dataset = create_dataset_structure(dbuuid,auth)
        except ValueError as err:
            print(err)
            return
    # import pdb; pdb.set_trace()
    for distribution in json_data:
        distribution_name = distribution['fields']['name']
        if distribution_name in existing_dataset:
            # This updates the distribution
            distribution['fields']['uuid'] = existing_dataset[distribution_name]['uuid']
        data_elements = distribution['fields']['data_elements']
        for i, data_element_payload in enumerate(data_elements):
            data_elements[i]['data_element'] = get_data_element(existing_dataset,data_element_payload,distribution_name,auth,aristotleurl)
        utils.request_post(
            auth=auth,
            payload=distribution,
            url=aristotleurl
            )

def get_data_element(existing_dataset, data_element_payload, distribution_name, auth, aristotleurl):
    """ Get the data element id. Either from existing dataset or by creating new"""
    logical_path = data_element_payload['logical_path']
    if (distribution_name in existing_dataset and 
        logical_path in existing_dataset[distribution_name]['tables']):
        data_element_id = existing_dataset[distribution_name]['tables'][logical_path]
    else:
        value_domain_payload = data_element_payload['data_element']['fields']['valueDomain']
        value_domain_id = get_value_domain(value_domain_payload,auth,aristotleurl)
        data_element_payload['data_element']['fields']['valueDomain'] = value_domain_id
        data_element_id = utils.request_post(
            auth=auth,
            payload=data_element_payload['data_element'],
            url=aristotleurl
            )
    return data_element_id

def get_value_domain(value_domain_payload, auth, aristotleurl):
    """ Get the value domain id. Either from existing value domain or by creating new"""
    valueDomainResponse = utils.request_get(
        auth=auth,
        payload = {
            'name__icontains': value_domain_payload['fields']['name'],
            'type': 'aristotle_mdr:valuedomain'
        },
        url=aristotleurl)
    if valueDomainResponse.json()['count'] > 0:
        value_domain_id = valueDomainResponse.json()['results'][0]['uuid']
    else:
        value_domain_id = False
    
    if not value_domain_id:
        value_domain_id = utils.request_post(
            auth=auth,
            payload=value_domain_payload,
            url=aristotleurl
            )
    return value_domain_id

def create_dataset_structure(dbuuid,auth):
    """Returns the metadata schema for the given dbuuid"""
    datasetResponse = utils.request_get(
        auth=auth,
        payload = {
        'type': 'aristotle_dse:distribution',
        'dq':'dataset__uuid:'+dbuuid
        },
        url=aristotleurl)
    if datasetResponse.status_code != 200:
        raise ValueError('Invalid uuid.')
    import ast
    dataset = {}
    for dist in datasetResponse.json()["results"]:
        dist_data =  utils.request_get(
            auth=auth,
            uuid=dist['uuid'],
            url=aristotleurl
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
