# Docker image to run solution for the Compass data challenge.

FROM ubuntu:18.04

RUN apt-get update
RUN apt-get upgrade

RUN apt-get -y install iputils-ping
