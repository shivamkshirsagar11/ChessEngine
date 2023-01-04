from threading import Thread
from time import sleep

import numpy as np

from ChessEngine.Board import GameBoard


class CalculateNextMoveThread(Thread):
    def __init__(self,game_state:GameBoard,sleep_time):
        Thread.__init__(self)
        self.arr = np.array([])
        self.game_state = game_state
        self.sleep_time = sleep_time
    def run(self):
        self.arr = self.game_state.all_valid_move_c_check()
        sleep(self.sleep_time)