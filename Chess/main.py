import pygame as p
from ChessEngine.Board import GameBoard
from ChessEngine.MoveLibrary import MoveLib
from ChessEngine.Threading import CalculateNextMoveThread as moveThread
from threading import Thread
import numpy as np


HEIGHT = WIDTH = 800  # HEIGHT AND WIDTH OF CHESS BOARD
DIMENTIONS = 8  # DIMENTION OF CHESS BOARD
SQ_SIZE = HEIGHT // DIMENTIONS  # SQUARE SIZE
MAX_FPS = 30  # FOR ANIMATION
IMAGES = {}
RUNNING = False
SCALE_PIECE = 3
GAMENAME = "ChessPass"
CONTRIBUTED = "github.com/shivamkshirsagar11"
'''
load the images dictionary of images. this will be called only once in main
'''


def load_images():
    piece = np.array(
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR', 'bP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR', 'wP'])
    for i in piece:
        IMAGES[i] = p.transform.scale(p.image.load("../Images/Pieces/" + i + ".svg"),
                                      (SCALE_PIECE * SQ_SIZE, SCALE_PIECE * SQ_SIZE))


'''
now our main driver code this will handle user inputs and graphics design.
'''

'''
draw_board draws/adds squares onn game state board
'''


def draw_board(screen):
    colors = np.array([p.Color(255, 204, 153), p.Color(153, 102, 51)])
    for i in range(DIMENTIONS):
        for j in range(DIMENTIONS):
            p.draw.rect(screen, colors[(i + j) % 2], p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
draw_pieces is responsible for drawing pieces on square with respect to current game state's board
'''


def draw_pieces(screen, board):
    for i in range(DIMENTIONS):
        for j in range(DIMENTIONS):
            curr_piece = board[i, j]
            # if it's not an empty square
            if curr_piece != "--":
                screen.blit(IMAGES[curr_piece], p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
draw_game_state is responsible for all graphics related to game state 
'''


def draw_game_state(screen, gbs):
    # print("state drawn")
    draw_board(screen)  # draw square on board
    # add in piece high-lightning or move suggestion (later)
    draw_pieces(screen, gbs.board)  # draw pieces on top of square


def main():
    p.init()
    load_images()  # will only do this once in game playing period
    p.display.set_caption(f'{GAMENAME} ~ {CONTRIBUTED}')
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    game_state = GameBoard()
    valid_moves = game_state.all_valid_move_c_check()
    move_made = False
    moving = False
    global RUNNING
    if not RUNNING:
        RUNNING = True
    print(f'Playing game: {RUNNING}')
    selected_square = ()  # to keep track of last click of user[tuple(row, column)]
    player_click_log_from_to = np.array([])  # keep track of player clicks
    while RUNNING:
        # print(f'Selected Square: {selected_square}')
        # print(f'Player Clicks: {player_click_log_from_to}')
        for e in p.event.get():
            if e.type == p.QUIT:
                RUNNING = False
            elif e.type == p.MOUSEBUTTONDOWN:
                moving = True
                location = p.mouse.get_pos()  # (x,y) location of mouse
                row = location[1] // SQ_SIZE
                col = location[0] // SQ_SIZE
                if selected_square == (row, col):  # user selected same square to move
                    # de-select current selected piece and remove any previous moves and clicks
                    selected_square = ()
                    player_click_log_from_to = np.array([])

                else:
                    # store current move and append with last move
                    selected_square = (row, col)
                    player_click_log_from_to = np.append(player_click_log_from_to, [selected_square])
                    # print(player_click_log_from_to)

                if player_click_log_from_to.size == 4:
                    # when move made becomes (row, column) * 2 == making 4 vals
                    print(f'Player turn {"White" if game_state.whiteToMove else "Black"}')
                    # make intermediate temp move object
                    move = MoveLib(player_click_log_from_to[0:2].astype(int), player_click_log_from_to[2:4].astype(int),
                                   game_state.board)

                    # now check if current selected move is '--'; then discard all
                    if game_state.board[int(player_click_log_from_to[0]), int(player_click_log_from_to[1])] == '--':
                        player_click_log_from_to = np.array([])
                        selected_square = ()

                    else:
                        # current selected is not '--'
                        print(f'{move.get_chess_notation()},ID: {move}')
                        # now if made move is in valid moves list, then do  proceed further
                        if move in valid_moves:
                            game_state.make_move(move)  # making move here
                            move_made = True  # this will enable to generate new possible moves with updated board
                        # after move is made clear our current move and from-to-move-log of game
                        player_click_log_from_to = np.array([])
                        selected_square = ()

            elif e.type == p.KEYDOWN:

                # undo current move
                if e.key == p.K_z and game_state.move_log.size > 0:
                    game_state.undo_moves()
                    selected_square = ()
                    player_click_log_from_to = np.array([])
                    move_made = True
                # re-do undoed move
                elif e.key == p.K_u and game_state.undo_moves_log.size > 0:
                    game_state.redo_moves()
                    move_made = True
                    selected_square = ()
                    player_click_log_from_to = np.array([])

        # check if valid move made then updatte valid movelist with new
        # draw_game_state(screen, game_state)
        thread = Thread(target = draw_game_state, args=(screen, game_state))
        thread.start()
        thread.join()
        if move_made:
            print("start")
            mode_thread = moveThread(game_state,1)
            mode_thread.start()
            valid_moves = mode_thread.arr
            print("end")
            move_made = False

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
    print(f'Playing game: {RUNNING}')
