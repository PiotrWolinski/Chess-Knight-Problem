from __future__ import annotations
from typing import Tuple

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

