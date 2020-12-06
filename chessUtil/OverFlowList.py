class OverFlowList(list):
    def __init__(self, maxStorage=100):
        self.maxStorage = maxStorage
        list.__init__(self)

    def append(self, obj):
        if len(self) + 1 >= self.maxStorage:
            self.pop(0)

        list.append(self, obj)

    def findIndex(self, lmb):
        for o in self:
            if lmb(o):
                return o
        return None
