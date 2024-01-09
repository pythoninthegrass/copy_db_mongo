#!/usr/bin/env python

import csv
from decouple import config
from pathlib import Path
from pymongo import MongoClient
from typing import List, Dict, Union

# env vars
DB_HOST: str = config('DB_HOST')
DB_USER: str = config('DB_USER')
DB_PASS: str = config('DB_PASS')
DB_NAME: str = config('DB_NAME')
PORT: int = config('PORT', cast=int)

backup_dir = Path.cwd() / 'backup'

# read csv
with open(Path.cwd() / 'collections.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    collections: set = set([row['collection'] for row in reader])

# mongodb uri
URI: str = f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}:{PORT}/{DB_NAME}"
QUERY_STRING: str = "ssl=false&readPreference=secondaryPreferred"

# connect to mongodb
client: MongoClient = MongoClient(f"{URI}?{QUERY_STRING}")


def get_usernames_by_fullname(fullname: str) -> List[str]:
    """Find usernames by full name"""
    filter = {
        'fullName': {
            '$regex': f'.*{fullname}.*',
            '$options': 'i'
        }
    }

    result = client['bonfire']['User'].find(filter=filter)

    users = list(result)
    usernames = [user['email'] for user in users]
    return usernames


def get_collection_sizes() -> Dict[str, int]:
    """Get collection sizes"""
    sizes: Dict[str, int] = {}
    for collection in collections:
        sizes[collection] = client['bonfire'][collection].estimated_document_count()
    return sizes


def check_if_file_exists(filename: str) -> bool:
    """Check if file exists"""
    return Path(filename).is_file()


def export_collection_to_csv(collection: str, limit: Union[int, bool]) -> None:
    """Export collection to csv"""
    result = client['bonfire'][collection].find().limit(limit)
    documents = list(result)

    if len(documents) > 0:
        filename = f"{backup_dir}/{collection}.csv"
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = set()
            for document in documents:
                fieldnames.update(document.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(documents)


def main(skip_size=0, min_size=1000, max_size=True) -> None:
    """
    Export MongoDB collections to CSV files.

    * Get collection sizes.
    * If collection size is 0, skip.
    * If csv file exists, skip.
    * If collection size is less than n, export entire collection.
    * If collection size is set to true, export 5% of collection.
    """
    collection_sizes = get_collection_sizes()
    for collection, size in collection_sizes.items():
        if size == skip_size:
            continue
        elif size < min_size:
            filename = f"mongo_backup/{collection}.csv"
            if check_if_file_exists(filename):
                print(f"{collection}.csv exists! Skipping...")
                continue
            else:
                print(f"Exporting {collection}...")
                export_collection_to_csv(collection, size)
        else:
            if max_size is True:
                limit = min(min_size, int(size * 0.05))
            else:
                limit = size
            filename = f"mongo_backup/{collection}.csv"
            if check_if_file_exists(filename):
                print(f"{collection}.csv exists! Skipping...")
                continue
            else:
                print(f"Exporting {collection}...")
                export_collection_to_csv(collection, limit)


if __name__ == '__main__':
    try:
        main(skip_size=0, min_size=1000)
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
