![CONNECTOR](./docs/connector_logo.png)
# CONNECTOR - Sensor Data Gathering API Service
[![Build Status](https://travis-ci.com/encresearch/connector.svg?branch=master)](https://travis-ci.com/encresearch/connector)

Python application API that receives raw measurements data from an MQTT Broker, and stores it in InfluxDB.

Connector is a Python ETL data pipeline MQTT client that subscribes to sensor data sent by different [publishers](https://github.com/encresearch/publisher) and stores it in InfluxDB.

Connector also notifies our Calculator Microservice upon storing raw data within InfluxDB, allowing for Calculator to convert raw data into correct units

This service is part of our [Earthquake Data Assimilation System](https://github.com/encresearch/data-assimilation-system).

## Getting Started
These instructions are to get connector up and running in your local development environment.

The main python app ```connector``` is containarized, built and run using [docker compose](https://docs.docker.com/compose/). By doing this, all the dependencies are installed in a [conda](https://conda.io/docs/) environment running inside the container. Running docker compose will also fire up both an [InfluxDB](https://www.influxdata.com/products/influxdb-overview/) and an [Eclipse Mosquitto](https://mosquitto.org/) service.

### Install and Run Locally

**Install Docker CE and Docker Compose**

Make sure to follow the online instructions to install [Docker CE](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/) before trying to install and run ```connector```.

**Run Locally**

Clone the repo:

```
$ git clone git@github.com:encresearch/connector.git
```

Cd to the connector repo:

```
$ cd connector
```

Start services with docker-compose:

```
$ docker-compose -f docker-compose.dev.yml up
```

The ```docker-compose.dev.yml``` file builds the docker image using the files on your local machine and not pulled from our docker hub (our current production container). That way, all your local changes will take place when building the container.

**Run Local Tests**

We are using [pytest](https://docs.pytest.org/en/latest/) also inside a container. You can run local tests via:

```
$ chmod u+x test.sh #Make sure file is executable
$ ./test.sh
```

To stop and remove containers, networks and images created by up (external volumes won't be removed).
```docker-compose -f docker-compose.dev.yml down```.

## Contributing
Pull requests and stars are always welcome. To contribute, please fetch, create an issue explaining the bug or feature request, create a branch off this issue and submit a pull request.
