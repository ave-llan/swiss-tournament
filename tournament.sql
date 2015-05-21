-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- To install
-- \i tournament.sql

CREATE DATABASE tournament;

-- Connect to the newly created database
\c tournament;

-- Registry of player id's and their names
CREATE TABLE players (
    id serial PRIMARY KEY,
    name text
);

-- Registry of tour id's and tour names
CREATE TABLE tours (
    id serial PRIMARY KEY,
    name text
);

-- Registry of players associated with each tour
CREATE TABLE tour_registry(
    player int REFERENCES players(id),
    tour int REFERENCES tours(id),
    PRIMARY KEY (player, tour)
);

-- assigns ID numbers to matches and associates them with a tournament
CREATE TABLE matches (
    id serial PRIMARY KEY,
    tour int REFERENCES tours(id)
);

-- for a match, shows whether this player won, lost, or if it was a draw
CREATE TYPE match_result AS ENUM ('win', 'loss', 'draw');
CREATE TABLE player_results (
    player int REFERENCES players(id),
    match int REFERENCES matches(id),
    result match_result
);


--A view showing number of players registered for each tour
CREATE VIEW tour_enrollment AS
    SELECT tours.id, tours.name as tourName, count(tour_registry.player) as num
    FROM tour_registry, tours
    WHERE tours.id = tour_registry.tour
    GROUP BY tours.id;



/*
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
*/

