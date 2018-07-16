# MQTT-Connector [Work in Progress]
MQTT connector client that subscribes to topics sent by sensors and stores them in InfluxDB

## Introduction
Python ETL data pipeline MQTT client that subscribes to data sent by different sensors, converts the voltage measurements into it's respective units (Data Conversion Functions pending) and stores it in InfluxDB.  

## Dependencies and Setup
The main python app ```connector.py``` is containarized, built and run using docker. By doing this, all the dependencies are installed in a [conda](https://conda.io/docs/) environment running inside the container.

### Docker
Install [Docker](https://docs.docker.com/install/) 

### Docker-Compose
Install [Docker-Compose](https://docs.docker.com/compose/install/)

## Install and Run Locally
1. Clone the repo.
    ```git clone https://github.com/encresearch/mqtt-connector.git```

2. Build images and run containers. 
     We will be using our **dev** compose file.This file builds the docker image using the files on your local machine and not pulled from our docker hub (our current production container). That way, all your local changes will take place when building the container.
    ```docker-compose -f docker-compose.dev.yml up -d```
    This command will spin up both the ```mqtt-connector``` container and an ```influxdb``` container.

    To stop and remove containers, networks and images created by up (external volumes won't be removed).
    ```docker-compose -f docker-compose.dev.yml down```

## Overview and Usage
### MQTT Connector
The main python application of this repo. Receives raw measurements data from an MQTT Broker, calculates actual values and stores them into an InfluxDB container.
### InfluxDB
[InfluxDB](https://www.influxdata.com/) is used to store sensor data. Since this is a **dev** environment, there is no data persistency. To access the **CLI** (for debugging and testing purposes) thrugh a container, enter ```docker exec -it influxdb influx``` while the containers are running. For configuration and environment variables, see [here](https://hub.docker.com/_/influxdb/).

## Contributing
Pull requests and stars are always welcome. To contribute [create an issue](https://github.com/encresearch/data-assimilation/issues) explaining the bug or feature request, create a branch off this issue and submit a pull request.