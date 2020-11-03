import chess

class QAgent:
    def __init__(self, file, epsilon, learningRate):
        self.file = file
        self.epsilon = epsilon
        self.learningRate = learningRate
        pass

    def makeMove(self, board: chess.Board):
        pass

    def getQValue(self, state, action):
        pass

    def update(self, state, action, reward, nextState):
        pass

    def getLegalActions(self, state: chess.Board):
        return state.legal_moves

    def getNextState(self, state: chess.Board, action):
        pass
