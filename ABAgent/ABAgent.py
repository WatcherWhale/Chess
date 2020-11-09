import chess

from chessUtil.Agent import Agent
from chessUtil.State import State

class ABAgent(Agent):
    def __init__(self, goTime = 5000):
        Agent.__init__(self, goTime)

    def makeMove(self, state: State):
        pass
