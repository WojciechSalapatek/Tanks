import pygame
import main_game as mg
import random
import math
import loader
import copy
import sys
import shelve
loader.init_game_images()
loader.init_menu_images()
gi = loader.game_images
mi = loader.menu_images


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
    bulletSpeed = 900

    def __init__(self, x, y, image, image1, image2, hp, speed, bullet_img, delay):
        super().__init__(x, y, image, hp)
        self.image1 = image1
        self.image2 = image2
        self.target_img = image
        self.speed = speed
        self.direction = 'right'
        self.bullet_img = bullet_img
        self.anim_timer = 0
        self.delay = delay

    def rotate(self, angle):
        saved_x = self.rect.x
        saved_y = self.rect.y
        self.image = pygame.transform.rotate(self.target_img, angle)
        self.rect = self.image.get_rect()
        self.rect.x = saved_x
        self.rect.y = saved_y

    def move_x(self, dist, groups_list, delta):
        amount = int(dist*delta)
        is_in = False
        self.rect.x += amount
        for i in range(0, 11):
            if i < 4 or i == 10:
                if self in groups_list[i].sprites():
                    groups_list[i].remove(self)
                    is_in = True
                if pygame.sprite.spritecollide(self, groups_list[i], False) or not self.has_good_position():
                    self.rect.x -= amount
                if is_in:
                    groups_list[i].add(self)
                    is_in = False
        if self.anim_timer < 6:
            self.target_img = self.image2
        else:
            self.target_img = self.image1
            if self.anim_timer > 12:
                self.anim_timer = 0
        self.anim_timer += 10*delta

    def move_y(self, dist, groups_list, delta):
        amount = int(dist*delta)
        is_in = False
        self.rect.y += amount
        for i in range(0, 11):
            if i < 4 or i == 10:
                if self in groups_list[i].sprites():
                    groups_list[i].remove(self)
                    is_in = True
                if pygame.sprite.spritecollide(self, groups_list[i], False) or not self.has_good_position():
                    self.rect.y -= amount
                if is_in:
                    groups_list[i].add(self)
                    is_in = False

        if self.anim_timer < 6:
            self.target_img = self.image2
        else:
            self.target_img = self.image1
            if self.anim_timer > 12:
                self.anim_timer = 0
        self.anim_timer += 10*delta

    def move_up(self, groups_list, delta):
        self.move_y(-self.speed, groups_list, delta)
        self.rotate(90)
        self.direction = 'up'

    def move_down(self, groups_list, delta):
        self.move_y(self.speed, groups_list, delta)
        self.rotate(-90)
        self.direction = 'down'

    def move_right(self, groups_list, delta):
        self.move_x(self.speed, groups_list, delta)
        self.rotate(0)
        self.direction = 'right'

    def move_left(self, groups_list, delta):
        self.move_x(-self.speed, groups_list, delta)
        self.rotate(180)
        self.direction = 'left'

    def shoot(self, handler, delta):
        if self.delay > 0:
            return False
        if self.direction == 'up':
            x = self.rect.x + self.image.get_width() / 2 - self.bullet_img.get_width() / 2
            y = self.rect.y
            handler.add_bullet(Bullet(x, y, 0, -self.bulletSpeed, self))
        elif self.direction == 'down':
            x = self.rect.x + self.image.get_width() / 2 - self.bullet_img.get_width() / 2
            y = self.rect.y + self.image.get_height()
            handler.add_bullet(Bullet(x, y, 0, self.bulletSpeed, self))
        elif self.direction == 'right':
            x = self.rect.x + self.image.get_width()
            y = self.rect.y + self.image.get_height() / 2 - self.bullet_img.get_height() / 2
            handler.add_bullet(Bullet(x, y, self.bulletSpeed, 0, self))
        elif self.direction == 'left':
            x = self.rect.x
            y = self.rect.y + self.image.get_height() / 2 - self.bullet_img.get_height() / 2
            handler.add_bullet(Bullet(x, y, -self.bulletSpeed, 0, self))
        self.delay = 0.35
        return True


class Player(Tank):
    def __init__(self, x, y, hp, speed, delay):
        super().__init__(x, y, gi["player1"], gi["player1"], gi["player2"], hp, speed, gi["bullet"], delay)
        self.shoot_sound = pygame.mixer.Sound('Music/shoot.wav')
        self.move_sound = pygame.mixer.music.load('Music/mv.wav')
        self.shield_timer = 0
        pygame.mixer.music.play(-1)

    def update(self, delta, handler):
        while True:
            if pygame.key.get_pressed()[pygame.K_UP] == 1:
                pygame.mixer.music.unpause()
                self.move_up(handler.groups_list, delta)
                break
            if pygame.key.get_pressed()[pygame.K_DOWN] == 1:
                pygame.mixer.music.unpause()
                self.move_down(handler.groups_list, delta)
                break
            if pygame.key.get_pressed()[pygame.K_RIGHT] == 1:
                pygame.mixer.music.unpause()
                self.move_right(handler.groups_list, delta)
                break
            if pygame.key.get_pressed()[pygame.K_LEFT] == 1:
                pygame.mixer.music.unpause()
                self.move_left(handler.groups_list, delta)
                break
            else:
                pygame.mixer.music.pause()
                break
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.shoot(handler, delta)

        if self.has_shield:
            self.shield_timer -= delta
            if self.shield_timer <= 0:
                self.has_shield = False
            else:
                self.update_shield(handler.displaysurface)
        self.delay -= delta

    def shoot(self, handler, delta):
        if super().shoot(handler, delta):
            pygame.mixer.Sound.play(self.shoot_sound)

    def update_shield(self, displaysurface):
        sh = GameObject(self.rect.x - 7, self.rect.y - 7, gi["shiel"], 1)
        shg = pygame.sprite.Group([sh])
        sh.rect.x = self.rect.x - 7
        sh.rect.y = self.rect.y - 7
        shg.draw(displaysurface)

    def give_shield(self, groups_list):
        self.shield_timer = 6
        self.has_shield = True


class Enemy(Tank):
    def __init__(self, x, y, hp, speed, delay, eyesight):
        super().__init__(x, y, gi['enemy1'], gi['enemy1'], gi['enemy2'], hp, speed, gi['bullet'], delay)
        self.tick = 0
        self.eyesight = eyesight
        self.random_axe = None
        self.randomize_axis()
        self.strategy_delay = 2
        self.timer = 0
        self.has_turned = False
        self.random_direction = None

    def randomize_axis(self):
        choice = random.randint(0, 1)
        choice2 = random.randint(0, 1)
        self.random_axe = "horizontal" if choice else "vertical"
        self.random_direction = "positive" if choice2 else "negative"

    def chase(self, dist_x, dist_y, handler, delta):
        def move_horizontal():
            if dist_x < 0:
                self.move_right(handler.groups_list, delta)

            else:
                self.move_left(handler.groups_list, delta)

        def move_vertical():
            if dist_y < 0:
                self.move_down(handler.groups_list, delta)
            else:
                self.move_up(handler.groups_list, delta)

        if self.random_axe == "horizontal":
            if abs(dist_x > 10):
                self.has_turned = False
                move_horizontal()
            elif abs(dist_y) > 10 and not self.has_turned:
                self.has_turned = True
                move_vertical()

        elif self.random_axe == "vertical":
            if abs(dist_y) > 10:
                self.has_turned = False
                move_vertical()
            elif abs(dist_x) > 10 and not self.has_turned:
                self.has_turned = True
                move_horizontal()

        if self.timer >= self.strategy_delay:
            self.randomize_axis()
            self.timer = 0
        self.timer += delta

    def explore(self, handler, delta):
        if self.random_axe == "horizontal":
            self.move_right(handler.groups_list, delta) if self.random_direction == "positive" \
                else self.move_left(handler.groups_list, delta)

        if self.random_axe == "vertical":
            self.move_down(handler.groups_list, delta) if self.random_direction == "positive" \
                else self.move_up(handler.groups_list, delta)

        if self.timer >= self.strategy_delay:
            self.randomize_axis()
            self.timer = 0
        self.timer += delta

    def trace(self, handler, delta):
        player = handler.groups_list[0].sprites()[0]
        base = handler.groups_list[7].sprites()[0]
        distance_to_player_x = self.rect.x - player.rect.x
        distance_to_player_y = self.rect.y - player.rect.y
        distance_to_base_x = self.rect.x - base.rect.x
        distance_to_base_y = self.rect.y - base.rect.y
        distance_to_player = int(math.sqrt(distance_to_player_x**2 + distance_to_player_y**2))
        min_distance_to_player = min(abs(distance_to_player_x), abs(distance_to_player_y))
        distance_to_base = int(math.sqrt(distance_to_base_x**2 + distance_to_base_y**2))
        min_distance_to_base = min(abs(distance_to_base_x), abs(distance_to_base_y))

        if distance_to_player < self.eyesight:
            self.chase(distance_to_player_x, distance_to_player_y, handler, delta)
            if min_distance_to_player < 12:
                self.shoot(handler, delta)

        elif min_distance_to_base < self.eyesight:
            # if min_distance_to_base < 25:
            #     self.shoot(handler, delta)
            self.chase(distance_to_base_x, distance_to_base_y, handler, delta)
        else:
            self.explore(handler, delta)

    def update(self, delta, handler):
        self.trace(handler, delta)
        self.delay -= delta


class Bullet(GameObject):

    def __init__(self, x, y, velocity_x, velocity_y, owner):
        super().__init__(x, y, gi['bullet'], 1)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.owner = owner

    def update(self, delta, handler):
        if not self.has_good_position():
            handler.groups_list[3].remove(self)
        for i in range(0, 3):
            if self.owner in handler.groups_list[i]:
                continue
            if pygame.sprite.spritecollide(self, handler.groups_list[i], False):
                handler.groups_list[4].add(Boom(self.rect.x - self.image.get_width() / 2,
                                                self.rect.y - self.image.get_height() / 2,
                                                self.owner))
                handler.groups_list[3].remove(self)
        self.rect.x += self.velocity_x*delta
        self.rect.y += self.velocity_y*delta


class Boom (GameObject):
    def __init__(self, x, y, owner):
        super().__init__(x, y, gi['boom'], 1)
        self.owner = owner
        self.img1 = gi['boom1']
        self.img2 = gi['boom2']
        self.img3 = gi['boom3']
        self.img4 = gi['boom4']
        self.img5 = gi['boom5']
        self.img6 = gi['boom6']
        self.img7 = gi['boom7']
        self.timer = -1
        self.hit = pygame.mixer.Sound('Music/hit.wav')
        self.hit2 = pygame.mixer.Sound('Music/hit2.wav')

    def check_destroyed(self, i, handler):
        for gameObject in pygame.sprite.spritecollide(self, handler.groups_list[i], False):
            if i == 0:
                pygame.mixer.Sound.play(self.hit)
            else:
                pygame.mixer.Sound.play(self.hit2)
            if gameObject.decrease_hp(1) <= 0:
                if i == 2:
                    handler.groups_list[4].add(
                        BigBoom(self.rect.x - 23, self.rect.y - 23))
                if i != 0:
                    handler.groups_list[i].remove(gameObject)

    def update(self, delta, handler):
        if self.timer < 0:

            for i in range(0, 3):
                if self.owner in handler.groups_list[i]:
                    handler.groups_list[i].remove(self.owner)
                    self.check_destroyed(i, handler)
                    handler.groups_list[i].add(self.owner)
                else:
                    self.check_destroyed(i, handler)

        elif 0 <= self.timer < 3:
            self.image = self.img1
        elif 3 <= self.timer < 6:
            self.image = self.img2
        elif 6 <= self.timer < 9:
            self.image = self.img3
        elif 9 <= self.timer < 12:
            self.image = self.img4
        elif 12 <= self.timer < 15:
            self.image = self.img5
        elif 15 <= self.timer < 20:
            self.image = self.img6
        elif 20 <= self.timer < 25:
            self.image = self.img7
        else:
            handler.groups_list[4].remove(self)
        self.timer += 63*delta


class BigBoom(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, gi['boom11'], 1)
        self.music = pygame.mixer.Sound('Music/boom.wav')
        self.img1 = gi['boom11']
        self.img2 = gi['boom12']
        self.img3 = gi['boom13']
        self.img4 = gi['boom14']
        self.img5 = gi['boom15']
        self.img6 = gi['boom16']
        self.img7 = gi['boom17']
        self.timer = 0
        pygame.mixer.Sound.play(self.music)

    def update(self, delta, handler):
        if 0 <= self.timer < 3:
            self.image = self.img1
        elif 3 <= self.timer < 6:
            self.image = self.img2
        elif 6 <= self.timer < 9:
            self.image = self.img3
        elif 9 <= self.timer < 12:
            self.image = self.img4
        elif 12 <= self.timer < 15:
            self.image = self.img5
        elif 15 <= self.timer < 20:
            self.image = self.img6
        elif 20 <= self.timer < 25:
            self.image = self.img7
        else:
            choice = random.randrange(6)
            if choice == 1:
                handler.groups_list[12].add(HpItem(self.rect.x + 15, self.rect.y + 15))
            elif choice == 2:
                handler.groups_list[12].add(ShieldItem(self.rect.x + 15, self.rect.y + 15))
            elif choice == 3:
                handler.groups_list[12].add(BaseItem(self.rect.x + 15, self.rect.y + 15))
            handler.groups_list[4].remove(self)
        self.timer += 63*delta


class Base(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, gi['eagle'], 1)

    def update(self, delta, handler):
        if pygame.sprite.spritecollide(self, handler.groups_list[2], False):
            handler.groups_list[0].sprites()[0].hp = 0


class NormalBricksBlock(GameObject):
    def __init__(self, x, y, hp):
        super().__init__(x, y, gi['bricks'], hp)


class WhiteBricksBlock(GameObject):
    def __init__(self, x, y, hp):
        super().__init__(x, y, gi['b_bricks'], hp)


class Bush(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, gi['bush'], 1)


class Plate(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, gi['plate'], 1)


class Water(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, gi['water1'], 21)
        self.timer = 0
        self.image1 = gi['water1']
        self.image2 = gi['water2']

    def update(self, delta, handler):
        if self.timer < 0.4:
            self.image = self.image1
        elif self.timer < 0.8:
            self.image = self.image2
        else:
            self.timer = 0

        self.timer += delta


class Item(GameObject):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, 1)
        self.sound = pygame.mixer.Sound('Music/item.wav')
        self.timer = 160

    def update(self, delta, handler):
        if pygame.sprite.spritecollide(self, handler.groups_list[0], False):
            pygame.mixer.Sound.play(self.sound)
            self.pickup(handler.groups_list)
            handler.groups_list[12].remove(self)
        if self.timer <= 0:
            handler.groups_list[12].remove(self)
        self.timer -= 1

    def pickup(self, groups_list):
        pass


class HpItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, gi['hp'])

    def pickup(self, groups_list):
        groups_list[0].sprites()[0].hp += 1


class ShieldItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, gi['shield'])

    def pickup(self, groups_list):
        groups_list[0].sprites()[0].give_shield(groups_list)


class BaseItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, gi['base'])

    def pickup(self, groups_list):
        x = 410
        y = 610
        groups_list[1].add(NormalBricksBlock(x + 25, y + 25, 1))
        groups_list[1].add(NormalBricksBlock(x + 50, y + 25, 1))
        groups_list[1].add(NormalBricksBlock(x + 75, y + 25, 1))
        groups_list[1].add(NormalBricksBlock(x + 100, y + 25, 1))
        groups_list[1].add(NormalBricksBlock(x + 25, y + 50, 1))
        groups_list[1].add(NormalBricksBlock(x + 25, y + 75, 1))
        groups_list[1].add(NormalBricksBlock(x + 100, y + 50, 1))
        groups_list[1].add(NormalBricksBlock(x + 100, y + 75, 1))


class Spawner(GameObject):
    def __init__(self, x, y,):
        super().__init__(x, y, gi['spawn1'], 1)
        self.tick = 0
        self.image1 = gi['spawn1']
        self.image2 = gi['spawn2']
        self.image3 = gi['spawn3']
        self.image_count = -1
        self.timer = 0

    def switch_img(self):
        self.image_count = (self.image_count + 1) % 3
        if self.image_count == 0:
            self.image = self.image1
        elif self.image_count == 1:
            self.image = self.image2
        elif self.image_count == 2:
            self.image = self.image3

    def update(self, delta, handler):
        if self.timer > 0.08:
            self.switch_img()
            self.timer = 0
        if self.tick > 1.5:
            handler.groups_list[9].remove(self)
            handler.groups_list[2].add(
                Enemy(self.rect.x, self.rect.y, 2, 150, 0, 350))
        if pygame.sprite.spritecollide(self, handler.groups_list[0], False) or \
                pygame.sprite.spritecollide(self, handler.groups_list[2], False) or \
                pygame.sprite.spritecollide(self, handler.groups_list[1], False):
            self.image = gi['empty']
            if self.rect.x < mg.FIELD_WIDTH - 55:
                self.rect.x += 55
            else:
                self.rect.x -= 55
        if self in handler.groups_list[9]:
            handler.groups_list[9].remove(self)
            if pygame.sprite.spritecollide(self, handler.groups_list[9], False):
                self.image = gi['empty']
                if self.rect.x < mg.FIELD_WIDTH - 55:
                    self.rect.x += 55
                else:
                    self.rect.x -= 55
            handler.groups_list[9].add(self)
        self.tick += delta
        self.timer += delta


class Frame(GameObject):
    def __init__(self):
        super().__init__(0, 0, gi["frame"], 1)
        self.img = gi["frame"]

    def update(self, delta, handler):
        font = pygame.font.SysFont("arial", 35)
        self.image = copy.copy(self.img)
        self.image.blit(font.render("HP: {}".format(handler.groups_list[0].sprites()[0].hp), 15, (0, 0, 0)), (1125, 50))
        handler.groups_list[8] = pygame.sprite.Group([self])
        y = 40
        for i in range(handler.game_manager.to_spawn):
            x = 1100 if i % 2 == 0 else 1200
            y += 60 if i % 2 == 0 else 0
            handler.groups_list[8].add(GameObject(x, y, gi["tank"], 1))


class Button(GameObject):
    def __init__(self, x, y, image1, image2, image3, label, *args, action=None):
        super().__init__(x, y, image1, None)
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.label = label
        self.action = action
        self.clicked = False
        self.play = True
        self.sound1 = pygame.mixer.Sound('Music/button1.wav')
        self.args = args

    def update(self):
        mouse = pygame.mouse.get_pos()
        if (self.rect.x < mouse[0] <= self.rect.x + self.image.get_width()) and (self.rect.y < mouse[1] <= self.rect.y + self.image.get_height()):
            self.image = self.image2
            if self.play:
                pygame.mixer.Sound.play(self.sound1)
                self.play = False
            if pygame.mouse.get_pressed()[0] == 1:
                self.image = self.image3
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] != 1:
                if self.clicked:
                    if self.action is not None:
                        self.action(*self.args)
        else:
            self.image = self.image1
            self.play = True


class Menu:
    def __init__(self, displaysurface):
        self.buttons = pygame.sprite.Group(
            [Button(535, 250, mi["bs1"], mi["bs2"], mi["bs3"], "start", action=self.choose_mode),
             Button(535, 350, mi["be1"], mi["be2"], mi["be3"], "exit", action=sys.exit)])
        self.background = pygame.sprite.Group(GameObject(0, 0, mi["background"], 1))
        self.displaysurface = displaysurface
        self.level = None
        self.mode = None
        self.in_menu = True
        self.win_sound = pygame.mixer.Sound('Music/win.wav')
        self.lose_sound = pygame.mixer.Sound('Music/lose.wav')

    def update(self):
        self.buttons.update()
        self.background.draw(self.displaysurface)
        self.buttons.draw(self.displaysurface)

    def clear_buttons(self):
        self.buttons = pygame.sprite.Sprite([])

    def choose_mode(self):
        self.clear_buttons()
        self.buttons = pygame.sprite.Group([
            Button(535, 250, mi["bl1"], mi["bl2"], mi["bl3"], "levels", action=self.levels),
            Button(535, 350, mi["ba1"], mi["ba2"], mi["ba3"], "arcade", "level6", 0, action=self.quit)])

    def levels(self):
        self.clear_buttons()
        self.buttons = pygame.sprite.Group([
            Button(535, 125, mi["bl11"], mi["bl12"], mi["bl13"], "level1", "level1", 1, action=self.quit),
            Button(535, 225, mi["bl21"], mi["bl22"], mi["bl23"], "level2", "level2", 1, action=self.quit),
            Button(535, 325, mi["bl31"], mi["bl32"], mi["bl33"], "level3", "level3", 1, action=self.quit),
            Button(535, 425, mi["bl41"], mi["bl42"], mi["bl43"], "level4", "level4", 1, action=self.quit),
            Button(535, 525, mi["bl51"], mi["bl52"], mi["bl53"], "level5", "level5", 1, action=self.quit)])

    def quit(self, level, mode):
        self.in_menu = False
        self.level = level
        self.mode = mode

    def end_menu(self, score):
        pygame.mixer.music.stop()
        if score == -1:
            self.clear_buttons()
            pygame.mixer.Sound.play(self.win_sound)
            self.buttons = pygame.sprite.Group([
                Button(535, 400, mi["bm1"], mi["bm2"], mi["bm3"], "menu", action=self.choose_mode),
                Button(535, 500, mi["be1"], mi["be2"], mi["be3"], "menu", action=sys.exit),
                GameObject(240, 100, mi["pass"], 1)
            ])
        elif score == 0:
            self.clear_buttons()
            pygame.mixer.Sound.play(self.lose_sound)
            self.buttons = pygame.sprite.Group([
                Button(535, 400, mi["bm1"], mi["bm2"], mi["bm3"], "menu", action=self.choose_mode),
                Button(535, 500, mi["be1"], mi["be2"], mi["be3"], "menu", action=sys.exit),
                GameObject(315, 50, mi["def"], 1)
            ])

        elif score > 0:
            self.clear_buttons()
            pygame.mixer.Sound.play(self.lose_sound)
            font = pygame.font.SysFont('Comic Sans MS', 67)
            d = shelve.open('data')
            hsc = d['score']
            if score > hsc:
                d['score'] = score
                hsc = score
            sc_surface = font.render(str(score), False, (255, 102, 0))
            hsc_surface = font.render(str(hsc), False, (255, 102, 0))
            self.buttons = pygame.sprite.Group([
                Button(535, 500, mi["bm1"], mi["bm2"], mi["bm3"], "menu", action=self.choose_mode),
                Button(535, 600, mi["be1"], mi["be2"], mi["be3"], "menu", action=sys.exit),
                GameObject(315, 50, mi["def"], 1),
                GameObject(460, 280, mi["score"], 1),
                GameObject(460, 350, mi["hi_score"], 1),
                GameObject(670, 280, sc_surface, 1),
                GameObject(720, 360, hsc_surface, 1),
            ])












