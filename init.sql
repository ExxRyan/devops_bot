CREATE DATABASE DB_DATABASE;

CREATE USER DB_REPL_USER WITH REPLICATION ENCRYPTED PASSWORD 'DB_REPL_PASSWORD';

\connect DB_DATABASE;

CREATE TABLE IF NOT EXISTS emails(
        id SERIAL PRIMARY KEY,
        email VARCHAR (255) NOT NULL
    );

CREATE TABLE IF NOT EXISTS numbers(
        ID SERIAL PRIMARY KEY,
        number VARCHAR (50) NOT NULL
    );

INSERT INTO emails (email) VALUES ('sarah.connor@skynet.com'), ('clark.kent@dailyplanet.com');
INSERT INTO numbers (number) VALUES ('+7 (123) 456-78-90'), ('8-123-456-78-90');