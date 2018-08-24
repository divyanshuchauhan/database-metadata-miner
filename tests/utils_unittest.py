import unittest
import os
# import sys 
# sys.path.append('.')
import demo_meta_miner.utils as utils
import json


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


if __name__ == '__main__':
    unittest.main()