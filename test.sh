#!/bin/bash
docker-compose -f docker-compose.test.yml up

# Destroy containers
docker-compose -f docker-compose.test.yml down
