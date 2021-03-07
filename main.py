from collections import namedtuple
import json

WeightedBallot = namedtuple('WeightedBallot', ('weight', 'ranking'))

def get_droop_quota(seats: int, ballot_count: int) -> float:
    return ballot_count / (seats + 1)

def tally_first_place_votes(candidates: tuple[str], ballots) -> dict[str, int]:
    '''Return a dict tallying the first choice votes for each candidate.'''
    first_place_ballots = tuple(ballot.ranking[0] for ballot in ballots if len(ballot.ranking) > 0)
    tally = {candidate: first_place_ballots.count(candidate) for candidate in candidates}
    tally = {candidate: tally[candidate] for candidate in sorted(tally, key= lambda x: tally[x], reverse=True)}
    return tally

def stv(seats: int, candidates: tuple[str], ballots: tuple[tuple[str]], quota=get_droop_quota):
    ballots = tuple(WeightedBallot(1, ballot) for ballot in ballots)

    while True:
        # Round step order should be something like
        # 1. Tally
        # 2. Eliminate a candidate
        # 3. Repeat until seats filled or no more candidates
        #
        # Step 2 (Eliminate a candidate) means both checking for winners, and
        # eliminating the weakest candidate if no candidates have reached
        # the required quota.  Most complicated parts are probably
        # redistributing votes from winners and picking picking weakest
        # candidates
        # Want to attempt to keep it as close to functional as possible so that
        # round history can be recorded
    tally = tally_first_place_votes(candidates, ballots)
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