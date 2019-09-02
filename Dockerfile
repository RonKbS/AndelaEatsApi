FROM python:3.7-alpine

LABEL MAINTAINER="tolu.aina@andela.com"

LABEL application="eats-backend"

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --no-cache \
    build-base \
    git \
    libffi-dev \
    openssh-client \
    openssl-dev \
    python-dev 

# Required for building psycopg2-binary: https://github.com/psycopg/psycopg2/issues/684
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Install requirements
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install --upgrade -r /requirements.txt \
    && rm -r /root/.cache

RUN mkdir /usr/andelaeats
WORKDIR /usr/andelaeats
COPY . /usr/
