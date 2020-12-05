import chess
import math
import time
import random

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
        else:
            fs.weights[i] = -1
    return fs

class ABAgent(Agent):
    def __init__(self, goTime = 5, deltaTime = 1, maxDepth = 10, features = getFeatures()):
        Agent.__init__(self, goTime, deltaTime)
        self.maxDepth = maxDepth
        self.features = features

    def makeMove(self, state: State, startTime = time.time()):
        alpha = -math.inf
        value = -math.inf

        startTime = time.time()

        action = None

        for a in state.getLegalActions():
            nextState = state.newStateFromAction(a)
            new_value = self.abIteration(nextState, False, alpha, math.inf, startTime, 1)
            value = max(value, new_value)

            if value == new_value:
                action = a

            alpha = max(alpha, value)

        return action

    def abIteration(self, state: State, maxTurn, alpha, beta, startTime, depth):

        if state.isTerminalState() or self.isTerminalTime(startTime) or depth >= self.maxDepth:
            return utility(state, self.features)


        if maxTurn:
            value = -math.inf
            for action in state.getLegalActions():
                nextState = state.newStateFromAction(action)
                value = max(value, self.abIteration(nextState, not maxTurn, alpha, beta, startTime, depth + 1))

                alpha = max(alpha,value)
                if alpha >= beta:
                    return value

            return value
        else:
            value = math.inf

            for action in state.getLegalActions():
                nextState = state.newStateFromAction(action)

                value = min(value, self.abIteration(nextState, not maxTurn, alpha, beta, startTime, depth + 1))
                beta = min(beta, value)

                if beta <= alpha:
                    return value

            return value

    def isTerminalTime(self, startTime):
        now = time.time()
        elapsed = now - startTime

        return elapsed >= self.goTime - self.deltaTime
