from Features import Features, Feature
from State import State

import chess

class SimpleFeatures(Features):
    def __init__(self):
        Features.__init__(self)
        self.append(AttackersFeature())
        self.append(CheckFeature())

class AttackersFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "attackers"

    def calculateValue(self, state: State, action):
        nextState = state.newStateFromAction(action)

        opponentSquareSet = chess.SquareSet()
        for piece_type in range(1, 7):
            squares = nextState.getBoard().pieces(piece_type, not nextState.isWhite())
            for square in squares:
                opponentSquareSet.add(square)

        sum = 0
        for square in opponentSquareSet:
            sum += len(nextState.getBoard().attackers(nextState.isWhite(), square))

        return sum

class CheckFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "check"

    def calculateValue(self, state: State, action):
        return float(state.getBoard().gives_check(chess.Move.from_uci(action)))
