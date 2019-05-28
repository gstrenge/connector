#!/bin/bash

# This script will run local tests
docker-compose -f docker-compose.test.yml up

# Destroy containers
docker-compose -f docker-compose.test.yml down
