import chess
from Features import Feature, Features
import numpy as np
import random

class QAgent:
    def __init__(self, file, epsilon, discount, learningRate, features: Features):
        self.file = file
        self.epsilon = epsilon
        self.discount = discount
        self.learningRate = learningRate
        self.features = features
        pass

    def computeAction(self, state):
        actions = state.legal_moves
        posActions = []
        maxValue = self.maxQValue(state)

        if len(actions) == 0:
            return None

        for action in actions:
            if maxValue == self.getQValue(state, action):
                posActions.append(action)

        return random.choice(posActions)

    def makeMove(self, state: chess.Board):
        if random.random() < self.epsilon:
            return random.choice(state.legal_moves)
        else:
            return self.computeAction(state)


    def getQValue(self, state, action):
        return np.sum(self.features.calculateFeatures(state, action))

    def update(self, state, action, reward, nextState):

        diff = (reward + self.discount * self.maxQValue(nextState)) - self.getQValue(state, action)
        self.features.updateWeights(state, action, self.learningRate * diff)


    def maxQValue(self, state: chess.Board):
        if len(state.legal_moves == 0):
            return 0.0

        vals = []
        for action in state.legal_moves:
            vals.append(self.getQValue(state, action))

        return max(vals)

    def getNextState(self, state: chess.Board, action):
        nextState = state.copy()
        nextState.push_uci(action)
        return nextState
