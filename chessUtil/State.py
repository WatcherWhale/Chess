import chess
import random

class State:
    def __init__(self, board: chess.Board, isWhite: bool, agent):
        self.board = board
        self.white = isWhite
        self.agent = agent

    def getLegalActions(self):
        actions = []
        for a in self.board.legal_moves:
            actions.append(a.uci())
        random.shuffle(actions)
        return actions

    def addMove(self, move):
        self.board.push_uci(move)

    def isTerminalState(self):
        return self.board.is_checkmate() or self.board.is_stalemate()

    def getBoard(self):
        return self.board

    def getPlayer(self):
        return self.white

    def setPlayer(self, isWhite):
        self.white = isWhite

    def getAgent(self):
        return self.agent

    def copy(self):
        return State(self.board.copy(), self.white, self.agent)

    def newStateFromAction(self, action):
        newState = self.copy()
        newState.addMove(action)
        newState.setPlayer(not self.white)
        return newState

    def getPreviousState(self):
        newState = self.copy()
        action = newState.getBoard().pop().uci()
        newState.setPlayer(not self.white)
        return (newState, action)
