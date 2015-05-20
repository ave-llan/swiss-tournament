# Swiss Tournament

 A Python module that keeps tracks of players and determines matches for a [Swiss tournament](http://en.wikipedia.org/wiki/Swiss-system_tournament) using the PostgreSQL database.

### Requirements
Python >2.7 and <3.0.

[PostgreSQL](https://www.codefellows.org/blog/three-battle-tested-ways-to-install-postgresql)

### Usage

First, create the tournament database and tables:

`psql` initialize the interactive terminal for PostgreSQL

`\i tournament.sql` execute the contents of tournament.sql to create database and tables

`\q` exit Psql interactive
