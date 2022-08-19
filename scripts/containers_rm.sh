#!/bin/bash

echo "oti container: remove"

docker rm bot-api bot-db app-proxy
docker image rm oti_bot-api
docker volume rm -f oti_postgres_data

exit