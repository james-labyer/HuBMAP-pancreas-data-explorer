#!/bin/bash

docker volume create config-data-test
docker run -d --name temp -v config-data-test:/data busybox sleep infinity
docker cp ./start/. temp:/data/
docker stop temp
docker compose -f docker-compose-test.yaml build
docker compose -f docker-compose-test.yaml up # --detach
# docker exec hubmap-pancreas-data-explorer-display-1 pytest
# docker rm temp
# docker stop hubmap-pancreas-data-explorer-display-1
# docker rm hubmap-pancreas-data-explorer-display-1
# docker volume rm config-data-test