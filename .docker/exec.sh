#!/usr/bin/env bash

docker exec -it deeplearningtools-testing-env sh -c "cd /tests_directory && qgis_testrunner.sh tests.test_image_processing"