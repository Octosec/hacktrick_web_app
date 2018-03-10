FROM python:3.5.5
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get upgrade -y && apt-get install -y python-lz4 liblz4-tool apt-utils
RUN mkdir /code
RUN mkdir /code/logs/
RUN touch /code/logs/logfile
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
CMD bash -c "python web/manage.py migrate && uwsgi --http 0.0.0.0:8000 web.wsgi"
ADD web /code/web