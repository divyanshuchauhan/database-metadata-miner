.. Database-Metadata-Miner documentation master file, created by
   sphinx-quickstart on Wed Sep 19 12:53:06 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Database-Metadata-Miner's documentation!
===================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


What is it?
-----------

Database-Metadata-Miner is a set of command line tools that help in extracting the metadata schema of the database and uploading it to aristotle metedata registry.

It is a database independent tool and would work for any relational database.

Installing
----------

python3 -m pip install --index-url https://test.pypi.org/project/ --extra-index-url https://pypi.org/simple demo-meta-miner


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


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
