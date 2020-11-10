import chess
import math
import time

from chessUtil.Agent import Agent
from chessUtil.State import State
from chessUtil.Utility import utility

class ABAgent(Agent):
    def makeMove(self, state: State, startTime = time.time()):
        actions = []
        alpha = -math.inf
        beta = math.inf
        value = -math.inf;

        for action in state.getLegalActions():
            nextState = state.newStateFromAction(action)
            value = max(value, self.abIteration(nextState, False, alpha, beta, startTime))
            if value >= beta:
                return action

            alpha = max(alpha, value)

            actions.append((action, value))

        return max(actions, key=lambda x: x[1])[0]

    def abIteration(self, state: State, maxTurn, alpha, beta, startTime):

        if state.isTerminalState() or self.isTerminalTime(startTime):
            return utility(state)

        if maxTurn:
            value = -math.inf
            for action in state.getLegalActions():
                nextState = state.newStateFromAction(action)
                value = max(value, self.abIteration(nextState, not maxTurn, alpha, beta, startTime))

                if value >= beta:
                    return value
                alpha = max(alpha, value)
        else:
            value = math.inf

            for action in state.getLegalActions():
                nextState = state.newStateFromAction(action)

                value = min(value, self.abIteration(nextState, not maxTurn, alpha, beta, startTime))

                if value <= alpha:
                    return value

                beta = min(beta, value)

    def isTerminalTime(self, startTime):
        now = time.time()
        elapsed = (now - startTime) * 1000

        return elapsed >= self.goTime - self.deltaTime
