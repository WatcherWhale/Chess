import chess



def queenMobility(position: chess.Square, board: chess.Board):
    return bishopMobility(position,board) + rookHorizontalMobility(position, board) + rookVerticalMobility(position, board)


def kingMobility(position: chess.Square, board: chess.Board):
    return 0

    
def bishopMobility(position: chess.Square, board: chess.Board):
    return 0

    
def knightMobility(position: chess.Square, board: chess.Board):
    return 0


def rookHorizontalMobility(position: chess.Square, board: chess.Board):
    return 0


def rookVerticalMobility(position: chess.Square, board: chess.Board):
    return 0

def rookMobility(position: chess.Square, board: chess.Board):
    return rookHorizontalMobility(position, board) + rookVerticalMobility(position,board)
    
def pawnMobility(position: chess.Square, board: chess.Board):
    return 0

mobilityFunction = [pawnMobility, knightMobility, bishopMobility, rookMobility, queenMobility, kingMobility]  


def totalMobility(board: chess.Board, player):
    
    mobility=0

    #go over every piece type followed by the amount of pieces of that type and calculate the mobility with the corresponding mobility calculation

    for piece_type in range(1,7):                                       
        for position in board.pieces(piece_type, player):
            mobility += mobilityFunction[piece_type-1](position, board)     

    return mobility        