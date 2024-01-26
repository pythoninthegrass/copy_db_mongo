# copy_mongodb

Copy all collections from one database to another on a separate server.

## Setup
### Minimal Requirements
* [Python 3.11](https://www.python.org/downloads/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [mongosh](https://docs.mongodb.com/mongodb-shell/install/)

## Usage
The workflow for this project is as follows:
1. Export collections from source database as CSVs to `backup` directory
2. Start MongoDB container
3. Import collections into destination database

After the first run, `entrypoint.sh` will no longer overwrite the existing data in the destination database. To overwrite the existing data, run `docker-compose down --volumes` to remove the container(s) and then run `docker-compose up -d` to start the container(s) again.

## Quickstart
* Copy `.env.example` to `.env` and update the environment variables
```bash
# setup virtual environment
python -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# export collections from source database
python export.py

# deactivate virtual environment
deactivate

# start container
docker-compose up -d

# connect to mongodb container
export $(grep -v '^#' .env | xargs)
mongosh --host "$DB_HOST" \
    --port "$PORT" \
    --username "$DB_USER" \
    --password "$DB_PASS"

# show dbs
show dbs

# use destination database
use <DB_NAME>

# show collections
show collections

# run query
db.<COLLECTION_NAME>.find()

# quit
exit

# stop container(s)
docker-compose stop

# remove container(s)
docker-compose down
```

## TODO
* [Issues](https://github.com/pythoninthegrass/copy_mongodb/issues)
* Finish `main.py` functions to connect to MongoDB and handle exceptions based on source material
  * Merge `copy_mongodb.py` into `main.py`
* Clean up documentation

## Further Reading
[bitnami/mongodb - Docker Image | Docker Hub](https://hub.docker.com/r/bitnami/mongodb)

[Is there a sample MongoDB Database along the lines of world for MySql? - Stack Overflow](https://stackoverflow.com/questions/5723896/is-there-a-sample-mongodb-database-along-the-lines-of-world-for-mysql/13860389#13860389)

[nsidnev/fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app)

[markqiu/fastapi-mongodb-realworld-example-app](https://github.com/markqiu/fastapi-mongodb-realworld-example-app)
