import chess
import math
import time

import numpy as np

from chessUtil.Agent import Agent
from chessUtil.State import State
from chessUtil.Utility import utility
from chessUtil.ChessFeatures import ChessFeatures

def getFeatures():
    fs = ChessFeatures()
    for i in range(len(fs)):
        f = fs[i]
        if f.getName()[-1] != "O":
            fs.weights[i] = 1
    return fs

class ABAgent(Agent):
    def __init__(self, goTime = 5000, deltaTime = 1000, maxDepth = 100, features = getFeatures()):
        Agent.__init__(self, goTime, deltaTime)
        self.maxDepth = maxDepth
        self.features = features

    def makeMove(self, state: State, startTime = time.time()):
        actions = []
        alpha = -math.inf
        beta = math.inf
        value = -math.inf

        for action in state.getLegalActions():
            nextState = state.newStateFromAction(action)
            value = max(value, self.abIteration(nextState, False, alpha, beta, self.features, startTime, 1))
            if value >= beta:
                return action

            alpha = max(alpha, value)

            actions.append((action, value))

        return max(actions, key=lambda x: x[1])[0]

    def abIteration(self, state: State, maxTurn, alpha, beta, features, startTime, depth):

        if state.isTerminalState() or self.isTerminalTime(startTime) or depth >= self.maxDepth:
            return utility(state, features)

        if maxTurn:
            value = -math.inf
            for action in state.getLegalActions():
                nextState = state.newStateFromAction(action)
                value = max(value, self.abIteration(nextState, not maxTurn, alpha, beta, features, startTime, depth + 1))

                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value
        else:
            value = math.inf

            for action in state.getLegalActions():
                nextState = state.newStateFromAction(action)

                value = min(value, self.abIteration(nextState, not maxTurn, alpha, beta, features, startTime, depth + 1))

                if value <= alpha:
                    return value

                beta = min(beta, value)
            return value

    def isTerminalTime(self, startTime):
        now = time.time()
        elapsed = (now - startTime) * 1000

        return elapsed >= self.goTime - self.deltaTime
