import chess

from .State import State
from .Material import calculateMaterialValue
from .Mobility import totalMobility
from .ChessFeatures import ChessFeatures

features = ChessFeatures()

def utility(state: State):
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

    return value + features.utility(state)
