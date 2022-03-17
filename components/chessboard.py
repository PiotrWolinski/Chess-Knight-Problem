from typing import List
from .position import Position

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
        Return: 
            xjbool - boolean if the given position is valid for this chessboard
        """
        
        row, col = position.to_tuple()

        return row >= 0 and row < self.length and col >= 0 and col < self.length
        
    @property
    def board(self) -> List[List]:
        """Returns two dimensional list to represent chessboard.
        0 for white tile, and 1 for black tile.
        """
        
        return [[(x + y) % 2 for x in range(self.length)] for y in range(self.length)]

