import unittest
from tu_games.game import ShapleyGame, powerset


class TestSol(unittest.TestCase):
    def test_solution(self):
        players = [0, 1, 2]
        pset = powerset(players)

        coalition_scores = {frozenset(coal): 0 for coal in pset}
        coalition_scores[frozenset([0, 2])] = 1
        coalition_scores[frozenset([1, 2])] = 1
        coalition_scores[frozenset([0, 1, 2])] = 1
        game = ShapleyGame(3, coalition_scores)
        game.compute_solution()

        solution = [1 / 6, 1 / 6, 2 / 3]

        self.assertEqual(solution, game.solution)


if __name__ == "__main__":
    unittest.main()
