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

def runEpisode(white_player: Agent):

    global FORCEFULLY_STOPPED
    global GRANDQ_WINS
    global AB_WINS
    global STALEMATES

    black_player = ABAgent(white_player.getGoTime(), white_player.getDeltaTime(), white_player.getMaxDepth())

    state = State(chess.Board(), True, white_player)

    running = True
    action = None
    prevState = (None, None)
    moves = 0

    bar = progressbar.ProgressBar(max_value=2*MAX_MOVES)

    while running:

        if state.getPlayer():
            action = white_player.makeMove(state)
        else:
            action = black_player.makeMove(state)

        halfState = state.newStateFromAction(action)

        if halfState.isTerminalState():
            if halfState.getBoard().is_checkmate():
                if state.getPlayer():
                    print("\nGrandQ has won!")
                    GRANDQ_WINS += 1
                else:
                    print("\nAlpha-Beta has won")
                    AB_WINS += 1
            else:
                print("\nStalemate")
                STALEMATES += 1

            running = False

        if not state.getPlayer():
            white_player.update(prevState[0], prevState[1], halfState)
        elif not running:
            white_player.update(state, action, halfState)
        else:
            prevState = (state, action)

        if LOUD:
            print(state.getBoard())

        state = halfState
        moves += 1
        bar.update(moves)

        if moves >= MAX_MOVES*2:
            print("\nForcefully stopped")
            FORCEFULLY_STOPPED += 1
            running = False
