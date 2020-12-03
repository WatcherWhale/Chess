import inspect
import sys
import itertools
import numpy as np


from .Features import Features, Feature
from chessUtil.Material import calculateMaterialAdvantage, calculateMaterialValue, getMaterialValue
from chessUtil.State import State
from chessUtil.Mobility import mobilityFunction
from chessUtil.PositionParser import getRowColumn, getSquareFromRowColumn, scoreMatrix

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


def calculateMobility(nextState: State, piece_type, self):
    board = nextState.getBoard().copy()
    player = nextState.getPlayer()

    if self:
        board.turn = not board.turn
        pieces = board.pieces(piece_type, not player)
    else:
        pieces = board.pieces(piece_type, player)

    if len(pieces) == 0:
        return 0

    sum = 0

    for piece in pieces:
        sum += mobilityFunction[piece_type-1](piece, board)

    return sum


class MobilityQueenS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityQueenS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, chess.QUEEN, True) / 26.0


class MobilityQueenO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityQueenO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, chess.QUEEN, False) / 26.0


class MobilityKingS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityKingS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, chess.KING, True) / 8.0


class MobilityKingO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityKingO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, chess.KING, False) / 8.0


class MobilityKnightS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityKnightS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, chess.KNIGHT, True) / 8.0


class MobilityKnightO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityKnightO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateMobility(nextState, chess.KNIGHT, False) / 8.0


class MobilityBishopS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityBishopS"

    def calculateValue(self, state: State, action, nextState):
        return calculateMobility(nextState, chess.BISHOP, True) / 13.0


class MobilityBishopO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "mobilityBishopO"

    def calculateValue(self, state: State, action, nextState):
        return calculateMobility(nextState, chess.BISHOP, False) / 13.0


def calculateCenterControl(nextState: State, player: bool):
    board = nextState.getBoard()
    sum = 0

    for s in [chess.D4, chess.E4, chess.D5, chess.E5]:
        piece = board.piece_at(s)
        sum += piece is not None and piece.color == player and piece.piece_type == chess.PAWN

    return sum / 4.0


class CenterControlS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "centerControlS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateCenterControl(nextState, state.getPlayer())


class CenterControlO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "centerControlO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateCenterControl(nextState, not state.getPlayer())


def calculateIsolationPawn(nextState: State, player: bool):
    board = nextState.getBoard()
    sum = 0

    pawns = board.pieces(chess.PAWN, player)

    for p1 in pawns:
        for p2 in pawns:
            if chess.square_distance(p1, p2) == 1:
                sum += 1
                break

    return (8 - sum) / 8.0


class IsolationPawnS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "isolationPawnS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateIsolationPawn(nextState, state.getPlayer())


class IsolationPawnO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "isolationPawnO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateIsolationPawn(nextState, not state.getPlayer())


def calculateLightFirstRank(nextState: State, player: bool):
    sum = 0

    board = nextState.getBoard()

    # if player is white check squares B1, C1, F1 and G1
    # if player is black check squares B8, C8, F8 and G8
    if player:
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


class LightFirstRankS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "lightOnFirstRankS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateLightFirstRank(nextState, state.getPlayer())


class LightFirstRankO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "lightOnFirstRankO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateLightFirstRank(nextState, not state.getPlayer())


class KingAttacked(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "kingAttacked"

    def calculateValue(self, state: State, action, nextState: State):
        return nextState.getBoard().is_check()


def calculateConnectedRooks(nextState: State, player: bool, isVertical: bool):

    rooks = nextState.getBoard().pieces(chess.ROOK, player)

    if len(rooks) < 2:
        return False

    # more than 2 rooks is possible
    pairs = list(itertools.combinations(rooks, 2))

    filteredPairs = []
    for pair in pairs:
        if getRowColumn(pair[0])[isVertical] == getRowColumn(pair[1])[isVertical]:
            filteredPairs.append(pair)

    if filteredPairs:
        # filteredPairs is not empty
        isConnected = True
        for r1, r2 in filteredPairs:
            squares = chess.SquareSet().between(r1, r2)

            for s in squares:
                if nextState.getBoard().piece_at(s) is not None:
                    isConnected = False
            if isConnected:
                return True

    return False


class ConnectedRooksHorizontalS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "connectedRooksHorizontalS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateConnectedRooks(nextState, state.getPlayer(), False)


class ConnectedRooksHorizontalO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "connectedRooksHorizontalO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateConnectedRooks(nextState, not state.getPlayer(), False)


class ConnectedRooksVerticalS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "connectedRooksVerticalS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateConnectedRooks(nextState, state.getPlayer(), True)


class ConnectedRooksVerticalO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "connectedRooksVerticalO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateConnectedRooks(nextState, not state.getPlayer(), True)


def calculatePawnFork(nextState: State, player: bool):

    board = nextState.getBoard()
    pawns = board.pieces(chess.PAWN, player)
    sum = 0

    for p in pawns:
        r, c = getRowColumn(p)

        if 0 < c < 7:

            forked_piece1 = board.piece_at(getSquareFromRowColumn(r + 1, c - 1))
            forked_piece2 = board.piece_at(getSquareFromRowColumn(r + 1, c + 1))

            if forked_piece1 is not None and forked_piece2 is not None and forked_piece1.piece_type > 1 and forked_piece2.piece_type > 1 \
                    and forked_piece1.color is not player and forked_piece2.color is not player:
                sum += 1

    return sum / 8.0


class ForkPawnS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "forkPawnS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculatePawnFork(nextState, state.getPlayer())


class ForkPawnO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "forkPawnO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculatePawnFork(nextState, not state.getPlayer())


def calculateForkKnights(nextState: State, player: bool):

    board = nextState.getBoard()
    knights = board.pieces(chess.KNIGHT, player)
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
            if 0 <= rowColumn[0] < 8 and 0 <= rowColumn[1] < 8 and amountSuperior < 2:
                if board.piece_at(getSquareFromRowColumn(rowColumn[0], rowColumn[1])) is not None and board.color_at(square) is not player:
                    amountSuperior += board.piece_at(square).piece_type > 2

        if amountSuperior >= 2:
            sum += 1

    return sum / 2.0


class ForkKnightS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "forkKnightS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateForkKnights(nextState, state.getPlayer())


class ForkKnightO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "forkKnightO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateForkKnights(nextState, not state.getPlayer())


# DistanceToCenterKingO can't be changed by current player so isn't useful.
class DistanceToCenterKingS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "distanceToCenterKingS"

    def calculateValue(self, state: State, action, nextState: State):
        kingSet = nextState.getBoard().pieces(chess.KING, state.getPlayer())
        king = kingSet.pop()

        centerSquares = chess.SquareSet()
        centerSquares.update(chess.E4, chess.D4, chess.E5, chess.D5)
        minDistance = 99
        for square in centerSquares:
            minDistance = min(minDistance, chess.square_distance(king, square))

        return minDistance / 16


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


def calculateRooksOnSeventhRankForPlayer(nextState: State, player):
    if player == chess.WHITE:
        seven = 6
    else:
        seven = 1

    amount = 0
    rookSet = nextState.getBoard().pieces(chess.ROOK, player)
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


def calculateAttacked(nextState: State, attacked_piece_type, inferior_pieces_range, self: bool):
    board = nextState.getBoard().copy()
    player = nextState.getPlayer()

    if not self:
        board.turn = not board.turn
        player = not player

    attacked_pieces = board.pieces(attacked_piece_type, not player)

    sum = 0
    for ap in attacked_pieces:

        attacked = False

        if inferior_pieces_range is not None:
            for piece_type in inferior_pieces_range:

                for piece in board.pieces(piece_type, player):
                    attacked = board.is_legal(chess.Move(piece, ap))

                if attacked:
                    break

        else:
            for piece in board.pieces(chess.PAWN, player):
                attacked = board.is_legal(chess.Move(piece, ap))

        if attacked:
            sum += 1
            break

    return sum


class AttackedQueensS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "attackedQueensS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttacked(nextState, chess.QUEEN, range(1, 5), True)


class AttackedRooksS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "attackedRooksS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttacked(nextState, chess.ROOK, range(1, 4), True)


class AttackedBishopsS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "attackedBishopsS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttacked(nextState, chess.BISHOP, None, True)


class AttackedKnightsS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "attackedKnightS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttacked(nextState, chess.KNIGHT, None, True)


class AttackedQueensO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "attackedQueensO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttacked(nextState, chess.QUEEN, range(1, 5), False)


class AttackedRooksO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "attackedRooksO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttacked(nextState, chess.ROOK, range(1, 4), False)


class AttackedBishopsO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "attackedBishopsO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttacked(nextState, chess.BISHOP, None, False)


class AttackedKnightsO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "attackedKnightO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateAttacked(nextState, chess.KNIGHT, None, False)


class IsCastling(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "isCastling"

    def calculateValue(self, state: State, action, nextState: State):
        return state.getBoard().is_castling(chess.Move.from_uci(action))


def calculateDoubledPawns(nextState: State, player: bool):
    board = nextState.getBoard()

    columns = np.zeros(8)

    for p in board.pieces(chess.PAWN, player):
        r, c = getRowColumn(p)
        columns[c] += 1

    return sum(columns > 1)


class DoubledPawnsS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "doubledPawnsS"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateDoubledPawns(nextState, state.getPlayer())


class DoubledPawnsO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "doubledPawnsO"

    def calculateValue(self, state: State, action, nextState: State):
        return calculateDoubledPawns(nextState, not state.getPlayer())


class BoardControl(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "boardControl"

    def calculateValue(self, state: State, action, nextState: State):

        board = nextState.getBoard()
        player = state.getPlayer()

        emptySquareSet = chess.SquareSet()

        for i in range(0, 64):
            piece = board.piece_at(i)
            if piece is None:
                emptySquareSet.add(i)

        controlS = 0.0
        controlO = 0.0

        for square in emptySquareSet:
            attackersPlayer = nextState.getBoard().attackers(player, square)
            attackersNotPlayer = nextState.getBoard().attackers(not player, square)

            smallestValue = 10
            smallestPiece = None

            for a in itertools.chain(attackersPlayer, attackersNotPlayer):
                a_value = getMaterialValue(board.piece_type_at(a))
                if smallestValue > a_value:
                    smallestValue = a_value
                    smallestPiece = a
                if smallestPiece and smallestValue == a_value and board.color_at(smallestPiece) is not board.color_at(a):
                    smallestPiece = None    # Both teams can access the empty square with same value pieces
                    if smallestValue == 1:
                        break

            if smallestPiece:
                if board.color_at(smallestPiece) == player:
                    controlS += 1
                else:
                    controlO += 1

        return (controlS - controlO)/64


class PositionScoreBalanceS(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "positionScoreBalanceS"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        score = 0

        for piece_type in range(1, 7):
            for p in board.pieces(piece_type, state.getPlayer()):
                m = np.asmatrix(scoreMatrix[piece_type - 1])
                flip = np.flipud(m)
                r, c = getRowColumn(p)
                score += flip[r, c]

        return score / 10.0

class PositionScoreBalanceO(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "positionScoreBalanceO"

    def calculateValue(self, state: State, action, nextState: State):
        board = nextState.getBoard()
        score = 0

        for piece_type in range(1, 7):
            for p in board.pieces(piece_type, not state.getPlayer()):
                m = np.asmatrix(scoreMatrix[piece_type - 1])
                r, c = getRowColumn(p)
                score += m[r, c]

        return score / 10.0

class CheckMate(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "checkMate"

    def calculateValue(self, state: State, action, nextState: State):
        return nextState.getBoard().is_checkmate()
