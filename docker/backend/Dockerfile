FROM python:3.6.7-slim-jessie
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y cmake
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip
RUN apt-get install -y python-imaging
RUN apt-get install -y mc
RUN apt-get install -y nano

RUN pip install pip --upgrade
RUN pip install virtualenv

RUN mkdir /backend
WORKDIR /backend
ADD examples/requirements/ /backend/requirements/
RUN pip install -r /backend/requirements/dev.txt
RUN pip install -r /backend/requirements/elastic_6x.txt
COPY . /backend/
RUN python /backend/setup.py develop
#RUN python /backend/examples/simple/manage.py books_create_test_data --settings=settings.docker
#RUN python /backend/examples/simple/manage.py search_index --rebuild -f --settings=settings.docker
