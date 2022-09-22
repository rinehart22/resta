FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN pip install --upgrade pip

RUN apt-get update
RUN apt-get -y install git

WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code/