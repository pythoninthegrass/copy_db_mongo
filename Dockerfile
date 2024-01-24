# syntax=docker/dockerfile:1.6

FROM mongo:7.0.4-jammy

ENV MONGO_INITDB_DATABASE=${DB_NAME}
ENV MONGO_INITDB_ROOT_USERNAME=${DB_USER:-root}
ENV MONGO_INITDB_ROOT_PASSWORD=${DB_PASS:-root}
ENV MONGO_PORT=${PORT:-27017}

WORKDIR /app

COPY ./backup/*.csv /app/backup

COPY entrypoint.sh .

EXPOSE 27017

# CMD ["sleep", "infinity"]
CMD ["./entrypoint.sh"]
