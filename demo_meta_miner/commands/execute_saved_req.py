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
    req_data = []
    with open(file, 'r') as fd:
        req_data = json.load(fd)
    dataset = {}
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
            import ast
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
    # import pdb; pdb.set_trace()
    for distribution in req_data:
        if distribution['fields']['name'] in dataset:
            distribution['fields']['uuid'] = dataset[distribution['fields']['name']]['uuid']

        for i, data_element in enumerate(distribution['fields']['data_elements']):
            if distribution['fields']['name'] in dataset and data_element['logical_path'] in dataset[distribution['fields']['name']]['tables']:
                distribution['fields']['data_elements'][i]['data_element'] = dataset[distribution['fields']['name']]['tables'][data_element['logical_path']]
            else:
                valueDomainResponse = utils.request_get(
                    auth=auth,
                    payload = {
                        'name__icontains': data_element['data_element']['fields']['valueDomain']['fields']['name'],
                        'type': 'aristotle_mdr:valuedomain'
                    })
                if valueDomainResponse.json()['count'] > 0:
                    valueDomain = valueDomainResponse.json()['results'][0]['uuid']
                else:
                    valueDomain = False
                
                if not valueDomain:
                    valueDomain = utils.request_post(
                        auth=auth,
                        payload=data_element['data_element']['fields']['valueDomain']
                        )
                data_element['data_element']['fields']['valueDomain'] = valueDomain
                distribution['fields']['data_elements'][i]['data_element'] = utils.request_post(
                    auth=auth,
                    payload=data_element['data_element']
                    )
        utils.request_post(
            auth=auth,
            payload=distribution
            )


if __name__ == '__main__':
    execute_saved_req()
