from .Features import Features, Feature
import chess

class SimpleFeatures(Features):
    def __init__(self):
        Features.__init__()
        self.append(TestFeature())


class AttackersFeature(Feature):
    def calculateValue(self, nextState: chess.Board, player):

        opponentSquareSet = chess.SquareSet()
        for piece_type in range(1, 7):
            squares = nextState.pieces(piece_type, not player)
            for square in squares:
                opponentSquareSet.add(square)

        sum = 0
        for square in opponentSquareSet:
            sum += len(nextState.attackers(player, square))

        return sum
