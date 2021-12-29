from __future__ import annotations
from typing import List, Optional, Iterable, Set

_NUMBERS = [
    [
        "┌─┐",
        "│ │",
        "└─┘"
    ],
    [
        "  ┐",
        "  │",
        "  │",
    ],
    [
        "┌─┐",
        "┌─┘",
        "└─┘"
    ],
    [
        "┌─┐",
        " ─┤",
        "└─┘"
    ],
    [
        "│ │",
        "└─┤",
        "  │"
    ],
    [
        "┌─┐",
        "└─┐",
        "└─┘"
    ],
    [
        "┌─┐",
        "├─┐",
        "└─┘"
    ],
    [
        "┌─┐",
        "  │",
        "  │"
    ],
    [
        "┌─┐",
        "├─┤",
        "└─┘"
    ],
    [
        "┌─┐",
        "└─┤",
        "└─┘"
    ],
]

class Grid:
    def __init__(self,
                 grid: List[List[Optional[int]]]):
        self.load(grid)

    def load(self,
             grid: List[List[Optional[int]]]):
        self._grid = []
        for row in grid:
            crow = [Cell(elm) for elm in row]
            self._grid.append(crow)


    def rows(self) -> Iterable[List[Cell]]:
        for row in self._grid:
            yield row

    def row(self, i: int) -> List[Cell]:
        return self._grid[i]

    def cols(self) -> Iterable[List[Cell]]:
        for i in range(9):
            yield self.col(i)

    def col(self, i: int) -> List[Cell]:
        return [ row[i] for row in self._grid ]

    def squares(self) -> Iterable[List[Cell]]:
        for i in range(9):
            yield self.square(i)

    def square(self, i: int) -> List[Cell]:
        row, col = i//3, i%3
        return [
            elm
            for row in self._grid[row*3:row*3+3]
            for elm in row[col*3:col*3+3]
        ]

    def set(self, i: int, j:int, nb:int):
        self._grid[i][j].value = nb

    @staticmethod
    def from_file(filepath: str) -> Grid:
        grid = []
        with open(filepath) as f:
            grid = []
            for row in f:
                srow = [
                    int(elm) if elm != ' ' else None
                    for elm in row.split('\n')[0]
                ]
                grid.append(srow)
            return Grid(grid)

    def __repr__(self) -> str:
        srows = [
            f'[{",".join(repr(c) for c in row)}]'
            for row in self._grid
        ]
        return f'Grid([{",".join(srows)}])'

    def __str__(self) -> str:
        srows = []
        for row in self._grid:
            scells = [
                str(cell).split('\n')
                for cell in row
            ]

            for i in range(3):
                scs0 = scells[:3]
                scs1 = scells[3:6]
                scs2 = scells[6:9]
                line = f'{scs0[0][i]}{scs0[1][i]}{scs0[2][i]}│{scs1[0][i]}{scs1[1][i]}{scs1[2][i]}│{scs2[0][i]}{scs2[1][i]}{scs2[2][i]}'
                srows.append(line)
        srows = srows[:9] +\
                ['─────────────────────────────'] +\
                srows[9:18] +\
                ['─────────────────────────────'] +\
                srows[18:27]
        return '\n'.join(srows)


class Cell:
    def __init__(self,
                 value: Optional[int],
                 guesses: Optional[Iterable[int]]=None):
        if guesses == None:
            guesses = []
        self._guesses = set(guesses)
        self._value = value

    @property
    def guesses(self) -> Set[int]:
        return self._guesses

    @property
    def value(self) -> Optional[int]:
        return self._value

    @value.setter
    def value(self, nb: int):
        self._value = nb

    def reset_guesses(self):
        self._guesses = set()

    def add_guess(self, nb: int):
        self._guesses.add(nb)

    def remove_guesses(self, guesses: Set[int]):
        self._guesses -= guesses

    def __repr__(self):
        return f"Cell({self._value}, {self._guesses})"

    def __str__(self):
        if self._value is not None:
            return '\n'.join(_NUMBERS[self._value])
        gstr = [str(g) for g in self._guesses]
        rows = []
        for i in range(3):
            crow = ''.join(gstr[i*3:i*3+3])
            if len(crow) < 3:
                crow += ' '*(3-len(crow))
            rows.append(crow)
        return '\n'.join(rows)
