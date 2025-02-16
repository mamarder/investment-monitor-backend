FROM python:3.12-alpine

RUN apk update && apk add bash

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000
