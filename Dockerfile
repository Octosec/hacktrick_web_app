FROM python:3.5.2
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get upgrade && apt-get install -y lz4
RUN mkdir /code
RUN mkdir /code/logs/
RUN touch /code/logs/logfile
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD web/* /code/