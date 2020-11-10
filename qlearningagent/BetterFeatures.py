from .Features import Features, Feature
from chessUtil.Material import calculateMaterialAdvantage, calculateMaterialValue
from chessUtil.State import State
from chessUtil.Mobility import queenMobility, knightMobility, kingMobility, bishopMobility, rookMobility
from chessUtil.PositionParser import getRowColumn, getSquareFromRowColumn

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
        self.append(VerticalConnectedRooks())

        self.append(PawnFork())
        
        self.append(SelfKingDistanceToCenterFeature())
        self.append(OpponentKingDistanceToCenterFeature())
        self.append(SelfConnectivity())
        self.append(OpponentConnectivity())
        self.append(SelfRooksOnSeventhRank())
        self.append(OpponentRooksOnSeventhRank())
        self.append(QueensAttacked())
        

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

class VerticalConnectedRooks(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "verticalConnectedRooks"

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

                if getRowColumn(r1)[1] == getRowColumn(r2)[1]:
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

class PawnFork(Feature):
    def __init__(self):
            Feature.__init__(self)
            self.name = "pawnFork"

    def calculateValue(self, state: State, action, nextState: State):

        board = nextState.getBoard()
        pawns = board.pieces(chess.PAWN, state.getPlayer())
        sum = 0

        if state.getPlayer():
            for p in pawns:
                r,c = getRowColumn(p)
                if r < 7 and c > 0 and c < 7:
                    if board.piece_at(getSquareFromRowColumn(r+1,c-1)) is not None and board.piece_at(getSquareFromRowColumn(r+1,c+1)) is not None:
                        sum += board.piece_at(getSquareFromRowColumn(r+1,c-1)).piece_type > 1 and not board.color_at(getSquareFromRowColumn(r+1,c-1)) \
                        and board.piece_at(getSquareFromRowColumn(r+1,c+1)).piece_type > 1 and not board.color_at(getSquareFromRowColumn(r+1,c+1))

        else:
            for p in pawns:
                r,c = getRowColumn(p)
                if r > 1  and c > 0 and c < 7:
                    if board.piece_at(getSquareFromRowColumn(r-1,c-1)) is not None and board.piece_at(getSquareFromRowColumn(r-1,c+1)) is not None:
                        sum += board.piece_at(getSquareFromRowColumn(r-1,c-1)).piece_type > 1 and board.color_at(getSquareFromRowColumn(r-1,c-1)) \
                        and board.piece_at(getSquareFromRowColumn(r-1,c+1)).piece_type > 1 and board.color_at(getSquareFromRowColumn(r-1,c+1))
                
        return sum / 8.0

class KnightFork(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "knightFork"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        knights = board.pieces(chess.KNIGHT, state.getPlayer())
        sum=0

        for k in knights:
            r,c = getRowColumn(p)

            squares = []
            squares.append((r+1, c-2))
            squares.append((r+2, c-1))
            squares.append((r+2, c+1))
            squares.append((r+1, c+2))
            squares.append((r-1, c+2))
            squares.append((r-2, c+1))
            squares.append((r-2, c-1))
            squares.append((r-1, c-2))

            amountSuperior = 0

            for s in squares:
                if s[0] > 0 and s[0] < 8 and s[1] > 0 and s[1] < 8 and amountSuperior < 2:
                    if board.piece_at(getSquareFromRowColumn(s[0],s[1])) is not None:
                        if state.getPlayer():
                            amountSuperior += board.piece_at(getSquareFromRowColumn(s[0],s[1])).piece_type > 2 and not board.color_at(getSquareFromRowColumn(s[0],s[1]))
                        else:
                            amountSuperior += board.piece_at(getSquareFromRowColumn(s[0],s[1])).piece_type > 2 and board.color_at(getSquareFromRowColumn(s[0],s[1]))

            if amountSuperior >= 2:
                sum += 1
        
        return sum/2.0



def calculateKingDistancetoCenter(nextState: State, player):
    kingSet = nextState.getBoard().pieces(chess.KING, player)
    king = kingSet.pop()

    centerSquares = chess.SquareSet()
    centerSquares.update(chess.E4, chess.D4, chess.E5, chess.D5)
    minDistance = 99
    for square in centerSquares:
        minDistance = min(minDistance, chess.square_distance(king, square))

    return minDistance / 16


class SelfKingDistanceToCenterFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "selfkingcenterdistance"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateKingDistancetoCenter(nextState, state.getPlayer())


class OpponentKingDistanceToCenterFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "opponentkingcenterdistance"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateKingDistancetoCenter(nextState, not state.getPlayer())


class SelfConnectivity(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "selfconnectivity"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateDefendersForPlayer(nextState, action, state.getPlayer())


class OpponentConnectivity(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "opponentconnectivity"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateDefendersForPlayer(nextState, action, not state.getPlayer())


def calculateDefendersForPlayer(nextState: State, action, player):

    opponentSquareSet = chess.SquareSet()
    for piece_type in range(1, 7):
        squares = nextState.getBoard().pieces(piece_type, player)
        for square in squares:
            opponentSquareSet.add(square)

    s = 0.0
    for square in opponentSquareSet:
        s += len(nextState.getBoard().attackers(player, square))

    return s / 16


def calculateRooksOnSeventhRankForPlayer(nextstate, player):
    if player == chess.WHITE:
        seven = 7
    else:
        seven = 2

    amount = 0
    rookSet = nextstate.getBoard().pieces(chess.ROOK, player)
    for rook in rookSet:
        if chess.square_rank(rook) == seven:
            amount += 1

    return amount


class SelfRooksOnSeventhRank(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "selfrooks7th"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateRooksOnSeventhRankForPlayer(nextState, state.getPlayer())


class OpponentRooksOnSeventhRank(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "opponentrooks7th"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateRooksOnSeventhRankForPlayer(nextState, not state.getPlayer())

class QueensAttacked(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "queensAttacked"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        queens = board.pieces(chess.QUEEN, state.getPlayer())

        sum = 0

        for q in queens:

            attacked = False

            for piece_type in range(1,4):
                for piece in board.pieces(piece_type, not state.getPlayer()):
                    attacked = board.is_legal(chess.Move(q,piece_type))

                    if attacked:
                        break

            if attacked:
                sum += 1
                break

        return sum

class RooksAttacked(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "rooksAttacked"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        rooks = board.pieces(chess.ROOK, state.getPlayer())

        sum = 0

        for r in rooks:

            attacked = False

            for piece_type in range(1,3):
                for piece in board.pieces(piece_type, not state.getPlayer()):
                    attacked = board.is_legal(chess.Move(r,piece_type))

                    if attacked:
                        break

            if attacked:
                sum += 1
                break

        return sum

class BishopsAttacked(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "bischopsAttacked"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        bishops = board.pieces(chess.BISHOP, state.getPlayer())

        sum = 0

        for b in bishops:

            attacked = False

            for piece in board.pieces(chess.PAWN, not state.getPlayer()):
                attacked = board.is_legal(chess.Move(q,chess.PAWN))

                if attacked:
                    sum += 1
                    break

        return sum

class KnightsAttacked(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "knightsAttacked"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        knights = board.pieces(chess.KNIGHT, state.getPlayer())

        sum = 0

        for k in knights:

            attacked = False

            for piece in board.pieces(chess.PAWN, not state.getPlayer()):
                attacked = board.is_legal(chess.Move(k,chess.PAWN))

                if attacked:
                    sum += 1
                    break

        return sum