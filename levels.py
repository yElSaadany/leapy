from pygame.image import load
from leapy import Leapy, Coin


class Level():
    def __init__(self, obstacles, coins):
        self.obstacles = obstacles
        self.coins = coins
        self.endCoord = None
        self.numberCoins = len(self.coins)


class Levels():
    end = load('data/assets/end_flag.png')

    def __init__(self):
        self.levels = []

    def addLevel(self, level):
        self.levels.append(level)
        return "Level added as number %d" % (len(self.levels) - 1)

    def getLevel1(self):
        return self.levels[0]

    def importLevel(self, levelFile):
        with open(levelFile, 'r') as level:
            lines = level.readlines()
        
        level = Level([], [])
        for line in lines:
            tmp = line.split(',')
            tmp[-1] = tmp[-1][:-1]
            tmp = list(map(int, tmp))
            if tmp[0] == 0:
                level.obstacles.append(Leapy(tmp[1], tmp[2], 50, 50,
                                       (255, 0, 0)))
            elif tmp[0] == 1:
                level.coins.append(Coin(tmp[1], tmp[2]))
            else:
                level.endCoord = [tmp[1], tmp[2]]
                print(level.endCoord)
        return self.addLevel(level)
