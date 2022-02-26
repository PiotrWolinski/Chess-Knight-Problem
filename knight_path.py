
from configparser import Interpolation
from dataclasses import dataclass
from typing import List
import matplotlib.pyplot as plt
from matplotlib import colors


@dataclass
class ChessBoard:
    """Class representing chessboard to make path finding algorithm more flexible.
    Assumption is that the board is square

    Arguments:
        length: int - amount of cells in one row/colum. 
    """
    
    length: int

    def get_rows_label(self, inverted=False):
        if not inverted:
            return [x for x in range(self.length, 0, -1)]
            
        return [x for x in range(1, self.length+1)]

    def get_columns_label(self, inverted=False):
        if not inverted:
            return [chr(x + 97) for x in range(self.length)]

        return [chr(x + 97) for x in range(self.length - 1, -1, -1)]

    @property
    def board(self):
        """
        Returns two dimensional list to represent chessboard.
        0 for white tile, and 1 for black tile.
        
        """
        
        return [[(x + y) % 2 for x in range(self.length)] for y in range(self.length)]


@dataclass(repr=False, eq=False)
class Position:
    """Class for holding position on the chessboard
    For the ease of implementation it will be initialized
    and operated on indexes from 0 to 7, but string representation
    will be adapted to chess notation.

    Position(row=2, col=3) == d3
    Postion(row=0, col=1) == b1
    
    Keyword arguments:
    row: int - the row index
    col: int - the col index
    """
    
    row: int
    col: int
    board_size: int

    def __repr__(self):
        return f'{chr(self.col + 97)}{self.row + 1}'

    def __eq__(self, other: object) -> bool:
        return self.row == other.row and self.col == other.col

    def to_tuple(self):
        return (self.row, self.col)

    def to_display_tuple(self):
        return (self.board_size - 1 - self.row, self.col)


def generate_possible_moves(start_position: Position, board_size: int) -> List[Position]:
    possible_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    output = []

    row = start_position.row
    col = start_position.col

    for row_move, col_move in possible_moves:
        if 7 >= row + row_move >= 0 and 7 >= col + col_move >= 0:
            output.append(Position(row + row_move, col + col_move, board_size))

    return output


def calculate_shortest_path(start_pos: Position, target_pos: Position, chessboard: ChessBoard) -> List[Position]:
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

def plot_path(path: List[str], chessboard: ChessBoard):

    size = chessboard.length

    board = chessboard.board

    step = 2
    for position in path:
        row, col = position.to_display_tuple()
        board[row][col] = step
        step += 1

    # Create discrete colormap
    cmap = colors.ListedColormap(['white', 'black'])
    cmap.set_over('red')

    fig, ax = plt.subplots()
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

    
def main():
    chessboard = ChessBoard(length=8)

    start_position = Position(0, 1, board_size=chessboard.length)
    target_position = Position(6, 5, board_size=chessboard.length)

    print(f'start = {start_position}')
    print(f'target = {target_position}')

    shortest_path = calculate_shortest_path(start_position, target_position, chessboard)

    print(shortest_path)
    plot_path(shortest_path, chessboard)
    

if __name__ == "__main__":
    main()
