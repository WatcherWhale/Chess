import chess
from .State import State

class Features(list):
    def calculateFeatures(self, state: State, action):
        vals = []

        nextState = state.newStateFromAction(action)

        for f in self:
            vals.append(f.calculateFeature(state, action, nextState))

        return vals

    def updateWeights(self, state: State, action, learningDifference):

        nextState = state.newStateFromAction(action)

        for f in self:
            f.updateWeight(state, action, nextState, learningDifference)

    def toDict(self):
        dict = {}

        for f in self:
            dict[f.getName()] = f.getWeight()

        return dict

    def fromDict(self, dict):
        for f in self:
            f.setWeight(dict[f.getName()])


class Feature:
    def __init__(self):
        self.name = "feature"
        self.weight = 0

    def calculateFeature(self, state: State, action, nextState: State):
        return self.weight * self.calculateValue(state, action, nextState)

    def calculateValue(self, state: chess.Board, action, nextState: State):
        pass

    def updateWeight(self, state: State, action, nextState: State, learningDifference):
        self.weight = self.weight + learningDifference * self.calculateValue(state, action, nextState)

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def getName(self):
        return self.name
