# Docker file to build container image based on 
# a miniconda image from the docker cloud
FROM continuumio/miniconda3
LABEL maintainer="Sebastian Arboleda <sebasarboleda22@gmail.com>" Name=mqtt-connector Version=0.0.1

COPY environment.yml /

# Create conda environment based on yaml file
RUN conda env create -f environment.yml
COPY ./app /app
WORKDIR /app
CMD /bin/bash -c "source activate mqtt-connector && python -u subscriber.py"

# To build:
# docker build -t mqtt-connector .

# To run:
# docker run -v --restart unless-stopped --name grafana1 grafana/grafana

# To debug locally:
# docker run -v ./mqtt_connector:/app --restart unless-stopped --name grafana1 grafana/grafana