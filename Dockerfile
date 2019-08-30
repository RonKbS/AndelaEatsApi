FROM python:3.7-alpine

LABEL MAINTAINER="dominic.motuka@gmail.com"

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

ARG WORKDIR=/usr/src/app

RUN mkdir $WORKDIR

ADD . /usr/src/

WORKDIR $WORKDIR

CMD ["gunicorn", "run:app", "-b", "0.0.0.0:4070", "--workers=5", "--threads=5", "--timeout", "360"]
