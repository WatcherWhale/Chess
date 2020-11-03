import chess

class State:
    def __init__(self, board: chess.Board, isWhite: bool):
        self.board = board
        self.white = isWhite

    def getLegalActions(self):
        return [lambda x: x.uci() for x in self.board.legal_moves]

    def addMove(self, move):
        self.board.push_uci(move)

    def isTerminalState(self):
        return self.board.is_checkmate or self.board.is_stalemate

    def getBoard(self):
        return self.board

    def isWhite(self):
        return self.isWhite

    def copy(self):
        return State(self.board.copy(), self.white)

    def newStateFromAction(self, action):
        newState = self.copy()
        newState.addMove(action)
        return newState
