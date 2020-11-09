from .State import State

class Agent:
    def __init__(self, goTime):
        self.goTime = goTime

    def setGoTime(self, goTime):
        self.goTime = goTime

    def update(self, state: State, nextState: State):
        pass

    def makeMove(self, state: State):
        raise NotImplementedError()

    def save(self):
        pass
