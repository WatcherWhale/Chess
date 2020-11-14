import random
import json
import os

import chess

from chessUtil.State import State
from chessUtil.Features import Feature, Features
from chessUtil.AlphaBetaFeatures import AlphaBetaFeatures

from chessUtil.Agent import Agent
from chessUtil.Reward import calculateReward


def loadAgentFromFile(file, features: Features = AlphaBetaFeatures()):
    f = open(file)
    saveData = json.load(f)
    f.close()

    features.fromDict(saveData['weights'])

    return QAgent(file, saveData['epsilon'], saveData['discount'], saveData['learningRate'], features, maxDepth=saveData['maxDepth'])


class QAgent(Agent):
    def __init__(self, file, epsilon, discount, learningRate, features: Features = AlphaBetaFeatures(), goTime = 5000, deltaTime = 1000, maxDepth = 2):
        Agent.__init__(self, goTime, deltaTime, maxDepth)
        self.file = file
        self.epsilon = epsilon
        self.discount = discount
        self.learningRate = learningRate
        self.features = features

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setDiscount(self, discount):
        self.discount = discount

    def setLearningRate(self, learningRate):
        self.learningRate = learningRate

    def setGoTime(self, goTime):
        self.goTime = goTime

    def computeAction(self, state: State ):
        actions = state.getLegalActions()
        posActions = []
        qVals = []

        if len(actions) == 0 or state.isTerminalState():
            return None

        for a in actions:
            qVals.append((a, self.getQValue(state, a)))

        maxValue = max(qVals, key=lambda x: x[1])[1]


        for action, qVal in qVals:
            if maxValue <= qVal:
                posActions.append(action)

        if len(posActions) == 0:
            return None

        return random.choice(posActions)

    def makeMove(self, state: State):
        if random.random() < self.epsilon:
            choice = random.choice(state.getLegalActions())
        else:
            choice = self.computeAction(state)

        if choice == None:
            print('None action detected')
            exit(1)

        return choice

    def getQValue(self, state: State, action):
        return self.features.calculateFeatures(state, action)

    def maxQValue(self, state: State):
        if len(state.getLegalActions()) == 0:
            return 0.0

        vals = []
        for action in state.getLegalActions():
            vals.append(self.getQValue(state, action))

        return max(vals)

    def update(self, state: State, action, nextState: State):
        reward = calculateReward(state, action, nextState)
        diff = (reward + self.discount * self.maxQValue(nextState)) - self.getQValue(state, action)
        self.features.updateWeights(state, action, self.learningRate * diff)

    def getGreedyAgent(self):
        return QAgent(self.file, 0, 0, 0, self.features, self.goTime, self.deltaTime, self.maxDepth)

    def save(self):
        saveData = {
            'epsilon': self.epsilon,
            'discount': self.discount,
            'learningRate': self.learningRate,
            'maxDepth': self.maxDepth,
            'weights': self.features.toDict()
        }

        if not os.path.isfile(self.file):
            wh = open("WeightHistory.csv", 'w')
            wh.write(self.features.getNames() + "\n")
            wh.close()

        jsonData = json.dumps(saveData)
        f = open(self.file, 'w')
        f.write(jsonData)
        f.close()

        wh = open("WeightHistory.csv", 'a')
        wh.write(self.features.nextWeightsForCSV() + "\n")

