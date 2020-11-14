#!/usr/bin/python3
import chess
import progressbar
import os.path

#from searchagent.search_agent import SearchAgent
from chessUtil.State import State
from chessUtil.Agent import Agent

QUIET = False
LOUD = False
MAX_MOVES = 130
STALEMATES = 0
BLACK_WINS = 0
WHITE_WINS = 0
FORCEFULLY_STOPPED = 0

prevWhiteState = (None, None)
prevBlackState = (None, None)

def runEpisode(player: Agent):

    global prevWhiteState
    global prevBlackState

    global STALEMATES
    global BLACK_WINS
    global WHITE_WINS
    global FORCEFULLY_STOPPED

    board = chess.Board()

    running = True
    turn_white_player = True
    counter = 0

    bar = progressbar.ProgressBar(max_value=MAX_MOVES * 2)
    while running and not board.is_game_over():
        bar.update(counter)
        counter += 1
        action = None
        state = State(board.copy(), turn_white_player, player)

        action = player.makeMove(state)
        if action == None:
            print(board)
            exit(1)

        turn_white_player = not turn_white_player

        board.push(chess.Move.from_uci(action))

        if LOUD:
            print('\n')
            print(board)
            print("###################")

        if board.is_checkmate():
            running = False

            player.update(state, action, state.newStateFromAction(action))

            if turn_white_player:
                print("\nBlack wins!")
                BLACK_WINS += 1

            else:
                print("\nWhite wins!")
                WHITE_WINS += 1

        if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():

            running = False
            print("\nStalemate")
            STALEMATES += 1

            player.update(state, action, state.newStateFromAction(action))

        if turn_white_player:
            if prevBlackState[0] is not None:
                player.update(prevBlackState[0], prevBlackState[1], state.newStateFromAction(action))

            prevWhiteState = (state, action)
        else:
            if prevWhiteState[0] is not None:
                player.update(prevWhiteState[0], prevWhiteState[1], state.newStateFromAction(action))

            prevBlackState = (state, action)

        if not running:
            player.update(state, action, state.newStateFromAction(action))

        if counter >= MAX_MOVES * 2:
            bar.update(MAX_MOVES * 2)
            print('\nForcefully stopped')
            FORCEFULLY_STOPPED += 1
            running = False

    print(board.result())

    if not QUIET:
        print(board)
        print("###################")
