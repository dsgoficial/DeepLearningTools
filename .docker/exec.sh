#!/usr/bin/env bash

docker exec -t deeplearningtools-testing-env sh -c "cd /github_repo && qgis_testrunner.sh tests.test_image_processing"