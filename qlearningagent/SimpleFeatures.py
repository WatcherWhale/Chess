from .Features import Features, Feature
from .State import State

import chess

class SimpleFeatures(Features):
    def __init__(self):
        Features.__init__(self)
        self.append(AttackersFeature())
        self.append(CheckFeature())
        self.append(DistanceToEnemyKing())

class AttackersFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "attackers"

    def calculateValue(self, state: State, action):
        nextState = state.newStateFromAction(action)

        opponentSquareSet = chess.SquareSet()
        for piece_type in range(1, 7):
            squares = nextState.getBoard().pieces(piece_type, not state.isWhite())
            for square in squares:
                opponentSquareSet.add(square)

        s = 0.0
        for square in opponentSquareSet:
            s += len(nextState.getBoard().attackers(state.isWhite(), square))

        return s/10

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

        kingSet = nextState.getBoard().pieces(chess.KING, not state.isWhite())
        king = kingSet.pop()

        minDistance = 16

        for piece_type in range(1,7):
            for piece in nextState.getBoard().pieces(piece_type, state.isWhite()):
                minDistance = min(minDistance, chess.square_distance(piece, king))

        return minDistance / 16
