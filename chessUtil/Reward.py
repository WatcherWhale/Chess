from .State import State
from .Material import calculateMaterialAdvantage

import chess


def calculateReward(state: State, action, nextState: State):

    # state: player moet nog een zet doen
    # nextState: opponent heeft zet net gedaan

    reward = 0

    if nextState.getBoard().is_checkmate():
        if nextState.getBoard().turn == state.getPlayer():
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

    reward += getCastleReward(state, chess.Move.from_uci(action))

    return reward


def getCastleReward(state: State, move):
    return state.getBoard().is_castling(move) * 2
