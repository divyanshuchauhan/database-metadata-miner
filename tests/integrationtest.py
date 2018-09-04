import unittest
import mock
import os
import demo_meta_miner.utils as utils
import json
import responses


if __name__ == '__main__':
    unittest.main()

class TestUtilsPy(unittest.TestCase):
    def test_request_get_no_result_case(self):

        result = utils.request_get(
            "testAuth",
            payload={},
            uuid = '123'
            )
        self.assertEqual({'count': 0,'results':[]},result.json())