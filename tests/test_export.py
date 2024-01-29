#!/usr/bin/env python

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import pymongo
import requests
from decouple import config
from export import main
from testcontainers.mongodb import MongoDbContainer

# env vars
DB_HOST: str = config('DB_HOST')
DB_USER: str = config('DB_USER')
DB_PASS: str = config('DB_PASS')
DB_NAME: str = config('DB_NAME')
PORT: int = config('PORT', cast=int)

backup_dir = Path.cwd() / 'backup'
zips_url = 'https://media.mongodb.org/zips.json'
zips_fn = Path.cwd() / 'zips.json'


def dl_zips(url, filename):
    """Download zips.json"""
    if not filename.is_file():
        response = requests.get(url)
        with open(filename, 'w') as f:
            f.write(response.text)


def cleanup(filename):
    """Cleanup zips.json"""
    if filename.is_file():
        filename.unlink()


# TODO: function: create mongodb container and populate it with data from zips.json
def test_main():
    """Test main function from export.py"""
    # download zips.json
    dl_zips(zips_url, zips_fn)

    # create mongodb container and populate it with data from zips.json
    with MongoDbContainer('mongo:7.0.4-jammy',
                          port_to_expose=PORT,
                          env_vars={'MONGO_INITDB_DATABASE': DB_NAME,
                                    'MONGO_INITDB_ROOT_USERNAME': DB_USER,
                                    'MONGO_INITDB_ROOT_PASSWORD': DB_PASS}
                          ) as mongo:
        client = pymongo.MongoClient(mongo.get_connection_url())
        db = client.test
        with open(zips_fn, 'r') as f:
            data = json.load(f)
            db.zips.insert_many(data)

        # run main function from export.py
        main()

        # assert that csv files were created in the backup directory
        for collection in db.list_collection_names():
            assert (backup_dir / f"{collection}.csv").is_file()

    # delete zips.json
    # cleanup(zips_fn)


if __name__ == '__main__':
    test_main()
