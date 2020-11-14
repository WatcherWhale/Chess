#!/usr/bin/python3
import chess.pgn

import progressbar

from chessUtil.State import State
from chessUtil.Agent import Agent

QUIET = True
LOUD = False

def updateAgent(player, prevState, currentState):
    player.update(prevState[0], prevState[1], currentState)

def runEpisode(player: Agent):
    # get from https://raw.githubusercontent.com/niklasf/python-chess/master/data/pgn/kasparov-deep-blue-1997.pgn
    pgn = open("data/kasparov-deep-blue-1997.pgn")
    running = True

    while running:
        pgn_game = chess.pgn.read_game(pgn)

        if pgn_game:
            prevWhite = (None, None)
            prevBlack = (None, None)

            board = pgn_game.board()

            turnWhite = True

            moves = 0
            for move in pgn_game.mainline_moves():
                moves += 1


            for move in progressbar.progressbar(pgn_game.mainline_moves(), max_value=moves):
                state = State(board.copy(), turnWhite, player)

                if LOUD:
                    print(board)
                    print("###################")

                board.push(move)

                newState = State(board.copy(), not turnWhite, player)
                turnWhite = not turnWhite

                if turnWhite:
                    if prevWhite[0] is not None:
                        updateAgent(player, prevWhite, newState)
                    prevBlack = (state, move.uci())
                else:
                    if prevBlack[0] is not None:
                        updateAgent(player, prevBlack, newState)

                    prevWhite = (state, move.uci())
            player.save()
        else:
            running = False
