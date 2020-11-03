import chess

class State:
    def __init__(self, board: chess.Board, isWhite: bool):
        self.board = board
        self.white = isWhite

    def getLegalActions(self):
        actions = []
        for a in self.board.legal_moves:
            actions.append(a.uci())
        return actions

    def addMove(self, move):
        self.board.push_uci(move)

    def isTerminalState(self):
        return self.board.is_checkmate or self.board.is_stalemate

    def getBoard(self):
        return self.board

    def isWhite(self):
        return self.white

    def copy(self):
        return State(self.board.copy(), self.white)

    def newStateFromAction(self, action):
        newState = self.copy()
        newState.addMove(action)
        return newState
