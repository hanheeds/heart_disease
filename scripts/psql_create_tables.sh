#!/bin/bash

PGPASSWORD=de300hardpassword
psql -U postgres -d heartdisease -f /tmp/create_tables.sql
