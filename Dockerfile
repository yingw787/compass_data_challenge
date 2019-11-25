# Docker image to run solution for the Compass data challenge.

FROM continuumio/anaconda3:latest

RUN apt-get -y update
RUN apt-get -y upgrade

ADD . /usr/src/compass
WORKDIR /usr/src/compass

RUN conda env create -f environment.yaml

ENV PATH /opt/conda/envs/compass/bin:$PATH
ENV CONDA_DEFAULT_ENV compass

RUN chmod 755 entrypoint.sh

ENTRYPOINT [ "/usr/src/compass/entrypoint.sh" ]
