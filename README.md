# Database-Metadata-Miner

[![Build Status](https://travis-ci.org/divyanshuchauhan/database-metadata-miner.svg?branch=master)](https://travis-ci.org/divyanshuchauhan/database-metadata-miner)

## What is it?
Database-Metadata-Miner is a set of command line tools that helps in extracting the metadata schema of the database and uploading it to aristotle metedata registry.

It is a database independent tool and would work for any relational database.

## Installing
Development: `python3 -m pip install --index-url https://test.pypi.org/project/ --extra-index-url https://pypi.org/simple demo-meta-miner`

## How to use it?

To run the miner use the command:

`AristotleDbTools miner --url <db url> --auth <auth token> --file <filename you prefer i.e. data.json> --aristotleurl <The url aristotle is setup on> --verbose <To print the background information>`
 
A data.json would be created in the same folder. 

Then run the following command to upload the metadata to your local aristotle:

`AristotleDbTools execute_saved_req --auth <auth token> --file <filename of json to read i.e. data.json> --dbuuid <database uuid, for incremental update> --aristotleurl <The url aristotle is setup on> --verbose <To print the background information>`


Create database tool:
This tool is used to generate a create table statement from the dataset specification set in aristotle.

`AristotleDbTools create_database --dssuuid <dataset specification uuid> --dbtype <Database for which to create query, options: postgresql, mysql, sqlite, oracle, firebird, sybase> --aristotleurl <The url aristotle is setup on> --verbose <To print the background information>`
