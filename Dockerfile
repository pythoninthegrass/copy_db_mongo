# syntax=docker/dockerfile:1.6

FROM mongo:7.0.4-jammy

ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER:-root}
ENV DB_PASS=${DB_PASS:-toor}
ENV PORT=${PORT:-27017}

RUN apt-get update && apt-get install --no-install-recommends -y \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./backup/* ./backup/
COPY entrypoint.sh .

EXPOSE ${PORT:-27017}

ENTRYPOINT [ "/app/entrypoint.sh" ]
