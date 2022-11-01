FROM python:3.10 as local

RUN mkdir /app
WORKDIR /app

COPY ./requirements-dev.txt requirements-dev.txt
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements-dev.txt

CMD ./docker/run.sh

