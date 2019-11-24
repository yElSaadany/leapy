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
        return "Level added as number %d" % (len(self.levels) - 1)

    def getLevel1(self):
        return self.levels[0]

    def importLevel(self, levelFile):
        with open(levelFile, 'r') as level:
            lines = level.readlines()
        
        level = Level([])
        for line in lines:
            tmp = line.split(',')
            tmp[-1] = tmp[-1][:-1]
            tmp = list(map(int, tmp))
            level.obstacles.append(Leapy(tmp[1], tmp[2], 50, 50,
                                   (255, 0, 0)))
        return self.addLevel(level)
