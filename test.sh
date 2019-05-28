#!/bin/bash
docker-compose -f docker-compose.test.yml up connector_test

# Destroy containers
docker-compose -f docker-compose.test.yml down
