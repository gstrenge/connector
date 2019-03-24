# MQTT-Connector: Sensor Data Acquisition, Visualization and Monitoring Platform
<<<<<<< HEAD
[![Build Status](https://travis-ci.com/encresearch/mqtt-connector.svg?branch=master)](https://travis-ci.com/encresearch/mqtt-connector)
Python application that receives raw measurements data from an MQTT Broker, and stores it in InfluxDB.
=======
This repository contains the docker-compose and configuration files for the deployment of the Data Acquisition, Visualization and Monitoring Platform. It makes use of a ```connector``` client in charge of receiving and storing the sensors' data into an [InfluxDB](https://www.influxdata.com/). Additionally, [Grafana](https://grafana.com/) is served as a web application for both data visualization and monitoring. The current database name used is ```testing```, the 'measurement' is ```measurements```, and the 'field' is ```mV```.
>>>>>>> d39f182... Update README.md

## Introduction
Python ETL data pipeline MQTT client that subscribes to sensor data sent by different [publishers](https://github.com/encresearch/mqtt-publisher) and stores it in InfluxDB. The main python app ```connector``` is containarized, built and run using docker. All the dependencies are installed in a [conda](https://conda.io/docs/) environment running inside the container.

## Dependencies and Setup
The main python app ```connector``` is containarized, built and run using docker. By doing this, all the dependencies are installed in a [conda](https://conda.io/docs/) environment running inside the container.

### Docker and Docker-Compose
Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/).

## Install and Run Locally
1. Clone the repo.
    ```git clone https://github.com/encresearch/mqtt-connector.git```

2. Build images and run containers.
<<<<<<< HEAD
    The ```docker-compose.dev.yml``` file builds the docker image using the files on your local machine and not pulled from our docker hub (our current production container). That way, all your local changes will take place when building the container.
=======


    For **production environments** run: 
    
    ```docker-compose -f docker-compose.yml up -d```
    
    
    This file includes the creation of persistent [docker volumes](https://docs.docker.com/storage/volumes/) and contains its own database containers.
    
    For **dev environments** run:
    
>>>>>>> d39f182... Update README.md
    ```docker-compose -f docker-compose.dev.yml up -d```
    
    
    The ```docker-compose.dev.yml``` file builds the docker image using the files on your local machine and not pulled from our docker hub (our current production container). That way, all your local changes will take place when building the container.

To stop and remove containers, networks and images created by up (external volumes won't be removed).
```docker-compose -f docker-compose.dev.yml down```.

## Run Local Tests
PyTest. [Pending]

## Contributing
Pull requests and stars are always welcome. To contribute, please fetch, create an issue explaining the bug or feature request, create a branch off this issue and submit a pull request.
