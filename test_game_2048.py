import unittest
import random
from game_2048 import Game2048

class TestGame2048(unittest.TestCase):

    def setUp(self):
        # Seed the random number generator for reproducibility
        random.seed(0)
        self.game = Game2048()

    def test_initial_board(self):
        # Test that the initial board has exactly two tiles with values 2 or 4
        board = self.game.get_board()
        non_zero_tiles = [tile for row in board for tile in row if tile != 0]
        self.assertEqual(len(non_zero_tiles), 2)
        for tile in non_zero_tiles:
            self.assertIn(tile, [2, 4])

    def test_get_set_cell(self):
        # Test the get_cell and set_cell methods
        self.game.set_cell(0, 1)
        self.assertEqual(self.game.get_cell(0), 1)
        self.game.set_cell(15, 2)
        self.assertEqual(self.game.get_cell(15), 2)
        self.game.set_cell(0, 0)
        self.assertEqual(self.game.get_cell(0), 0)

    def test_move_left(self):
        # Test moving tiles to the left and merging
        self.game.board = 0
        # Set up a specific board state
        # Board before move:
        # [2, 2, 0, 0]
        # [4, 0, 4, 0]
        # [2, 2, 2, 2]
        # [0, 0, 0, 0]
        initial_tiles = [
            (0, 1), (1, 1),
            (4, 2), (6, 2),
            (8, 1), (9, 1), (10, 1), (11, 1)
        ]
        for index, value in initial_tiles:
            self.game.set_cell(index, value)

        moved = self.game.move('left', spawn_tile=False)
        # Expected board after move:
        # [4, 0, 0, 0]
        # [8, 0, 0, 0]
        # [4, 4, 0, 0]
        # [0, 0, 0, 0]
        expected_tiles = {
            0: 2,  # Exponent 2 -> Value 4
            4: 3,  # Exponent 3 -> Value 8
            8: 2,  # Exponent 2 -> Value 4
            9: 2   # Exponent 2 -> Value 4
        }
        for i in range(16):
            exponent = self.game.get_cell(i)
            expected_exponent = expected_tiles.get(i, 0)
            self.assertEqual(exponent, expected_exponent)

        self.assertTrue(moved)

    def test_move_right_no_move(self):
        # Test moving right when no tiles can move or merge
        self.game.board = 0
        # Set up a specific board state
        # [0, 0, 0, 2]
        initial_tiles = [(3, 1)]
        for index, value in initial_tiles:
            self.game.set_cell(index, value)

        moved = self.game.move('right', spawn_tile=False)
        # Expect the board to remain the same
        exponent = self.game.get_cell(3)
        self.assertEqual(exponent, 1)
        self.assertFalse(moved)

    def test_move_up(self):
        # Test moving tiles up and merging
        self.game.board = 0
        # Set up a specific board state
        # [2, 0, 0, 0]
        # [2, 0, 0, 0]
        # [4, 0, 0, 0]
        # [4, 0, 0, 0]
        initial_tiles = [
            (0, 1), (4, 1),
            (8, 2), (12, 2)
        ]
        for index, value in initial_tiles:
            self.game.set_cell(index, value)

        moved = self.game.move('up', spawn_tile=False)
        # Expected board after move:
        # [4, 0, 0, 0]
        # [8, 0, 0, 0]
        # [0, 0, 0, 0]
        # [0, 0, 0, 0]
        expected_tiles = {
            0: 2,  # Exponent 2 -> Value 4
            4: 3   # Exponent 3 -> Value 8
        }
        for i in range(16):
            exponent = self.game.get_cell(i)
            expected_exponent = expected_tiles.get(i, 0)
            self.assertEqual(exponent, expected_exponent)

        self.assertTrue(moved)

    def test_move_down(self):
        # Test moving tiles down and merging
        self.game.board = 0
        # Set up a specific board state
        # [0, 0, 0, 0]
        # [0, 0, 0, 0]
        # [2, 0, 0, 0]
        # [2, 0, 0, 0]
        initial_tiles = [
            (8, 1), (12, 1)
        ]
        for index, value in initial_tiles:
            self.game.set_cell(index, value)

        moved = self.game.move('down', spawn_tile=False)
        # Expected board after move:
        # [0, 0, 0, 0]
        # [0, 0, 0, 0]
        # [0, 0, 0, 0]
        # [4, 0, 0, 0]
        expected_tiles = {
            12: 2  # Exponent 2 -> Value 4
        }
        for i in range(16):
            exponent = self.game.get_cell(i)
            expected_exponent = expected_tiles.get(i, 0)
            self.assertEqual(exponent, expected_exponent)

        self.assertTrue(moved)

    def test_no_move_possible(self):
        # Test that no move is possible and game detects game over
        self.game.board = 0
        # Fill the board with exponents where no adjacent tiles can merge
        exponents = [1, 2, 3, 4,
                     2, 3, 4, 5,
                     3, 4, 5, 6,
                     4, 5, 6, 7]
        for i in range(16):
            self.game.set_cell(i, exponents[i])

        self.assertTrue(self.game.is_game_over())

    def test_game_not_over(self):
        # Test that the game is not over when moves are possible
        self.game.board = 0
        # Fill the board with tiles that can merge
        exponents = [1, 1, 2, 2] * 4
        for i in range(16):
            self.game.set_cell(i, exponents[i])

        self.assertFalse(self.game.is_game_over())

    def test_invalid_move_direction(self):
        # Test that an invalid move direction raises ValueError
        with self.assertRaises(ValueError):
            self.game.move('invalid_direction')

    def test_merge_once_per_move(self):
        # Tiles should only merge once per move
        self.game.board = 0
        # Set up a specific board state
        # [2, 2, 2, 2]
        initial_tiles = [(0, 1), (1, 1), (2, 1), (3, 1)]
        for index, value in initial_tiles:
            self.game.set_cell(index, value)

        moved = self.game.move('left', spawn_tile=False)
        # Expected board after move:
        # [4, 4, 0, 0]
        expected_tiles = {
            0: 2,  # Exponent 2 -> Value 4
            1: 2   # Exponent 2 -> Value 4
        }
        for i in range(4):
            exponent = self.game.get_cell(i)
            expected_exponent = expected_tiles.get(i, 0)
            self.assertEqual(exponent, expected_exponent)

        self.assertTrue(moved)

    def test_spawn_tile_after_move(self):
        # Test that a new tile is spawned after a successful move
        initial_board = self.game.board
        moved = self.game.move('left')
        new_board = self.game.board
        self.assertNotEqual(initial_board, new_board)
        # Since random is seeded, we can predict the new tile position and value
        # However, due to the randomness of the tile spawning, we can check that
        # the number of non-zero tiles has increased by 1 after the move
        initial_tiles = sum(1 for i in range(16) if (initial_board >> (i * 4)) & 0xF)
        new_tiles = sum(1 for i in range(16) if (new_board >> (i * 4)) & 0xF)
        self.assertEqual(new_tiles, initial_tiles + 1)

    def test_move_with_no_effect(self):
        # Test moving when there is no possible move in that direction
        self.game.board = 0
        # Set up a specific board state
        # [0, 0, 0, 2]
        initial_tiles = [(3, 1)]
        for index, value in initial_tiles:
            self.game.set_cell(index, value)

        initial_board = self.game.board
        moved = self.game.move('up', spawn_tile=False)
        new_board = self.game.board

        self.assertFalse(moved)
        self.assertEqual(initial_board, new_board)

    def test_process_line(self):
        # Test the internal method process_line
        line = [1, 1, 1, 1]  # Exponents corresponding to [2, 2, 2, 2]
        new_line = self.game.process_line(line)
        expected_line = [2, 2, 0, 0]  # Exponents corresponding to [4, 4, 0, 0]
        self.assertEqual(new_line, expected_line)

    def test_random_tile_values(self):
        # Test that spawned tiles are either 2 or 4
        for _ in range(10):
            self.game.board = 0
            self.game.spawn_tile()
            non_zero_tiles = [self.game.get_cell(i) for i in range(16) if self.game.get_cell(i) != 0]
            self.assertEqual(len(non_zero_tiles), 1)
            value = 2 ** non_zero_tiles[0]
            self.assertIn(value, [2, 4])

    def test_spawn_tile_no_empty_cells(self):
        # Test that spawn_tile returns False when no empty cells are available
        self.game.board = 0xFFFFFFFFFFFFFFFF  # All cells filled with max exponent 15
        result = self.game.spawn_tile()
        self.assertFalse(result)

    def test_set_get_row(self):
        # Test set_row and get_row methods
        exponents = [1, 2, 3, 4]
        self.game.set_row(0, exponents)
        row = self.game.get_row(0)
        self.assertEqual(row, exponents)

    def test_set_get_column(self):
        # Test set_column and get_column methods
        exponents = [1, 2, 3, 4]
        self.game.set_column(0, exponents)
        column = self.game.get_column(0)
        self.assertEqual(column, exponents)

    def test_large_exponents(self):
        # Test handling of large exponents (e.g., reaching 2048 tile)
        self.game.board = 0
        self.game.set_cell(0, 10)  # Exponent 10 -> Value 1024
        self.game.set_cell(1, 10)  # Exponent 10 -> Value 1024
        self.game.move('left', spawn_tile=False)
        exponent = self.game.get_cell(0)
        self.assertEqual(exponent, 11)  # Exponent 11 -> Value 2048

    def test_overflow_exponent(self):
        # Test that exponents do not overflow beyond 15 (maximum 4 bits)
        self.game.board = 0
        self.game.set_cell(0, 15)  # Exponent 15 is the maximum representable
        self.game.set_cell(1, 15)
        self.game.move('left', spawn_tile=False)
        exponent = self.game.get_cell(0)
        self.assertEqual(exponent, 15)  # Should remain at maximum value

if __name__ == '__main__':
    unittest.main()
