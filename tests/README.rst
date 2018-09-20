Database-Metadata-Miner Testing Guide
=====================================

- During development all the tests can be run by the following command:

        ``python -m unittest discover -s tests -p '*test.py'``


- To run the test individually:

        ``python -m unittest tests.integrationtest.TestUtilsPy.test_miner``

        All the tests can be run by just changing the name accordingly.


- chinook.db file is present for integration testing. It can be downloaded from http://www.sqlitetutorial.net/sqlite-sample-database/


- data.json file is present for integration testing and is used to match the output of the miner.