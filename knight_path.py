
from __future__ import annotations

import argparse
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib import colors


class Position:
    """Class for holding position on the chessboard
    For the ease of implementation it will be initialized
    and operated on indexes from 0 to 7, but string representation
    will be adapted to chess notation.

    Position(row=2, col=3) == d3
    Postion(row=0, col=1) == b1
    
    Arguments:
        row: int - the row index
        col: int - the col index
    """

    def __init__(self, row: int, col: int, board_size: int):
        if row >= board_size or row < 0:
            raise ValueError('Incorrect row index') 

        if col >= board_size or col < 0:
            raise ValueError('Incorrect col index')

        self._row = row
        self._col = col
        self.board_size = board_size

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col

    def __repr__(self) -> str:
        return f'{chr(self._col + 97)}{self._row + 1}'

    def __eq__(self, other: object) -> bool:
        return self._row == other.row and self._col == other.col

    @classmethod
    def parse_from_str(cls, position_str: str, board_size: int) -> Position:
        if not position_str:
            raise ValueError('Empty string or None passed to string position parser')

        STR_LEN = 2 if board_size < 10 else 3

        if len(position_str) != STR_LEN:
            raise ValueError('Incorrect string size')

        position_str = position_str.lower()

        col = ord(position_str[0]) - 97
        row = int(position_str[1:]) - 1

        pos = cls(row, col, board_size)

        return pos

    def to_tuple(self) -> Tuple:
        return (self._row, self._col)

    def to_display_tuple(self) -> Tuple:
        return (self.board_size - 1 - self._row, self._col)


class Chessboard:
    """Class representing chessboard to make path finding algorithm more flexible.
    Assumption is that the board is square. 

    Max size of the chess board is set to 26x26, to keep it clean with labeling
    and min size is 4x4, so that the knight will have place to move.

    Arguments:
        length: int - amount of cells in one row/colum. 
    """

    MAX_LENGTH = 26
    MIN_LENGTH = 4

    def __init__(self, length: int) -> None:
        if length < self.MIN_LENGTH:
            self.length = self.MIN_LENGTH
            return
        
        if length > self.MAX_LENGTH:
            self.length = self.MAX_LENGTH
            return

        self.length = length

    def get_rows_label(self, inverted: bool=False) -> List:
        if not inverted:
            return [x for x in range(self.length, 0, -1)]
            
        return [x for x in range(1, self.length+1)]

    def get_columns_label(self, inverted: bool=False) -> List:
        if not inverted:
            return [chr(x + 97) for x in range(self.length)]

        return [chr(x + 97) for x in range(self.length-1, -1, -1)]

    def check_position(self, position: Position) -> bool:
        """Checks if given position is valid in terms of current chessboard
        
        Arguments:
            position: Position -- position to check
        Return: return_description
        """
        
        row, col = position.to_tuple()

        return row >= 0 and row < self.length and col >= 0 and col < self.length
        
    @property
    def board(self) -> List[List]:
        """Returns two dimensional list to represent chessboard.
        0 for white tile, and 1 for black tile.
        """
        
        return [[(x + y) % 2 for x in range(self.length)] for y in range(self.length)]


def generate_possible_moves(position: Position, board_size: int) -> List[Position]:
    possible_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    output = []

    row, col = position.to_tuple()

    for row_move, col_move in possible_moves:
        if board_size-1 >= row + row_move >= 0 and board_size-1 >= col + col_move >= 0:
            output.append(Position(row + row_move, col + col_move, board_size))

    return output


def calculate_shortest_path(start_pos: Position, target_pos: Position, chessboard: Chessboard) -> List[Position]:
    """Returns list of positions that will make the path from the start_pos to the target_pos, 
    start_pos is included as the first element.
    
    Arguments:
        start_pos: Position - position on which knight starts the path
        target_pos: Position - position which knight needs to finish on
        chessboard: Chessboard - object representing chessboard on which the task is conducted

    Return:
        List[Position]
    """
    
    visited = []
    paths = []

    queue = [[start_pos]]
    while len(queue) != 0:
        current_path = queue.pop(0)
        last_position = current_path[-1]

        # Check if path was not found
        if last_position == target_pos:
            paths.append(current_path)
            continue

        # Check possible moves from the current position
        possible_moves = generate_possible_moves(last_position, chessboard.length)
        actual_moves = []

        # Check if generated positions were not visited earlier
        for position in possible_moves:
            if position not in visited:
                actual_moves.append(position)
                visited.append(position)
        
        # Generate new paths from the current position
        for next_position in actual_moves:
            new_path = current_path[:]
            new_path.append(next_position)
            queue.append(new_path)
    
    shortest_path = ['' for _ in range(chessboard.length ** 2)]

    for path in paths:
        if len(path) < len(shortest_path):
            shortest_path = path

    return shortest_path

def plot_path(path: List[str], chessboard: Chessboard) -> None:

    size = chessboard.length

    board = chessboard.board

    # Set to 2, so it can be distinguished from the black and white tiles
    step = 2
    for position in path:
        row, col = position.to_display_tuple()
        board[row][col] = step
        step += 1

    # Create discrete colormap
    cmap = colors.ListedColormap(['white', 'black'])
    cmap.set_over('red')

    _, ax = plt.subplots()
    ax.imshow(board, cmap=cmap, interpolation='nearest', vmax=1)

    row_labels = chessboard.get_rows_label()
    col_labels = chessboard.get_columns_label()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 1:
                ax.text(j, i, f'{board[i][j]-1}', ha='center', va='center')

    ax.set_xticks(range(size), col_labels);
    ax.set_yticks(range(size), row_labels);

    ax.set_title(f'Start = {path[0]}   Target = {path[-1]}')
    plt.show()

def handle_input(default: bool=True) -> Tuple[Position, Position, Chessboard]:
    
    chessboard = None
    start_position = None
    target_position = None

    if default:
        # Define chessboard that will be used to solve the problem
        chessboard = Chessboard(length=8)

        # Define start and target position for the knight
        start_position = Position(0, 1, board_size=chessboard.length)
        target_position = Position(6, 5, board_size=chessboard.length)
    else:
        print('Provide chessboard size (standard is 8)')
        size = int(input('> '))

        chessboard = Chessboard(length=size)

        print('Enter starting position in chess notation (ex. a2)')
        print('Just make sure it fits on Your chessboard!')
        start_pos_str = input('> ')

        start_position = Position.parse_from_str(start_pos_str, chessboard.length)

        print('Enter target position in chess notation (ex. a2')
        print('Just make sure it fits on Your chessboard!')
        target_pos_str = input('> ')

        target_position = Position.parse_from_str(target_pos_str, chessboard.length)

    return start_position, target_position, chessboard

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--default', action='store_true', default=False)

    # TODO -- Add user input and split to files

    args = parser.parse_args()

    # # Define chessboard that will be used to solve the problem
    # chessboard = Chessboard(length=2)

    # # Define start and target position for the knight
    # start_position = Position(0, 1, board_size=chessboard.length)
    # target_position = Position(1, 3, board_size=chessboard.length)

    start_position, target_position, chessboard = handle_input(default=args.default)

    print(f'start = {start_position}')
    print(f'target = {target_position}')

    # Calculate the shortest path using BFS algorithm
    shortest_path = calculate_shortest_path(start_position, target_position, chessboard)

    # Plot path on the chessboard
    plot_path(shortest_path, chessboard)
    

if __name__ == "__main__":
    main()
