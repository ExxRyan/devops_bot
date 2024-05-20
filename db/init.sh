#!/bin/bash

psql --username "${POSTGRES_USER:-postgres}"  <<-EOSQL
    \c ${DB_NAME:-tg_bot};

    CREATE TABLE emails(
        id SERIAL PRIMARY KEY,
        email VARCHAR (255) NOT NULL
    );

    CREATE TABLE numbers(
        ID SERIAL PRIMARY KEY,
        number VARCHAR (50) NOT NULL
    );

    INSERT INTO emails (email) VALUES ('sarah.connor@skynet.com'), ('clark.kent@dailyplanet.com');

    INSERT INTO numbers (number) VALUES ('+7 (123) 456-78-90'), ('8-123-456-78-90');

    CREATE USER ${DB_REPL_USER:-repl_user} WITH REPLICATION ENCRYPTED PASSWORD '${DB_REPL_PASSWORD:-repl_password}';
EOSQL
