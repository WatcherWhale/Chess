import chess

class State:
    def __init__(self, board: chess.Board, isWhite: bool):
        self.board = board
        self.white = isWhite

    def getLegalActions(self):
        return self.board.legal_moves

    def getBoard(self):
        return self.board

    def isWhite(self):
        return self.isWhite

    def copy(self):
        return State(self.board.copy(), self.white)
