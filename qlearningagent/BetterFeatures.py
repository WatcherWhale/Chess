from .Features import Features, Feature
from chessUtil.Material import calculateMaterialAdvantage, calculateMaterialValue
from chessUtil.State import State
from chessUtil.Mobility import queenMobility, knightMobility, kingMobility, bishopMobility, rookMobility
from chessUtil.PositionParser import getRowColumn

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

        self.append(QueenMobilityFeature())
        self.append(KingMobilityFeature())
        self.append(KnightMobilityFeature())
        self.append(BischopMobilityFeature())

        self.append(CenterPossesionFeature())
        self.append(IsolationFeature())

        self.append(LightFirstRank())
        
        self.append(KingSelfAttacked())
        self.append(KingOpponentAttacked())

        self.append(HorizontalConnectedRooks())
        

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
        return len(nextState.getBoard().pieces(chess.PAWN, not state.getPlayer())) / 8.0

class TotalAmountPiecesFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "totalAmount"

    def calculateValue(self, state: State, action, nextState):       
        return (calculateMaterialValue(nextState, True) + calculateMaterialValue(nextState, False)) / 80.0

class TotalPiecesBalanceFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "totalPiecesBalance"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMaterialAdvantage(nextState, state.getPlayer())

class QueenMobilityFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "queenMobility"

    def calculateValue(self, state: State, action, nextState: State):
        queens = nextState.getBoard().pieces(chess.QUEEN, state.getPlayer())

        if len(queens) == 0:
            return 0

        minMobility = 64

        for queen in queens:
            minMobility = min(minMobility, queenMobility(queen, nextState.getBoard()))

        return minMobility

class KingMobilityFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "knightMobility"

    def calculateValue(self, state: State, action, nextState: State):
        minMobility = kingMobility(nextState.getBoard().pieces(chess.KING, state.getPlayer()).pop(), nextState.getBoard())

        return minMobility/8

class KnightMobilityFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "knightMobility"

    def calculateValue(self, state: State, action, nextState: State):
        knights = nextState.getBoard().pieces(chess.KNIGHT, state.getPlayer())

        if  len(knights) == 0:
            return 0

        minMobility = 64

        for knight in knights:
            minMobility = min(minMobility, knightMobility(knight, nextState.getBoard()))

        return minMobility/8

class BischopMobilityFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "bishopMobility"

    def calculateValue(self, state: State, action, nextState):
        bishops = nextState.getBoard().pieces(chess.BISHOP, state.getPlayer())

        if  len(bishops) == 0:
            return 0

        minMobility = 64

        for bishop in bishops:
            minMobility = min(minMobility, bishopMobility(bishop, nextState.getBoard()))

        return minMobility/13

class CenterPossesionFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "centerPossesion"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        sum = 0

        for s in [chess.D4, chess.E4, chess.D5, chess.E5]:
            piece = board.piece_at(s)
            sum += piece is not None and piece.color == state.getPlayer() and piece.piece_type == chess.PAWN

        return sum / 4.0

class IsolationFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "isolation"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        sum = 0

        pawns = board.pieces(chess.PAWN, state.getPlayer())

        for p1 in pawns:
            for p2 in pawns:
                if chess.square_distance(p1, p2) == 1:
                    sum += 1
                    break

        return (8 - sum) / 8.0

class LightFirstRank(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "lightFirstRank"  

    def calculateValue(self, state: State, action, nextState: State):
        sum = 0
        
        board = nextState.getBoard()

        #if player is white check squares B1, C1, F1 and G1
        #if player is black check squares B8, C8, F8 and G8
        if state.getPlayer():
            sum += ((board.piece_type_at(chess.B1) == 2) and board.color_at(chess.B1)) + ((board.piece_type_at(chess.G1) == 2) and board.color_at(chess.G1))
            sum += ((board.piece_type_at(chess.C1) == 3) and board.color_at(chess.C1)) + ((board.piece_type_at(chess.F1) == 3) and board.color_at(chess.F1))
        else:
            sum += ((board.piece_type_at(chess.B8) == 2) and (not board.color_at(chess.B1))) + ((board.piece_type_at(chess.G8) == 2) and (not board.color_at(chess.G8)))
            sum += ((board.piece_type_at(chess.C8) == 3) and (not board.color_at(chess.C8))) + ((board.piece_type_at(chess.F8) == 3) and (not board.color_at(chess.F8)))

        return sum / 4.0

class KingSelfAttacked(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "kingSelfAttacked"

    def calculateValue(self, state: State, action, nextState: State):
        return state.getBoard().is_check()


class KingOpponentAttacked(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "kingOpponentAttacked"

    def calculateValue(self, state: State, action, nextState: State):
        return nextState.getBoard().is_check()

class HorizontalConnectedRooks(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "horizontalConnectedRooks"

    def calculateValue(self, state: State, action, nextState: State):

        rooks = nextState.getBoard().pieces(chess.ROOK, state.getPlayer())

        if len(rooks) < 2:
            return False
        
        pairs = []

        for r1 in rooks:
            for r2 in rooks:
                if r1 == r2:
                    continue
                
                if (r2, r1) in pairs:
                    continue

                if getRowColumn(r1)[0] == getRowColumn(r2)[0]:
                    pairs.append((r1,r2))

        for r1, r2 in pairs:
            squares = chess.SquareSet().ray(r1, r2)
            notConnected = False

            for s in squares:
                if nextState.getBoard().piece_at(s) is not None:
                    notConnected = True
                    break
            if notConnected == False:
                return True

        return False
