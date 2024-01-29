# syntax=docker/dockerfile:1.6

FROM mongo:7.0.4-jammy

ARG USERNAME=appuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

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

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

USER $USERNAME

EXPOSE ${PORT:-27017}

ENTRYPOINT [ "/app/entrypoint.sh" ]
