import json
import random

candidates = tuple('Candidate ' + str(i) for i in range(10))

ballots = tuple(
    random.sample(candidates, random.randrange(0, len(candidates)))
    for i in range(100)
)

with open('testballots.json', 'w') as f:
    json.dump(ballots, f, indent=4)