# syntax=docker/dockerfile:1.6

# use the official mongodb docker image
FROM mongo:7.0.4-jammy

# copy the csv files into the docker image
COPY ./backup/*.csv /tmp/

# environment variables for the mongodb instance
ENV MONGO_INITDB_DATABASE=${DB_NAME}
ENV MONGO_PORT=${PORT}

# set the working directory
WORKDIR /app

# TODO: qa
# # install mongo cli
# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt -qq update && apt -qq install -y mongodb-clients

# copy the script that will import the csv files into the mongodb instance
COPY entrypoint.sh .

# run the script when the docker image is run
# CMD ["./entrypoint.sh"]
CMD ["sleep", "infinity"]
