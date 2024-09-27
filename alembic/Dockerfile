FROM python:3.10-slim

RUN mkdir /alembic

WORKDIR /alembic

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .