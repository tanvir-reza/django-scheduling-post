FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app


RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE ${WEB_PORT}