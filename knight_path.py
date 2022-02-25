
from configparser import Interpolation
from dataclasses import dataclass
from typing import List
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

CHESSBOARD_SIZE = 8

@dataclass
class ChessBoard:
    pass



@dataclass
class Position:
    """Class for holding position on the chessboard
    For the ease of implementation it will be initialized
    and operated on indexes from 0 to 7, but string representation
    will be adapted to chess notation.

    Position(row=2, col=3) == d3
    Postion(row=0, col=1) == b1
    
    Keyword arguments:
    row -- int for the row index
    col -- int for the col index
    """
    
    row: int
    col: int

    def __repr__(self):
        return f'{chr(self.col + 97)}{self.row + 1}'

    def __eq__(self, other: object) -> bool:
        return self.row == other.row and self.col == other.col

    def to_tuple(self):
        return (self.row, self.col)

    def to_display_tuple(self):
        return (7 - self.row, self.col)


def generate_possible_moves(start_position: Position) -> List[Position]:
    possible_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    output = []

    row = start_position.row
    col = start_position.col

    for row_move, col_move in possible_moves:
        if 7 >= row + row_move >= 0 and 7 >= col + col_move >= 0:
            output.append(Position(row + row_move, col + col_move))

    return output


def calculate_shortest_path(start_pos: Position, target_pos: Position) -> List[Position]:
    visited = []
    paths = []

    queue = [[start_pos]]
    while len(queue) != 0 and len(visited) != CHESSBOARD_SIZE ** 2:
        current_path = queue.pop(0)
        last_position = current_path[-1]

        # Check if path was not found
        if last_position == target_pos:
            paths.append(current_path)
            continue

        # Check possible moves from the current position
        possible_moves = generate_possible_moves(last_position)
        actual_moves = []

        # Check if generated positions were not visited earlier
        for position in possible_moves:
            if position not in visited:
                actual_moves.append(position)
                visited.append(position)
        
        # Generate new paths from the current position
        for next_position in possible_moves:
            new_path = current_path[:]
            new_path.append(next_position)
            queue.append(new_path)

    
    shortest_path = ['' for _ in range(CHESSBOARD_SIZE ** 2)]

    for path in paths:
        if len(path) < len(shortest_path):
            shortest_path = path

    return shortest_path

def plot_path(path: List[str]):

    size = CHESSBOARD_SIZE

    board = [[(x + y) % 2 for x in range(size)] for y in range(size)]

    step = 2
    for position in path:
        row, col = position.to_display_tuple()
        board[row][col] = step
        step += 1

    # create discrete colormap
    cmap = colors.ListedColormap(['white', 'black'])
    cmap.set_over('red')

    fig, ax = plt.subplots()
    ax.imshow(board, cmap=cmap, interpolation='nearest', vmax=1)

    row_labels = range(size, 0, -1)
    col_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    for (i, j), z in np.ndenumerate(board):
        if board[i][j] > 1:
            ax.text(j, i, f'{board[i][j]-1}', ha='center', va='center')

    ax.set_xticks(range(size), col_labels);
    ax.set_yticks(range(size), row_labels);

    ax.set_title(f'Start = {path[0]}   Target = {path[-1]}')

    # ax.set_xticks(np.arange(-.5, size, 1), minor=True)
    # ax.set_yticks(np.arange(-.5, size, 1), minor=True)
    
    # ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

    plt.show()

    
def main():
    start_position = Position(0, 1)
    target_position = Position(0, 2)

    print(f'start = {start_position}')
    print(f'target = {target_position}')

    shortest_path = calculate_shortest_path(start_position, target_position)

    print(shortest_path)
    plot_path(shortest_path)
    

if __name__ == "__main__":
    main()
