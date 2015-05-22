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

    # delete player_results associated with this tour
    c.execute("""DELETE FROM player_results USING matches
                    WHERE player_results.match = matches.id AND matches.tour = %s""",
              (tour_id,))

    # delete matches associated with this tour
    c.execute("DELETE FROM matches WHERE tour = %s",
              (tour_id,))

    # delete tour_registry of players for this tour
    c.execute("DELETE FROM tour_registry WHERE tour = %s",
              (tour_id,))

    # finally, delete tour from tours table
    c.execute("DELETE FROM tours WHERE id = %s",
              (tour_id,))

    DB.commit()
    DB.close()


def reportMatch(tour_id, winner, loser, draw=False):
    """Records the outcome of a single match between two players.

    Args:
      tour_id: the id of the tour this match was part of
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      draw: optional boolean indicating if this match was a draw (defaults to false)
    """
    # first, create the match
    match_id = createMatch(tour_id)

    DB, c = connect()

    # insert the results into the player_results table
    if draw:
        c.execute("INSERT INTO player_results (player, match, result) VALUES (%s, %s, %s)",
                  (winner, match_id, 'draw'))
        c.execute("INSERT INTO player_results (player, match, result) VALUES (%s, %s, %s)",
                  (loser, match_id, 'draw'))
    else:
        c.execute("INSERT INTO player_results (player, match, result) VALUES (%s, %s, %s)",
                  (winner, match_id, 'win'))
        c.execute("INSERT INTO player_results (player, match, result) VALUES (%s, %s, %s)",
                  (loser, match_id, 'loss'))
    DB.commit()
    DB.close()


# number of points assigned for a win or a draw (used to calculate score for player standings)
WIN_POINTS  = 1.0
DRAW_POINTS = 0.5


def opponentMatchScore(player_id, tour_id):
    """Returns the total score of all competitors this player has played in this tour

    Used to break ties in player standings.

    Args:
        player_id: player's unique id#
        tour_id: tour's unique id#
    Returns: the total score of all opponents
    """
    DB, c = connect()
    c.execute("""SELECT SUM(wins * %(winPoints)s + draws * %(drawPoints)s) AS oms
                FROM standings where tour = %(tour)s AND player IN
                    (SELECT player
                    FROM player_results
                    WHERE player != %(player)s AND match IN
                        (SELECT match
                        FROM player_results_with_tour
                        WHERE player = %(player)s AND tour = %(tour)s))""",
              {'winPoints': WIN_POINTS, 'drawPoints': DRAW_POINTS,
               'player': player_id, 'tour': tour_id})
    oms = c.fetchall()[0][0]
    DB.close()
    return oms


def playerStandings(tour_id):
    """Returns a list of the players and their win records, sorted by score.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.


    Args:
        tour_id: the unique id of the tour to use for report
    Returns:
      A list of tuples, each of which contains (id, name, wins, losses, draws, matches, score):
        (0)id: the player's unique id (assigned by the database)
        (1)name: the player's full name (as registered)
        (2)wins: the number of matches the player has won
        (3)losses: the number of matches the player has lost
        (4)draws: the number of matches involving the player which ended in a draw
        (5)matches: the number of matches the player has played
        (6)score: the score of this player
    """
    DB, c = connect()
    c.execute("""SELECT players.id, players.name,
                wins, losses, draws, played, (wins * %s) + (draws * %s) as score
                FROM players, standings
                WHERE players.id = standings.player AND standings.tour = %s
                ORDER BY score DESC""",
              (WIN_POINTS, DRAW_POINTS, tour_id))
    results = c.fetchall()
    DB.close()
    # check for ties and break ties with opponentMatchScore
    # sort using Insertion Sort because list is already mostly in order
    for i in range(1, len(results)):
        j = i
        while(j > 0 and results[j][6] >= results[j-1][6] and
              opponentMatchScore(results[j][0], tour_id) >
              opponentMatchScore(results[j-1][0], tour_id)):
            results[i-1], results[i] = results[i], results[i-1]
            j -= 1
    return results


def alreadyPlayed(player1, player2, tour_id):
    """Have these two players already played in this tour?

    Args:
        player1: player's unique id#
        player2: player's unique id#
        tour_id: tour's unique id#
    Returns:
        A boolean indicating if this would be a rematch
    """
    DB, c = connect()
    c.execute("""SELECT count(*) as gamesPlayed
                FROM player_results
                WHERE player = %s AND match IN
                    (SELECT match
                    FROM player_results_with_tour
                    WHERE player = %s AND tour = %s)""",
              (player1, player2, tour_id))
    gamesPlayed = c.fetchall()[0][0]
    DB.close()
    return gamesPlayed > 0


def swissPairings(tour_id):
    """Returns a list of pairs of players for the next round of a match in this tour.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.  Rematches are not allowed, so all pairings are new.


    Args:
        tour_id: this tour's unique id#
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings(tour_id)
    pairings = []

    for i in range(0, len(standings), 2):
        for j in range(i+1, len(standings)):
            if not alreadyPlayed(standings[i][0], standings[j][0], tour_id):
                # good pair found, swap into place then break the inner loop
                while j > i + 1:
                    standings[j-1], standings[j] = standings[j], standings[j-1]
                    j -= 1
                break
        pairings.append((standings[i][0],
                        standings[i][1],
                        standings[i+1][0],
                        standings[i+1][1]))
    return pairings
