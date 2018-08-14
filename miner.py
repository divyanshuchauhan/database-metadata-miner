from sqlalchemy import create_engine
import click
import yaml
import json
import pprint
import req
from save_req import save_req

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
    save_req_object.create_req(model="dataset",name= "testDatabase",app="aristotle_dse")
    # import pdb; pdb.set_trace()
    for table in metadata.tables.keys():
        
        table_data[table] = []
        for columns in metadata.tables[table].c:
            save_req_object.create_req(model="valuedomain",name= columns.type.__repr__(),app="aristotle_mdr")

            save_req_object.create_req(model="dataelement",name= columns.name.__repr__(),app="aristotle_mdr")
        save_req_object.create_req(model="distribution",name= table,app="aristotle_dse")
    save_req_object.save_req_file()
    conn.close()

if __name__ == '__main__':
    demo()