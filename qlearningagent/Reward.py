from .State import State

def calculateReward(state: State, action):
    nextState = state.newStateFromAction(action)

    if nextState.getBoard().is_checkmate():
        if nextState.getBoard().turn == state.isWhite():
            return 100
        else:
            return -100
    elif state.getBoard().is_stalemate():
        return -30

    return 0
