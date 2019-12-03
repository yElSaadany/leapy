import pygame as pg
import os
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
                return "quit"
        
        keys = pg.key.get_pressed()
        if keys[pg.K_q]:
            return "quit"
        if keys[pg.K_RETURN]:
            return "play"

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
                return "play"
        window.blit(titleText, titleRect)
        window.blit(playText, playRect)
        
        quit = text_object("Exit", 60, purple)
        quitAction = button(quit, gray, (300 - (quit.get_width() / 2), 400), "quit")
        if quitAction is not None:
            return quitAction
        # only one level warning
        oneLevel = text_object("This is a very early alpha, there's only one level, but more are coming.", 23, white)
        window.blit(oneLevel, (300 - (oneLevel.get_width() / 2), 250))
        pg.display.update()


def button(text_object, color, pos, handler):
    pg.draw.rect(window, color, (pos[0],
                                 pos[1],
                                 text_object.get_width(),
                                 text_object.get_height()))
    window.blit(text_object, pos)

    mouseX = pg.mouse.get_pos()[0]
    mouseY = pg.mouse.get_pos()[1]
    click = pg.mouse.get_pressed()[0]

    if (mouseX >= pos[0]
            and mouseX <= (pos[0] + text_object.get_width())
            and mouseY >= pos[1]
            and mouseY <= (pos[1] + text_object.get_height())):
        if click:
            return handler
    return None


def gameover(winner=False):
    sleep(2)
    play = False

    while not play:
        window.blit(bg_image, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
        keys = pg.key.get_pressed()
        if keys[pg.K_q]:
            return "quit"

        if winner:
            byeText = text_object("You Win!", 100, white)
        else:
            byeText = text_object("Game Over", 100, white)
        playAgain = text_object("Play Again", 60, white)
        quit = text_object("Exit", 60, white)

        window.blit(byeText, (300 - (byeText.get_width() / 2), 100))
        playAction = button(playAgain, purple, (300 - (playAgain.get_width() / 2), 300),
                            "play")
        quitAction = button(quit, purple, (300 - (quit.get_width() / 2), 400), "quit")
        if playAction is not None:
            return playAction
        if quitAction is not None:
            return quitAction
        pg.display.update()
    sleep(2)


def exit_sequence():
    return


def wait_pregame(level):
    level = "Level %d" % (level+1)
    
    for i in [3, 2, 1]:
        countdown = text_object(str(i), 200, white)
        window.blit(bg_image, (0, 0))
        window.blit(countdown, (300 - (countdown.get_width() / 2),
                                300 - (countdown.get_height() / 2)))

        levelText = text_object(level, 50, purple)
        window.blit(levelText, (300 - (levelText.get_width() / 2), 100))
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
        level = levels.levels[i]
        wait_pregame(i)
        # todo: add end game
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
    if not run:
        return "over"
    if run and i == len(levels.levels):
        return "win"


game = True
switch = intro_loop()
while game:
    if switch == "play":
        leapy = Leapy(x, y, width, height, purple)
        levels = lvls.Levels()
        for level in os.listdir("./data/levels"):
            print(levels.importLevel('data/levels/%s' % level))
        switch = game_loop()
    if switch == "quit":
        game = False
    if switch == "over":
        switch = gameover()
    if switch == "win":
        switch = gameover(True)
pg.quit()
