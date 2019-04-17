# Connector: Sensor Data Gathering API Service
[![Build Status](https://travis-ci.com/encresearch/mqtt-connector.svg?branch=master)](https://travis-ci.com/encresearch/mqtt-connector)

Python application API that receives raw measurements data from an MQTT Broker, and stores it in InfluxDB.

## Introduction
Python ETL data pipeline MQTT client that subscribes to sensor data sent by different [publishers](https://github.com/encresearch/publisher) and stores it in InfluxDB. The main python app ```connector``` is containarized, built and run using docker. All the dependencies are installed in a [conda](https://conda.io/docs/) environment running inside the container.

This service is part of our [Earthquake Data Assimilation System](https://github.com/encresearch/data-assimilation-system).

## Dependencies and Setup
The main python app ```connector``` is containarized, built and run using docker. By doing this, all the dependencies are installed in a [conda](https://conda.io/docs/) environment running inside the container.

### Docker and Docker-Compose
Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/).

## Install and Run Locally
1. Clone the repo.
    ```git clone https://github.com/encresearch/mqtt-connector.git```

2. Build images and run containers.
    The ```docker-compose.dev.yml``` file builds the docker image using the files on your local machine and not pulled from our docker hub (our current production container). That way, all your local changes will take place when building the container.
    ```docker-compose -f docker-compose.dev.yml up -d```
    
    
    The ```docker-compose.dev.yml``` file builds the docker image using the files on your local machine and not pulled from our docker hub (our current production container). That way, all your local changes will take place when building the container.

To stop and remove containers, networks and images created by up (external volumes won't be removed).
```docker-compose -f docker-compose.dev.yml down```.

## Run Local Tests
PyTest. [Pending]

## Contributing
Pull requests and stars are always welcome. To contribute, please fetch, create an issue explaining the bug or feature request, create a branch off this issue and submit a pull request.
