# Swiss Tournament

 A Python module that keeps tracks of players and determines matches for a [Swiss tournament](http://en.wikipedia.org/wiki/Swiss-system_tournament) using the PostgreSQL database.

### Requirements
Python >2.7 and <3.0.

[psycopg2](http://initd.org/psycopg/)

[PostgreSQL](https://www.codefellows.org/blog/three-battle-tested-ways-to-install-postgresql)

### Set up

To create the tournament database and tables:

`psql` initialize the interactive terminal for PostgreSQL

`\i tournament.sql` execute the contents of tournament.sql to create database, tables, and views

`\q` exit Psql interactive

### Usage

On the command line, import the tournament.py module's functions:
`python`
`from tournament import *`

####Register players for your tournament.
`registerPlayer('Rudy')`
The database will assign a unique id# to each player which you will use to refer to this player going forward. `registerPlayer(name)` returns this id#, and you should probably capture it for future use like so:
```
playerDictionary = {}
playerDictionary['Rudy'] = registerPlayer('Rudy')
```
