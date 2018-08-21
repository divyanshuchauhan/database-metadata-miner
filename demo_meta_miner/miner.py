from sqlalchemy import create_engine
import click
import utils as utils
# from demo_meta_miner.save_req import save_req


@click.command()
@click.option('--url', default='sqlite:///Test2.db', help='Full Database URl')
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
def demo(url, auth, file):
    """This script creates a data.json file,
    that contains all the database schema to be uploaded in Aristotle"""
    engine = create_engine(url)
    from sqlalchemy import MetaData
    metadata = MetaData()

    conn = engine.connect()

    metadata.reflect(engine)
    # print(metadata.tables)

    table_data = {}
    distributions = []
    dataset = utils.create_req(
        model="dataset",
        name="testDatabase",
        app="aristotle_dse"
        )
    dataset = utils.request_post(auth=auth, payload=dataset)
    # import pdb; pdb.set_trace()
    for table in metadata.tables.keys():
        extra_information_distribution = {
            "data_elements": [],
            "dataset": dataset
            }
        table_data[table] = []
        for columns in metadata.tables[table].c:
            value_domain = utils.create_req(
                model="valuedomain",
                name=columns.type.__repr__(),
                app="aristotle_mdr"
                )
            extra_information_dataelement = {"valueDomain": value_domain}
            data_element = utils.create_req(
                model="dataelement",
                name=columns.name.__repr__(),
                app="aristotle_mdr",
                other_field_data=extra_information_dataelement
                )
            extra_information_distribution['data_elements'].append({
                'data_element': data_element,
                "logical_path": table+"."+columns.name.__repr__()
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
    demo()
