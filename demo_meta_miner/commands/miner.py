from sqlalchemy import create_engine, MetaData
import click
import demo_meta_miner.utils as utils
# from demo_meta_miner.save_req import save_req


@click.command()
@click.option('--url', default='sqlite:///Test2.db', help='Full Database URl')
@click.option(
    '--database',
    default='testDatabase1',
    help='Database name on aristotle'
    )
@click.option(
    '--auth',
    default='910923131171f6c4ae9bd84cbb5d5d44edb14436',
    help='Authentication token'
    )
@click.option(
    '--file',
    default='data.json',
    help='Spicify the json file name'
    )
def miner(url, database, auth, file):
    """This script creates a data.json file,
    that contains all the database schema to be uploaded in Aristotle"""
    engine = create_engine(url)
    metadata = MetaData()

    conn = engine.connect()

    metadata.reflect(engine)
    # print(metadata.tables)

    table_data = {}
    distributions = []
    dataset = utils.create_req(
        model="dataset",
        name=database,
        app="aristotle_dse"
        )
    dataset = utils.request_post(auth=auth, payload=dataset)
    # import pdb; pdb.set_trace()
    for table_object in metadata.sorted_tables:
        table = table_object.name
        extra_information_distribution = {
            "data_elements": [],
            "dataset": dataset
            }
        table_data[table] = []
        for columns in metadata.tables[table].c:
            column_type = str(columns.type)
            extra_information_value_domain = {}
            if 'enum' in column_type.lower():
                enum_types = column_type.replace("'","").split('(')[1].strip(')').split(',')
                extra_information_value_domain['permissible_values'] = []
                for index,enum_type in enumerate(enum_types):
                    extra_information_value_domain['permissible_values'].append({"value": enum_type,
                "meaning": "placeholder", "order":index})
                
            value_domain = utils.create_req(
                model="valuedomain",
                name=column_type,
                app="aristotle_mdr",
                other_field_data=extra_information_value_domain
                )
            extra_information_dataelement = {"valueDomain": value_domain}
            data_element = utils.create_req(
                model="dataelement",
                name=str(columns.name),
                app="aristotle_mdr",
                other_field_data=extra_information_dataelement
                )
            extra_information_distribution['data_elements'].append({
                'data_element': data_element,
                "logical_path": table+"."+str(columns.name)
                })
        distribution = utils.create_req(
            model="distribution",
            name=table, app="aristotle_dse",
            other_field_data=extra_information_distribution
            )
        distributions.append(distribution)
    utils.save_req_file(distributions, file)
    conn.close()


if __name__ == '__main__':
    miner()
