#!/usr/bin/python3
import chess
import chess.engine

import os.path

from chessUtil.State import State
from chessUtil.Agent import Agent

STOCKFISH_BIN = '/usr/bin/stockfish'
QUIET = False
LOUD = False
LIMIT = 5.0
MAX_MOVES = 130

STALEMATES = 0
STOCKFISH_WINS = 0
GRANDQ_WINS = 0


def runEpisode(player: Agent):

    global STALEMATES
    global STOCKFISH_WINS
    global GRANDQ_WINS


    board = chess.Board()
    black_player = chess.engine.SimpleEngine.popen_uci(STOCKFISH_BIN)
    limit = chess.engine.Limit(time=LIMIT)

    running = True
    turn_white_player = True

    prevState = (None, None)
    moves = 0

    while running:
        move = None
        moves += 1

        state = State(board.copy(), turn_white_player, player)

        if turn_white_player:
            move = chess.Move.from_uci(player.makeMove(state))
            turn_white_player = False

        else:
            move = black_player.play(board, limit).move
            turn_white_player = True

        board.push(move)

        if LOUD:
            print(board)
            print("###################")

        if board.is_checkmate():
            running = False

            if turn_white_player:
                print("Stockfish wins!")
                STOCKFISH_WINS += 1
            else:
                print("GrandQ wins!")
                GRANDQ_WINS += 1

        if board.is_stalemate():
            running = False
            print("Stalemate")
            STALEMATES += 1

        action = move.uci()
        if not turn_white_player:
            if prevState[0] is not None:
                player.update(prevState[0], prevState[1], state.newStateFromAction(action))
        elif not running:
            player.update(state, action, state.newStateFromAction(action))
        else:
            prevState = (state, action)

        if moves >= MAX_MOVES * 2:
            print('Forcefully stopped')
            running = False

    black_player.quit()

    if not QUIET:
        print(board)
        print("###########################")
