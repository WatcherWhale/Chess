import chess
import math
import time
import random

import queue
from threading import Thread

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
        self.nodes = 0

    def makeMove(self, state: State, startTime = time.time()):
        startTime = time.time()

        pool = []
        que = queue.Queue()

        self.nodes = 0

        for a in state.getLegalActions():
            t = Thread(target=doThread, args=(self, state, a, startTime, que))
            t.start()
            pool.append(t)
            self.nodes += 1

        for t in pool:
            t.join()

        maxAction = None
        maxUtil = -math.inf

        while not que.empty():
            action, uVal = que.get()
            if uVal >= maxUtil:
                maxUtil = uVal
                maxAction = action

        return maxAction

    def abIteration(self, state: State, maxTurn, alpha, beta, startTime, depth):
        self.nodes += 1
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


def doThread(self: ABAgent, state: State, action, startTime, que : queue.Queue):
    uVal = self.abIteration(state.newStateFromAction(action), False, math.inf, math.inf, startTime, 1)
    que.put((action, uVal))
