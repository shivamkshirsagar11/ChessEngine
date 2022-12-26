import numpy as np

from ChessEngine.MoveLibrary import MoveLib


class GameBoard:
    def __init__(self):
        self.board = np.array([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ])
        self.whiteToMove = True
        self.move_log = np.array([])

    # this is 8*8 chess board:
    # b: black
    # w: white
    # second character represents piece of game (R, N, B, Q, K, P)

    def make_move(self, move:MoveLib):
        # print(self.board)
        self.board[move.start_row,move.start_col] = '--'
        self.board[move.end_row, move.end_col] = move.piece_moved
        self.move_log = np.append(self.move_log, [move])
        self.whiteToMove = not self.whiteToMove
        # print(self.board)

    def __str__(self):
        return "this is game state board"
