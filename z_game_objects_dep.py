import pygame, sys, os
import z_main_game_dep as mg
import random


# Base
class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, hp):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        self.has_shield = False

    # Checks if object is in valid position
    def has_good_position(self):
        offset = 10
        if self.rect.x < offset or self.rect.x + self.image.get_width() > mg.FIELD_WIDTH + offset:
            return False
        if self.rect.y < offset or self.rect.y + self.image.get_height() > mg.FIELD_HEIGHT + offset:
            return False

        return True

    def decrease_hp(self, amount):
        if not self.has_shield:
            self.hp -= amount
        return self.hp


# Tank base class
class Tank(GameObject):
    bulletSpeed = 20*(3/2)

    def __init__(self, x, y, image, image1, image2, hp, speed, bulletImg):
        super().__init__(x,y,image, hp)
        self.image1 = image1
        self.image2 = image2
        self.toTargetImg = image
        self.speed = speed
        self.direction = 'right'
        self.bulletImg = bulletImg
        self.animTick = 0


    # obrót (Sprita)zarówno wyświetlanego obrazka jak i rectangla
    def rotate(self,angle):
        savedX = self.rect.x
        savedY = self.rect.y
        self.image = pygame.transform.rotate(self.toTargetImg, angle)
        self.rect = self.image.get_rect()
        self.rect.x = savedX
        self.rect.y = savedY

    # przesuwanie vertykalnie i sprawdzanie czy nastąpiła intersekcja z innymi obiektami nawet ze swojej sprite grupy
    # jeśli tak to sprite jest przesuwany w przeciwnym kieruku o 1 pixel aż do ustąpienie intersekcji
    # Ponadto sprawdzamy czy obiekt ma goodpos
    #  aoraz animowane sa gosienice

    def moveX(self, amount, groupsList):
        isIn = False
        self.rect.x += amount
        for i in range(0, 11):
            if i < 4 or i == 10:
                if self in groupsList[i].sprites():
                    groupsList[i].remove(self)
                    isIn = True
                tick = 0
                if pygame.sprite.spritecollide(self, groupsList[i], False) or not self.has_good_position():
                    self.rect.x -= amount
                    tick += 1
                if isIn:
                    groupsList[i].add(self)
                    isIn = False
        if self.animTick < 6:
            self.toTargetImg = self.image2
        else:
            self.toTargetImg = self.image1
            if self.animTick > 12:
                self.animTick = 0
        self.animTick += 1**(3/2)


    # tak jak moveX tylko że hryzontalnie
    def moveY(self, amount, groupsList):
        isIn = False
        self.rect.y += amount
        for i in range(0, 11):
            if i < 4 or i == 10:
                if self in groupsList[i].sprites():
                    groupsList[i].remove(self)
                    isIn = True
                tick = 0
                if pygame.sprite.spritecollide(self, groupsList[i], False) or not self.has_good_position():
                    self.rect.y -= amount
                    tick += 1
                if isIn:
                   groupsList[i].add(self)
                   isIn = False
        if self.animTick < 6:
            self.toTargetImg = self.image2
        else:
            self.toTargetImg = self.image1
            if self.animTick > 12:
                self.animTick = 0
        self.animTick += 1**(3/2)

    def moveUp(self, groupsList):
        self.moveY(-self.speed, groupsList)
        self.rotate(90)
        self.direction = 'up'

    def moveDown(self, groupsList):
        self.moveY(self.speed, groupsList)
        self.rotate(-90)
        self.direction = 'down'                                         # metody do poruszania sie czołgu/czołgiem

    def moveRight(self, groupsList):
        self.moveX(self.speed, groupsList)
        self.rotate(0)
        self.direction = 'right'

    def moveLeft(self, groupsList):
        self.moveX(-self.speed, groupsList)
        self.rotate(180)
        self.direction = 'left'

    def shoot(self, handler):
        if self.direction == 'up':
            x = self.rect.x + self.image.get_width()/2 -self.bulletImg.get_width()/2
            y = self.rect.y
            handler.addBullet(Bullet(x, y, self.bulletImg, 0, -self.bulletSpeed, self))
        elif self.direction == 'down':
            x = self.rect.x + self.image.get_width()/2 -self.bulletImg.get_width()/2
            y = self.rect.y + self.image.get_height()
            handler.addBullet(Bullet(x, y, self.bulletImg, 0, self.bulletSpeed, self))
        elif self.direction == 'right':
            x = self.rect.x + self.image.get_width()
            y = self.rect.y + self.image.get_height()/2 - self.bulletImg.get_height()/2
            handler.addBullet(Bullet(x, y,self.bulletImg, self.bulletSpeed, 0, self))
        elif self.direction == 'left':
            x = self.rect.x
            y = self.rect.y + self.image.get_height()/2 - self.bulletImg.get_height()/2
            handler.addBullet(Bullet(x, y,self.bulletImg, -self.bulletSpeed, 0, self))


#  klasa rozszerza klase tank
class Player(Tank):
    def __init__(self, x, y, image, image1, image2, hp, speed, bulletImg, delay):
        super().__init__(x, y, image, image1, image2, hp, speed, bulletImg)
        self.delay = delay
        self.shootSound = pygame.mixer.Sound('Music/shoot.wav')
        self.moveSound = pygame.mixer.music.load('Music/mv.wav')
        self.shieldTimer = 0
        pygame.mixer.music.play(-1)


    def update(self, handler, groupsList, displaysurface):
        #  sterowanie(sprawdzanie czy został wciśniety klawisz aż do wykrycia jednego z nich)
        while True:
            if pygame.key.get_pressed()[pygame.K_UP] == 1:
                pygame.mixer.music.unpause()
                self.moveUp(groupsList)
                break
            if pygame.key.get_pressed()[pygame.K_DOWN] == 1:
                pygame.mixer.music.unpause()
                self.moveDown(groupsList)
                break
            if pygame.key.get_pressed()[pygame.K_RIGHT] == 1:
                pygame.mixer.music.unpause()
                self.moveRight(groupsList)
                break
            if pygame.key.get_pressed()[pygame.K_LEFT] == 1:
                pygame.mixer.music.unpause()
                self.moveLeft(groupsList)
                break
            else:
                pygame.mixer.music.pause()
                break
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.delay <= 0:
                pygame.mixer.Sound.play(self.shootSound)
                self.shoot(handler)
                self.delay = 19
        else:
            self.delay -= 1.5*(3/2)
        self.delay -= 1*(3/2)

        if self.has_shield:
            self.shieldTimer -= 1
            if self.shieldTimer <= 0:
                self.has_shield = False
            else:
                self.updateShield(displaysurface)

    def updateShield(self, displaysurface):
        sh = GameObject(self.rect.x - 7, self.rect.y - 7, pygame.image.load('Sprites/shiel.png'), 1)
        shg = pygame.sprite.Group([sh])
        sh.rect.x = self.rect.x - 7
        sh.rect.y = self.rect.y - 7
        shg.draw(displaysurface)

    def giveShield(self, groupsList):
        self.shieldTimer = 200
        self.hasShield = True

class Base(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, 1)

    def update(self, groupsList, gameover):
        if pygame.sprite.spritecollide(self, groupsList[2], False):
            groupsList[0].sprites()[0].hp = 0


class Enemy(Tank):
    def __init__(self, x, y, image, image1, image2, hp, speed, bulletImg, delay, eyesight):
        super().__init__(x, y, image, image1, image2, hp, speed, bulletImg)
        self.delay = delay
        self.r = random.randrange(2)
        self.tick = 0
        self.change = random.randrange(100, 200)
        self.eyesight = eyesight
        self.dir = random.randrange(5)
        self.target = ""

    def trace(self, player, groupsList, handler):
        shooted = False
        player = player.sprites()[0]
        base = groupsList[7].sprites()[0]
        if min(abs(self.rect.x - player.rect.x), abs(self.rect.x - player.rect.x)) <= min(abs(self.rect.x - base.rect.x), abs(self.rect.y - base.rect.y)):
            diffX = self.rect.x - player.rect.x
            diffY = self.rect.y - player.rect.y
            self.target = "player"
        else:
            diffX = self.rect.x - base.rect.x
            diffY = self.rect.y - base.rect.y
            self.target = "base"

        if max(abs(diffX), abs(diffY)) <= self.eyesight:
            if self.r == 1 and (abs(diffY) - self.speed+1) > 0:
                if diffY >= 0:
                    self.moveUp(groupsList)
                else:
                    self.moveDown(groupsList)
            elif (abs(diffX) - self.speed+1) > 0:
                if diffX >= 0:
                    self.moveLeft(groupsList)
                else:
                    self.moveRight(groupsList)
            else:
                if diffY > 0:
                    self.moveUp(groupsList)
                elif diffY < 0:
                    self.moveDown(groupsList)
        else:
            if self.dir == 0:
                self.moveRight(groupsList)
            elif self.dir == 1:
                self.moveLeft(groupsList)
            elif self.dir == 2:
                self.moveUp(groupsList)
            elif self.dir == 3 or self.dir == 5:
                self.moveDown(groupsList)
        if (((abs(diffX) - self.speed -3) < 0) or ((abs(diffY) - self.speed -3) < 0)) and self.target != "base":
            if self.delay <= 0:
                self.shoot(handler)
                self.delay = 45
        self.delay -= 1*(3/2)

        if self.tick >= self.change:
            self.r = random.randrange(2)
            self.dir = random.randrange(6)
            self.change = random.randrange(60, 150)
            self.tick = 0
        self.tick += 1*(3/2)
        if shooted:
            return "shoot"
        else:
            return "move"

    def update(self, handler, groupsList):
        currX = self.rect.x
        currY = self.rect.y
        if self.trace(groupsList[0], groupsList, handler) == "move":
            if ((self.rect.x - currX) == 0) and ((self.rect.y - currY) == 0) and self.delay <= 0:
                self.shoot(handler)
                self.delay = 45


# pocisk
class Bullet(GameObject):
    boomImage = pygame.image.load('Sprites/boom.png')

    def __init__(self, x, y, image, velocityX, velocityY, owner):
        super().__init__(x, y, image,1)
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.owner = owner

    def update(self, groupsList):
        if not self.has_good_position():
            groupsList[3].remove(self)
        for i in range(0, 3):
            if self.owner in groupsList[i]:
                continue
            if pygame.sprite.spritecollide(self, groupsList[i], False):  # Jeśli w coś uderzy to tworzy wybuch - boom
                groupsList[4].add(Boom(self.rect.x - 17, self.rect.y -17, self.boomImage, self.owner))
                groupsList[3].remove(self)
        self.rect.x += self.velocityX
        self.rect.y += self.velocityY


# Zmniejsza hp obiektów w swoim zasiegu
class Boom (GameObject):
    def __init__(self, x, y, image, owner):
        super().__init__(x, y, image, 1)
        self.owner = owner
        self.img1 = pygame.image.load('Sprites/boom1.png')
        self.img2 = pygame.image.load('Sprites/boom2.png')
        self.img3 = pygame.image.load('Sprites/boom3.png')
        self.img4 = pygame.image.load('Sprites/boom4.png')
        self.img5 = pygame.image.load('Sprites/boom5.png')
        self.img6 = pygame.image.load('Sprites/boom6.png')
        self.img7 = pygame.image.load('Sprites/boom7.png')
        self.timer = -1
        self.hit = pygame.mixer.Sound('Music/hit.wav')
        self.hit2 = pygame.mixer.Sound('Music/hit2.wav')

    def update(self, groupsList, gameover):
        if self.timer < 0:
            self.rect.x += 12
            self.rect.y += 12
            for i in range(0, 3):
                if self.owner in groupsList[i]:
                    groupsList[i].remove(self.owner)
                    for gameObject in pygame.sprite.spritecollide(self, groupsList[i], False):
                        if i == 0:
                            pygame.mixer.Sound.play(self.hit)
                        else:
                            pygame.mixer.Sound.play(self.hit2)
                        if gameObject.decrease_hp(1) <= 0:
                            if i== 2:
                                groupsList[4].add(BigBoom(self.rect.x, self.rect.y, pygame.image.load('Sprites/boom11.png')))
                            if i != 0:
                                groupsList[i].remove(gameObject)
                    groupsList[i].add(self.owner)
                else:
                    for gameObject in pygame.sprite.spritecollide(self, groupsList[i], False):
                        if i == 0:
                            pygame.mixer.Sound.play(self.hit)
                        else:
                            pygame.mixer.Sound.play(self.hit2)
                        if gameObject.decrease_hp(1) <= 0:
                            if i ==2:
                                groupsList[4].add(BigBoom(self.rect.x -23, self.rect.y -23, pygame.image.load('Sprites/boom11.png')))
                            if i != 0:
                                groupsList[i].remove(gameObject)

            self.rect.x -= 6
            self.rect.y -= 6

        elif self.timer >= 0 and self.timer < 3:
            self.image = self.img1
        elif self.timer >= 3 and self.timer < 6:
            self.image = self.img2
        elif self.timer >= 6 and self.timer < 9:
            self.image = self.img3
        elif self.timer >=9 and self.timer < 12:
            self.image = self.img4
        elif self.timer >= 12 and self.timer < 15:
            self.image = self.img5
        elif self.timer >= 15 and self.timer < 20:
            self.image = self.img6
        elif self.timer >= 20 and self.timer < 25:
            self.image = self.img7
        else:
            groupsList[4].remove(self)
        self.timer += 1*(3/2)

class BigBoom(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, 1)
        self.music = pygame.mixer.Sound('Music/boom.wav')
        self.img1 = pygame.image.load('Sprites/boom11.png')
        self.img2 = pygame.image.load('Sprites/boom12.png')
        self.img3 = pygame.image.load('Sprites/boom13.png')
        self.img4 = pygame.image.load('Sprites/boom14.png')
        self.img5 = pygame.image.load('Sprites/boom15.png')
        self.img6 = pygame.image.load('Sprites/boom16.png')
        self.img7 = pygame.image.load('Sprites/boom17.png')
        self.timer = 0
        pygame.mixer.Sound.play(self.music)

    def update(self, groupsList, gameover):
        if self.timer >= 0 and self.timer < 3:
            self.image = self.img1
        elif self.timer >= 3 and self.timer < 6:
            self.image = self.img2
        elif self.timer >= 6 and self.timer < 9:
            self.image = self.img3
        elif self.timer >=9 and self.timer < 12:
            self.image = self.img4
        elif self.timer >= 12 and self.timer < 15:
            self.image = self.img5
        elif self.timer >= 15 and self.timer < 20:
            self.image = self.img6
        elif self.timer >= 20 and self.timer < 25:
            self.image = self.img7
        else:
            choice = random.randrange(6)
            if choice == 1:
                groupsList[12].add(HpItem(self.rect.x + 15, self.rect.y + 15))
            elif choice == 2:
                groupsList[12].add(ShieldItem(self.rect.x + 15, self.rect.y + 15))
            elif choice == 3:
                groupsList[12].add(BaseItem(self.rect.x + 15, self.rect.y + 15))
            groupsList[4].remove(self)
        self.timer += 1*(3/2)

class Item(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, 1)
        self.sound = pygame.mixer.Sound('Music/item.wav')
        self.timer = 160

    def update(self, groupsList):
        if pygame.sprite.spritecollide(self, groupsList[0], False):
            pygame.mixer.Sound.play(self.sound)
            self.pickup(groupsList)
            groupsList[12].remove(self)
        if self.timer <= 0:
            groupsList[12].remove(self)
        self.timer -= 1

    def pickup(self, groupsList):
        pass


class HpItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load('Sprites/hp.png'))

    def pickup(self, groupsList):
        groupsList[0].sprites()[0].hp += 1


class ShieldItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load('Sprites/shield.png'))

    def pickup(self, groupsList):
        groupsList[0].sprites()[0].giveShield(groupsList )

class BaseItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load('Sprites/base.png'))

    def pickup(self, groupsList):
        x = 410
        y = 610
        bricksImg = pygame.image.load('Sprites/bricks.png')
        groupsList[1].add(NormalBricksBlock(x + 25, y + 25, bricksImg, 1))
        groupsList[1].add(NormalBricksBlock(x + 50, y + 25, bricksImg, 1))
        groupsList[1].add(NormalBricksBlock(x + 75, y + 25, bricksImg, 1))
        groupsList[1].add(NormalBricksBlock(x + 100, y + 25, bricksImg, 1))
        groupsList[1].add(NormalBricksBlock(x + 25, y + 50, bricksImg, 1))
        groupsList[1].add(NormalBricksBlock(x + 25, y + 75, bricksImg, 1))
        groupsList[1].add(NormalBricksBlock(x + 100, y + 50, bricksImg, 1))
        groupsList[1].add(NormalBricksBlock(x + 100, y + 75, bricksImg, 1))


# blok cegieł
class NormalBricksBlock(GameObject):
    def __init__(self, x, y, image,hp):
        super().__init__(x, y, image, hp)


class Bush(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, 1)


class Plate(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, 1)


class Water(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load('Sprites/water1.png'), 21)
        self.timer = 0
        self.image1 = pygame.image.load('Sprites/water1.png')
        self.image2 = pygame.image.load('Sprites/water2.png')

    def update(self):
        if self.timer < 30:
            self.image = self.image1
        elif self.timer < 60:
            self.image = self.image2
        else:
            self.timer = 0

        self.timer += 1*(3/2)




class Gui(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, 1)


class Button(GameObject):
    def __init__(self, x, y, image1, image2, image3, label, action = None, arg=None, arg2 = None):
        super().__init__(x, y, image1, None)
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.label = label
        self.action = action
        self.clicked = False
        self.arg = arg
        self.arg2 = arg2
        self.play = True
        self.sound1 = pygame.mixer.Sound('Music/button1.wav')

    def update(self):
        mouse = pygame.mouse.get_pos()
        if (mouse[0] >= self.rect.x and mouse[0] <= self.rect.x + self.image.get_width()) and (mouse[1] >= self.rect.y and mouse[1] <= self.rect.y + self.image.get_height()):
            self.image = self.image2
            if self.play:
                pygame.mixer.Sound.play(self.sound1)
                self.play = False
            if pygame.mouse.get_pressed()[0] == 1:
                self.image = self.image3
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] != 1:
                if self.clicked:
                    if self.action != None and self.arg == None:
                        self.action()
                    elif self.action != None and  self.arg != None and self.arg2 == None:
                        self.action(self.arg)
                    elif self.action != None and  self.arg != None and self.arg2 != None:
                        self.action(self.arg, self.arg2)
        else:
            self.clicked = False
            self.image = self.image1
            self.play = True

class Spawner(GameObject):
    def __init__(self, x, y,):
        super().__init__(x, y, pygame.image.load('Sprites/empty.png'), 1)
        self.tick = 0
        self.enemy1 = (pygame.image.load('Sprites/enemy1.png'), pygame.image.load('Sprites/enemy1.png'), pygame.image.load('Sprites/enemy12.png'), 2, 3, pygame.image.load('Sprites/bullet.png'), 1, 350)

    def update(self, groupsList):
        if self.tick < 2:
            self.image = pygame.image.load('Sprites/empty.png')
        elif self.tick < 5:
            self.image = pygame.image.load('Sprites/spawn1.png')
        elif self.tick < 10:
            self.image = pygame.image.load('Sprites/spawn2.png')
        elif self.tick < 15:
            self.image = pygame.image.load('Sprites/spawn3.png')
        elif self.tick < 20:
            self.image = pygame.image.load('Sprites/spawn2.png')
        elif self.tick < 25:
            self.image = pygame.image.load('Sprites/spawn1.png')
        elif self.tick < 30:
            self.image = pygame.image.load('Sprites/spawn2.png')
        else:
            groupsList[9].remove(self)
            groupsList[2].add(
                Enemy(self.rect.x, self.rect.y, self.enemy1[0], self.enemy1[1], self.enemy1[2], self.enemy1[3],
                      self.enemy1[4], self.enemy1[5], self.enemy1[6], self.enemy1[7]))
        if pygame.sprite.spritecollide(self, groupsList[0], False) or pygame.sprite.spritecollide(self, groupsList[2], False) or pygame.sprite.spritecollide(self, groupsList[1], False):
            self.image = pygame.image.load('Sprites/empty.png')
            if self.rect.x < 1000:
                self.rect.x += 55
            else:
                self.rect.x -= 55
        if self in groupsList[9]:
            groupsList[9].remove(self)
            if pygame.sprite.spritecollide(self, groupsList[9], False):
                self.image = pygame.image.load('Sprites/empty.png')
                if self.rect.x < 1000:
                    self.rect.x += 55
                else:
                    self.rect.x -= 55
            groupsList[9].add(self)
        self.tick += 1*(3/2)


class Menu():
    def __init__(self):
        self.buttonGroup = pygame.sprite.Group([])
        self.image = pygame.image.load('Sprites/menu.png')

    def update(self, displaysurface):
        displaysurface.blit(self.image, (0,0))
        self.buttonGroup.update()
        self.buttonGroup.draw(displaysurface)

    def addButton(self, button):
        self.buttonGroup.add(button)

    def clearButtons(self):
        self.buttonGroup = pygame.sprite.Group([])



    '''def trace(self, player, groupsList, handler):
        shooted = False
        player = player.sprites()[0]
        diffX = self.rect.x - player.rect.x
        diffY = self.rect.y - player.rect.y
        if abs(diffX) >= abs(diffY) and (abs(diffY) - self.speed) > 0:
            if diffY >= 0:
                self.moveUp(groupsList)
            else:
                self.moveDown(groupsList)
        elif (abs(diffX) - self.speed) > 0:
            if diffX >= 0:
                self.moveLeft(groupsList)
            else:
                self.moveRight(groupsList)
        else:
            if diffY > 0:
                self.moveUp(groupsList)
            elif diffY < 0:
                self.moveDown(groupsList)

        if ((abs(diffX) - self.speed -3) < 0) or ((abs(diffY) - self.speed -3) < 0):
            if self.delay <= 0:
                self.shoot(handler)
                self.delay = 45
        self.delay -= 1

        if shooted:
            return "shoot"
        else:
            return "move"'''
