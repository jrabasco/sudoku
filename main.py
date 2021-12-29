#!/usr/bin/python3.8
import os
from libs import Grid, solve, verify, annotate


for prefix, _, files in os.walk('dataset'):
    for f in files:
        sudoku = f'{prefix}/{f}'
        print(f'{sudoku}:')
        G = Grid.from_file(sudoku)
        print(G)
        print()
        solve(G)
        annotate(G)
        print(G)
        if not verify(G):
            print(f'Could not solve {sudoku}')
            raise SystemExit(1)
