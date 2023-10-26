#!/bin/bash

PGPASSWORD=de300hardpassword
psql -U postgres -f /tmp/create_db.sql

