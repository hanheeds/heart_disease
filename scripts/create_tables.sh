#!/bin/bash

docker exec -d hearts-postgres /bin/bash /tmp/psql_create_tables.sh
