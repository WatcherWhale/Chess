import chess

from .State import State
from .Material import calculateMaterialValue
from .Mobility import totalMobility
from .Features import Features
from .PositionParser import scoreMatrix


def utility(state: State, features: Features):
    value = 0

    if state.getBoard().is_checkmate():
        return 100
    elif state.getBoard().is_stalemate() or state.getBoard().is_insufficient_material() \
            or state.getBoard().is_seventyfive_moves() or state.getBoard().is_fivefold_repetition():
        return -30

    prevState, action = state.getPreviousState()

    if prevState.getBoard().is_castling(chess.Move.from_uci(action)):
        value += 2

    if state.getBoard().is_check():
        value += 2

    value += calculateMaterialValue(state, state.getPlayer())

    value += totalMobility(state.getBoard(), state.getPlayer())

    for i in range(0, 64):
        piece = state.getBoard().piece_at(i)
        if piece is not None:
            if piece.color is state.getBoard().turn:
                value += scoreMatrix[piece.piece_type - 1][i] / 10.0
            else:
                value -= scoreMatrix[piece.piece_type - 1][63 - i] / 10.0

    return value + features.calculateFeatures(prevState, action)
