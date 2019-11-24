# Docker image to run solution for the Compass data challenge.

FROM continuumio/miniconda3:latest

RUN apt-get -y update
RUN apt-get -y upgrade

ADD . /usr/src/compass
WORKDIR /usr/src/compass
