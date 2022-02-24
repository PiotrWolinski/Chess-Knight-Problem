
from dataclasses import dataclass


CHESSBOARD_SIZE = 8

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

def generate_possible_moves(start_position):
    possible_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    output = []

    row = start_position.row
    col = start_position.col

    for row_move, col_move in possible_moves:
        if 7 >= row + row_move >= 0 and 7 >= col + col_move >= 0:
            output.append(Position(row + row_move, col + col_move))

    return output

def calculate_shortest_path(start_pos, target_pos):
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

    
def main():
    start_position = Position(0, 1)
    target_position = Position(0, 2)

    print(f'start = {start_position}')
    print(f'finish = {target_position}')

    print(calculate_shortest_path(start_position, target_position))
    


if __name__ == "__main__":
    main()