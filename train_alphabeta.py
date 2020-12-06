import chess
import progressbar

from chessUtil.State import State
from chessUtil.Agent import Agent

from ABAgent.ABAgent import ABAgent

LOUD = False
QUIET = False
MAX_MOVES = 130

STALEMATES = 0
AB_WINS = 0
GRANDQ_WINS = 0
FORCEFULLY_STOPPED = 0


def runEpisode(player: Agent):

    global STALEMATES
    global AB_WINS
    global GRANDQ_WINS
    global FORCEFULLY_STOPPED

    board = chess.Board()
    black_player = ABAgent(player.getGoTime(), player.getDeltaTime(), player.getMaxDepth())

    running = True
    turn_white_player = True

    prevState = (None, None)

    moves = 0

    bar = progressbar.ProgressBar(max_value=MAX_MOVES * 2)

    while running:
        bar.update(moves)
        move = None
        state = State(board.copy(), turn_white_player, player)

        if turn_white_player:
            move = chess.Move.from_uci(player.makeMove(state))
        else:
            move = chess.Move.from_uci(black_player.makeMove(state))


        turn_white_player = not turn_white_player

        board.push(move)

        if LOUD:
            print('\n')
            print(board)
            print("###################")

        debug = False
        if board.is_checkmate():
            debug = True
            running = False


            if turn_white_player:
                print("\nAlpha Beta wins")
                AB_WINS += 1
            else:
                print("\nGrandQ wins!")
                GRANDQ_WINS += 1

        if board.is_stalemate():
            running = False
            print("\nStalemate")
            STALEMATES += 1

        action = move.uci()

        if not turn_white_player:
            if prevState[0] is not None:
                player.update(prevState[0], prevState[1], state.newStateFromAction(action))
        elif not running:
            player.update(prevState[0], prevState[1], state.newStateFromAction(action))
            bar.__del__()
        else:
            prevState = (state, action)

        moves += 1

        if moves >= MAX_MOVES * 2:
            print('\nForcefully stopped')
            FORCEFULLY_STOPPED += 1
            running = False
