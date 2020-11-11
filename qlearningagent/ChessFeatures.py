import inspect
import sys

from .Features import Features, Feature
from chessUtil.Material import calculateMaterialAdvantage, calculateMaterialValue
from chessUtil.State import State
from chessUtil.Mobility import mobilityFunction
from chessUtil.PositionParser import getRowColumn, getSquareFromRowColumn
from ABAgent.ABAgent import ABAgent

import chess


# Source: https://areeweb.polito.it/didattica/gcia/tesine/Tesine_2016/Mannella/Thesis_Mannen-Learning_to_Play_Chess_Using_Reinforcement_Learning.pdf


#################
# S -> Self     #
# O -> Opponent #
#################

class ChessFeatures(Features):
    def __init__(self):
        Features.__init__(self)

        classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        for c in classes:
            if issubclass(c[1], Feature) and c[0] != "Feature":
                self.append(c[1]())

class AmountQueensS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountQueensS"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.QUEEN, state.getPlayer())) / 3.0


class AmountQueensO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountQueensO"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.QUEEN, not state.getPlayer())) / 3.0


class AmountRooksS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountRooksS"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.ROOK, state.getPlayer())) / 2.0


class AmountRooksO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountRooksO"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.ROOK, not state.getPlayer())) / 2.0


class AmountBishopsS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountBishopsS"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.BISHOP, state.getPlayer())) / 2.0


class AmountBishopsO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountBishopsO"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.BISHOP, not state.getPlayer())) / 2.0


class AmountKnightsS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountKnightsS"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.KNIGHT, state.getPlayer())) / 2.0


class AmountKnights0(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountKnightsO"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.KNIGHT, not state.getPlayer())) / 2.0


class AmountPawnsS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountPawnsS"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.PAWN, state.getPlayer())) / 8.0


class AmountPawnsO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "amountPawnsO"

    def calculateValue(self, state: State, action, nextState: State):
        return len(nextState.getBoard().pieces(chess.PAWN, not state.getPlayer())) / 8.0


class AmountTotalPieces(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "totalPiecesAmount"

    def calculateValue(self, state: State, action, nextState: State):
        return (calculateMaterialValue(nextState, True) + calculateMaterialValue(nextState, False)) / 80.0


class AmountBalancePieces(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "totalPiecesBalance"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMaterialAdvantage(nextState, state.getPlayer())


def calculateMobility(nextState: State, player, piece_type, mirror):
    board = nextState.getBoard()
    pieces = board.pieces(piece_type, player)

    if len(pieces) == 0:
        return 0

    sum =0
    if mirror:
        board = board.mirror()

    for piece in pieces:
        sum += mobilityFunction[piece_type-1](piece, board)

    return sum


class MobilityQueenS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityQueenS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, state.getPlayer(), chess.QUEEN, True) / 26.0


class MobilityQueenO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityQueenO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, not state.getPlayer(), chess.QUEEN, False) / 26.0


class MobilityKingS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityKingS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, state.getPlayer(), chess.KING, True) / 8.0


class MobilityKingO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityKingO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, not state.getPlayer(), chess.KING, False) / 8.0


class MobilityKnightS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityKnightS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, state.getPlayer(), chess.KNIGHT, True) / 8.0


class MobilityKnightO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityKnightO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, not state.getPlayer(), chess.KNIGHT, False) / 8.0


class MobilityBishopS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityBishopS"

    def calculateValue(self, state: State, action, nextState):
        return calculateMobility(nextState, state.getPlayer(), chess.BISHOP, True) / 13.0


class MobilityBishopO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityBishopO"

    def calculateValue(self, state: State, action, nextState):
        return calculateMobility(nextState, not state.getPlayer(), chess.BISHOP, False) / 13.0


class CenterPossessionS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "centerPossessionS"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        sum = 0

        for s in [chess.D4, chess.E4, chess.D5, chess.E5]:
            piece = board.piece_at(s)
            sum += piece is not None and piece.color == state.getPlayer() and piece.piece_type == chess.PAWN

        return sum / 4.0


class IsolationPawnS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "isolationS"

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


class LightFirstRankS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "lightOnFirstRankS"

    def calculateValue(self, state: State, action, nextState: State):
        sum = 0

        board = nextState.getBoard()

        # if player is white check squares B1, C1, F1 and G1
        # if player is black check squares B8, C8, F8 and G8
        if state.getPlayer():
            sum += ((board.piece_type_at(chess.B1) == 2) and board.color_at(chess.B1)) + (
                    (board.piece_type_at(chess.G1) == 2) and board.color_at(chess.G1))
            sum += ((board.piece_type_at(chess.C1) == 3) and board.color_at(chess.C1)) + (
                    (board.piece_type_at(chess.F1) == 3) and board.color_at(chess.F1))
        else:
            sum += ((board.piece_type_at(chess.B8) == 2) and (not board.color_at(chess.B1))) + (
                    (board.piece_type_at(chess.G8) == 2) and (not board.color_at(chess.G8)))
            sum += ((board.piece_type_at(chess.C8) == 3) and (not board.color_at(chess.C8))) + (
                    (board.piece_type_at(chess.F8) == 3) and (not board.color_at(chess.F8)))

        return sum / 4.0


class KingAttacked(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "kingAttacked"

    def calculateValue(self, state: State, action, nextState: State):
        return nextState.getBoard().is_check()


class HorizontalConnectedRooksS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "horizontalConnectedRooksS"

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
                    pairs.append((r1, r2))

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


class VerticalConnectedRooksS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "verticalConnectedRooksS"

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
                    pairs.append((r1, r2))

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


class PawnForkS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "pawnForkS"

    def calculateValue(self, state: State, action, nextState: State):

        board = nextState.getBoard()
        pawns = board.pieces(chess.PAWN, state.getPlayer())
        sum = 0

        if state.getPlayer():
            for p in pawns:
                r, c = getRowColumn(p)
                if r < 7 and c > 0 and c < 7:
                    if board.piece_at(getSquareFromRowColumn(r + 1, c - 1)) is not None and board.piece_at(
                            getSquareFromRowColumn(r + 1, c + 1)) is not None:
                        sum += board.piece_at(
                            getSquareFromRowColumn(r + 1, c - 1)).piece_type > 1 and not board.color_at(
                            getSquareFromRowColumn(r + 1, c - 1)) \
                               and board.piece_at(
                            getSquareFromRowColumn(r + 1, c + 1)).piece_type > 1 and not board.color_at(
                            getSquareFromRowColumn(r + 1, c + 1))

        else:
            for p in pawns:
                r, c = getRowColumn(p)
                if r > 1 and c > 0 and c < 7:
                    if board.piece_at(getSquareFromRowColumn(r - 1, c - 1)) is not None and board.piece_at(
                            getSquareFromRowColumn(r - 1, c + 1)) is not None:
                        sum += board.piece_at(getSquareFromRowColumn(r - 1, c - 1)).piece_type > 1 and board.color_at(
                            getSquareFromRowColumn(r - 1, c - 1)) \
                               and board.piece_at(
                            getSquareFromRowColumn(r - 1, c + 1)).piece_type > 1 and board.color_at(
                            getSquareFromRowColumn(r - 1, c + 1))

        return sum / 8.0


class KnightForkS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "knightForkS"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        knights = board.pieces(chess.KNIGHT, state.getPlayer())
        sum = 0

        for k in knights:
            r, c = getRowColumn(k)

            rowColumns = []
            rowColumns.append((r + 1, c - 2))
            rowColumns.append((r + 2, c - 1))
            rowColumns.append((r + 2, c + 1))
            rowColumns.append((r + 1, c + 2))
            rowColumns.append((r - 1, c + 2))
            rowColumns.append((r - 2, c + 1))
            rowColumns.append((r - 2, c - 1))
            rowColumns.append((r - 1, c - 2))

            amountSuperior = 0

            for rowColumn in rowColumns:
                square = getSquareFromRowColumn(rowColumn[0], rowColumn[1])
                if rowColumn[0] > 0 and rowColumn[0] < 8 and rowColumn[1] > 0 and rowColumn[1] < 8 and amountSuperior < 2:
                    if board.piece_at(getSquareFromRowColumn(rowColumn[0], rowColumn[1])) is not None:
                        if state.getPlayer():
                            amountSuperior += board.piece_at(square).piece_type > 2 and not board.color_at(square)
                        else:
                            amountSuperior += board.piece_at(square).piece_type > 2 and board.color_at(square)

            if amountSuperior >= 2:
                sum += 1

        return sum / 2.0


def calculateKingDistanceToCenter(nextState: State, player):
    kingSet = nextState.getBoard().pieces(chess.KING, player)
    king = kingSet.pop()

    centerSquares = chess.SquareSet()
    centerSquares.update(chess.E4, chess.D4, chess.E5, chess.D5)
    minDistance = 99
    for square in centerSquares:
        minDistance = min(minDistance, chess.square_distance(king, square))

    return minDistance / 16


class DistanceToCenterKingS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "distanceToCenterKingS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateKingDistanceToCenter(nextState, state.getPlayer())


class DistanceToCenterKingO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "distanceToCenterKingO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateKingDistanceToCenter(nextState, not state.getPlayer())


def calculateAttackers(attackingPlayer, attackedPlayer, nextState):
    attackedSquareSet = chess.SquareSet()
    for piece_type in range(1, 7):
        squares = nextState.getBoard().pieces(piece_type, attackedPlayer)
        for square in squares:
            attackedSquareSet.add(square)

    s = 0.0
    for square in attackedSquareSet:
        s += len(nextState.getBoard().attackers(attackingPlayer, square))

    return s / 16


class ProvokersS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "provokersS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttackers(state.getPlayer(), not state.getPlayer(), nextState)


class ProvokersO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "provokersO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttackers(not state.getPlayer(), state.getPlayer(), nextState)


class ConnectivityS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "connectivityS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttackers(state.getPlayer(), state.getPlayer(), nextState)


class ConnectivityO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "connectivityO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttackers(not state.getPlayer(), not state.getPlayer(), nextState)


def calculateRooksOnSeventhRankForPlayer(nextstate: State, player):
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


class RooksOnSeventhRankS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "Rooks7thS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateRooksOnSeventhRankForPlayer(nextState, state.getPlayer())


class RooksOnSeventhRankO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "Rooks7thO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateRooksOnSeventhRankForPlayer(nextState, not state.getPlayer())


class AlphaBeta(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "alphaBeta"

    def calculateValue(self, state: State, action, nextState: State):
        divider = len(state.getLegalActions())
        agent = ABAgent(state.getAgent().getGoTime() / divider, state.getAgent().getDeltaTime() / divider, state.getAgent().getMaxDepth())
        didMove = action == agent.makeMove(state.copy())

        return didMove


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
        self.name = "bishopsAttacked"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        bishops = board.pieces(chess.BISHOP, state.getPlayer())

        sum = 0

        for b in bishops:

            attacked = False

            for piece in board.pieces(chess.PAWN, not state.getPlayer()):
                attacked = board.is_legal(chess.Move(b,chess.PAWN))

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


class IsCastling(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "isCastling"

    def calculateValue(self, state: State, action, nextState: State):
        return state.getBoard().is_castling(chess.Move.from_uci(action))
