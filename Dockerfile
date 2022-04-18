FROM ubuntu:latest
FROM python:3.8
ENV GCR_APPLICATION=1
#ENV REDISHOST="10.70.99.140"
RUN mkdir /code

WORKDIR /code

ADD . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8000

#Entrypoint to run docker-entrypoit.sh file
ADD docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod a+x /code/docker-entrypoint.sh
ENTRYPOINT ["/code/docker-entrypoint.sh"]
# RUN python manage.py loaddata /code/db.json

CMD gunicorn --bind=0.0.0.0 --log-level "debug" --workers 4 --timeout 900 limoucloud_backend.wsgi
