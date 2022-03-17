
from __future__ import annotations

import argparse
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib import colors

from components.chessboard import Chessboard
from components.position import Position


def generate_possible_moves(position: Position, board_size: int) -> List[Position]:
    """Returns list of possible positions for the knight, based on the current position.
    
    Arguments:
        position: Position - position from which the knight will move

    Return: 
        List[Position]
    """
    
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
    args = parser.parse_args()

    start_position, target_position, chessboard = handle_input(default=args.default)

    print(f'start = {start_position}')
    print(f'target = {target_position}')

    # Calculate the shortest path using BFS algorithm
    shortest_path = calculate_shortest_path(start_position, target_position, chessboard)

    # Plot path on the chessboard
    plot_path(shortest_path, chessboard)
    

if __name__ == "__main__":
    main()
