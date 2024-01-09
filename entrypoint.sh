#!/usr/bin/env bash

# wait for the mongodb server to start
sleep 10

# import the csv files
for filename in /tmp/*.csv; do
	collection=${filename%.csv}
	mongoimport --type csv \
		--db "${DB_NAME}" \
		--collection $collection \
		--headerline \
		--file $filename \
		--drop
done

# start the mongodb server
mongod
