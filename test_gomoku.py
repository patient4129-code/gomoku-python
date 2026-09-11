import unittest

from gomoku import BLACK, EMPTY, GomokuGame


class GomokuGameTests(unittest.TestCase):
    def test_players_take_turns(self) -> None:
        game = GomokuGame()
        self.assertTrue(game.place_stone(7, 7))
        self.assertEqual(game.board[7][7], BLACK)
        self.assertNotEqual(game.current_player, BLACK)

    def test_rejects_occupied_and_outside_positions(self) -> None:
        game = GomokuGame()
        self.assertTrue(game.place_stone(0, 0))
        self.assertFalse(game.place_stone(0, 0))
        self.assertFalse(game.place_stone(-1, 0))
        self.assertFalse(game.place_stone(game.size, 0))

    def test_horizontal_win(self) -> None:
        game = GomokuGame()
        for col in range(4):
            self.assertTrue(game.place_stone(7, col))
            self.assertTrue(game.place_stone(0, col))
        self.assertTrue(game.place_stone(7, 4))
        self.assertEqual(game.winner, BLACK)

    def test_diagonal_win(self) -> None:
        game = GomokuGame()
        for index in range(4):
            self.assertTrue(game.place_stone(index, index))
            self.assertTrue(game.place_stone(index, index + 5))
        self.assertTrue(game.place_stone(4, 4))
        self.assertEqual(game.winner, BLACK)

    def test_reset_clears_state(self) -> None:
        game = GomokuGame()
        game.place_stone(3, 3)
        game.reset()
        self.assertEqual(game.board[3][3], EMPTY)
        self.assertEqual(game.moves, 0)
        self.assertEqual(game.current_player, BLACK)


if __name__ == "__main__":
    unittest.main()
