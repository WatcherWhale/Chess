import chess
import numpy as np

import time

from chessUtil.State import State

ENABLE_TIMING = False

class Features(list):

    def __init__(self):
        list.__init__(self)
        self.weights = np.array([])

    def append(self, feature):
        super(Features, self).append(feature)
        self.weights = np.append(self.weights, 0)
        feature.setWeight(0)

    def calculateFeatures(self, state: State, action):
        nextState = state.newStateFromAction(action)

        fs = np.zeros(len(self))
        if ENABLE_TIMING:
            for f in range(len(self)):
                start = time.time()
                fs[f] = self[f].calculateValue(state, action, nextState)
                stop = time.time()

                if stop-start >= 0.03:
                    print(self[f].getName())
        else:
            fs = np.array([f.calculateValue(state, action, nextState) for f in self])

        fs = 2/(1 + np.exp(-fs)) - 1

        return np.sum(np.multiply(self.weights, fs))

    def updateWeights(self, state: State, action, learningDifference):
        nextState = state.newStateFromAction(action)

        fs = np.array([f.calculateValue(state, action, nextState) for f in self])
        fs = 2/(1 + np.exp(-fs)) - 1

        self.weights = self.weights + learningDifference * fs

    def toDict(self):
        dict = {}

        for f in self:
            dict[f.getName()] = self.weights[self.index(f)]

        return dict

    def fromDict(self, dict):
        for f in self:
            f.setWeight(dict[f.getName()])
            self.weights[self.index(f)] = dict[f.getName()]

    def nextWeightsForCSV(self):
        csv = ""
        for f in self:
            csv = csv + str(self.weights[self.index(f)]) + ";"

        return csv

    def getNames(self):
        names = ""
        for f in self:
            names = names + f.getName() + ";"
        return names

class Feature:
    def __init__(self):
        self.name = "feature"
        self.weight = 0

    def calculateValue(self, state: chess.Board, action, nextState: State):
        pass

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def getName(self):
        return self.name
