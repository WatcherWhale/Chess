#!/usr/bin/python3
import chess
import os.path

#from searchagent.search_agent import SearchAgent
from chessUtil.State import State
from chessUtil.Agent import Agent

QUIET = False
LOUD = False

prevWhiteState = (None, None)
prevBlackState = (None, None)

def runEpisode(player: Agent):

    global prevWhiteState
    global prevBlackState

    board = chess.Board()

    running = True
    turn_white_player = True
    counter = 0

    while running and not board.is_game_over():
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
            print(board)
            print("###################")

        if board.is_checkmate():
            running = False

            player.update(state, action, state.newStateFromAction(action))

            if turn_white_player:
                print("Black wins!")
            else:
                print("White wins!")

        if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():

            running = False
            print("Stalemate")

            player.update(state, action, state.newStateFromAction(action))

        if turn_white_player:
            if prevBlackState[0] is not None:
                player.update(prevBlackState[0], prevBlackState[1], state.newStateFromAction(action))

            prevWhiteState = (state, action)
        else:
            if prevWhiteState[0] is not None:
                player.update(prevWhiteState[0], prevWhiteState[1], state.newStateFromAction(action))

            prevBlackState = (state, action)

    player.save()
    print(board.result())

    if not QUIET:
        print(board)
        print("###################")
