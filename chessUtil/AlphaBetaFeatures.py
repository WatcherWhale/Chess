from .ChessFeatures import ChessFeatures
from .Features import Feature
from .State import State
from ABAgent.ABAgent import ABAgent

class AlphaBetaFeatures(ChessFeatures):
    def __init__(self):
        ChessFeatures.__init__(self)
        self.append(AlphaBeta())

class AlphaBeta(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "alphaBeta"

    def calculateValue(self, state: State, action, nextState: State):
        divider = len(state.getLegalActions())
        agent = ABAgent(state.getAgent().getGoTime() / divider, state.getAgent().getDeltaTime() / divider, state.getAgent().getMaxDepth())
        didMove = action == agent.makeMove(state.copy())

        return didMove
