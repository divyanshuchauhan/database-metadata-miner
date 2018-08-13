from sqlalchemy import create_engine
import click
import yaml
import json
import pprint
import req

@click.command()
@click.option('--url', default='sqlite:///Test2.db', help='Full Database URl')
# @click.option('--name', prompt='Your name',
            #   help='The person to greet.')

def demo(url):
    # print(count)
    # print(name)
    # engine = create_engine('sqlite:///Test2.db', echo=True)
    engine = create_engine(url)
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
    metadata = MetaData()

    conn = engine.connect()

    metadata.reflect(engine)
    # print(metadata)

    table_data = {}
    dataset = req.request_post(model="dataset",name= "testDatabase",app="aristotle_dse")
    # import pdb; pdb.set_trace()
    for table in metadata.tables.keys():
        # print('---table---')
        # print(table)
        
        table_data[table] = []
        extra_information_dataset = {"data_elements": [], "dataset": dataset}
        for columns in metadata.tables[table].c:

            valueDomain = req.request_get(model="valuedomain",name= columns.type.__repr__(),app="aristotle_mdr")
            if not valueDomain:
                valueDomain = req.request_post(model="valuedomain",name= columns.type.__repr__(),app="aristotle_mdr")
            extra_information_dataelement = {"valueDomain": valueDomain}
            dataElement = req.request_post(model="dataelement",name= columns.name.__repr__(),app="aristotle_mdr", other_field_data=extra_information_dataelement)
            extra_information_dataset["data_elements"].append({"data_element": dataElement, "logical_path": table+"."+columns.name})
            table_data[table].append({columns.name.__repr__() :{'type' : columns.type.__repr__(), 'nullable' : columns.nullable.__repr__(), 'primary_key' : columns.primary_key.__repr__(),'foreign_keys' : columns.foreign_keys.__repr__()}})
        distribution = req.request_post(model="distribution",name= table,app="aristotle_dse", other_field_data=extra_information_dataset)
        print(distribution)
    # import yaml
    # pp = pprint.PrettyPrinter(depth=6)
    # pp.pprint(table_data)
    # print(yaml.dump(table_data,default_flow_style=False))


if __name__ == '__main__':
    demo()