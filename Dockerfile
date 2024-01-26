# syntax=docker/dockerfile:1.6

FROM mongo:7.0.4-jammy

ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER:-root}
ENV DB_PASS=${DB_PASS:-toor}
ENV PORT=${PORT:-27017}

WORKDIR /app

COPY ./backup/*.csv ./backup/
COPY entrypoint.sh .

EXPOSE ${PORT:-27017}

ENTRYPOINT [ "/app/entrypoint.sh" ]
