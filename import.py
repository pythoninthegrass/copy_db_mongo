#!/usr/bin/env python

import csv
from decouple import config
from pathlib import Path
from pymongo import MongoClient
from typing import List, Dict, Union

# env vars
DB_HOST: str = config('DEST_DB_HOST', default='localhost')
DB_USER: str = config('DEST_DB_USER', default='root')
DB_PASS: str = config('DEST_DB_PASS', default='toor')
DB_NAME: str = config('DEST_DB_NAME', default='test')
PORT: int = config('PORT', cast=int, default=27017)

backup_dir = Path.cwd() / 'backup'

# prompt user to ask if the env vars are correct
print("Use default values for destination MongoDB? (y/n)")
input_value = input().casefold()

if input_value in ['n', 'no']:
    input_mapping = {
        'DB_HOST': "Enter the destination MongoDB host:",
        'DB_USER': "Enter the destination MongoDB user:",
        'DB_PASS': "Enter the destination MongoDB password:",
        'DB_NAME': "Enter the destination MongoDB database name:",
        'PORT': "Enter the destination MongoDB port:"
    }

    for key, prompt in input_mapping.items():
        print(prompt)
        globals()[key] = input()

# read csvs from backup dir
files = [fn for fn in backup_dir.glob('*.csv')]

# mongodb uri
URI: str = f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}:{PORT}/{DB_NAME}"
QUERY_STRING: str = "ssl=false&readPreference=secondaryPreferred"

# connect to mongodb
client: MongoClient = MongoClient(f"{URI}?{QUERY_STRING}")

# read csv
with open(Path.cwd() / 'collections.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    collections: set = set([row['collection'] for row in reader])


def insert_documents(collection: str, documents: List[Dict]) -> None:
    """Insert documents into collection"""
    result = client[DB_NAME][collection].insert_many(documents)
    print(f"Inserted {len(result.inserted_ids)} documents into {collection}")


def get_documents(collection: str, limit: Union[int, bool]) -> List[Dict]:
    """Get documents from collection"""
    if limit:
        result = client[DB_NAME][collection].find().limit(limit)
    else:
        result = client[DB_NAME][collection].find()

    documents = list(result)
    return documents


def check_if_file_exists(filename: str) -> bool:
    """Check if file exists"""
    return Path(filename).is_file()


def import_collection_from_csv(collection: str, limit: Union[int, bool]) -> None:
    """Import collection from csv"""
    filename = f"{backup_dir}/{collection}.csv"

    if check_if_file_exists(filename):
        documents = get_documents(collection, limit)
        insert_documents(collection, documents)
    else:
        print(f"File {filename} does not exist")


def main() -> None:
    """Main function"""
    for collection in collections:
        import_collection_from_csv(collection, False)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
