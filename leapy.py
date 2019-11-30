import pygame as pg


class Leapy():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def jump():
        pass

    def getRect(self):
        return (self.x, self.y, self.width, self.height)

    def getColor(self):
        return self.color

    def moveLeft(self):
        self.x -= 10

    def draw(self, window):
        pg.draw.rect(window, self.getColor(), self.getRect())

    def getHitbox(self, axis):
        if axis == 'x':
            return (self.x, self.x + self.width)
        else:
            return (self.y, self.y + self.height)

    def getPoints(self):
        return [(self.x, self.y),
                (self.x + self.width, self.y),
                (self.x, self.y + self.height),
                (self.x + self.width, self.y + self.height)]


class Coin():
    image = pg.image.load('assets/coin.png')

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def moveLeft(self):
        self.x -= 10

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
