import pygame

game_images = None


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
        "water1": pygame.image.load('Sprites/water1.png'),
        "water2": pygame.image.load('Sprites/water2.png'),
    }
