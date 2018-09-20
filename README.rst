
Database-Metadata-Miner
=======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. image:: https://travis-ci.org/divyanshuchauhan/database-metadata-miner.svg?branch=master
    :target: https://travis-ci.org/divyanshuchauhan/database-metadata-miner
.. image:: https://coveralls.io/repos/github/divyanshuchauhan/database-metadata-miner/badge.svg?branch=master
:target: https://coveralls.io/github/divyanshuchauhan/database-metadata-miner?branch=master
.. image:: https://readthedocs.org/projects/database-metadata-miner/badge/?version=latest
:target: https://database-metadata-miner.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status


What is it?
-----------

Database-Metadata-Miner is a set of command line tools that help in extracting the metadata schema of the database and uploading it to aristotle metedata registry.

It is a database independent tool and would work for any relational database.

Installing
----------

``python3 -m pip install --index-url https://test.pypi.org/project/ --extra-index-url https://pypi.org/simple demo-meta-miner``


How to use it?
--------------

Miner command:
^^^^^^^^^^^^^^
This command extracts metadata from the given database and stores it in a json file in the location from where command is run.

``AristotleDbTools miner --url <> --auth <> --file <> --aristotleurl <> --verbose <>``

Options:

- --url: Database url from which the metedata has to be extracted
- --auth: Authentication token, which can be generated from aristotleurl + /api/token/list/
- --file: Name of the file that contains the output json
- --aristotleurl: The url enpoint for aristotle software
- --verbose: Prints internal statements (Optional)



execute_saved_req command:
^^^^^^^^^^^^^^^^^^^^^^^^^^
This command executes and upload the data to aristotle endpoint from the json file provided by the miner command.

``AristotleDbTools execute_saved_req --auth <> --file <> --dbuuid <> --aristotleurl <> --verbose``

Options:

- --auth: Authentication token, which can be generated from aristotleurl + /api/token/list/
- --file: Name of the file that contains the output json from the miner command
- --dbuuid: Database UUID, used for uploading changes to this DB UUID (Optional)
- --aristotleurl: The url enpoint for aristotle software
- --verbose: Prints internal statements (Optional)



create_database command:
^^^^^^^^^^^^^^^^^^^^^^^^
This command is used to generate a create table statement from the dataset specification set in aristotle.

``AristotleDbTools create_database --dssuuid <> --dbtype <> --aristotleurl <> --verbose <>``

Options:

- --dssuuid: dataset specification UUID
- --dbtype: Database type for which to create query, options: postgresql, mysql, sqlite, oracle, firebird, sybase
- --aristotleurl: The url enpoint for aristotle software
- --verbose: Prints internal statements (Optional)


Additional Information
----------------------

- Chinook db is used for integration testing. It can be downloaded from http://www.sqlitetutorial.net/sqlite-sample-database/


