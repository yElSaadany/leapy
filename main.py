import pygame as pg
from leapy import Leapy
import levels as lvls
from physics import collide
from time import sleep


pg.init()

window = pg.display.set_mode((600, 600))
pg.display.set_caption("Leapy")
bg_image = pg.image.load('data/assets/bg.png').convert()
score_text = pg.font.Font('data/assets/RightBankFLF.ttf', 36)

x = 100
y = 550
width = 50
height = 50

white = (255, 255, 255)
purple = (255, 0, 255)
gray = (180, 180, 180)

leapy = Leapy(x, y, width, height, purple)
levels = lvls.Levels()
print(levels.importLevel('data/levels/level1.lvl'))


def text_object(text, size, color):
    font = pg.font.Font('data/assets/RightBankFLF.ttf', size)
    textSurface = font.render(text, True, color)
    return textSurface


def intro_loop():
    intro = True
    while intro:
        window.blit(bg_image, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 1
        
        keys = pg.key.get_pressed()
        if keys[pg.K_q]:
            return 1
        if keys[pg.K_RETURN]:
            return 0

        mouseX = pg.mouse.get_pos()[0]
        mouseY = pg.mouse.get_pos()[1]
        click = pg.mouse.get_pressed()[0]

        titleText = text_object("Leapy", 100, purple)
        titleRect = (300 - (titleText.get_width() / 2), 70)
        playText = text_object("Play Solo", 50, purple)
        playRect = (300 - (playText.get_width() / 2), 300)
        pg.draw.rect(window, gray, (playRect[0],
                                    playRect[1],
                                    playText.get_width(),
                                    playText.get_height()))

        if (mouseX >= playRect[0]
                and mouseX <= (playRect[0] + playText.get_width())
                and mouseY >= playRect[1]
                and mouseY <= (playRect[1] + playText.get_height())):
            if click:
                return 0
        window.blit(titleText, titleRect)
        window.blit(playText, playRect)
        pg.display.update()


def wait_pregame():
    for i in [3, 2, 1]:
        countdown = text_object(str(i), 200, white)
        window.blit(bg_image, (0, 0))
        window.blit(countdown, (300 - (countdown.get_width() / 2),
                                300 - (countdown.get_height() / 2)))
        pg.display.update()
        sleep(1)


def game_loop():
    score = 0
    run = True
    jumping = False
    inversing = False
    inverseJump = False
    transDown = False
    transUp = False
    pg.key.set_repeat(500)
    jump_count = 10
    i = 0
    while run and i < len(levels.levels):
        # todo: add end game
        level = levels.levels[i]
        inGame = True
        while inGame:
            pg.time.delay(30)
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
            if (keys[pg.K_SPACE] and inversing and not transDown
                    and not transUp):
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

            if leapy.x > level.endCoord[0]:
                inGame = False
            window.blit(bg_image, [0, 0])
            window.blit(levels.end, level.endCoord)
            level.endCoord = (level.endCoord[0] - 10, level.endCoord[1])
            [coin.draw(window) for coin in level.coins]
            [coin.moveLeft() for coin in level.coins]
            [obs.draw(window) for obs in level.obstacles]
            [obs.moveLeft() for obs in level.obstacles]
            window.blit(score_text.render(str(score), False, white), (550, 10))
            leapy.draw(window)
            pg.display.update()

        i += 1


if intro_loop() == 0:
    wait_pregame()
    game_loop()
pg.quit()
