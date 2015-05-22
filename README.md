# Swiss Tournament

 A Python module that keeps tracks of players and determines matches for a [Swiss tournament](http://en.wikipedia.org/wiki/Swiss-system_tournament) using the PostgreSQL database.

### Requirements
Python >2.7 and <3.0.

[psycopg2](http://initd.org/psycopg/)

[PostgreSQL](https://www.codefellows.org/blog/three-battle-tested-ways-to-install-postgresql)

### Set up

To create the tournament database and tables:

`>>> psql` initialize the interactive terminal for PostgreSQL

`>>> \i tournament.sql` execute the contents of tournament.sql to create database, tables, and views

`>>> \q` exit Psql interactive



### Usage

Start the Python interpreter and import the tournament.py module.

```
>>> python
>>> from tournament import *
```

###### 1. Register players for your tournament.

The database will assign a unique id# to each player which you will use to refer to this player going forward. `registerPlayer(name)` returns this id#, and you can capture it for future use like so:
```
>>> playerID = {}
>>> playerID['Rudy'] = registerPlayer('Rudy')
>>> playerID['Fido'] = registerPlayer('Fido')
```

###### 2. Register tours.

Tournaments can be made up of multiple tours. Again, the database assigns a unique id# to each tour when you register it using `registerTour(name)`. Capture it like this:
```
>>> tourID = {}
>>> tourID['agility'] = registerTour('agility')
>>> tourID['tug_of_war'] = registerTour('tug_of_war')
```

###### 3. Register players for tours.
Players can participate in multiple tours. Register them using `enrollPlayerInTour(player_id, tour_id)`. Note: The tournament module is currently configured to only work with an even number of players for each tour.
```
>>> enrollPlayerInTour(playerID['Rudy'], tourID['agility'])
>>> enrollPlayerInTour(playerID['Fido'], tourID['agility'])
```

###### 4. Record matches and get Swiss pairings.
Each player is paired with another player with an equal or nearly-equal win record using `swissPairings(tour_id)`. Rematches are avoided, so all pairings are new. The function returns a list of tuples, each of which contains (id1, name1, id2, name2).
```
>>> swissPairings(tourID['agility'])
[(1, 'Rudy', 2, 'Fido'),...]
```
Record the results of matches by using `reportMatch(tour_id, winner, loser, draw=False)`. If the match was a draw, you can supply the optional argument `draw=True`.
```
>>> reportMatch(tourID['agility'], playerID['Rudy'], playerID['Fido'])
```

###### 5. Check the standings for this tour.
`playerStandings(tour_id)` Returns a list of the players and their win, loss, draw records, sorted by total score. Currently wins are worth 1 point and draws are worth 0.5 points (configure these by changing the values of `WIN_POINTS` and `DRAW_POINTS` in the python file).
When two or more players have the same score, they are ranked according to the total score of players they have played against.

Returns a list of tuples, each of which contains (id, name, wins, losses, draws, matches, score).
```
>>> playerStandings(tourID['agility'])
[(1, 'Rudy', 3, 0, 1, 4, 3.5), ...]
```

