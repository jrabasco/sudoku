from typing import List

from .grid import Grid, Cell

def add_solo_annotations(g: Grid) -> bool:
    changed = False
    for row in g.rows():
        for cell in row:
            if len(cell.guesses) == 1:
                changed = True
                cell.value = cell.guesses.pop()
    return changed

def annotate(g: Grid):
    for i, row in enumerate(g.rows()):
        for j, cell in enumerate(row):
            if cell.value is not None:
                continue
            srow = i//3
            scol = j//3
            square = g.square(srow*3 + scol)
            col = g.col(j)
            cell.reset_guesses()
            for nb in range(1, 10):
                if in_list(nb, row):
                    continue
                if in_list(nb, col):
                    continue
                if in_list(nb, square):
                    continue
                cell.add_guess(nb)


def add_solo_numbers(g: Grid) -> bool:
    changed = False
    for nb in range(1, 10):
        for i,row in enumerate(g.rows()):
            if in_list(nb, row):
                continue
            fits = 0
            last_fit = -1
            for j, elm in enumerate(row):
                if elm.value is None and can_fit(g,nb, i, j):
                    fits += 1
                    last_fit = j
            if fits == 1:
                changed = True
                g.set(i, last_fit, nb)

        for j,col in enumerate(g.cols()):
            if in_list(nb, col):
                continue
            fits = 0
            last_fit = -1
            for i, elm in enumerate(col):
                if elm.value is None and can_fit(g,nb, i, j):
                    fits += 1
                    last_fit = i
            if fits == 1:
                changed = True
                g.set(last_fit, j, nb)

        for n,square in enumerate(g.squares()):
            if in_list(nb, square):
                continue
            fits = 0
            last_i = -1
            last_j = -1
            for ns, elm in enumerate(square):
                i,j = square_to_coords(n, ns)
                if elm.value is None and can_fit(g,nb, i, j):
                    fits += 1
                    last_i = i
                    last_j = j
            if fits == 1:
                changed = True
                g.set(last_i, last_j, nb)
    return changed


def square_to_coords(n,ns):
    i = (n//3)*3 + ns//3
    j = (n%3)*3 + ns%3
    return i,j


def can_fit(g: Grid, nb: int, i: int, j: int):
    srow = i//3
    scol = j//3
    square = g.square(srow*3 + scol)
    if in_list(nb, square):
        return False
    row = g.row(i)
    if in_list(nb, row):
        return False
    col = g.col(j)
    if in_list(nb, col):
        return False
    return True



def in_list(nb: int, cells: List[Cell]) -> bool:
    for c in cells:
        if nb == c.value:
            return True
    return False

def verify(g: Grid):
    for row in g.rows():
        for nb in range(1,10):
            if not in_list(nb, row):
                return False

    for col in g.cols():
        for nb in range(1,10):
            if not in_list(nb, col):
                return False

    for square in g.squares():
        for nb in range(1,10):
            if not in_list(nb, square):
                return False
    return True

def red(g: Grid) -> bool:
    changed = add_solo_numbers(g)
    annotate(g)
    changed = changed or add_solo_annotations(g)
    return changed

def solve(g: Grid):
    changed = True
    i = 1
    while changed:
        i+=1
        changed = red(g)
