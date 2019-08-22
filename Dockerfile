FROM python:3.7-slim

RUN apt-get -y update \
  && apt-get install -y jq dos2unix curl wget \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY tests/requirements.txt /tmp

WORKDIR /tmp

RUN curl -s https://api.github.com/repos/ssllabs/ssllabs-scan/releases/latest | grep "browser_download_url.*-linux64.tgz" | cut -d '"' -f 4 | wget -qi - \
  && tar xvfz ssllabs-*.tgz \
  && rm -f ssllabs-*.tgz* \
  && mv ssllabs-scan /usr/local/bin

RUN pip install -r requirements.txt \
  && rm requirements.txt

WORKDIR /home