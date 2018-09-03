import unittest
import mock
import os
import demo_meta_miner.utils as utils
import json
import responses


class TestUtilsPy(unittest.TestCase):

    def test_create_req(self):
        result = utils.create_req(
            model="test_dataelement",
            name="Test1",
            app="aristotle_mdr",
            other_field_data={
                "test_field1":"test_data1",
                "test_field2":"test_data2"
                }
            )
        payload = {
            "concept_type": {
                "app": "aristotle_mdr",
                "model": "test_dataelement"
            },
            "fields": {
                "name": "Test1",
                "definition": "Placeholder",
                "test_field1":"test_data1",
                "test_field2":"test_data2",
            }
        }
        self.assertEqual(payload, result)

    def test_save_req_file(self):
        file_name = "test.json"
        data = {"test_data":"test_value"}
        utils.save_req_file(data,file_name)
        with open(file_name) as f:
            read_data = f.read()
        os.remove(file_name)
        self.assertEqual(json.loads(read_data),data)
    	
    @responses.activate
    def test_request_get_no_result_case(self):
        responses.add(
            responses.GET,
            'http://localhost:8080/api/v3/metadata/',
            json={'count': 0,'results':[]},
            status=200
            )

        result = utils.request_get(
            "testAuth",
            model="valuedomain",
            name="Test1",
            app="aristotle_mdr"
            )
        self.assertEqual(False,result)

    @responses.activate
    def test_request_get_result_case(self):
        responses.add(
            responses.GET,
            'http://localhost:8080/api/v3/metadata/',
            json={
                'count': 2, 'results':[{'uuid':'result1'},{'uuid':'result2'}]
                },
            status=200)

        result = utils.request_get(
            "qweqw",
            model="valuedomain",
            name="Test1",
            app="aristotle_mdr"
            )
        self.assertEqual('result1',result)

    @responses.activate
    def test_request_post(self):
        responses.add(
            responses.POST,
            'http://localhost:8080/api/v3/metadata/',
            json={'created':[{'uuid':'uuid1'}]},
            status=200,
            content_type='application/json'
            )

        result = utils.request_post(
            "testAuth",
            payload={'valuedomain':'test'}
            )
        self.assertEqual('uuid1',result)


if __name__ == '__main__':
    unittest.main()