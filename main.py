import pygame as pg
pg.init()

window = pg.display.set_mode((600, 600))
pg.display.set_caption("Leapy")

x = 100
y = 550
width = 50
height = 50

class Leapy():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def jump():
        pass
        

    def getRect(self):
        return (self.x, self.y, self.width, self.height)

leapy = Leapy(x, y , width, height)
run = True
jumping = False
inversing = False
inverseJump = False
transDown = False
transUp = False
pg.key.set_repeat(500)
jump_count = 10
while run:
    hold_return = False
    pg.time.delay(50)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()
    if (keys[pg.K_RETURN] and not jumping and not inverseJump
        and not transDown and not transUp):
        if inversing:
            inversing = False
            transDown = True
        else:
            inversing = True
            transUp = True
    if keys[pg.K_SPACE] and not inversing:
        jumping = True
    if keys[pg.K_SPACE] and inversing:
        inverseJump = True
    if keys[pg.K_q]:
        run = False

    if jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            leapy.y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10

    if inverseJump:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            leapy.y += (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            inverseJump = False
            jump_count = 10

    if inversing:
        jumping = False

    if transDown:
        if leapy.y < 550:
            leapy.y += 50
        else:
            transDown = False

    if transUp:
        if leapy.y > 0:
            leapy.y -= 50
        else:
            transUp = False
        
    window.fill((255, 255, 255))
    pg.draw.rect(window, (255, 0, 255), leapy.getRect())
    pg.display.update()

pg.quit()
