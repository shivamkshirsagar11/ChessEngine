class MoveLib:
    ranks_to_rows = {"1":7, "2":6, "3":5, "4":4, "5":3,"6":2,"7":1,"8":0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    cols_ranks = {"a":0, "b":1, "c":2, "d":3,"e":4, "f":5,"g":6,"h":7}
    reverse_col_ranks = {v: k for k, v in cols_ranks.items()}
    def __init__(self,start_sq,end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row,self.start_col]
        self.piece_captured = board[self.end_row, self.end_col]

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) +" - "+ self.get_rank_file(self.end_row, self.end_col)
    def get_rank_file(self, r,c ):
        return self.reverse_col_ranks[c] + self.rows_to_ranks[r]