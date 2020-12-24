FROM docker.io/node:14.15

RUN apt-get update
RUN apt-get install -y mc
RUN apt-get install -y nano

RUN mkdir /frontend

RUN npx create-react-app my-app

ADD examples/frontend/package.json /frontend/
ADD . /frontend/

WORKDIR /frontend
RUN npm install
