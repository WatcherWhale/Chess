from .State import State

def calculateReward(state: State, action, nextState: State):

    if nextState.getBoard().is_checkmate():
        if nextState.getBoard().turn == nextState.isWhite():
            return 100
        else:
            return -100
    elif nextState.getBoard().is_stalemate() or nextState.getBoard().is_insufficient_material():
        return -30
    elif nextState.getBoard().is_check():
        return -10
    elif state.newStateFromAction(action).getBoard().is_check():
        return 10

    return 0
