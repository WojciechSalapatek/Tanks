from Objects import *

class GameMenager():
    def __init__(self, toSpawn, groupsList, mode):
        self.mode = mode
        self.toSpawn = toSpawn
        self.spawn1 = (10, 10)
        self.spawn2 = (1019, 10)
        self.spawn3 = (515, 10)
        self.t1 = Gui(1125, 150,  pygame.image.load('Sprites/tank.png'))
        self.t2 = Gui(1175, 150,  pygame.image.load('Sprites/tank.png'))
        self.t3 = Gui(1125, 225, pygame.image.load('Sprites/tank.png'))
        self.t4 = Gui(1175, 225, pygame.image.load('Sprites/tank.png'))
        self.t5 = Gui(1125, 300, pygame.image.load('Sprites/tank.png'))
        self.t6 = Gui(1175, 300, pygame.image.load('Sprites/tank.png'))
        self.t7 = Gui(1125, 375, pygame.image.load('Sprites/tank.png'))
        self.t8 = Gui(1175, 375, pygame.image.load('Sprites/tank.png'))
        self.t9 = Gui(1125, 450, pygame.image.load('Sprites/tank.png'))
        self.t10 = Gui(1175, 450, pygame.image.load('Sprites/tank.png'))
        tlist = pygame.sprite.Group([])
        groupsList.append(tlist)
        groupsList.append(pygame.sprite.Group([]))
        groupsList[11].add(self.t1)
        groupsList[11].add(self.t2)
        groupsList[11].add(self.t3)
        groupsList[11].add(self.t4)
        groupsList[11].add(self.t5)
        groupsList[11].add(self.t6)
        groupsList[11].add(self.t7)
        groupsList[11].add(self.t8)
        groupsList[11].add(self.t9)
        groupsList[11].add(self.t10)
        self.groupsList = groupsList
        self.score = 0

    def update(self, groupsList):
        if self.mode == 'levels':
            if len(groupsList[2]) + len(groupsList[9]) < 3 and self.toSpawn > 0:
                self.spawn(groupsList)
            if self.toSpawn == 9:
                groupsList[11].remove(self.t10)
            elif self.toSpawn == 8:
                groupsList[11].remove(self.t9)
            elif self.toSpawn == 7:
                groupsList[11].remove(self.t8)
            elif self.toSpawn == 6:
                groupsList[11].remove(self.t7)
            elif self.toSpawn == 5:
                groupsList[11].remove(self.t6)
            elif self.toSpawn == 4:
                groupsList[11].remove(self.t5)
            elif self.toSpawn == 3:
                groupsList[11].remove(self.t4)
            elif self.toSpawn == 2:
                groupsList[11].remove(self.t3)
            elif self.toSpawn == 1:
                groupsList[11].remove(self.t2)
            elif self.toSpawn == 0:
                groupsList[11].remove(self.t1)

        elif self.mode == 'arcade':
            if len(groupsList[2]) + len(groupsList[9]) < 3:
                self.score += 100
                self.spawn(groupsList)

    def status(self):
        if self.mode == 'levels':
            if (len(self.groupsList[2]) + self.toSpawn) <= 0:
                return 1
            elif self.groupsList[0].sprites()[0].hp <= 0:
                return -1
            else:
                return 0
        if self.mode == 'arcade':
            if self.groupsList[0].sprites()[0].hp <= 0:
                return -1
            else:
                return 0


    def gameEnd(self, main, code):
        if self.mode == 'levels' and code == 1:
            main.endStatus(self.mode, 1)
        if self.mode == 'levels' and code == -1:
            main.endStatus(self.mode, -1)

        elif self.mode == 'arcade':
            main.endStatus(self.mode, self.score)


    def spawn(self, groupsList):
        r = random.randrange(3)
        if r == 0:
            spawnp = self.spawn1
        elif r == 1:
            spawnp = self.spawn2
        elif r == 2:
            spawnp = self.spawn3
        groupsList[9].add(Spawner(spawnp[0], spawnp[1]))
        self.toSpawn -= 1

# level bulder przygotowyje lvl
def buildLevel(B, W, H, mode):
    bricksImg = pygame.image.load('Sprites/bricks.png')
    if mode == 'level1':
        levelmap = "E    X    E   X     E"\
                   "     X        X      "\
                   "     XXXXXXXXXX      "\
                   "     X   EE   X      "\
                   "LLLLLX BBBBBB XLLLLLL"\
                   "LLLLLX BLLLLB XLLLLLL"\
                   "XXXXXX BLLLLB XXXXXXX"\
                   "BBBBBX BLLLLB XBBBBBB"\
                   "BBBBBX BBBBBB XBBBBBB"\
                   "     X        X      "\
                   "     XXXXXXXXXX      "\
                   "                     "\
                   "        S        E   "\
                   "      P              "
        modearg = 'levels'
    elif mode == 'level2':
        levelmap = "E    X    E   X     E"\
                   "   XXXX       X X    "\
                   "   XXXX      BBBBBXXX"\
                   "   XXXX UUU      LLLL"\
                   "   X     U       LLLL"\
                   "UUUX        LLLL     "\
                   "UUUX  BBB   LLLLXXXXX"\
                   "BBBX  BBB   LLLL  U B"\
                   "BBBLLLLLLLLLLLLL    B"\
                   "        XXBBBBB     B"\
                   "        XXBBBBBXXXX B"\
                   "XXXUU          XXUU B"\
                   "UU      S           B"\
                   "      P             B"
        modearg = 'levels'

    elif mode == 'level3':
        levelmap = "E    XX   E   X     E"\
                   "BBBXXXXXXLLLXXXXXXXXX"\
                   "BBBXXXXXXLLLXXXXXXWWW"\
                   "LLLLLLLLLLLLLLLLLLLXX"\
                   "WWWWWWXXLXXXXXXXXXLXX"\
                   "BBBBBBBBLLLLLEXXXXLXX"\
                   "WWWWWWWWWWXXLXXXXXLWW"\
                   "BBBBBBBBBBLLLLLLLLLWW"\
                   "XXUUX  EXXXLLXEXBBBXX"\
                   "XXUUX   XXXLLXXXBBBXX"\
                   "XXXXX   XXXLLXXXXXXXX"\
                   "XXX            UUBLLL"\
                   "XX      S       WBLLL"\
                   "X     P       WWWBLLL"

        modearg = 'levels'
    elif mode == 'level4':
        levelmap = "E    XXXL E   X     E"\
                   "BBBBBB       XXXXXXBL"\
                   "XXXXBB       LLLLLLBL"\
                   "XXXXBBBBBX   LBBLLLBL"\
                   "LWBXUUBBXXX WLLLLLLBL"\
                   "LWBX ULB XXBBLLXXXXBX"\
                   "LLLL XXL XXBBLLXXWXBX"\
                   "LLBW XXL XXBBLLXXUXBU"\
                   "WWWWXX UU   WLLXXUXBX"\
                   "BBBBBB LLXX WWLLWWWBX"\
                   "XBBBBX LLXX W  LWWWBX"\
                   "XXXBB          LLLLBX"\
                   "XXBB    S       UE  X"\
                   "XXXX  P          XXXX"
        modearg = 'levels'
    elif mode == 'level5':
        levelmap = "E    XL   E   XBB  BE"\
                   "LBBXXXLLLLU   XBB  BX"\
                   "LBBXXXXXXXXXXXXBBX BX"\
                   "U    LLLLLLLLLLLBBBBX"\
                   "U  BBBBBWWWWBBULXXXBX"\
                   "XXBBBBBWWWWWWBBL  XBX"\
                   "XX  BBWWWWWWWWBL XXBX"\
                   "XXX  BBWWWWWWBBLBBBBX"\
                   "   XL BBWWWWBLLLBBBBL"\
                   "XXXXL BBBULLLLXXXXXLL"\
                   "LLLLLXXXBBBBXXX   XLL"\
                   "LXX        BBB WW  LL"\
                   "UUXX    S    B WW LLL"\
                   "      P      B   LLLL"
        modearg = 'levels'
    else:
        levelmap = "E    X    E   X     E"\
                   "LLLXXXX       X X    "\
                   "LLLXXXX      BBBBBXXX"\
                   "   XXXX UUU  BBBBLLLL"\
                   "   XWWW  U       LLLL"\
                   "UUUX W      LLLL     "\
                   "UUUX  BBB   LLLLXXXXX"\
                   "BBBX  BBB   LLLL WU B"\
                   "BBBLLLLLLLLLLLLL W  B"\
                   "  W     XXBBBBB  W  B"\
                   "  W     XXBBBBBXXXX B"\
                   "XXXUU          XXUU B"\
                   "UU      S           B"\
                   "      P             B"
        modearg = 'arcade'
    neutralGroup, enemyGroup, playerGroup, bushGroup, plateGroup, baseGroup, waterGroup = buildMap(levelmap, B, W, H)
    bulletGroup = pygame.sprite.Group([])
    boomGroup = pygame.sprite.Group([])
    spawnerGroup = pygame.sprite.Group([])
    guiGroup = pygame.sprite.Group([Gui(0, 0, pygame.image.load('Sprites/frame.png'))])
    groupsList = [playerGroup, neutralGroup, enemyGroup, bulletGroup, boomGroup, bushGroup, plateGroup,baseGroup, guiGroup, spawnerGroup, waterGroup]
    return groupsList, GameMenager(10, groupsList, modearg)


# Funkcja ta na pdstawie stringa buduje mape levela
# X-birckblock E-enemy P-palyer [sapce] -nic
def buildMap(toParse, BLOCKSIZE, WIDTH, HEIGHT):
    x = 10
    y = 10
    neutralGroup = pygame.sprite.Group([])
    enemyGroup = pygame.sprite.Group([])
    playerGroup = pygame.sprite.Group([])
    bushGroup = pygame.sprite.Group([])
    plateGroup = pygame.sprite.Group([])
    baseGroup = pygame.sprite.Group([])
    waterGroup = pygame.sprite.Group([])
    enemy1 = (pygame.image.load('Sprites/enemy1.png'), pygame.image.load('Sprites/enemy1.png'), pygame.image.load('Sprites/enemy12.png'), 2, 3, pygame.image.load('Sprites/bullet.png'), 1, 350)
    bricksImg = pygame.image.load('Sprites/bricks.png')
    bbricksImg = pygame.image.load('Sprites/bbricks.png')
    bushImg = pygame.image.load('Sprites/bush.png')
    plateImg = pygame.image.load('Sprites/plate.png')
    baseImg = pygame.image.load('Sprites/eagle.png')
    for ch in toParse:
        if ch == "X":
            neutralGroup.add(NormalBricksBlock(x, y, bricksImg, 1))
            neutralGroup.add(NormalBricksBlock(x + 25, y, bricksImg, 1 ))
            neutralGroup.add(NormalBricksBlock(x, y + 25, bricksImg, 1))
            neutralGroup.add(NormalBricksBlock(x + 25, y + 25, bricksImg, 1))
        elif ch == 'U':
            neutralGroup.add(NormalBricksBlock(x, y, bbricksImg, 300))
        elif ch == "S":
            neutralGroup.add(NormalBricksBlock(x + 25, y + 25, bricksImg, 1))
            baseGroup.add(Base(x + 50, y + 50, baseImg))
            neutralGroup.add(NormalBricksBlock(x + 50, y + 25, bricksImg, 1))
            neutralGroup.add(NormalBricksBlock(x + 75, y + 25, bricksImg, 1))
            neutralGroup.add(NormalBricksBlock(x + 100, y + 25, bricksImg, 1))
            neutralGroup.add(NormalBricksBlock(x + 25, y + 50, bricksImg, 1))
            neutralGroup.add(NormalBricksBlock(x + 25, y + 75, bricksImg, 1))
            neutralGroup.add(NormalBricksBlock(x + 100, y + 50, bricksImg, 1))
            neutralGroup.add(NormalBricksBlock(x + 100, y + 75, bricksImg, 1))

        elif ch == "B":
            bushGroup.add(Bush(x, y, bushImg))
            bushGroup.add(Bush(x + 25, y, bushImg))
            bushGroup.add(Bush(x, y + 25, bushImg))
            bushGroup.add(Bush(x + 25, y + 25, bushImg))
        elif ch == "E":
            enemyGroup.add(Enemy(x, y, enemy1[0], enemy1[1], enemy1[2], enemy1[3], enemy1[4], enemy1[5], enemy1[6], enemy1[7]))
        elif ch == "L":
            plateGroup.add(Plate(x, y, plateImg))
        elif ch == "W":
            waterGroup.add(Water(x, y))
        elif ch == "P":
            playerGroup.add(pygame.sprite.Group([Player(x, y, pygame.image.load('Sprites/player.png'), pygame.image.load('Sprites/player.png'), pygame.image.load('Sprites/player2.png'), 5, 5, pygame.image.load('Sprites/bullet.png'), 1)]))
        if (x + BLOCKSIZE) >= WIDTH:
            x = 10
            y += BLOCKSIZE
        else:
            x += BLOCKSIZE
    return neutralGroup, enemyGroup, playerGroup, bushGroup,  plateGroup,  baseGroup, waterGroup
