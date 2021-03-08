#!/usr/bin/env bash

docker-compose up -d --build
echo 'Wait 10 seconds'
sleep 10
echo 'Installation of the plugin'
docker exec -t deeplearningtools-testing-env sh -c "qgis_setup.sh DeepLearningTools"
echo 'Containers are running'