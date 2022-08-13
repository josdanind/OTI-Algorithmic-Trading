#!/bin/bash

echo "oti-bot container: remove"
docker rm oti-backend oti-db
docker image rm oti_backend
docker volume rm -f oti_postgres_data 

exit