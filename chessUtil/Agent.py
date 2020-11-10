from .State import State

class Agent:
    def __init__(self, goTime = 5000, deltaTime = 1000, maxDepth = 2):
        self.goTime = goTime
        self.deltaTime = deltaTime
        self.maxDepth = maxDepth

    def getGoTime(self):
        return self.goTime

    def getDeltaTime(self):
        return self.deltaTime

    def getMaxDepth(self):
        return self.maxDepth

    def setGoTime(self, goTime):
        self.goTime = goTime

    def setDeltaTime(self, deltaTime):
        self.deltaTime = deltaTime

    def setMaxDepth(self, maxDepth):
        self.maxDepth = maxDepth

    def update(self, state: State, action, nextState: State):
        pass

    def makeMove(self, state: State):
        raise NotImplementedError()

    def save(self):
        pass
