from typing import NamedTuple
import json

class WeightedBallot(NamedTuple):
    weight: float
    ranking: tuple[str]

    def remove_candidate(self, candidate):
        return WeightedBallot(self.weight, tuple(c for c in self.ranking if c != candidate))

    def remove_winner(self, winner, weight_frac):
        if len(self.ranking) > 0 and self.ranking[0] == winner:
            return WeightedBallot(self.weight * weight_frac, self.ranking).remove_candidate(winner)
        return self

class WeightedBallots(NamedTuple):
    ballots: tuple[WeightedBallot]

    def remove_candidate(self, candidate):
        return WeightedBallots(
            tuple(ballot.remove_candidate(candidate) for ballot in self.ballots)
        )

    def remove_winner(self, winner, weight_frac):
        return WeightedBallots(
            tuple(ballot.remove_winner(winner, weight_frac) for ballot in self.ballots)
        )

    def tally_first_place(self, candidates):
        '''Return a dict tallying the first choice votes for each candidate.'''
        first_place_ballots = tuple(ballot.ranking[0] for ballot in self.ballots if len(ballot.ranking) > 0)
        tally = {candidate: first_place_ballots.count(candidate) for candidate in candidates}
        tally = {candidate: tally[candidate] for candidate in sorted(tally, key= lambda x: tally[x], reverse=True)}
        return tally


def get_droop_quota(seats: int, ballot_count: int) -> float:
    return ballot_count / (seats + 1)


def remove_candidate(candidate: str, ballots: tuple[WeightedBallot]):
    '''Remove a candidate from all ballots in a tuple of WeightedBallot'''
    return tuple(ballot.remove_candidate(candidate) for ballot in ballots)

def remove_winner(winner: str, vote_frac: int, ballots: tuple[WeightedBallot]):
    '''remove_candidate but also lower the weight for ballots for candidate'''
    return tuple(ballot.remove_winner(winner, vote_frac) for ballot in ballots)


def stv(seats: int, candidates: tuple[str], ballots: tuple[tuple[str]], quota=get_droop_quota):
    ballots = WeightedBallots(tuple(WeightedBallot(1, ballot) for ballot in ballots))

    #while True:
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
    tally = ballots.tally_first_place(candidates)
    quota = quota(seats, sum(candidate_tally for candidate_tally in tally.values()))

    if max(tally.values()) > quota:
        pass
    else:
        pass

    nb = ballots.remove_winner("Candidate 7", 0.5)
    for b in nb.ballots[:5]:
        print(b.weight, b.ranking)
    

def main():
    with open('testballots.json') as f:
        ballots = json.load(f)
    ballots = tuple(tuple(ballot) for ballot in ballots)

    candidates = {c for ballot in ballots for c in ballot}
    candidates = tuple(sorted(candidates))

    stv(2, candidates, ballots)

if __name__ == '__main__': main()