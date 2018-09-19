.. Database-Metadata-Miner documentation master file, created by
   sphinx-quickstart on Wed Sep 19 12:53:06 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Database-Metadata-Miner's documentation!
===================================================

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

``AristotleDbTools miner --url <db url> --auth <auth token> --file <filename you prefer i.e. data.json> --aristotleurl <The url aristotle is setup on> --verbose <To print the background information>``

Options:

- --url: Database url from which the metedata has to be extracted


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
