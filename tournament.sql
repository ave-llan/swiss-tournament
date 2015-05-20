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
    winner int REFERENCES players(id),
    loser int REFERENCES players(id)
);

--A view showing number of wins for each player
CREATE VIEW win_record AS
    SELECT players.id, count(matches.winner) as num
    FROM players LEFT JOIN matches
        on players.id = matches.winner
    GROUP BY players.id
    ORDER BY num DESC;

--A view showing number of losses for each player
CREATE VIEW loss_record AS
    SELECT players.id, count(matches.loser) as num
    FROM players LEFT JOIN matches
        on players.id = matches.loser
    GROUP BY players.id
    ORDER BY num DESC;

--A view of players id, name, wins, and games played sorted by number of wins
CREATE VIEW standings AS
    SELECT players.id, players.name, win_record.num AS wins, win_record.num + loss_record.num AS played
    FROM players, win_record, loss_record
    WHERE players.id = win_record.id AND players.id = loss_record.id
    ORDER BY win_record.num DESC;

