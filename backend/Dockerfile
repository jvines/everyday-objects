FROM python:3.12-slim

LABEL authors="jayvains"

ARG PUID
ARG PGID

RUN groupadd -g ${PGID} mygroup && \
    useradd -u ${PUID} -g mygroup -m myuser

RUN apt-get update && apt-get upgrade --yes && \
    apt-get install libpq-dev gcc --yes && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY --chown=myuser:mygroup ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY --chown=myser:mygroup ./ /code/app

USER myuser

CMD ["fastapi", "dev", "/code/app/main.py", "--host", "0.0.0.0", "--port", "80"]