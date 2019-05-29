#!/bin/bash

# This script will run local tests
docker-compose -f docker-compose.test.yml up connector_test

# Destroy containers
docker-compose -f docker-compose.test.yml down
