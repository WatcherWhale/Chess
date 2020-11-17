import chess
import progressbar

from chessUtil.State import State
from chessUtil.Agent import Agent

from ABAgent.ABAgent import ABAgent

from tom.search_agent import SearchAgent

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
    black_player = ABAgent(0.1, 0, 5)
    tom_player = SearchAgent()

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
            #move = chess.Move.from_uci(black_player.makeMove(state))
            move = tom_player.ab_minimax_r(state.getBoard())

        turn_white_player = not turn_white_player

        board.push(move)

        if LOUD:
            print('\n')
            print(board)
            print("###################")

        if board.is_checkmate():
            running = False

            if turn_white_player:
                print("\nTom wins")
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
            player.update(state, action, state.newStateFromAction(action))
        else:
            prevState = (state, action)

        moves += 1

        if moves >= MAX_MOVES * 2:
            bar.update(MAX_MOVES * 2)
            print('\nForcefully stopped')
            FORCEFULLY_STOPPED += 1
            running = False
