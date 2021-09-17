# Move to default python container, because it easier and faster to change python versions
# and it has gdal version(2.4) supported by Django 3.
FROM python:3.9.6-slim-buster

WORKDIR /app
ENV C_FORCE_ROOT=True \
  DJANGO_SETTINGS_MODULE=config.settings.deploy

### Dependencies:
# build-essential: dependencies for building Python packages
# openssh-client: to download deps from private repos
# git: to install python deps for github
# mime-support for `uwsgi --http` to serve assets files
# curl: to download rattus

RUN apt-get update && \
  apt-get install -y \
  build-essential \
  git \
  mime-support \
  openssh-client \
  curl && \
  ### Install tools for python
  pip install -U --no-cache-dir pip setuptools wheel && \
  ### Install rattus
  curl -LSs -o /usr/bin/rattus \
  https://github.com/Saritasa/rattus/releases/download/0.3.0/rattus-linux-amd64 && \
  chmod +x /usr/bin/rattus && \
  ### Cleaning up unused files
  apt-get purge -yqq --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
  rm -rf /var/lib/apt/lists/*


### Django environment variable. Used for settings and requirements installation
ARG REQUIREMENTS_FILE=development
ENV REQUIREMENTS_FILE=${REQUIREMENTS_FILE}

### Install requirements
COPY requirements/${REQUIREMENTS_FILE}.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

### Add source code to container
COPY . /app/
