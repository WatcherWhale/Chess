import random
import json

import chess
import numpy as np

from Features import Feature, Features
from State import State


class QAgent:
    def __init__(self, file, epsilon, discount, learningRate, features: Features):
        self.file = file
        self.epsilon = epsilon
        self.discount = discount
        self.learningRate = learningRate
        self.features = features
        pass

    def computeAction(self, state: State ):
        actions = state.getLegalActions()
        posActions = []
        maxValue = self.maxQValue(state)

        if len(actions) == 0:
            return None

        for action in actions:
            if maxValue == self.getQValue(state, action):
                posActions.append(action)

        return random.choice(posActions)

    def makeMove(self, state: State):
        if random.random() < self.epsilon:
            return random.choice(state.getLegalActions())
        else:
            return self.computeAction(state)


    def getQValue(self, state: State, action):
        return np.sum(self.features.calculateFeatures(state, action))

    def update(self, state: State, action, reward, nextState: State):

        diff = (reward + self.discount * self.maxQValue(nextState)) - self.getQValue(state, action)
        self.features.updateWeights(state, action, self.learningRate * diff)


    def maxQValue(self, state: State):
        if len(state.getLegalActions() == 0):
            return 0.0

        vals = []
        for action in state.getLegalActions():
            vals.append(self.getQValue(state, action))

        return max(vals)

    def save(self):
        saveData = {
            'epsilon': self.epsilon,
            'discount': self.discount,
            'learningRate': self.learningRate,
            'weights': self.features.toDict()
        }

        jsonData = json.dumps(saveData)
        f = open(self.file, 'w')
        f.write(jsonData)
        f.close()
