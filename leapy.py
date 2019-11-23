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
