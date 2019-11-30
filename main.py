import pygame as pg
from leapy import Leapy, Coin
import levels as lvls
from physics import collide


pg.init()

window = pg.display.set_mode((600, 600))
pg.display.set_caption("Leapy")
bg_image = pg.image.load('assets/bg.png').convert()

x = 100
y = 550
width = 50
height = 50

leapy = Leapy(x, y, width, height, (255, 0, 255))
coin = Coin(250, 250)
levels = lvls.Levels()
print(levels.importLevel('data/levels/level1.lvl'))

score = 0
run = True
jumping = False
inversing = False
inverseJump = False
transDown = False
transUp = False
pg.key.set_repeat(500)
jump_count = 10
while run:
    # todo: add end game
    level = levels.levels[0]
    inGame = True
    while inGame:
        hold_return = False
        pg.time.delay(50)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                inGame = False
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
        if (keys[pg.K_SPACE] and not inversing and not transDown
                and not transUp):
            jumping = True
        if keys[pg.K_SPACE] and inversing and not transDown and not transUp:
            inverseJump = True
        if keys[pg.K_q]:
            inGame = False
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
        if True in [collide(leapy, obs) for obs in level.obstacles]:
            inGame = False
            run = False

        coins_collisions = [collide(leapy, coin) for coin in level.coins]
        if True in coins_collisions:
            del level.coins[coins_collisions.index(True)]
            score += 1
            print(score)
        window.blit(bg_image, [0, 0])
        [coin.draw(window) for coin in level.coins]
        [coin.moveLeft() for coin in level.coins]
        [obs.draw(window) for obs in level.obstacles]
        [obs.moveLeft() for obs in level.obstacles]
        leapy.draw(window)
        pg.display.update()

pg.quit()
