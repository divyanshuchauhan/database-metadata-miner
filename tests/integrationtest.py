import unittest
import mock
import os
import demo_meta_miner.utils as utils
from demo_meta_miner.commands.miner import miner
from demo_meta_miner.commands.execute_saved_req import execute_saved_req
import json
import responses
import click
import sys
from click.testing import CliRunner
from subprocess import call,check_output

class TestUtilsPy(unittest.TestCase):
    # auth = os.environ.get('test_auth')
    auth = str(check_output("./test_project/manage.py create_access_token|tail -1",shell=True).decode('UTF-8')).rstrip('\n')
    # x = check_output("(ls -l|tail -1)",shell=True).decode('UTF-8')
    # import pdb; pdb.set_trace()
    dataset_id = ''
    def test_request_get_no_result_case(self):
        result = utils.request_get(
            "testAuth",
            payload={},
            uuid = '',
            url = 'http://0.0.0.0:8080'
            )
        self.assertEqual({'detail': 'Invalid token.'},result.json())
    def test_request_get_no_result_case2(self):
        result = utils.request_get(
            self.auth,
            payload={},
            uuid = '',
            url = 'http://0.0.0.0:8080'
            )
        self.assertEqual({'count': 0, 'next': None, 'previous': None, 'results': []},result.json())

    def test_miner(self):
        # self.auth = call(["./test_project/manage.py create_access_token"],shell=True)
        runner = CliRunner()
        result = runner.invoke(miner, ['--url','sqlite:///Test2.db','--database','testDatabase1','--auth', self.auth,'--file','./tests/data_result.json','--aristotleurl','http://0.0.0.0:8080'])
        self.dataset_id = result.output.replace('\n','')
        print('hiiii')
        print(self.dataset_id)
        result_data = utils.read_file('./tests/data_result.json')
        compare_data = utils.read_file('./tests/data.json')
        for distribution in compare_data:
            distribution['fields']['dataset'] = self.dataset_id
        print('hiiii')
        self.assertEqual(result_data,compare_data)
        self.execute_saved_req_check(result_data)

    def execute_saved_req_check(self,result_data):
        runner = CliRunner()
        aristotleurl = 'http://0.0.0.0:8080'
        result = runner.invoke(execute_saved_req, ['--auth', self.auth,'--file','./tests/data_result.json','--aristotleurl',aristotleurl])
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
                print(data_element_json['data_element']['fields']['name'])

                data_element_name = data_element_json['data_element']['fields']['name']
                print(dataset[distribution_name]['columns'])
                self.assertTrue(
                    data_element_name in dataset[distribution_name]['columns']
                    )
                self.assertEqual(data_element_json['data_element']['fields']['valueDomain']['fields']['name'],dataset[distribution_name]['columns'][data_element_name])
        


if __name__ == '__main__':
    TestUtilsPy.auth = os.environ.get('test_auth', TestUtilsPy.auth) 
    unittest.main()