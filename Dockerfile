FROM python:2.7

MAINTAINER Angelo Suinan <suinanangelo@gmail.com>

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python-dev
RUN apt-get install -y libjpeg-dev libz-dev
RUN apt-get -y autoremove

RUN mkdir /app
VOLUME /app
WORKDIR /app
ADD ./src/requirements.txt .
RUN pip install -r requirements.txt

