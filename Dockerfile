# Docker image to run solution for the Compass data challenge.

FROM ubuntu:18.04

RUN apt-get update
RUN apt-get upgrade

ADD . /usr/src/compass
WORKDIR /usr/src/compass
