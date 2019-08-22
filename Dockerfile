FROM python:3.7-slim

RUN apt-get -y update \
  && apt-get install -y jq dos2unix curl wget \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

RUN curl -s https://api.github.com/repos/ssllabs/ssllabs-scan/releases/latest | grep "browser_download_url.*-linux64.tgz" | cut -d '"' -f 4 | wget -qi - \
  && tar xvfz ssllabs-*.tgz \
  && rm -f ssllabs-*.tgz* \
  && chmod u+x ssllabs-scan

RUN pip install -r tests/requirements.txt \
    && dos2unix ./scripts/* \
    && chmod u+x ./scripts/*.sh