import copy
import numpy as np
import time
from threading import Lock

from .ChessFeatures import ChessFeatures
from .Features import Feature, Features
from .State import State
from .OverFlowList import OverFlowList
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
        self.mutex = Lock()
        self.lastAction = None
        self.lastState = None

    def calculateValue(self, state: State, action, nextState: State):
        if self.mutex.acquire(blocking=False) is not False:
            if self.lastState is not state:
                self.agent.setGoTime(state.getAgent().getGoTime())
                self.agent.setDeltaTime(state.getAgent().getDeltaTime())
                self.agent.setMaxDepth(state.getAgent().maxDepth)
                self.lastState = state
                self.lastAction = self.agent.makeMove(state)
            self.mutex.release()

        while self.mutex.locked():
            time.sleep(0.01)

        return self.lastAction == action
