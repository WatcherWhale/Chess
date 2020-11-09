from .State import State

import chess


def calculateMaterialValue(state: State, player):
    material = 0
    for piece_type in range(1, 7):
        material += getMaterialValue(piece_type) * len(state.getBoard().pieces(piece_type, player))

    return material

def calculateMaterialAdvantage(state: State, player):
    return calculateMaterialValue(state, player) - calculateMaterialValue(state, not player)

def getMaterialValue(piece_type):
    if piece_type is chess.PAWN or piece_type is chess.KING:
        return 1
    elif piece_type is chess.KNIGHT or piece_type is chess.BISHOP:
        return 3
    elif piece_type is chess.ROOK:
        return 5
    elif piece_type is chess.QUEEN:
        return 9

    return 0
