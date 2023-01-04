import numpy as np

from ChessEngine.MoveLibrary import MoveLib

WHITE_PAWN_START_ROW = 6
BLACK_PAWN_START_ROW = 1


class GameBoard:
    def __init__(self):
        self.board = np.array([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', 'wB', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ])
        self.whiteToMove = True
        self.move_log = np.array([])
        self.undo_moves_log = np.array([])
        self.move_func_dict = {
            "P": self.get_all_pawn_moves,
            "R": self.get_all_rook_moves,
            "B": self.get_all_bishop_moves,
            "N": self.get_all_knight_moves,
            "Q": self.get_all_queen_moves,
            "K": self.get_all_king_moves
        }

    # this is 8*8 chess board:
    # b: black
    # w: white
    # second character represents piece of game (R, N, B, Q, K, P)
    '''
    this makemove fxn just takes move object and moves chosen to destination. will not work for castling and pawn promotion
    '''

    def make_move(self, move: MoveLib):
        # print(self.board)
        moved = move.piece_moved[0]
        captured = move.piece_captured[0]
        if ((moved == 'w' and self.whiteToMove) or (moved == 'b' and (not self.whiteToMove))):
            if ((captured == 'w' and (not self.whiteToMove)) or (captured == 'b' and (self.whiteToMove)) or (
                    captured == '-')):
                self.undo_moves_log = np.array([])
                self.board[move.start_row, move.start_col] = '--'
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

    '''
    this function will generate mall valid moves along with check possibility
    '''

    def all_valid_move_c_check(self):
        return self.all_valid_move_woc_check()  # for now we will not worry about check

    '''
    this function will generate move without considering check and other mate tricks
    '''

    def all_valid_move_woc_check(self):
        # [MoveLib((6, 4), (4, 4), self.board)]
        moves = np.array([])
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                piece = self.board[i, j][1]
                if piece != '-':
                    moves = np.append(moves, [self.move_func_dict[piece](i, j, moves)])
        return moves

    def __str__(self):
        return "this is game state board"

    '''
    if possible make 2 moves and store it, if not then make one move and store, then check for cross moves if possible make 
    also check for boundary conditions if making move goes beyond board limit
    also check if in capturing the captured piece is of opposite team
    '''

    def get_all_pawn_moves(self, i, j, moves: np.array):
        if self.whiteToMove:
            if self.board[i - 1, j] == '--':
                moves = np.append(moves, [MoveLib((i, j), (i - 1, j), self.board)])
            if i == WHITE_PAWN_START_ROW and self.board[i - 2, j] == '--':
                moves = np.append(moves, [MoveLib((i, j), (i - 2, j), self.board)])
            if j + 1 < 8:
                if self.board[i - 1, j + 1] != '--' and self.board[i - 1, j + 1][0] == 'b':
                    moves = np.append(moves, [MoveLib((i, j), (i - 1, j + 1), self.board)])
            if j - 1 > 0:
                if self.board[i - 1, j - 1] != '--' and self.board[i - 1, j - 1] == 'b':
                    moves = np.append(moves, [MoveLib((i, j), (i - 1, j - 1), self.board)])
        else:
            if self.board[i + 1, j] == '--':
                moves = np.append(moves, [MoveLib((i, j), (i + 1, j), self.board)])
            if i == BLACK_PAWN_START_ROW and self.board[i + 2, j] == '--':
                moves = np.append(moves, [MoveLib((i, j), (i + 2, j), self.board)])
            if j + 1 < 8:
                if self.board[i + 1, j + 1] != '--' and self.board[i + 1, j + 1] == 'w':
                    moves = np.append(moves, [MoveLib((i, j), (i + 1, j + 1), self.board)])
            if j - 1 > 0:
                if self.board[i + 1, j - 1] != '--' and self.board[i + 1, j - 1] == 'w':
                    moves = np.append(moves, [MoveLib((i, j), (i + 1, j - 1), self.board)])
        return moves

    def get_all_rook_moves(self, i, j, moves: np.array):
        count = 0
        fake_i = i
        fake_j = j
        shadow_i = i  # this will go down in board simultaneously as i goes up
        shadow_j = j  # this will go left in board simultaneously as j goes right
        if self.whiteToMove and self.board[fake_i, fake_j][0] != 'b':
            while i - 1 > 0 or shadow_i + 1 < 8 or j + 1 < 8 or shadow_j - 1 > 0:
                count = count + 1
                if i - 1 > 0:  # go up and check, stop when encounter white or black piece
                    if self.board[i - 1, fake_j] == '--':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (i - 1, fake_j), self.board)])
                    elif self.board[i - 1, fake_j][0] == 'b' and self.board[fake_i, fake_j][0] != 'b':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (i - 1, fake_j), self.board)])
                        i = 0
                    else:
                        i = 0

                if shadow_i + 1 < 8:  # go down and check, stop when encounter white or black piece
                    if self.board[shadow_i + 1, fake_j] == '--':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (shadow_i + 1, fake_j), self.board)])
                    elif self.board[shadow_i + 1, fake_j][0] == 'b' and self.board[fake_i, fake_j][0] != 'b':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (shadow_i + 1, fake_j), self.board)])
                        shadow_i = 7
                    else:
                        shadow_i = 7

                if j + 1 < 8:  # go right and check, stop when black or white piece found
                    if self.board[fake_i, j + 1] == '--':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (fake_i, j + 1), self.board)])
                    elif self.board[fake_i, j + 1][0] == 'b' and self.board[fake_i, fake_j][0] != 'b':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (fake_i, j + 1), self.board)])
                        j = 7
                    else:
                        j = 7

                if shadow_j - 1 > 0:  # go left and check, stop when black or white piece found
                    if self.board[fake_i, shadow_j - 1] == '--':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (fake_i, shadow_j - 1), self.board)])
                    elif self.board[fake_i, shadow_j - 1][0] == 'b' and self.board[fake_i, fake_j][0] != 'b':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (fake_i, shadow_j - 1), self.board)])
                        shadow_j = 0
                    else:
                        shadow_j = 0
                i = i - 1
                shadow_i = shadow_i + 1
                j = j + 1
                shadow_j = shadow_j - 1

        elif self.board[fake_i, fake_j][0] != 'w':
            while i - 1 > 0 or shadow_i + 1 < 8 or j + 1 < 8 or shadow_j - 1 > 0:
                count = count + 1
                if i - 1 > 0:  # go up and check, stop when encounter white or black piece
                    if self.board[i - 1, fake_j] == '--':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (i - 1, fake_j), self.board)])
                    elif self.board[i - 1, fake_j][0] == 'w' and self.board[fake_i, fake_j][0] != 'w':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (i - 1, fake_j), self.board)])
                        i = 0
                    else:
                        i = 0

                if shadow_i + 1 < 8:  # go down and check, stop when encounter white or black piece
                    if self.board[shadow_i + 1, fake_j] == '--':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (shadow_i + 1, fake_j), self.board)])
                    elif self.board[shadow_i + 1, fake_j][0] == 'w' and self.board[fake_i, fake_j][0] != 'w':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (shadow_i + 1, fake_j), self.board)])
                        shadow_i = 7
                    else:
                        shadow_i = 7

                if j + 1 < 8:  # go right and check, stop when black or white piece found
                    if self.board[fake_i, j + 1] == '--':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (fake_i, j + 1), self.board)])
                    elif self.board[fake_i, j + 1][0] == 'w' and self.board[fake_i, fake_j][0] != 'w':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (fake_i, j + 1), self.board)])
                        j = 7
                    else:
                        j = 7

                if shadow_j - 1 > 0:  # go left and check, stop when black or white piece found
                    if self.board[fake_i, shadow_j - 1] == '--':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (fake_i, shadow_j - 1), self.board)])
                    elif self.board[fake_i, shadow_j - 1][0] == 'w' and self.board[fake_i, fake_j][0] != 'w':
                        moves = np.append(moves, [MoveLib((fake_i, fake_j), (fake_i, shadow_j - 1), self.board)])
                        shadow_j = 0
                    else:
                        shadow_j = 0
                i = i - 1
                shadow_i = shadow_i + 1
                j = j + 1
                shadow_j = shadow_j - 1
        # print(count)
        return moves

    def get_all_bishop_moves(self, i, j, moves):
        fake_i = i
        fake_j = j
        shadow_i = i
        shadow_j_1 = j  # quad 1
        shadow_j_2 = j  # quad2

        shadow_j_3 = j  # quad 3
        shadow_j_4 = j  # quad 4
        if self.whiteToMove:
            while i - 1 > 0 or shadow_i + 1 < 8:
                if i - 1 > 0:
                    if shadow_j_1 + 1 < 8:
                        if self.board[i - 1, shadow_j_1 + 1] == '--':
                            moves = np.append(moves, [MoveLib((fake_i, fake_j), (i - 1, shadow_j_1 + 1), self.board)])
                        elif self.board[i - 1, shadow_j_1 + 1][0] == 'b':
                            moves = np.append(moves, [MoveLib((fake_i, fake_j), (i - 1, shadow_j_1 + 1), self.board)])
                        else:
                            shadow_j_1 = 7  # quad 1 is blocked now
                    if shadow_j_2 - 1 > 0:
                        if self.board[i - 1, shadow_j_2 - 1] == '--':
                            moves = np.append(moves, [MoveLib((fake_i, fake_j), (i - 1, shadow_j_2 - 1), self.board)])
                        elif self.board[i - 1, shadow_j_2 - 1][0] == 'b':
                            moves = np.append(moves, [MoveLib((fake_i, fake_j), (i - 1, shadow_j_2 - 1), self.board)])
                        else:
                            shadow_j_2 = 0  # quad 2 is blocked now
                elif shadow_i + 1 < 8:
                    if shadow_j_3 + 1 < 8:
                        if self.board[shadow_i + 1, shadow_j_3 + 1] == '--':
                            moves = np.append(moves,
                                              [MoveLib((fake_i, fake_j), (shadow_i + 1, shadow_j_3 + 1), self.board)])
                        elif self.board[i - 1, shadow_j_1 + 1][0] == 'b':
                            moves = np.append(moves,
                                              [MoveLib((fake_i, fake_j), (shadow_i + 1, shadow_j_3 + 1), self.board)])
                        else:
                            shadow_j_3 = 7  # quad 4 is blocked now
                    if shadow_j_4 - 1 > 0:
                        if self.board[shadow_i + 1, shadow_j_4 - 1] == '--':
                            moves = np.append(moves,
                                              [MoveLib((fake_i, fake_j), (shadow_i + 1, shadow_j_4 - 1), self.board)])
                        elif self.board[i - 1, shadow_j_4 - 1][0] == 'b':
                            moves = np.append(moves,
                                              [MoveLib((fake_i, fake_j), (shadow_i + 1, shadow_j_4 - 1), self.board)])
                        else:
                            shadow_j_4 = 0  # quad 3 is blocked now
                shadow_i = shadow_i + 1
                i = i - 1
                shadow_j_1 = shadow_j_1 + 1
                shadow_j_2 = shadow_j_2 - 1
                shadow_j_3 = shadow_j_3 + 1
                shadow_j_4 = shadow_j_4 - 1

        return moves

    def get_all_knight_moves(self, i, j, moves):
        pass

    def get_all_queen_moves(self, i, j, moves):
        pass

    def get_all_king_moves(self, i, j, moves):
        pass
