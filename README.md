# copy_mongodb

Copy all collections from one database to another on a separate server.

## Setup
### Minimal Requirements
* [Python 3.11](https://www.python.org/downloads/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## Quickstart
```bash
# create bridge network
docker network create app-tier --driver bridge

# start container(s)
docker-compose up -d

# download official example mongodb collection
curl -LJO http://media.mongodb.org/zips.json

# list volumes
docker volume ls

# copy file to container
docker cp zips.json <container>:/tmp/zips.json

# import file to mongodb
docker exec -it <container> mongoimport --db test --collection zips --file /tmp/zips.json

# connect to container
docker exec -it <container> bash

# connect to mongodb
mongo

# list databases
show dbs

# list collections
show collections

# list documents
db.zips.find()

# exit mongodb
exit

# test python script
python main.py

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
