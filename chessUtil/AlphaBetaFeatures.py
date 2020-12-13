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
        self.stateMap = {}
        self.currentIndex = 0
        self.lastAction = None
        self.lastState = None

    def calculateValue(self, state: State, action, nextState: State):
        if self.mutex.acquire(blocking=False) is not False:
            if self.getAction(state) is None:
                self.agent.setGoTime(state.getAgent().getGoTime())
                self.agent.setDeltaTime(state.getAgent().getDeltaTime())
                self.agent.setMaxDepth(state.getAgent().maxDepth)
                self.addToMap(state, self.agent.makeMove(state))
            self.mutex.release()

        while self.mutex.locked():
            time.sleep(0.001)

        return self.getAction(state) == action

    def getAction(self, state: State):
        if str(state.getBoard()) in self.stateMap:
            return self.stateMap[str(state.getBoard())]
        else:
            return None

    def addToMap(self, state: State, action):

        self.currentIndex = (self.currentIndex + 1) % 10000
        self.remove()

        self.stateMap[str(state.getBoard())] = (self.currentIndex, action)

    def remove(self):
        for k in self.stateMap:
            if self.stateMap[k][0] == self.currentIndex:
                self.stateMap.pop(k)
                return
