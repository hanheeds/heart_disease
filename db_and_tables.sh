#!/bin/bash

# create db and tables
bash ./scripts/create_db.sh
bash ./scripts/create_tables.sh

### can go into docker container to confirm db and tables were correctly made using these commands
# docker exec -it hearts-postgres /bin/bash
# PGPASSWORD=de300hardpassword
# psql -U postgres -d heartdisease