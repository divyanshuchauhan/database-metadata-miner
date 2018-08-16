from sqlalchemy import create_engine
import click
import yaml
import json
import pprint
import demo_meta_miner.req as req
from demo_meta_miner.save_req import save_req

@click.command()
@click.option('--url', default='sqlite:///Test2.db', help='Full Database URl')

def demo(url):
    engine = create_engine(url)
    # from sqlalchemy.ext.automap import automap_base
    # from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
    from sqlalchemy import MetaData
    metadata = MetaData()

    conn = engine.connect()

    metadata.reflect(engine)
    # print(metadata.tables)
    save_req_object = save_req()
    table_data = {}
    distributions = []
    dataset = save_req_object.create_req(model="dataset",name= "testDatabase",app="aristotle_dse")
    dataset = req.request_post(payload=dataset)
    # import pdb; pdb.set_trace()
    for table in metadata.tables.keys():
        extra_information_distribution = {"data_elements": [], "dataset": dataset}
        table_data[table] = []
        for columns in metadata.tables[table].c:
            value_domain = save_req_object.create_req(model="valuedomain",name= columns.type.__repr__(),app="aristotle_mdr")
            extra_information_dataelement = {"valueDomain": value_domain}
            data_element = save_req_object.create_req(model="dataelement",name= columns.name.__repr__(),app="aristotle_mdr", other_field_data=extra_information_dataelement)
            extra_information_distribution['data_elements'].append({'data_element' : data_element, "logical_path": table+"."+columns.name.__repr__()})
        distribution = save_req_object.create_req(model="distribution",name= table,app="aristotle_dse",other_field_data=extra_information_distribution)
        distributions.append(distribution)
    save_req_object.save_req_file(distributions)
    conn.close()

if __name__ == '__main__':
    demo()