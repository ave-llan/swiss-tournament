-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- To install
-- \i tournament.sql

CREATE DATABASE tournament;

--Connect to the newly created database
\c tournament;

CREATE TABLE players (
    id serial PRIMARY KEY,
    name text
);

CREATE TABLE matches (
    id serial PRIMARY KEY,
    player1 int REFERENCES players(id),
    player2 int REFERENCES players(id),
    winner  int REFERENCES players(id)
);
