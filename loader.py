import pygame

game_images = None

menu_images = None


def init_game_images():
    global game_images

    game_images = {
        "base": pygame.image.load('Sprites/base.png'),
        "b_bricks": pygame.image.load('Sprites/bbricks.png'),
        "boom": pygame.image.load('Sprites/boom.png'),
        "boom1": pygame.image.load('Sprites/boom1.png'),
        "boom2": pygame.image.load('Sprites/boom2.png'),
        "boom3": pygame.image.load('Sprites/boom3.png'),
        "boom4": pygame.image.load('Sprites/boom4.png'),
        "boom5": pygame.image.load('Sprites/boom5.png'),
        "boom6": pygame.image.load('Sprites/boom6.png'),
        "boom7": pygame.image.load('Sprites/boom7.png'),
        "boom11": pygame.image.load('Sprites/boom11.png'),
        "boom12": pygame.image.load('Sprites/boom12.png'),
        "boom13": pygame.image.load('Sprites/boom13.png'),
        "boom14": pygame.image.load('Sprites/boom14.png'),
        "boom15": pygame.image.load('Sprites/boom15.png'),
        "boom16": pygame.image.load('Sprites/boom16.png'),
        "boom17": pygame.image.load('Sprites/boom17.png'),
        "bricks": pygame.image.load('Sprites/bricks.png'),
        "bullet": pygame.image.load('Sprites/bullet.png'),
        "bush": pygame.image.load('Sprites/bush.png'),
        "eagle": pygame.image.load('Sprites/eagle.png'),
        "empty": pygame.image.load('Sprites/empty.png'),
        "enemy1": pygame.image.load('Sprites/enemy1.png'),
        "enemy2": pygame.image.load('Sprites/enemy12.png'),
        "frame": pygame.image.load('Sprites/frame.png'),
        "hp": pygame.image.load('Sprites/hp.png'),
        "plate": pygame.image.load('Sprites/plate.png'),
        "player1": pygame.image.load('Sprites/player.png'),
        "player2": pygame.image.load('Sprites/player2.png'),
        "shiel": pygame.image.load('Sprites/shiel.png'),
        "shield": pygame.image.load('Sprites/shield.png'),
        "spawn1": pygame.image.load('Sprites/spawn1.png'),
        "spawn2": pygame.image.load('Sprites/spawn2.png'),
        "spawn3": pygame.image.load('Sprites/spawn3.png'),
        "tank": pygame.image.load('Sprites/tank.png'),
        "water1": pygame.image.load('Sprites/water1.png'),
        "water2": pygame.image.load('Sprites/water2.png'),
    }


def init_menu_images():
    global menu_images

    menu_images = {
        "base": pygame.image.load('Sprites/base.png'),
        "background": pygame.image.load('Sprites/Menu/background.jpeg'),
        "bs1": pygame.image.load('Sprites/Menu/bs1.png'),
        "bs2": pygame.image.load('Sprites/Menu/bs2.png'),
        "bs3": pygame.image.load('Sprites/Menu/bs3.png'),
        "bm1": pygame.image.load('Sprites/Menu/bm1.png'),
        "bm2": pygame.image.load('Sprites/Menu/bm2.png'),
        "bm3": pygame.image.load('Sprites/Menu/bm3.png'),
        "be1": pygame.image.load('Sprites/Menu/be1.png'),
        "be2": pygame.image.load('Sprites/Menu/be2.png'),
        "be3": pygame.image.load('Sprites/Menu/be3.png'),
        "bl1": pygame.image.load('Sprites/Menu/bl1.png'),
        "bl2": pygame.image.load('Sprites/Menu/bl2.png'),
        "bl3": pygame.image.load('Sprites/Menu/bl3.png'),
        "ba1": pygame.image.load('Sprites/Menu/ba1.png'),
        "ba2": pygame.image.load('Sprites/Menu/ba2.png'),
        "ba3": pygame.image.load('Sprites/Menu/ba3.png'),
        "bl11": pygame.image.load('Sprites/Menu/bl11.png'),
        "bl12": pygame.image.load('Sprites/Menu/bl12.png'),
        "bl13": pygame.image.load('Sprites/Menu/bl13.png'),
        "bl21": pygame.image.load('Sprites/Menu/bl21.png'),
        "bl22": pygame.image.load('Sprites/Menu/bl22.png'),
        "bl23": pygame.image.load('Sprites/Menu/bl23.png'),
        "bl31": pygame.image.load('Sprites/Menu/bl31.png'),
        "bl32": pygame.image.load('Sprites/Menu/bl32.png'),
        "bl33": pygame.image.load('Sprites/Menu/bl33.png'),
        "bl41": pygame.image.load('Sprites/Menu/bl41.png'),
        "bl42": pygame.image.load('Sprites/Menu/bl42.png'),
        "bl43": pygame.image.load('Sprites/Menu/bl43.png'),
        "bl51": pygame.image.load('Sprites/Menu/bl51.png'),
        "bl52": pygame.image.load('Sprites/Menu/bl52.png'),
        "bl53": pygame.image.load('Sprites/Menu/bl53.png'),
        "pass": pygame.image.load('Sprites/Menu/pass.png'),
        "def": pygame.image.load('Sprites/Menu/def1.png'),
        "score": pygame.image.load('Sprites/Menu/sc.png'),
        "hi_score": pygame.image.load('Sprites/Menu/hsc.png'),


    }
