import json
import utils as utils
import click

@click.command()
@click.option('--auth', default='910923131171f6c4ae9bd84cbb5d5d44edb14436', help='Authentication token')

def execute_migration(auth):
    """This script consumes the data.json file to upload the metadata to Aristotle"""
    req_data = []
    with open('data.json', 'r') as fd:
        req_data = json.load(fd)

    for distribution in req_data:
        for i,data_element in enumerate(distribution['fields']['data_elements']):
            valueDomain = utils.request_get(auth=auth,model="valuedomain",name= data_element['data_element']['fields']['valueDomain']['fields']['name'],app="aristotle_mdr")
            if not valueDomain:
                valueDomain = utils.request_post(auth=auth,payload=data_element['data_element']['fields']['valueDomain'])
            data_element['data_element']['fields']['valueDomain'] = valueDomain
            distribution['fields']['data_elements'][i]['data_element'] = utils.request_post(auth=auth,payload=data_element['data_element'])
        utils.request_post(auth=auth,payload=distribution)

if __name__ == '__main__':
    execute_migration()