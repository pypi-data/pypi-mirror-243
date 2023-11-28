from math import factorial
from itertools import chain, combinations
import logging
import random


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


class ShapleyGame:
    def __init__(self, num_players: int, coal_scores: dict = None):
        """Create a synthetic TU Game with its Shapley value solution

        Args:
            num_players (int): number of players in the TU-game
            coal_scores (dict[frozenset, int], optional): Coalition scores, if already known. Defaults to None.
        """
        self.num_players = num_players
        self.coal_scores = coal_scores

        if self.coal_scores is None:
            self.powerset = powerset(list(range(self.num_players)))
            self.coal_scores = self.generate_random_scores()
            # By convention, value of empty coalition is 0
            self.coal_scores[frozenset()] = 0
        else:
            self.powerset = [tuple(k) for k in self.coal_scores.keys()]

    def compute_solution(self):
        if self.num_players > 5:
            logging.info("Number of players is more than 5, this may take some time...")

        # Create all permutations
        n_fact = factorial(self.num_players)

        self.solution = [None] * self.num_players

        for player in range(self.num_players):
            phi = 0
            for coalition in self.powerset:
                if player not in coalition:
                    factor = factorial(len(coalition))
                    factor *= factorial(self.num_players - len(coalition) - 1)
                    factor /= n_fact

                    phi += factor * (
                        self.coal_scores[frozenset(list(coalition) + [player])]
                        - self.coal_scores[frozenset(coalition)]
                    )

            self.solution[player] = phi

    def generate_random_scores(self):
        scores = [random.uniform(0, 10) for i in range(len(self.powerset))]

        # Make sure empty set has value of 0
        scores[0] = 0

        return {frozenset(self.powerset[i]): scores[i] for i in range(len(scores))}
