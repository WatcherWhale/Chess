import random
import json

import chess


from .Features import Feature, Features
from .State import State
from .SimpleFeatures import SimpleFeatures

def loadAgentFromFile(file, features: Features = SimpleFeatures()):
    f = open(file)
    saveData = json.load(f)
    f.close()

    features.fromDict(saveData['weights'])

    return QAgent(file, saveData['epsilon'], saveData['discount'], saveData['learningRate'], features)

class QAgent:
    def __init__(self, file, epsilon, discount, learningRate, features: Features = SimpleFeatures()):
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

    def computeAction(self, state: State ):
        actions = state.getLegalActions()
        posActions = []
        qVals = []
        maxValue = self.maxQValue(state)

        if len(actions) == 0 or state.isTerminalState():
            return None

        for action in actions:
            qVal = self.getQValue(state, action)
            qVals.append(qVal)
            if maxValue == qVal:
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
            print(state.getLegalActions())
            exit(1)

        return choice


    def getQValue(self, state: State, action):
        return sum(self.features.calculateFeatures(state, action))

    def update(self, state: State, action, reward, nextState: State):
        diff = (reward + self.discount * self.maxQValue(nextState)) - self.getQValue(state, action)
        self.features.updateWeights(state, action, self.learningRate * diff)


    def maxQValue(self, state: State):
        if len(state.getLegalActions()) == 0:
            return 0.0

        vals = []
        for action in state.getLegalActions():
            vals.append(self.getQValue(state, action))

        return max(vals)

    def getGreedyAgent(self):
        return QAgent(self.file, 0, self.discount, self.learningRate, self.features)

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
