from Features import Features, Feature
from State import State

import chess

class SimpleFeatures(Features):
    def __init__(self):
        Features.__init__()
        self.append(AttackersFeature())


class AttackersFeature(Feature):
    def calculateValue(self, nextState: State):

        opponentSquareSet = chess.SquareSet()
        for piece_type in range(1, 7):
            squares = nextState.getBoard().pieces(piece_type, not nextState.isWhite())
            for square in squares:
                opponentSquareSet.add(square)

        sum = 0
        for square in opponentSquareSet:
            sum += len(nextState.getBoard().attackers(nextState.isWhite(), square))

        return sum
