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

2. 

3. Build images and run containers. 
     We will be using our **dev** compose file.This file ensures that the ```mqtt-connector``` image is built using the files on your local machine and not pulled from our docker hub (our current production container). That way, all your local changes will take place when building the container.
    ```docker-compose -f docker-compose.dev.yml up -d```
    You can visit http://localhost to checkout grafana webapp

Docker helps ensure that, besides the ```mqtt-connector``` container, all other containers are identical to those on our production environments, as they're pulled from our Docker Hub cloud.

To stop and remove containers, networks and images created by up (external volumes won't be removed). **We recommend doing this and rebuilding images (```up```) every time testing is performed, making sure all the pulled images are the latest builds on our hub.**
```docker-compose -f docker-compose.dev.yml down```

## Testing
Tests are performed automatically everytime changes are pushed. To test locally, 

## Overview and Usage
### MQTT Connector
The main python application of this repo. Receives raw measurements data from an MQTT Broker, calculates actual values and stores them into an InfluxDB container.
### InfluxDB
[InfluxDB](https://www.influxdata.com/) will be used to store our incoming sensor data. For data persistency, a docker volume ```influx_data``` is created. To access the **CLI** thorugh a container, enter ```docker exec -it influxdb influx```. For configuration and environment variables, see [here](https://hub.docker.com/_/influxdb/).
### Grafana
[Grafana](https://grafana.com/) will be used as web application for data visualization. It runs on port 3000 on the container, which is then mapped to port 80 on the host. For data persistency, a volume named ```grafana_data``` is created.
**Configuration**
The configuration file can be found in the ```etc/``` directory. For more info, see [grafana configuration docs](http://docs.grafana.org/installation/configuration/).
### Telegraf
Plugin-driven server agent for collecting and reporting metrics about the hosting server. Data is also stored in InfluxDB. Configuration file can also be found in the ```etc/``` directory.
### Data Analysis [Work in Progress]
Flask microservice that makes continuous queries to the InfluxDB and performs analysis and predictions based on the data. Repo can be found [here](https://github.com/encresearch/data-analysis)

## Contributing
Pull requests and stars are always welcome. To contribute [create an issue](https://github.com/encresearch/data-assimilation/issues) explaining the bug or feature request, create a branch off this issue and submit a pull request.