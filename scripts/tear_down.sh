#!/usr/bin/env bash

./script_teardown.sh
docker-compose up --build -d mysql
docker-compose up --build --exit-code-from build_index build_index
