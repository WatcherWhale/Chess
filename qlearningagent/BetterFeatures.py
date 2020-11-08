from .Features import Features, Feature
from .Reward import getPieceReward, calculatePieceAdvantage
from .State import State
from ..chessUtil.Mobility import queenMobility, knightMobility, kingMobility, bishopMobility, rookMobility

import chess


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

class AmountSelfQueensFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountSelfQueens"

    def calculateValue(self, state: State, action):
        
        nextState = state.newStateFromAction(action)
        return len(nextState.getBoard().pieces(chess.QUEEN, state.getPlayer())) / 2.0
        
class AmountOpponentQueensFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountOpponentQueens"

    def calculateValue(self, state: State, action):
        
        nextState = state.newStateFromAction(action)
        return len(nextState.getBoard().pieces(chess.QUEEN, not state.getPlayer())) / 2.0  

class AmountSelfRooksFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountSelfRooks"

        def calculateValue(self, state: State, action):
            
            nextState = state.newStateFromAction(action)
            return len(nextState.getBoard().pieces(chess.ROOK, state.getPlayer())) / 2.0

class AmountOpponentRooksFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountOpponentRooks"

    def calculateValue(self, state: State, action):
        
        nextState = state.newStateFromAction(action)
        return len(nextState.getBoard().pieces(chess.ROOK, not state.getPlayer())) / 2.0              

class AmountSelfBishopsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountSelfBishops"

        def calculateValue(self, state: State, action):
            
            nextState = state.newStateFromAction(action)
            return len(nextState.getBoard().pieces(chess.BISHOP, state.getPlayer())) / 2.0

class AmountOpponentBishopsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountOpponentBishops"

        def calculateValue(self, state: State, action):
            
            nextState = state.newStateFromAction(action)
            return len(nextState.getBoard().pieces(chess.BISHOP, not state.getPlayer())) / 2.0

class AmountSelfKnightsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountSelfKnights"

        def calculateValue(self, state: State, action):
            
            nextState = state.newStateFromAction(action)
            return len(nextState.getBoard().pieces(chess.KNIGHT, state.getPlayer())) / 2.0

class AmountOpponentKnightsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountOpponentKnights"

        def calculateValue(self, state: State, action):
            
            nextState = state.newStateFromAction(action)
            return len(nextState.getBoard().pieces(chess.KNIGHT, not state.getPlayer())) / 2.0

class AmountSelfPawnsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountSelfPawns"

        def calculateValue(self, state: State, action):
            
            nextState = state.newStateFromAction(action)
            return len(nextState.getBoard().pieces(chess.PAWN, state.getPlayer())) / 8.0

class AmountOpponentPawnsFeature(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "amountOpponentPawns"

        def calculateValue(self, state: State, action):
            
            nextState = state.newStateFromAction(action)
            return len(nextState.getBoard().pieces(chess.PAWNS, not state.getPlayer())) / 8.0

class TotalAmountPiecesFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "totalAmount"

    def calculateValue(self, state: State, action):
        
        nextState = state.newStateFromAction(action)
        sum=0

        for pieceType in range(1,7):
            sum += len(nextState.getBoard().pieces(piece_type, True)) * getPieceReward(piece_type)
            sum += len(nextState.getBoard().pieces(piece_type, False)) * getPieceReward(piece_type)
        
        return sum/(80.0)

class TotalPiecesBalanceFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "totalPiecesBalance"

    def calculateValue(self, state: State, action):
        
        nextState = state.newStateFromAction(action)
        return calculatePieceAdvantage(state,nextState)

class QueensMobilityFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "queensMobility"

    def calculateValue(self, state: State, action):

        nextState = state.newStateFromAction(action)
        queens = nextState.getBoard().pieces(chess.QUEEN, state.getPlayer())
        
        if  len(queens) == 0
            return 0

        minMobility = 64

        for queen in queens:
            minMobility = min(minMobility, queenMobility(queen))
            
        return minMobility

class KingMobilityFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "knightMobility"

    def calculateValue(self, state: State, action):

        nextState = state.newStateFromAction(action)
        
        minMobility = kingMobility(king)
            
        return minMobility/8

class KnightMobilityFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "knightMobility"

    def calculateValue(self, state: State, action):

        nextState = state.newStateFromAction(action)
        knights = nextState.getBoard().pieces(chess.KNIGHT, state.getPlayer())
        
        if  len(knights) == 0
            return 0

        minMobility = 64

        for knight in knights:
            minMobility = min(minMobility, knightMobility(knight))
            
        return minMobility/8

class BischopMobilityFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "bishopMobility"

    def calculateValue(self, state: State, action):

        nextState = state.newStateFromAction(action)
        bishops = nextState.getBoard().pieces(chess.BISHOP, state.getPlayer())
        
        if  len(bishops) == 0
            return 0

        minMobility = 64

        for bishop in bishop:
            minMobility = min(minMobility, bishopMobility(bishop))
            
        return minMobility/13