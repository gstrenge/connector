# Docker file to build container image based on 
# a miniconda image from the docker cloud
FROM continuumio/miniconda3
LABEL maintainer="Sebastian Arboleda <sebasarboleda22@gmail.com>"

LABEL Name=mqtt-connector Version=0.0.1

COPY environment.yml /

# Create conda environment based on yaml file
RUN conda env create -f environment.yml

ADD mqtt_connector /app
WORKDIR /app
CMD /bin/bash -c "source activate mqtt-connector && python subscriber.py"