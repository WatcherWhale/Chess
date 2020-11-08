from .Features import Features, Feature
from .Reward import getPieceReward, calculatePieceAdvantage
from .State import State
from ..chessUtil.Mobility import queenMobility, knightMobility, kingMobility, bishopMobility, rookMobility

import chess

# Source: https://areeweb.polito.it/didattica/gcia/tesine/Tesine_2016/Mannella/Thesis_Mannen-Learning_to_Play_Chess_Using_Reinforcement_Learning.pdf

class BetterFeatures(Features):
    def __init__(self):
        Features.__init__(self)
        self.append(AmountSelfQueensFeature())
        self.append(AmountOpponentQueensFeature())
        self.append(AmountSelfRooksFeature())
        self.append(AmountOpponentRooksFeature())
        self.append(AmountSelfBishopsFeature())
        self.append(AmountOpponentBishopsFeature())
        self.append(AmountSelfKnightsFeature())
        self.append(AmountOpponentKnightsFeature())
        self.append(AmountSelfPawnsFeature())
        self.append(AmountOpponentPawnsFeature())
        self.append(TotalAmountPiecesFeature())
        self.append(TotalPiecesBalanceFeature())
        self.append(CenterPossesionFeature())
        self.append(IsolationFeature())

class AmountSelfQueensFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountSelfQueens"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.QUEEN, state.getPlayer())) / 2.0

class AmountOpponentQueensFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountOpponentQueens"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.QUEEN, not state.getPlayer())) / 2.0  

class AmountSelfRooksFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountSelfRooks"

        def calculateValue(self, state: State, action, nextState: State):
            return len(nextState.getBoard().pieces(chess.ROOK, state.getPlayer())) / 2.0

class AmountOpponentRooksFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountOpponentRooks"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.ROOK, not state.getPlayer())) / 2.0

class AmountSelfBishopsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountSelfBishops"

        def calculateValue(self, state: State, action, nextState: State):
            return len(nextState.getBoard().pieces(chess.BISHOP, state.getPlayer())) / 2.0

class AmountOpponentBishopsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountOpponentBishops"

        def calculateValue(self, state: State, action, nextState: State):
            return len(nextState.getBoard().pieces(chess.BISHOP, not state.getPlayer())) / 2.0

class AmountSelfKnightsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountSelfKnights"

        def calculateValue(self, state: State, action, nextState: State):
            return len(nextState.getBoard().pieces(chess.KNIGHT, state.getPlayer())) / 2.0

class AmountOpponentKnightsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountOpponentKnights"

        def calculateValue(self, state: State, action, nextState: State):
            return len(nextState.getBoard().pieces(chess.KNIGHT, not state.getPlayer())) / 2.0

class AmountSelfPawnsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountSelfPawns"

        def calculateValue(self, state: State, action, nextState: State):
            return len(nextState.getBoard().pieces(chess.PAWN, state.getPlayer())) / 8.0

class AmountOpponentPawnsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountOpponentPawns"

        def calculateValue(self, state: State, action, nextState):
            return len(nextState.getBoard().pieces(chess.PAWNS, not state.getPlayer())) / 8.0

class TotalAmountPiecesFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "totalAmount"

    def calculateValue(self, state: State, action, nextState):
        sum=0

        for pieceType in range(1,7):
            sum += len(nextState.getBoard().pieces(piece_type, True)) * getPieceReward(piece_type)
            sum += len(nextState.getBoard().pieces(piece_type, False)) * getPieceReward(piece_type)

        return sum/(80.0)

class TotalPiecesBalanceFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "totalPiecesBalance"

    def calculateValue(self, state: State, action, nextState: State):
        return calculatePieceAdvantage(state,nextState)

class QueensMobilityFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "queensMobility"

    def calculateValue(self, state: State, action, nextState: State):
        queens = nextState.getBoard().pieces(chess.QUEEN, state.getPlayer())

        if len(queens) == 0
            return 0

        minMobility = 64

        for queen in queens:
            minMobility = min(minMobility, queenMobility(queen))

        return minMobility

class KingMobilityFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "knightMobility"

    def calculateValue(self, state: State, action, nextState: State):
        minMobility = kingMobility(king)

        return minMobility/8

class KnightMobilityFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "knightMobility"

    def calculateValue(self, state: State, action, nextState: State):
        knights = nextState.getBoard().pieces(chess.KNIGHT, state.getPlayer())

        if  len(knights) == 0
            return 0

        minMobility = 64

        for knight in knights:
            minMobility = min(minMobility, knightMobility(knight))

        return minMobility/8

class CenterPossesionFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "centerPossesion"

    def calculateValue(self, state: State, action, nexState: State):

        board : chess.Board = nextState.getBoard()
        sum = 0

        for s in chess.BB_CENTER:
            piece = board.piece_at(s)
            sum += piece.color == state.getPlayer() and piece.piece_type == chess.PAWN

        return sum / 4.0

class IsolationFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "isolation"

    def calculateValue(self, state: State, action, nexState: State):

        board : chess.Board = nextState.getBoard()
        sum = 0

        pawns = board.pieces(chess.PAWN, state.getPlayer())

        for p1 in pawns:
            for p2 in pawns:
                if chess.square_distance(p1, p2) == 1:
                    sum += 1
                    break

        return (8 - sum)
