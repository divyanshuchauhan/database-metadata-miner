import unittest
# import mock
import os
import demo_meta_miner.utils as utils
from demo_meta_miner.commands.miner import miner
from demo_meta_miner.commands.execute_saved_req import execute_saved_req
from demo_meta_miner.commands.create_database import create_database

import json
import responses
import click
import sys
from click.testing import CliRunner
from subprocess import call,check_output

class TestUtilsPy(unittest.TestCase):
    # auth = os.environ.get('test_auth')
    auth = str(check_output("./test_project/manage.py create_access_token|tail -1",shell=True).decode('UTF-8')).rstrip('\n')
    dataset_id = ''
    def test_request_get_no_result_case(self):
        result = utils.request_get(
            "testAuth",
            payload={},
            uuid = '',
            url = 'http://0.0.0.0:8080'
            )
        self.assertEqual({'detail': 'Invalid token.'},result.json())


    def test_miner(self):
        runner = CliRunner()
        result = runner.invoke(miner, ['--url','sqlite:///tests/chinook.db','--database','testDatabase1','--auth', self.auth,'--file','./tests/data_result.json','--aristotleurl','http://0.0.0.0:8080'], '--verbose', False)
        self.dataset_id = result.output.replace('\n','')
        result_data = utils.read_file('./tests/data_result.json')
        compare_data = utils.read_file('./tests/data.json')
        for distribution in compare_data:
            distribution['fields']['dataset'] = self.dataset_id
        self.assertEqual(result_data,compare_data)
        self.execute_saved_req_check(result_data)

    def execute_saved_req_check(self,result_data):
        runner = CliRunner()
        aristotleurl = 'http://0.0.0.0:8080'
        result = runner.invoke(execute_saved_req, ['--auth', self.auth,'--file','./tests/data_result.json','--aristotleurl',aristotleurl], '--verbose', False)
        datasetResponse = utils.request_get(
            auth=self.auth,
            payload = {
            'type': 'aristotle_dse:distribution',
            'dq':'dataset__uuid:'+self.dataset_id
        },
        url=aristotleurl)
        # Collect all data from server
        dataset = {}
        for dist in datasetResponse.json()["results"]:
            dist_data =  utils.request_get(
                auth=self.auth,
                uuid=dist['uuid'],
                url=aristotleurl
            )
            dataset[dist['name']] = {'slots': dist_data.json()['slots'] ,'columns': {}}
            for data_elements in dist_data.json()['fields']['data_elements']:
                data_element_data =  utils.request_get(
                    auth=self.auth,
                    uuid=data_elements["data_element"],
                    url=aristotleurl
                )
                value_domain_data =  utils.request_get(
                    auth=self.auth,
                    uuid=data_element_data.json()['fields']['valueDomain'],
                    url=aristotleurl
                )
                dataset[dist['name']]['columns'][data_element_data.json()['fields']['name']] = value_domain_data.json()['fields']['name']
        # Match server data and json data
        for dist_json in result_data:
            distribution_name = dist_json['fields']['name']
            self.assertTrue(distribution_name in dataset)
            for slot in dist_json['slots']:
                slot['value'] = str(slot['value'])
            self.assertEqual(dist_json['slots'],dataset[distribution_name]['slots'])
            for data_element_json in dist_json['fields']['data_elements']:

                data_element_name = data_element_json['data_element']['fields']['name']
                self.assertTrue(
                    data_element_name in dataset[distribution_name]['columns']
                    )
                self.assertEqual(data_element_json['data_element']['fields']['valueDomain']['fields']['name'],dataset[distribution_name]['columns'][data_element_name])
        result = runner.invoke(execute_saved_req, ['--auth', self.auth,'--file','./tests/data_result.json','--aristotleurl',aristotleurl, '--dbuuid', self.dataset_id], '--verbose', False)
        

    def test_create_database(self):
        runner = CliRunner()
        result = runner.invoke(create_database, ['--dssuuid','6aee1c50-158c-11e7-803e-0242ac110017','--dbtype','sqlite','--aristotleurl', 'https://registry.aristotlemetadata.com'])
        result = result.output.replace('\n','')
        self.assertTrue('CREATE TABLE' in result)


    def test_create_database_invalid_dbtype(self):
        runner = CliRunner()
        result = runner.invoke(create_database, ['--dssuuid','6aee1c50-158c-11e7-803e-0242ac110017','--dbtype','sqlit','--aristotleurl', 'https://registry.aristotlemetadata.com'])
        result = result.output.replace('\n','')
        self.assertEqual("dbtype name 'sqlit' is not defined",result)


    def test_create_database_invalid_url(self):
        runner = CliRunner()
        result = runner.invoke(create_database, ['--dssuuid','6aee1c50-158c-11e7-803e-0242ac11001','--dbtype','sqlite','--aristotleurl', 'https://registry.aristotlemetadata.com'])
        result = result.output.replace('\n','')
        self.assertEqual("Given https://registry.aristotlemetadata.com aristotleurl does not contain 6aee1c50-158c-11e7-803e-0242ac11001 dssuuid",result)


if __name__ == '__main__':
    TestUtilsPy.auth = os.environ.get('test_auth', TestUtilsPy.auth) 
    unittest.main()