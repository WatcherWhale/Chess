#!/usr/bin/python3
import chess.pgn
import chessUtil.Reward
from chessUtil.State import State
import qlearningagent.QAgent

QUIET = False

def updateAgent(player, prevState, currentState):
    reward = chessUtil.Reward.calculateReward(prevState[0], prevState[1], currentState)
    player.update(prevState[0], prevState[1], reward, currentState)

def runEpisode(player: qlearningagent.QAgent.QAgent):
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

            for move in pgn_game.mainline_moves():
                state = State(board.copy(), turnWhite)

                if not QUIET:
                    print(board)
                    print("###################")

                board.push(move)

                newState = State(board.copy(), not turnWhite)
                turnWhite = not turnWhite

                if turnWhite:
                    if prevWhite[0] is not None:
                        updateAgent(player, prevWhite, newState)
                    prevBlack = (state, move.uci())
                else:
                    if prevBlack[0] is not None:
                        updateAgent(player, prevBlack, newState)

                    prevWhite = (state, move.uci())

        else:
            running = False

        player.save()
