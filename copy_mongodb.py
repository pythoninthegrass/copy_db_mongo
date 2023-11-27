#!/usr/bin/env python

import urllib.parse
from decouple import config
from pymongo import MongoClient

# env vars
db_src = config("DB_SRC")
db_dst = config("DB_DST")
db_user = config("DB_USER")
db_pass = config("DB_PASS")
db_name = config("DB_NAME")

# connection params
params = {
    "readPreference": "secondaryPreferred"
}
encoded_params = urllib.parse.quote_plus(params)

# conn strings
conn_str_src = f"mongodb://{db_user}:{db_pass}@{db_src}/{db_name}?{encoded_params}"
conn_str_dst = f"mongodb://{db_user}:{db_pass}@{db_dst}/{db_name}?{encoded_params}"

# connect to both engines
mongo_client_src = MongoClient(conn_str_src)
mongo_client_dst = MongoClient(conn_str_dst)

# set both databases
mongodb_src = f"{mongo_client_src}.{db_name}"
mongodb_dst = f"{mongo_client_dst}.{db_name}"

# TODO: delete code block after testing `get_collections` and `insert_collections` functions
# # start copy
# for collection in mongodb_src.collection_names():
#     print("collection " + str(collection))
#     # delete all existing documents in current collection on target database
#     mongodb_dst[collection].delete_many({})
#     documents = 0
#     # get all source documents from current collection
#     for document in mongodb_src[collection].find({}):
#         # insert document into target collection
#         documentId = mongodb_dst[collection].insert_one(document).inserted_id
#         documents += 1
#     print("\t" + str(collection) + "migrated: "+ str(documents))


def get_collections(mongodb_src):
    return mongodb_src.collection_names()


def insert_collections(mongodb_src, mongodb_dst, collections):
    # set for document ids
    doc_ids = set()
    # start copy
    for collection in collections:
        print("collection " + str(collection))
        # delete all existing documents in current collection on target database
        mongodb_dst[collection].delete_many({})
        docs = 0
        # get all source documents from current collection
        for document in mongodb_src[collection].find({}):
            # insert document into target collection
            doc_id = mongodb_dst[collection].insert_one(document).inserted_id
            docs += 1
            # add document id to set
            doc_ids.add(doc_id)
        print("\t" + str(collection) + " migrated: "+ str(docs))


def main():
    # start copy
    collections = get_collections(mongodb_src)
    insert_collections(mongodb_src, mongodb_dst, collections)


if __name__ == "__main__":
    main()
