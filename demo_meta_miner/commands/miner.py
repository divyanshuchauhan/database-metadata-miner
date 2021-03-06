from sqlalchemy import create_engine, MetaData
import click
import demo_meta_miner.utils as utils


@click.command()
@click.option('--url', default='sqlite:///Test2.db', help='Full Database URl')
@click.option(
    '--database',
    default='testDatabase',
    help='Database name on aristotle'
    )
@click.option(
    '--auth',
    help='Authentication token'
    )
@click.option(
    '--file',
    default='data.json',
    help='Spicify the json file name'
    )
@click.option(
    '--aristotleurl',
    default='http://127.0.0.1:8080',
    help='Spicify the aristotle url'
    )
@click.option(
    '--verbose',
    is_flag=True,
    help="Will print verbose messages."
    )
def miner(url, database, auth, file, aristotleurl, verbose):
    """
    This script creates a data.json file,
    that contains all the database schema to be uploaded in Aristotle
    """
    engine = create_engine(url)
    metadata = MetaData()
    conn = engine.connect()
    metadata.reflect(engine)

    table_data = {}
    distributions = []
    dataset = utils.create_req(
        model="dataset",
        name=database,
        app="aristotle_dse"
        )
    dataset = utils.request_post(
        auth=auth,
        payload=dataset,
        url=aristotleurl,
        verbose=verbose
        )
    for table_object in metadata.sorted_tables:
        table = table_object.name
        extra_information_distribution = {
            "data_elements": [],
            "dataset": dataset
            }
        table_data[table] = []
        for columns in metadata.tables[table].c:
            value_domain = create_value_domain_request(columns)
            data_element = create_data_element_request(columns, value_domain)
            extra_information_distribution['data_elements'].append({
                'data_element': data_element,
                "logical_path": table+"."+str(columns.name)
                })
        distribution = create_distribution_request(
            table_object,
            extra_information_distribution
            )
        distributions.append(distribution)
    utils.save_req_file(distributions, file)
    conn.close()
    print(dataset)


def create_distribution_request(table_object, extra_information_distribution):
    """
    Create a json payload for distribution request
    """
    slots_information_distribution = []
    table = table_object.name
    primary_keys = []
    for pk in table_object.primary_key.columns_autoinc_first:
        primary_keys.append(table + '.' + pk.name)
    slots_information_distribution.append({
            'name': "distribution",
            "type": "Aristotle DB Tools Field",
            "value": str(table)
            })
    slots_information_distribution.append({
            'name': "primary key",
            "type": "Aristotle DB Tools Field",
            "value": primary_keys
            })
    distribution = utils.create_req(
        model="distribution",
        name=table,
        app="aristotle_dse",
        other_field_data=extra_information_distribution,
        slots_data=slots_information_distribution
        )
    return distribution


def create_data_element_request(columns, value_domain):
    """
    Create a json payload for data element request
    """
    extra_information_dataelement = {"valueDomain": value_domain}
    data_element = utils.create_req(
        model="dataelement",
        name=str(columns.name),
        app="aristotle_mdr",
        other_field_data=extra_information_dataelement
        )
    return data_element


def create_value_domain_request(columns):
    """
    Create a json payload for value domain request
    """
    column_type = repr(columns.type)
    extra_information_value_domain = {}
    if 'enum' in column_type.lower():
        enum_types = column_type.replace(
            "'", "").split('(')[1].strip(')').split(',')
        extra_information_value_domain['permissible_values'] = []
        for index, enum_type in enumerate(enum_types):
            extra_information_value_domain['permissible_values'].append({
                "value": enum_type,
                "meaning": "placeholder",
                "order": index
                })
    value_domain = utils.create_req(
        model="valuedomain",
        name=column_type,
        app="aristotle_mdr",
        other_field_data=extra_information_value_domain
        )
    return value_domain


if __name__ == '__main__':
    miner()
