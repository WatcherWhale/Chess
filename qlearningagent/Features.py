import chess

class Features(list):
    def calculateFeatures(self, state: chess.Board, action):
        return [lambda x: x.calculateFeature(state, action) for x in self]

    def updateWeights(self, state: chess.Board, action, learningDifference):
        for f in self:
            f.updateWeight(state, action, learningDifference)

    def saveWeights(self, file):
        pass

class Feature:
    def __init__(self, default = False, weight = 0):
        if not default:
            self.weight = weight
        else:
            self.weight = 0

    def calculateFeature(self, state: chess.Board, action):
        return self.weight * self.calculateValue(state, action)

    def calculateValue(self, state: chess.Board, action):
        pass

    def updateWeight(self, state: chess.Board, action, learningDifference):
        self.weight = self.weight + learningDifference * self.calculateValue(state, action)

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight
