from leapy import Leapy


class Level():
    def __init__(self, obstacles):
        self.obstacles = obstacles


class Levels():
    def __init__(self):
        self.levels = []
        self.levels.append(Level([Leapy(400 + (i * 100), 550, 50, 50,
                                        (255, 0, 0))
                                  for i in range(4)]))

    def addLevel(self, level):
        self.levels.append(level)

    def getLevel1(self):
        return self.levels[0]
