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


/**********
*
*  Tables
*
***********/

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

-- type used in player_results
CREATE TYPE match_result AS ENUM ('win', 'loss', 'draw');

-- for a match, shows whether this player won, lost, or if it was a draw
CREATE TABLE player_results (
    player int REFERENCES players(id),
    match int REFERENCES matches(id),
    result match_result
);


/**********
*
*  Views
*
***********/

-- shows number of players registered for each tour
CREATE VIEW tour_enrollment AS
    SELECT tours.id, tours.name as tourName, count(tour_registry.player) as num
    FROM tour_registry, tours
    WHERE tours.id = tour_registry.tour
    GROUP BY tours.id;

-- adds tour column to player_results
CREATE VIEW player_results_with_tour AS
    SELECT player, matches.tour, player_results.match, result
    FROM player_results, matches
    WHERE player_results.match = matches.id;

-- shows number of wins by player for each tour
CREATE VIEW player_wins AS
    SELECT tour_registry.player, tour_registry.tour, count(result) AS wins
    FROM tour_registry LEFT JOIN player_results_with_tour
        on tour_registry.player = player_results_with_tour.player
        AND tour_registry.tour =  player_results_with_tour.tour
        AND result = 'win'
    GROUP BY tour_registry.player, tour_registry.tour
    ORDER BY tour_registry.tour, tour_registry.player;

-- shows number of losses by player for each tour
CREATE VIEW player_losses AS
    SELECT tour_registry.player, tour_registry.tour, count(result) AS losses
    FROM tour_registry LEFT JOIN player_results_with_tour
        on tour_registry.player = player_results_with_tour.player
        AND tour_registry.tour =  player_results_with_tour.tour
        AND result = 'loss'
    GROUP BY tour_registry.player, tour_registry.tour
    ORDER BY tour_registry.tour, tour_registry.player;

-- shows number of draws by player for each tour
CREATE VIEW player_draws AS
    SELECT tour_registry.player, tour_registry.tour, count(result) AS draws
    FROM tour_registry LEFT JOIN player_results_with_tour
        on tour_registry.player = player_results_with_tour.player
        AND tour_registry.tour =  player_results_with_tour.tour
        AND result = 'draw'
    GROUP BY tour_registry.player, tour_registry.tour
    ORDER BY tour_registry.tour, tour_registry.player;

-- combination of wins, losses, draws also with total games played
CREATE VIEW standings AS
    SELECT player_wins.player, player_wins.tour, wins, losses, draws, wins + losses + draws AS played
    FROM player_wins JOIN player_losses
        on player_wins.player = player_losses.player AND player_wins.tour = player_losses.tour
        JOIN player_draws
        on player_wins.player = player_draws.player AND player_wins.tour = player_draws.tour;
