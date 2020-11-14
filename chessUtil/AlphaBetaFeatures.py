import copy
import numpy as np

from .ChessFeatures import ChessFeatures
from .Features import Feature, Features
from .State import State
from ABAgent.ABAgent import ABAgent

class AlphaBetaFeatures(ChessFeatures):
    def __init__(self):
        ChessFeatures.__init__(self)
        self.append(AlphaBeta(self))

    def copySafe(self):
        cf = ChessFeatures()
        cf.fromDict(self.toDict())
        return cf

class AlphaBeta(Feature):
    def __init__(self, features: Features):
        Feature.__init__(self)
        self.name = "alphaBeta"
        self.features = features

    def calculateValue(self, state: State, action, nextState: State):
        divider = len(state.getLegalActions())
        agent = ABAgent(state.getAgent().getGoTime() / divider, state.getAgent().getDeltaTime() / divider,\
                        state.getAgent().getMaxDepth(), self.features.copySafe())

        return action == agent.makeMove(state.copy())
