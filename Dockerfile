FROM python:3.11

WORKDIR /app

RUN python -m pip install --upgrade pip \
    && pip install --quiet psycopg2 python-decouple faker

ENV PYTHONPATH=/app/src
