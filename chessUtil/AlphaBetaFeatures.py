import copy
import numpy as np

from .ChessFeatures import ChessFeatures
from .Features import Feature, Features
from .State import State
from ABAgent.ABAgent import ABAgent

class AlphaBetaFeatures(ChessFeatures):
    def __init__(self):
        ChessFeatures.__init__(self)
        self.append(AlphaBeta(ChessFeatures()))
        self.ab = self[-1]

    def calculateFeatures(self, state: State, action):
        index = self.index(self.ab)
        self.ab.agent.features.weights = np.delete(self.weights, index)
        return ChessFeatures.calculateFeatures(self, state, action)

class AlphaBeta(Feature):
    def __init__(self, features: Features):
        Feature.__init__(self)
        self.name = "alphaBeta"
        self.agent = ABAgent()
        self.agent.features = features
        self.lastState = None
        self.lastAction = None

    def calculateValue(self, state: State, action, nextState: State):
        if self.lastState != state:
            self.lastState = state
            self.agent.setGoTime(state.getAgent().getGoTime())
            self.agent.setDeltaTime(state.getAgent().getDeltaTime())
            self.agent.setMaxDepth(state.getAgent().maxDepth)
            self.lastAction = self.agent.makeMove(state)

        return action == self.lastAction
