from .Features import Features, Feature
from .State import State

import chess


class SimpleFeatures(Features):
    def __init__(self):
        Features.__init__(self)
        self.append(SelfAttackersFeature())
        self.append(OpponentAttackersFeature())
        self.append(CheckFeature())
        self.append(DistanceToEnemyKing())


class SelfAttackersFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "sattackers"

    def calculateValue(self, state: State, action):
        return calculateAttackersForPlayer(state, action, state.getPlayer())


class OpponentAttackersFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "oattackers"

    def calculateValue(self, state: State, action):
        return calculateAttackersForPlayer(state, action, not state.getPlayer())


def calculateAttackersForPlayer(state: State, action, player):
    nextState = state.newStateFromAction(action)

    opponentSquareSet = chess.SquareSet()
    for piece_type in range(1, 7):
        squares = nextState.getBoard().pieces(piece_type, not player)
        for square in squares:
            opponentSquareSet.add(square)

    s = 0.0
    for square in opponentSquareSet:
        s += len(nextState.getBoard().attackers(player, square))

    return s / 16


class CheckFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "check"

    def calculateValue(self, state: State, action):

        nextState = state.newStateFromAction(action)

        if (nextState.getBoard().is_check()):
            return 1.0
        else:
            return 0.0


class DistanceToEnemyKing(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "distance"

    def calculateValue(self, state: State, action):
        nextState = state.newStateFromAction(action)

        kingSet = nextState.getBoard().pieces(chess.KING, not state.getPlayer())
        king = kingSet.pop()

        minDistance = 16

        for piece_type in range(1, 7):
            for piece in nextState.getBoard().pieces(piece_type, state.getPlayer()):
                minDistance = min(minDistance, chess.square_distance(piece, king))

        return minDistance / 16
