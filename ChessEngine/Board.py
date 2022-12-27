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
        self.undo_moves_log = np.array([])

    # this is 8*8 chess board:
    # b: black
    # w: white
    # second character represents piece of game (R, N, B, Q, K, P)
    '''
    this makemove fxn just takes move object and moves chosen to destination. will not work for castling and pawn promotion
    '''
    def make_move(self, move:MoveLib):
        # print(self.board)
        moved = move.piece_moved[0]
        captured = move.piece_captured[0]
        if( (moved == 'w' and self.whiteToMove) or (moved == 'b' and (not self.whiteToMove))):
            if((captured == 'w' and (not self.whiteToMove)) or (captured == 'b' and ( self.whiteToMove)) or (captured == '-')):
                self.undo_moves_log = np.array([])
                self.board[move.start_row,move.start_col] = '--'
                self.board[move.end_row, move.end_col] = move.piece_moved
                self.move_log = np.append(self.move_log, [move])
                self.whiteToMove = not self.whiteToMove

        # print(self.board)
    '''
    this will undo moves made from last, with help of move_log we have
    '''
    def undo_moves(self):
        last_move: MoveLib = self.move_log[-1]
        last_move_start_col = last_move.start_col
        last_move_start_row = last_move.start_row
        last_move_end_row = last_move.end_row
        last_move_end_col = last_move.end_col
        self.board[last_move_start_row, last_move_start_col] = last_move.piece_moved
        self.board[last_move_end_row, last_move_end_col] = last_move.piece_captured
        self.move_log = np.delete(self.move_log, -1)
        self.whiteToMove = not self.whiteToMove
        self.undo_moves_log = np.append(self.undo_moves_log, [last_move])

    def redo_moves(self):
        last_move: MoveLib = self.undo_moves_log[-1]
        last_move_start_col = last_move.start_col
        last_move_start_row = last_move.start_row
        last_move_end_row = last_move.end_row
        last_move_end_col = last_move.end_col
        self.board[last_move_end_row, last_move_end_col] = last_move.piece_moved
        self.board[last_move_start_row, last_move_start_col] = '--'
        self.move_log = np.append(self.move_log, [last_move])
        self.whiteToMove = not self.whiteToMove
        self.undo_moves_log = np.delete(self.undo_moves_log, -1)
    def __str__(self):
        return "this is game state board"
