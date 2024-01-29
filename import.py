#!/usr/bin/env python

import csv
from argparse import ArgumentParser
from bson.json_util import loads, dumps
from decouple import config
from pathlib import Path
from pymongo import MongoClient, errors
from typing import List, Dict, Union

# env vars
DB_HOST: str = config('DB_HOST', default='localhost')
DB_USER: str = config('DB_USER', default='root')
DB_PASS: str = config('DB_PASS', default='toor')
DB_NAME: str = config('DB_NAME', default='test')
PORT: int = config('PORT', cast=int, default=27017)
DROP_DB: bool = config('DROP_DB', cast=bool, default=False)
COLLECTION: str = config('COLLECTION', default='default')
BACKUP_DIR = Path.cwd() / "backup"

# TODO: replace with typer
# cli args
parser = ArgumentParser(description="Import data to MongoDB")
parser.add_argument('--db-host', dest='DB_HOST', help="Destination MongoDB host")
parser.add_argument('--db-user', dest='DB_USER', help="Destination MongoDB user")
parser.add_argument('--db-pass', dest='DB_PASS', help="Destination MongoDB password")
parser.add_argument('--db-name', dest='DB_NAME', help="Destination MongoDB database name")
parser.add_argument('--port', dest='PORT', type=int, help="Destination MongoDB port")

args = parser.parse_args()

if args.DB_HOST:
    DB_HOST = args.DB_HOST
if args.DB_USER:
    DB_USER = args.DB_USER
if args.DB_PASS:
    DB_PASS = args.DB_PASS
if args.DB_NAME:
    DB_NAME = args.DB_NAME
if args.PORT:
    PORT = args.PORT

# ! qa
DROP_DB = True

# mongodb uri
URI: str = f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}:{PORT}"
QUERY_STRING: str = "ssl=false&readPreference=secondaryPreferred"

# connect to mongodb
client: MongoClient = MongoClient(f"{URI}?{QUERY_STRING}")


def test_connection() -> bool:
    """Test connection to MongoDB"""
    try:
        client.server_info()
        print("Connected to MongoDB")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


# TODO: remove bare except
def read_data(file_path):
    """Import data from file"""
    try:
        if file_path.endswith('.json'):
            data = []
            with open(file_path, 'r') as f:
                for line in f:
                    data.append(loads(line))
        elif file_path.endswith('.csv'):
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                next(reader)  # Skip header row
                data = [row for row in reader]
        else:
            # TODO: naive implementation (e.g., zips.csv.bak = zips.csv)
            print("Unsupported extension: " + Path(file_path).stem)
            print(f"Skipping file: {file_path}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        print(f"{file_path}\nSkipping file...")
        return None

    return data


def check_if_db_exists(db_name: str) -> bool:
    """Check if database exists"""
    return db_name in client.list_database_names()


def drop_database(db_name: str, enabled: bool = False) -> None:
    """Drop database"""
    if enabled:
        client.drop_database(db_name)


def create_db(db_name: str) -> None:
    """Create database"""
    if not check_if_db_exists(db_name):
        client[db_name]


def check_if_collection_exists(db_name: str, collection: str) -> bool:
    """Check if collection exists"""
    return collection in client[db_name].list_collection_names()


def create_collection(db_name: str, collection: str) -> None:
    """Create collection"""
    if not check_if_collection_exists(db_name, collection):
        client[db_name].create_collection(str(collection))


# TODO: refactor to be used in insert_documents
# def check_if_document_exists(collection: str, document: Dict) -> bool:
#     """Check if document exists"""
#     return client[DB_NAME][str(collection)].find_one(document) is not None


# TODO: use logging instead of stdout
def insert_documents(collection: str, documents: Union[List[Dict], Dict]) -> None:
    """Insert documents into collection"""
    if isinstance(documents, Dict):
        documents = [documents]
    if documents:
        try:
            result = client[DB_NAME][str(collection)].insert_many(documents)
        except errors.BulkWriteError as e:
            error_code = e.details['writeErrors'][0]['code']
            id_value = e.details['writeErrors'][0]['keyValue']['_id']
            error_message = e.details['writeErrors'][0]['errmsg']
            print(f"Error code: {error_code}")
            print(f"_id value: {id_value}")
            print(f"Error message: {error_message}")
            return 0
    else:
        print(f"No documents to insert into {collection}")

    return len(result.inserted_ids)


# TODO: test against mixed directories
def main():
    # collections = []
    # for fn in BACKUP_DIR.iterdir():
    #     data = read_data(str(fn))
    #     if data is not None:
    #         collections.extend(data)
    collections = [item for fn in BACKUP_DIR.iterdir() if (data := read_data(str(fn))) is not None for item in data]

    test_connection()

    if DROP_DB:
        drop_database(DB_NAME, DROP_DB)

    create_db(DB_NAME)

    if not check_if_collection_exists(DB_NAME, COLLECTION):
        create_collection(DB_NAME, COLLECTION)

    print(f"Inserting {len(collections)} records into {COLLECTION}...")
    total_inserted = sum(insert_documents(COLLECTION, item) for item in collections)
    print(f"Total records inserted: {total_inserted}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
