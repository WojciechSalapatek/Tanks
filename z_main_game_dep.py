import pygame, sys, shelve
import z_game_objects_dep as go
from pygame.locals import *
import z_level_builder_dep as lb



# GameHandler iteruje po każdej grupie Spritów w lście i wywołuche ich metody render i update
class GameHandler:
    # groups: 0-player 1-neutral, 2-enemy, 3-bullets, 4-boom 5-bushes , 6-plates, 7-base, 8-gui, 9-spawnerGroup 10 - water 12-items
    def __init__(self, displaysurface, gameover, gameMenager, groupsList = None):
        self.displaysurface = displaysurface
        self.gameover = gameover
        self.gameMenager = gameMenager
        if groupsList is None:
            self.groupsList = []
        else:
            self.groupsList = groupsList
        self.gameGui = gameGui(self.groupsList)

    def update(self):
        self.groupsList[0].update(self, self.groupsList, self.displaysurface)
        self.groupsList[2].update(self, self.groupsList)
        self.groupsList[3].update(self.groupsList)
        self.groupsList[4].update(self.groupsList, self.gameover)
        self.groupsList[7].update(self.groupsList, self.gameover)
        self.groupsList[9].update(self.groupsList)
        self.groupsList[10].update()
        self.groupsList[12].update(self.groupsList)
        self.gameGui.update()
        self.gameMenager.update(self.groupsList)

    def render(self, displaysurface):
        self.groupsList[6].draw(displaysurface)
        self.groupsList[12].draw(displaysurface)
        for i in range(0, 13):
            if i != 6 and i != 12:
                self.groupsList[i].draw(displaysurface)


    def addBullet(self, bullet):
        self.groupsList[3].add(bullet)


class gameGui():
    def __init__(self, groupsList):
        self.groupsList = groupsList
        self.myfont = pygame.font.SysFont('Comic Sans MS', 60)


    def update(self):
        player = self.groupsList[0].sprites()
        hp = player[0].hp
        hpsurf = self.myfont.render("HP: " + str(hp), False, (0, 0, 0))
        DISPLAYSURFACE.blit(hpsurf, (1100, 30))



BLOCKSIZE = 50
WIDTH = 1280
HEIGHT = 720
FIELD_WIDTH = 1050
FIELD_HEIGHT = 700
PADDING = 10
DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))

class main():
    def __init__(self):
        self.winSound = pygame.mixer.Sound('Music/win.wav')
        self.loseSound = pygame.mixer.Sound('Music/lose.wav')
        inMenu = True
        FPS = 60
        fpsClock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption('Tanki!')
        self.menu = go.Menu()
        self.menu.addButton(
            go.Button(535, 250, pygame.image.load('Sprites/Menu/bs1.png'), pygame.image.load('Sprites/Menu/bs2.png'),
                   pygame.image.load('Sprites/Menu/bs3.png'), "start", self.mode))
        self.menu.addButton(
            go.Button(535, 350, pygame.image.load('Sprites/Menu/be1.png'), pygame.image.load('Sprites/Menu/be2.png'),
                   pygame.image.load('Sprites/Menu/be3.png'), "exit", sys.exit))

        while inMenu:  # pętla menu
            DISPLAYSURFACE.fill((70, 70, 70))
            self.menu.update(DISPLAYSURFACE)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            fpsClock.tick(FPS)

    def levels(self):
        self.menu.clearButtons()
        self.menu.addButton(
            go.Button(535, 100, pygame.image.load('Sprites/Menu/bl11.png'), pygame.image.load('Sprites/Menu/bl12.png'),
                   pygame.image.load('Sprites/Menu/bl13.png'), "start", play, 'level1', self))
        self.menu.addButton(
            go.Button(535, 200, pygame.image.load('Sprites/Menu/bl21.png'), pygame.image.load('Sprites/Menu/bl22.png'),
                   pygame.image.load('Sprites/Menu/bl23.png'), "start", play, 'level2', self))
        self.menu.addButton(
            go.Button(535, 300, pygame.image.load('Sprites/Menu/bl31.png'), pygame.image.load('Sprites/Menu/bl32.png'),
                   pygame.image.load('Sprites/Menu/bl33.png'), "start", play, 'level3', self))
        self.menu.addButton(
            go.Button(535, 400, pygame.image.load('Sprites/Menu/bl41.png'), pygame.image.load('Sprites/Menu/bl42.png'),
                   pygame.image.load('Sprites/Menu/bl43.png'), "start", play, 'level4', self))
        self.menu.addButton(
            go.Button(535, 500, pygame.image.load('Sprites/Menu/bl51.png'), pygame.image.load('Sprites/Menu/bl52.png'),
                   pygame.image.load('Sprites/Menu/bl53.png'), "start", play, 'level5', self))

    def mode(self):
        self.menu.clearButtons()
        self.menu.addButton(go.Button(535, 250, pygame.image.load('Sprites/Menu/bl1.png'), pygame.image.load('Sprites/Menu/bl2.png'),
                            pygame.image.load('Sprites/Menu/bl3.png'), "levels", self.levels))
        self.menu.addButton(go.Button(535, 350, pygame.image.load('Sprites/Menu/ba1.png'), pygame.image.load('Sprites/Menu/ba2.png'),
                            pygame.image.load('Sprites/Menu/ba3.png'), "arcade", play, 'arcade', self))

    def endStatus(self, mode,  score):
        pygame.mixer.music.stop()
        if mode == 'levels' and score == 1:
            self.menu.clearButtons()
            pygame.mixer.Sound.play(self.winSound)
            self.menu.addButton(
                go.Button(240, 100, pygame.image.load('Sprites/Menu/pass.png'), pygame.image.load('Sprites/Menu/pass.png'),
                       pygame.image.load('Sprites/Menu/pass.png'), "sign"))
            self.menu.addButton(
                go.Button(535, 400, pygame.image.load('Sprites/Menu/bm1.png'), pygame.image.load('Sprites/Menu/bm2.png'),
                       pygame.image.load('Sprites/Menu/bm3.png'), "menu", self.mode))
            self.menu.addButton(
                go.Button(535, 500, pygame.image.load('Sprites/Menu/be1.png'), pygame.image.load('Sprites/Menu/be2.png'),
                       pygame.image.load('Sprites/Menu/be3.png'), "exit", sys.exit))

        elif mode == 'levels' and score == -1:
            self.menu.clearButtons()
            pygame.mixer.Sound.play(self.loseSound)
            self.menu.addButton(
                go.Button(315, 50, pygame.image.load('Sprites/Menu/def1.png'), pygame.image.load('Sprites/Menu/def1.png'),
                       pygame.image.load('Sprites/Menu/def1.png'), "sign"))
            self.menu.addButton(
                go.Button(535, 450, pygame.image.load('Sprites/Menu/bm1.png'), pygame.image.load('Sprites/Menu/bm2.png'),
                       pygame.image.load('Sprites/Menu/bm3.png'), "menu", self.mode))
            self.menu.addButton(
                go.Button(535, 550, pygame.image.load('Sprites/Menu/be1.png'), pygame.image.load('Sprites/Menu/be2.png'),
                       pygame.image.load('Sprites/Menu/be3.png'), "exit", sys.exit))

        elif mode == 'arcade':
            self.menu.clearButtons()
            pygame.mixer.Sound.play(self.winSound)
            self.menu.addButton(
                go.Button(335, 50, pygame.image.load('Sprites/Menu/def1.png'), pygame.image.load('Sprites/Menu/def1.png'),
                       pygame.image.load('Sprites/Menu/def1.png'), "sign"))
            self.menu.addButton(
                go.Button(460, 280, pygame.image.load('Sprites/Menu/sc.png'), pygame.image.load('Sprites/Menu/sc.png'),
                       pygame.image.load('Sprites/Menu/sc.png'), "sign"))
            self.menu.addButton(
                go.Button(460, 350, pygame.image.load('Sprites/Menu/hsc.png'), pygame.image.load('Sprites/Menu/hsc.png'),
                       pygame.image.load('Sprites/Menu/hsc.png'), "sign"))
            self.menu.addButton(
                go.Button(535, 450, pygame.image.load('Sprites/Menu/bm1.png'), pygame.image.load('Sprites/Menu/bm2.png'),
                       pygame.image.load('Sprites/Menu/bm3.png'), "menu", self.mode))
            self.menu.addButton(
                go.Button(535, 550, pygame.image.load('Sprites/Menu/be1.png'), pygame.image.load('Sprites/Menu/be2.png'),
                       pygame.image.load('Sprites/Menu/be3.png'), "exit", sys.exit))
            self.myfont = pygame.font.SysFont('Comic Sans MS', 67)
            d = shelve.open('data')
            hiscore = d['score']
            if score > hiscore:
                d['score'] = score
                hiscore = score
            scoresurf = self.myfont.render(str(score), False, (255, 102, 0))
            hiscoresurf = self.myfont.render(str(hiscore), False, (255, 102, 0))
            self.menu.addButton(
                go.Button(670, 280, scoresurf, scoresurf, scoresurf, "Sprite"))
            self.menu.addButton(
                go.Button(720, 360, hiscoresurf, hiscoresurf, hiscoresurf, "Sprite"))


def play(mode, main): # pętla gry
    playing = 0
    FPS = 40
    pygame.init()
    fpsClock = pygame.time.Clock()
    pygame.display.set_caption('Tanki!')
    glist , gmenager = lb.buildLevel(BLOCKSIZE, FIELD_WIDTH + PADDING, HEIGHT, mode)
    gameHandler = GameHandler(DISPLAYSURFACE, None, gmenager, glist)
    while playing == 0:  # główna pętla
        DISPLAYSURFACE.fill((0, 0, 0))
        gameHandler.render(DISPLAYSURFACE)
        if fpsClock.get_fps() > 0:
            gameHandler.update()
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
        playing = gmenager.status()
        pygame.display.update()
        fpsClock.tick(FPS)
    gmenager.gameEnd(main, playing)


if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 1, 1024)
    pygame.mixer.init()
    pygame.mixer.music.load('Music/button1.wav')
    gra = main()
