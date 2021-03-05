#!/usr/bin/env bash

docker-compose up -d
echo 'Wait 10 seconds'
sleep 10
echo 'Installation of the plugin'
docker exec -it deeplearningtools-testing-env sh -c "qgis_setup.sh DeepLearningTools"
echo 'Containers are running'