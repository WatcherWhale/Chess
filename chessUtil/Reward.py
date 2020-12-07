from .State import State
from .Material import calculateMaterialAdvantage

import chess

# afblijven

def calculateReward(state: State, action, nextState: State):

    # state: player moet nog een zet doen
    # nextState: opponent heeft zet net gedaan

    reward = 0

    if nextState.getBoard().is_checkmate():
        if nextState.getBoard().turn is not state.getPlayer():
            return 100
        else:
            return -100
    elif nextState.getBoard().is_stalemate() or nextState.getBoard().is_insufficient_material() \
            or nextState.getBoard().is_seventyfive_moves() or nextState.getBoard().is_fivefold_repetition():
        return -30

    if nextState.getBoard().is_check():
        reward += -2
    elif state.newStateFromAction(action).getBoard().is_check():
        reward += 2

    reward += calculateMaterialAdvantage(nextState, nextState.getPlayer())

    reward += state.getBoard().is_castling(chess.Move.from_uci(action)) * 2

    return reward

