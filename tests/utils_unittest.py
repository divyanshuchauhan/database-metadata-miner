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
                },
            slots_data = {
                'name': "distribution",
                "type": "Aristotle DB Tools Field",
                "value": ["table_name", {'primary_keys': 1}]
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
            },
        "slots": {
                'name': "distribution",
                "type": "Aristotle DB Tools Field",
                "value": ["table_name", {'primary_keys': 1}]
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
            'http://127.0.0.1:8080/api/v3/metadata/123',
            json={'count': 0,'results':[]},
            status=200
            )

        result = utils.request_get(
            "testAuth",
            payload={},
            uuid = '123'
            )
        self.assertEqual({'count': 0,'results':[]},result.json())

    @responses.activate
    def test_request_get_result_case(self):
        responses.add(
            responses.GET,
            'http://127.0.0.1:8080/api/v3/metadata/123',
            json={
                'count': 2, 'results':[{'uuid':'result1'},{'uuid':'result2'}]
                },
            status=200)

        result = utils.request_get(
            "qweqw",
            payload={},
            uuid = '123'
            )
        self.assertEqual({
            'count': 2, 'results':[{'uuid':'result1'},{'uuid':'result2'}]
            },result.json())

    @responses.activate
    def test_request_post(self):
        responses.add(
            responses.POST,
            'http://127.0.0.1:8080/api/v3_1/metadata/',
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