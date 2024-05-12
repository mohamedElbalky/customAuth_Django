FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

EXPOSE 8000

COPY . .

RUN apt-get update && apt-get -y install gcc libpq-dev
RUN pip install --upgrade pip

RUN pip install -r requirements.txt



