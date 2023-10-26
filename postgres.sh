#!/bin/bash

docker pull postgres
# start ther postgres container
docker run -p 5432:5432 --name hearts-postgres -e POSTGRES_PASSWORD=de300hardpassword -v "$(pwd)"/scripts:/tmp -v "$(pwd)"/postgres_data:/var/lib/postgresql/data -d postgres
