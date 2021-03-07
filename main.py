from collections import namedtuple
import json

WeightedBallot = namedtuple('WeightedBallot', ('weight', 'ranking'))

def get_droop_quota(seats: int, ballot_count: int) -> float:
    return ballot_count / (seats + 1)

def tally_votes(candidates, ballots) -> dict[str, int]:
    first_place_ballots = tuple(ballot.ranking[0] for ballot in ballots if len(ballot.ranking) > 0)
    tally = {candidate: first_place_ballots.count(candidate) for candidate in candidates}
    tally = {candidate: tally[candidate] for candidate in sorted(tally, key= lambda x: tally[x], reverse=True)}
    return tally

def stv(seats: int, candidates: tuple[str], ballots: tuple[tuple[str]], quota=get_droop_quota):
    ballots = tuple(WeightedBallot(1, ballot) for ballot in ballots)

    tally = tally_votes(candidates, ballots)    
    quota = quota(seats, sum(candidate_tally for candidate_tally in tally.values()))

    print(tally)
    

def main():
    with open('testballots.json') as f:
        ballots = json.load(f)
    ballots = tuple(tuple(ballot) for ballot in ballots)

    candidates = {c for ballot in ballots for c in ballot}
    candidates = tuple(sorted(candidates))

    stv(2, candidates, ballots)

if __name__ == '__main__': main()