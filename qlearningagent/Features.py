import chess
from State import State

class Features(list):
    def calculateFeatures(self, state: chess.Board, action):
        return [lambda x: x.calculateFeature(state, action) for x in self]

    def updateWeights(self, state: State, action, learningDifference):
        for f in self:
            f.updateWeight(state, action, learningDifference)

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

    def calculateFeature(self, state: State, action):
        return self.weight * self.calculateValue(state, action)

    def calculateValue(self, state: chess.Board, action):
        pass

    def updateWeight(self, state: State, action, learningDifference):
        self.weight = self.weight + learningDifference * self.calculateValue(state, action)

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def getName(self):
        return self.name
