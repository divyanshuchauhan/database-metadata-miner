from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.schema import CreateTable
from demo_meta_miner.PlaceholderType import PlaceholderType
from sqlalchemy.types import Date, Integer
import re
from sqlalchemy.dialects import *
import click
import requests


@click.command()
@click.option(
    '--dssuuid',
    default='6888c5aa-158c-11e7-803e-0242ac110017',
    help='Dataset Specification Set uuid'
    )
@click.option(
    '--dbtype',
    default='sqlite',
    help='Dataset Specification Set uuid'
    )
@click.option(
    '--aristotleurl',
    default='http://127.0.0.1:8080',
    help='Specify the aristotle url'
    )
def create_database(dssuuid, dbtype, aristotleurl):
    db_uri = 'sqlite:///Test2.db'
    engine = create_engine(db_uri)
    meta = MetaData(engine)

    grapgqlurl = aristotleurl+'/api/graphql/api'
    query = 'query {datasetSpecifications (uuid: "' + dssuuid + \
        '") {edges {node {name,dssclusterinclusionSet {dss {name}}' \
        ',dssdeinclusionSet {dataElement {name,valueDomain' \
        ' {dataType {name}}}}}}}}'
    payload = {
                'raw': 'True',
                'query': query
            }
    response = requests.get(
        grapgqlurl,
        params=(payload)
        )
    if response.status_code != 200:
        print(
            "Given {} aristotleurl does not contain {} dssuuid"
            .format(aristotleurl, dssuuid))
        return
    data_json = response.json()
    column_definitions = []
    column_names = []
    dss = data_json['data']['datasetSpecifications']['edges'][0]['node']
    for data_element in dss['dssdeinclusionSet']:
        column_name = re.sub(
            '[^a-zA-Z0-9\n\.]', '_', data_element['dataElement']['name']
            ).replace('__', '_')[:60].upper()
        i = 1
        while column_name in column_names:
            column_name = column_name[:60] + "_{}".format(i)
            i = i+1
        column_names.append(column_name)
        value_domain = PlaceholderType()
        if data_element['dataElement']['valueDomain']:
            data_value_domain = data_element['dataElement']['valueDomain']
            if 'Date' in data_value_domain['dataType']['name']:
                value_domain = Date
            if 'Number' in data_value_domain['dataType']['name']:
                value_domain = Integer
        column_definitions.append(Column(column_name, value_domain))
    table_name = dss['name'][:60]
    t1 = Table(table_name, meta)
    for column_definition in column_definitions:
        t1.append_column(column_definition)
    t1.append_column(Column('qwerty', Integer, primary_key=True))

    try:
        print(CreateTable(t1).compile(dialect=eval(dbtype).dialect()))
    except NameError as err:
            print("dbtype "+str(err))
            return


if __name__ == '__main__':
    create_database()
