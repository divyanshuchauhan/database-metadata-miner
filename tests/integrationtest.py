import unittest
import mock
import os
import demo_meta_miner.utils as utils
import json
import responses
import click
import sys
import os


if __name__ == '__main__':
    TestUtilsPy.auth = os.environ.get('test_auth', TestUtilsPy.auth) 
    unittest.main()

class TestUtilsPy(unittest.TestCase):
    auth = "testAuth"
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
            '56da9aee53cbf177f5826890d48233e6b3020871',
            payload={},
            uuid = '',
            url = 'http://0.0.0.0:8080'
            )
        self.assertEqual({'count': 0, 'next': None, 'previous': None, 'results': []},result.json())