from .State import State
import chess

def calculateReward(state: State, action, nextState: State):

    reward = 0

    if nextState.getBoard().is_checkmate():
        if nextState.getBoard().turn == nextState.getPlayer():
            return 100
        else:
            return -100
    elif nextState.getBoard().is_stalemate() or nextState.getBoard().is_insufficient_material() \
            or nextState.getBoard().is_seventyfive_moves() or nextState.getBoard().is_fivefold_repetition():
        return -30

    if nextState.getBoard().is_check():
        reward += -2
    elif state.newStateFromAction(action).getBoard().is_check():
        reward += 2

    reward += calculatePieceAdvantage(state.newStateFromAction(action), nextState)

    reward += getCastleReward(state, chess.Move.from_uci(action))

    return reward

def calculatePieceAdvantage(state: State, nextState: State):

    whiteAdvantage = 0
    blackAdvantage = 0
    for piece_type in range(1, 7):
        whiteAdvantage += getPieceReward(piece_type) * ( len(state.getBoard().pieces(piece_type, True)) - len(nextState.getBoard().pieces(piece_type, True)))
        blackAdvantage += getPieceReward(piece_type) * ( len(state.getBoard().pieces(piece_type, False)) - len(nextState.getBoard().pieces(piece_type, False)))

    if state.getPlayer():
        return whiteAdvantage - blackAdvantage
    else:
        return blackAdvantage - whiteAdvantage

def getPieceReward(piece_type):
    if piece_type is chess.PAWN:
        return 1
    elif piece_type is chess.KNIGHT or piece_type is chess.BISHOP:
        return 3
    elif piece_type is chess.ROOK:
        return 5
    elif piece_type is chess.QUEEN:
        return 9

    return 0

def getCastleReward(state: State, move):
    return state.getBoard().is_castling(move) * 2
