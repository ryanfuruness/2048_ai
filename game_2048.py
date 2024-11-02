import random

class Game2048:
    """
    A class to simulate the 2048 game with efficient bit manipulation.
    The board is represented as a 64-bit integer, with each cell occupying 4 bits.
    """

    def __init__(self):
        """
        Initialize a new game by resetting the board.
        """
        self.board = 0
        self.reset()

    def reset(self):
        """
        Reset the game to the initial state with two tiles spawned.
        """
        self.board = 0
        self.spawn_tile()
        self.spawn_tile()

    def get_cell(self, index):
        """
        Get the exponent value at the given cell index (0-15).
        :param index: Cell index from 0 to 15.
        :return: Exponent value at the cell.
        """
        shift = index * 4
        return (self.board >> shift) & 0xF  # Extract 4 bits for the cell

    def set_cell(self, index, value):
        """
        Set the exponent value at the given cell index (0-15).
        :param index: Cell index from 0 to 15.
        :param value: Exponent value to set at the cell.
        """
        shift = index * 4
        self.board &= ~(0xF << shift)  # Clear the 4 bits at the cell
        self.board |= (value & 0xF) << shift  # Set the new value

    def spawn_tile(self):
        """
        Spawn a new tile (2 or 4) at a random empty cell.
        :return: True if a tile was spawned, False if no empty cells are available.
        """
        empty_cells = [i for i in range(16) if self.get_cell(i) == 0]
        if not empty_cells:
            return False  # No empty cells, cannot spawn
        index = random.choice(empty_cells)
        value = 1 if random.random() < 0.9 else 2  # Exponent 1 for '2', exponent 2 for '4'
        self.set_cell(index, value)
        return True

    def get_board(self):
        """
        Get the current board state as a 4x4 list of lists.
        :return: 4x4 grid representing the board with actual tile values.
        """
        board = []
        for row in range(4):
            board_row = []
            for col in range(4):
                index = row * 4 + col
                exponent = self.get_cell(index)
                value = 0 if exponent == 0 else 2 ** exponent
                board_row.append(value)
            board.append(board_row)
        return board

    def get_row(self, row_index):
        """
        Get the exponents of a specific row.
        :param row_index: Row index from 0 to 3.
        :return: List of exponents in the row.
        """
        return [self.get_cell(row_index * 4 + col) for col in range(4)]

    def set_row(self, row_index, line):
        """
        Set the exponents of a specific row.
        :param row_index: Row index from 0 to 3.
        :param line: List of exponents to set in the row.
        """
        for col in range(4):
            self.set_cell(row_index * 4 + col, line[col])

    def get_column(self, col_index):
        """
        Get the exponents of a specific column.
        :param col_index: Column index from 0 to 3.
        :return: List of exponents in the column.
        """
        return [self.get_cell(row * 4 + col_index) for row in range(4)]

    def set_column(self, col_index, line):
        """
        Set the exponents of a specific column.
        :param col_index: Column index from 0 to 3.
        :param line: List of exponents to set in the column.
        """
        for row in range(4):
            self.set_cell(row * 4 + col_index, line[row])

    def process_line(self, line):
        """
        Process a line (row or column) for merging and shifting.
        :param line: List of exponents in the line.
        :return: New list of exponents after processing.
        """
        # Remove zeros and shift tiles
        new_line = [v for v in line if v != 0]
        merged_line = []
        skip = False
        for i in range(len(new_line)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_line) and new_line[i] == new_line[i + 1]:
                # Merge tiles by increasing exponent, cap at 15
                merged_exponent = min(new_line[i] + 1, 15)
                merged_line.append(merged_exponent)
                skip = True  # Skip next tile as it's merged
            else:
                merged_line.append(new_line[i])
        # Fill the rest with zeros
        merged_line.extend([0] * (4 - len(merged_line)))
        return merged_line

    def move(self, direction, spawn_tile=True):
        """
        Perform a move in the given direction.
        :param direction: One of 'up', 'down', 'left', 'right'.
        :param spawn_tile: Whether to spawn a new tile after the move.
        :return: True if any tiles moved or merged, False otherwise.
        """
        moved = False
        if direction == 'left':
            for row in range(4):
                line = self.get_row(row)
                new_line = self.process_line(line)
                if new_line != line:
                    moved = True
                self.set_row(row, new_line)
        elif direction == 'right':
            for row in range(4):
                line = self.get_row(row)
                reversed_line = line[::-1]
                new_line = self.process_line(reversed_line)
                new_line = new_line[::-1]
                if new_line != line:
                    moved = True
                self.set_row(row, new_line)
        elif direction == 'up':
            for col in range(4):
                line = self.get_column(col)
                new_line = self.process_line(line)
                if new_line != line:
                    moved = True
                self.set_column(col, new_line)
        elif direction == 'down':
            for col in range(4):
                line = self.get_column(col)
                reversed_line = line[::-1]
                new_line = self.process_line(reversed_line)
                new_line = new_line[::-1]
                if new_line != line:
                    moved = True
                self.set_column(col, new_line)
        else:
            raise ValueError("Invalid direction. Choose from 'up', 'down', 'left', 'right'.")
        if moved and spawn_tile:
            self.spawn_tile()
        return moved

    def is_game_over(self):
        """
        Check if no more moves are possible.
        :return: True if the game is over, False otherwise.
        """
        # If any cell is empty, game is not over
        for i in range(16):
            if self.get_cell(i) == 0:
                return False
        # Check for possible merges horizontally and vertically
        for row in range(4):
            for col in range(4):
                current = self.get_cell(row * 4 + col)
                # Check right neighbor
                if col < 3:
                    right = self.get_cell(row * 4 + col + 1)
                    if current == right:
                        return False
                # Check down neighbor
                if row < 3:
                    down = self.get_cell((row + 1) * 4 + col)
                    if current == down:
                        return False
        return True
