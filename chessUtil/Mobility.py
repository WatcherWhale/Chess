import chess
from .PositionParser import getRowColumn, getSquareFromRowColumn


def queenMobility(position: chess.Square, board: chess.Board):
    return bishopMobility(position,board) + rookHorizontalMobility(position, board) + rookVerticalMobility(position, board)


def kingMobility(position: chess.Square, board: chess.Board):
    row, column = getRowColumn(position)

    squares = []

    for r in range(-1, 2):
        for c in range(-1, 2):
            squares.append((row+r, column+c))
    squares.remove((row, column))

    sum = 0

    for s in squares:
        sum += s[0] > 0 and s[0] < 8 and s[1] > 0 and s[1] < 8 and board.is_legal(chess.Move(position, getSquareFromRowColumn(s[0], s[1])))

    return sum


def bishopMobility(position: chess.Square, board: chess.Board):
    row, column = getRowColumn(position)

    topLeft = getSquareFromRowColumn(row + min(7 - row, column), column - min(7 - row, column))
    topRight = getSquareFromRowColumn(row + min(7 - row, 7 - column), column + min(7 - row, 7 - column))
    bottomLeft = getSquareFromRowColumn(row - min(row, column), column - min(row, column))
    bottomRight = getSquareFromRowColumn(row - min(row, 7 - column), column + min(row, 7 - column))

    squares = chess.SquareSet.ray(topLeft, bottomRight)
    squares = squares.union(chess.SquareSet.ray(topRight, bottomLeft))

    sum = 0

    for s in squares:
        sum += board.is_legal(chess.Move(position,s))

    return sum


def knightMobility(position: chess.Square, board: chess.Board):
    row, column = getRowColumn(position)

    squares = []

    squares.append((row+1, column-2))
    squares.append((row+2, column-1))
    squares.append((row+2, column+1))
    squares.append((row+1, column+2))
    squares.append((row-1, column+2))
    squares.append((row-2, column+1))
    squares.append((row-2, column-1))
    squares.append((row-1, column-2))

    sum = 0

    for s in squares:
        sum += s[0] > 0 and s[0] < 8 and s[1] > 0 and s[1] < 8 and board.is_legal(chess.Move(position, getSquareFromRowColumn(s[0], s[1])))

    return sum


def rookHorizontalMobility(position: chess.Square, board: chess.Board):

    r, c = getRowColumn(position)

    squares = chess.SquareSet.ray(position, getSquareFromRowColumn(r, 0))
    squares = squares.union(chess.SquareSet.ray(position, getSquareFromRowColumn(r, 7)))

    sum = 0

    for s in squares:
        sum += board.is_legal(chess.Move(position, s))

    return sum


def rookVerticalMobility(position: chess.Square, board: chess.Board):
    r, c = getRowColumn(position)

    squares = chess.SquareSet.ray(position, getSquareFromRowColumn(0, c))
    squares = squares.union(chess.SquareSet.ray(position, getSquareFromRowColumn(7, c)))

    sum = 0

    for s in squares:
        sum += board.is_legal(chess.Move(position, s))

    return sum


def rookMobility(position: chess.Square, board: chess.Board):
    return rookHorizontalMobility(position, board) + rookVerticalMobility(position,board)


def pawnMobility(position: chess.Square, board: chess.Board):
    return 0

mobilityFunction = [pawnMobility, knightMobility, bishopMobility, rookMobility, queenMobility, kingMobility]

def totalMobility(board: chess.Board, player):
    mobility = 0

    #go over every piece type followed by the amount of pieces of that type and calculate the mobility with the corresponding mobility calculation

    for piece_type in range(1, 7):
        for position in board.pieces(piece_type, player):
            mobility += mobilityFunction[piece_type-1](position, board)

    return mobility
