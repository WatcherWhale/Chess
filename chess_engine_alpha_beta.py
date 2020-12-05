#!/usr/bin/python3
import chess
from ABAgent.ABAgent import ABAgent
from chessUtil.State import State

# https://ucichessengine.wordpress.com/2011/03/16/description-of-uci-protocol/

def uci(name, author):
    print("""id name {}
        id author {}

        option name DeltaTime type spin default 100 min 0 max 2000
        option name MaxDepth type spin default 10 min 1 max 200
        uciok""".format(name, author))


def main():
    board = chess.Board()
    player = ABAgent(maxDepth=2)

    running = True

    while running:
        input_val = input().split(' ')

        if len(input_val) > 2:
            if input_val[0] == "position" and \
                    input_val[1] == "startpos" and \
                    input_val[2] == "moves":
                board = chess.Board()
                for move in input_val[3::]:
                    board.push_uci(move)

            elif input_val[0] == "go":

                goTime = 5000

                if input_val[1] == "movetime":
                    goTime = float(input_val[2])

                player.setGoTime(goTime / 1000)

                action = player.makeMove(State(board, board.turn, player))
                print("bestmove {}".format(action))

            elif input_val[0] == "setoption":
                if input_val[2] == "DeltaTime":
                    player.setDeltaTime(float(input_val[-1])/1000)
                elif input_val[2] == "MaxDepth":
                    player.setMaxDepth(int(input_val[-1]))

            else:
                print("error command: {}".format(input_val))

        elif len(input_val) > 1:
            if input_val[0] == "position" and \
                    input_val[1] == "startpos":
                board = chess.Board()
                for move in input_val[3::]:
                    board.push_uci(move)

            else:
                print("error command: {}".format(input_val))

        elif len(input_val) > 0:

            if input_val[0] == "uci":
                uci(name="GrandAlphabet", author="Mathias Maes, Willem van der Elst, Tijs Van Alphen")

            elif input_val[0] == "quit":
                running = False

            elif input_val[0] == "ucinewgame":
                board = chess.Board()

            elif input_val[0] == "isready":
                print("readyok")

            else:
                print("error command: {}".format(input_val))

if __name__ == "__main__":
    main()
