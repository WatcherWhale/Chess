import chess


def getRowColumn(square: chess.Square):
    return (chess.square_rank(square), chess.square_file(square))

def getSquareFromRowColumn(row, column):
    return chess.Square(row*8 + column)