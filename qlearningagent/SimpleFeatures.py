from .Features import Features, Feature
from .Reward import calculatePieceAdvantage
from .State import State

import chess

class SimpleFeatures(Features):
    def __init__(self):
        Features.__init__(self)
        self.append(SelfAttackersFeature())
        self.append(OpponentAttackersFeature())
        self.append(CheckFeature())
        self.append(NextCheckFeature())
        self.append(DistanceToEnemyKing())
        self.append(AdvantageFeature())
        self.append(NextAdvantageFeature())


class SelfAttackersFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "sattackers"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttackersForPlayer(state, action, state.getPlayer(), nextState)


class OpponentAttackersFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "oattackers"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttackersForPlayer(state, action, not state.getPlayer(), nextState)


def calculateAttackersForPlayer(state: State, action, player, nextState):

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

    def calculateValue(self, state: State, action, nextState):

        if (nextState.getBoard().is_check()):
            return 1.0
        else:
            return 0.0

class NextCheckFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "ncheck"

    def calculateValue(self, state: State, action, nextState: State):

        checkMoves = 0
        for action in nextState.getLegalActions():
            nextNextState = nextState.newStateFromAction(action)
            if nextNextState.getBoard().is_check():
                checkMoves += 1

        return checkMoves / 16.0


class DistanceToEnemyKing(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "distance"

    def calculateValue(self, state: State, action, nextState: State):

        kingSet = nextState.getBoard().pieces(chess.KING, not state.getPlayer())
        king = kingSet.pop()

        minDistance = 16

        for piece_type in range(1, 7):
            for piece in nextState.getBoard().pieces(piece_type, state.getPlayer()):
                minDistance = min(minDistance, chess.square_distance(piece, king))

        return minDistance / 16

class AdvantageFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "advantage"

    def calculateValue(self, state: State, action, nextState: State):
        nextState = state.newStateFromAction(action)
        return calculatePieceAdvantage(state, nextState) / 39

class NextAdvantageFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "nextadvantage"

    def calculateValue(self, state: State, action, nextState: State):
        minAdvantage = 40

        for nextAction in nextState.getLegalActions():
            nextNextState = nextState.newStateFromAction(nextAction)
            minAdvantage = min(minAdvantage, calculatePieceAdvantage(state, nextNextState))

        return minAdvantage / 40
