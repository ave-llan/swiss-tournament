#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection and cursor."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    return DB, c


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).

    Returns:
      The ID number assigned to this player (as an int)
    """
    DB, c = connect()
    c.execute("INSERT INTO players (name) VALUES (%s) RETURNING id",
              (name,))
    id = c.fetchall()[0][0]
    DB.commit()
    DB.close()
    return id


def registerTour(name):
    """Adds a tour to the tournaments database.

    The database assigns a unique serial id number for the tour.

    Args:
      name: the tour's name (need not be unique).

    Returns:
      The ID number assigned to this tour (as an int)
    """
    DB, c = connect()
    c.execute("INSERT INTO tours (name) VALUES (%s) RETURNING id",
              (name,))
    id = c.fetchall()[0][0]
    DB.commit()
    DB.close()
    return id


def enrollPlayerInTour(player_id, tour_id):
    """Enrolls a player in a tour.

    The database assigns a unique serial id number for the tour.

    Args:
      player_id: the player's unique id (player must be registered in tournament).
      tour_id: the tour's unique id (tour must be registered in tournament)
    """
    DB, c = connect()
    c.execute("INSERT INTO tour_registry (player, tour) VALUES (%s, %s)",
              (player_id, tour_id))
    DB.commit()
    DB.close()


def createMatch(tour_id):
    """Creates a match for this tour

    ARGS:
      tour_id: the tour's unique id (tour must be registered in tournament)
    Returns:
      The ID number assigned to this match (as an int)
    """
    DB, c = connect()
    c.execute("INSERT INTO matches (tour) VALUES (%s) RETURNING id",
              (tour_id,))
    id = c.fetchall()[0][0]
    DB.commit()
    DB.close()
    return id


def countPlayers(tour_id):
    """Returns the number of players currently registered for this tour.

    Args:
      tour_id: the tour's unique id#.
    """
    DB, c = connect()
    c.execute("SELECT num FROM tour_enrollment WHERE id = %s",
              (tour_id,))
    enrollment_count = c.fetchall()[0][0]
    DB.close()
    return enrollment_count


def deleteTour(tour_id):
    """Remove all records associated with this tour from the database.

    Removes player_results results for matches that are part of this tour.
    Removes matches associated with this tour.
    Removes tour_registry of players for this tour
    Removes tour from tours table.

    Args:
      tour_id: the tour's unique id#.
    """
    DB, c = connect()
    c.execute("DELETE FROM player_results USING ")
    c.execute("DELETE FROM matches WHERE matches.tour = %s",
              (tour_id,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, c = connect()
    c.execute("SELECT * FROM standings")
    results = c.fetchall()
    DB.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, c = connect()
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)",
              (winner, loser))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairings = []
    for i in range(0, len(standings), 2):
        pairings.append((standings[i][0],
                        standings[i][1],
                        standings[i+1][0],
                        standings[i+1][1]))
    return pairings




