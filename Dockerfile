FROM python:3.7-slim

RUN apt-get -y update \
  && apt-get install -y jq dos2unix curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

RUN pip install -r tests/requirements.txt \
    && dos2unix ./scripts/* \
    && chmod u+x ./scripts/*.sh