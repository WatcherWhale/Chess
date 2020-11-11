import chess

from chessUtil.State import State
from chessUtil.Agent import Agent

from ABAgent.ABAgent import ABAgent

LOUD = False
QUIET = False

def runEpisode(player: Agent):
    board = chess.Board()
    black_player = ABAgent(0.1, 0, 5)

    running = True
    turn_white_player = True

    prevState = (None, None)

    while running:
        move = None
        state = State(board.copy(), turn_white_player, player)

        if turn_white_player:
            move = chess.Move.from_uci(player.makeMove(state))
        else:
            move = chess.Move.from_uci(black_player.makeMove(state))

        turn_white_player = not turn_white_player

        board.push(move)

        if LOUD:
            print(board)
            print("###################")

        if board.is_checkmate():
            running = False

            if turn_white_player:
                print("Alpha Beta wins")
            else:
                print("GrandQ wins!")

        if board.is_stalemate():
            running = False
            print("Stalemate")

        action = move.uci()

        if not turn_white_player:
            if prevState[0] is not None:
                player.update(prevState[0], prevState[1], state.newStateFromAction(action))
        elif not running:
            player.update(state, action, state.newStateFromAction(action))
        else:
            prevState = (state, action)
