
# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
FROM continuumio/miniconda3

LABEL Name=mqtt-connector Version=0.0.1
EXPOSE 1883

COPY environment.yml /

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
RUN conda env create -f environment.yml

ADD mqtt_connector /app
WORKDIR /app
CMD /bin/bash -c "source activate mqtt-connector && python subscriber.py"