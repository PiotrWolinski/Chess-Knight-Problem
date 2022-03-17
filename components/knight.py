from typing import List

from .chessboard import Chessboard
from .position import Position


class Knight:

    def __init__(self, start_position: Position, target_position: Position, chessboard: Chessboard) -> None:
        self._start_position = start_position
        self._target_position = target_position
        self._chessboard = chessboard

    @staticmethod
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

    def calculate_shortest_path(self) -> List[Position]:
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

        queue = [[self._start_position]]
        while len(queue) != 0:
            current_path = queue.pop(0)
            last_position = current_path[-1]

            # Check if path was not found
            if last_position == self._target_position:
                paths.append(current_path)
                continue

            # Check possible moves from the current position
            possible_moves = Knight.generate_possible_moves(last_position, self._chessboard.length)
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

        shortest_path = ['' for _ in range(self._chessboard.length ** 2)]

        for path in paths:
            if len(path) < len(shortest_path):
                shortest_path = path

        return shortest_path
