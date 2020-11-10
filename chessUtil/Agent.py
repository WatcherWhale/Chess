from .State import State

class Agent:
    def __init__(self, goTime, deltaTime = 1000):
        self.goTime = goTime
        self.deltaTime = deltaTime

    def setGoTime(self, goTime):
        self.goTime = goTime

    def setDeltaTime(self, deltaTime):
        self.deltaTime = deltaTime

    def update(self, state: State, nextState: State):
        pass

    def makeMove(self, state: State):
        raise NotImplementedError()

    def save(self):
        pass