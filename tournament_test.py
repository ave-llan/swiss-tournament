from tournament import *


# register players
dogs = ['Rudy', 'Jynx', 'Howie', 'Kip', 'August', 'Popeye']
dogIDs = []
for dog in dogs:
    dogIDs.append((registerPlayer(dog), dog))

# dogIDs
#[(1, 'Rudy'), (2, 'Jynx'), (3, 'Howie'), (4, 'Kip'), (5, 'August'), (6, 'Popeye')]


# register tour events
events = ['Agility', 'Frisbee', 'Retrieval', 'Obedience', 'Tug of War']
eventIDs = []
for event in events:
    eventIDs.append((registerTour(event), event))

# eventIDs
# [(1, 'Agility'), (2, 'Frisbee'), (3, 'Retrieval'), (4, 'Obedience'), (5, 'Tug of War')]


# register all dogs for all tours
for event in eventIDs:
    for dog in dogIDs:
        enrollPlayerInTour(dog[0], event[0])

# test countPlayers(tour_id)
for event in eventIDs:
    if countPlayers(event[0]) != len(dogs):
        raise ValueError("countPlayers(" + tour_id + ") incorrectly returned " + countPlayers(event[0]))


# test reportMatch

# ROUND 1
# Rudy draws with Jynx
reportMatch(eventIDs[0][0], dogIDs[0][0], dogIDs[1][0], draw=True)
# Howie beats Kip
reportMatch(eventIDs[0][0], dogIDs[2][0], dogIDs[3][0])
# August eats Popeye
reportMatch(eventIDs[0][0], dogIDs[4][0], dogIDs[5][0])


# ROUND 2
# Howie beats August
reportMatch(eventIDs[0][0], dogIDs[2][0], dogIDs[4][0])
# Rudy beats Kip
reportMatch(eventIDs[0][0], dogIDs[0][0], dogIDs[3][0])
# Jynx eats Popeye
reportMatch(eventIDs[0][0], dogIDs[1][0], dogIDs[5][0])

# CHECKPOINT check Swiss Pairings
expectedPairings = [dogIDs[2] + dogIDs[0], dogIDs[1] + dogIDs[4], dogIDs[3] + dogIDs[5]]
actualPairings = swissPairings(eventIDs[0][0])

for i in range(len(expectedPairings)):
    if expectedPairings[i][0] != actualPairings[i][0] and expectedPairings[i][0] != actualPairings[i][2]:
        raise ValueError('returned swissPairings do not match')
    if expectedPairings[i][2] != actualPairings[i][0] and expectedPairings[i][2] != actualPairings[i][2]:
        raise ValueError('returned swissPairings do not match')
print 'swissPairings passed tests'


# ROUND 3
# Rudy draws with Howie
reportMatch(eventIDs[0][0], dogIDs[2][0], dogIDs[0][0], draw=True)
# Jynx beats August
reportMatch(eventIDs[0][0], dogIDs[1][0], dogIDs[4][0])
# Kip eats Popeye
reportMatch(eventIDs[0][0], dogIDs[3][0], dogIDs[5][0])

# ROUND 4
# Howie beats Jynx
reportMatch(eventIDs[0][0], dogIDs[2][0], dogIDs[1][0])
# Rudy beats Popeye
reportMatch(eventIDs[0][0], dogIDs[0][0], dogIDs[5][0])
# Kip beats August
reportMatch(eventIDs[0][0], dogIDs[3][0], dogIDs[4][0])


# CHECKPOINT check standings

expectedStandings = [(dogIDs[2][0], 3.5), (dogIDs[0][0], 3.0), (dogIDs[1][0], 2.5),
                  (dogIDs[3][0], 2.0), (dogIDs[4][0], 1.0), (dogIDs[5][0], 0.0)]
standings = playerStandings(eventIDs[0][0])
for i in range(len(expectedStandings)):
    if expectedStandings[i][0] != standings[i][0] or expectedStandings[i][1] != standings[i][6]:
        raise ValueError('returned standings do not match')
print 'playerStandings passed tests'

