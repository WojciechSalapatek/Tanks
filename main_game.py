import pygame, os
import game_objects as go
import random
import level_builder as lb
import pygame.locals

class GameManager:
    def __init__(self, to_spawn, mode):
        self.mode = mode
        self.to_spawn = to_spawn
        self.spawn1 = (10, 10)
        self.spawn2 = (1019, 10)
        self.spawn3 = (515, 10)
        self.status = 1
        self.score = 0

    def spawn(self, groups_list):
        spawn_point = None
        choice = random.randint(0, 2)
        if not choice:
            spawn_point = self.spawn1
        elif choice == 1:
            spawn_point = self.spawn2
        elif choice == 2:
            spawn_point = self.spawn3

        groups_list[9].add(go.Spawner(spawn_point[0], spawn_point[1]))

    def update(self, groups_list):
        if len(groups_list[2]) + len(groups_list[9]) < 3 and self.to_spawn > 0:
            self.spawn(groups_list)
            if self.mode:
                self.to_spawn -= 1
            else:
                self.score += 100
        self.status = 1 if groups_list[0].sprites()[0].hp > 0 else (0 if self.mode else self.score)
        if self.mode and not self.to_spawn and len(groups_list[2]) + len(groups_list[9]) == 0:
            self.status = -1


class GameHandler:
    # groups: 0-player 1-neutral, 2-enemy, 3-bullets, 4-boom 5-bushes , 6-plates, 7-base,
    # 8-gui, 9-spawner 10 - water 12-items
    def __init__(self, displaysurface, game_manager, groups_list=None):
        self.displaysurface = displaysurface
        self.gameover = False
        self.game_manager = game_manager
        if groups_list is None:
            for _ in range(13):
                self.groups_list.append(pygame.sprite.Group([]))
        else:
            self.groups_list = groups_list

    def update(self, delta):
        for group in self.groups_list:
            group.update(delta, self)
        self.game_manager.update(self.groups_list)

    def render(self, displaysurface):
        self.groups_list[6].draw(displaysurface)
        self.groups_list[12].draw(displaysurface)
        for i in range(0, 13):
            if i != 6 and i != 12:
                self.groups_list[i].draw(displaysurface)

    def add_bullet(self, bullet):
        self.groups_list[3].add(bullet)


FPS = 60
BLOCK_SIZE = 50
WIDTH = 1280
HEIGHT = 720
FIELD_WIDTH = 1050
FIELD_HEIGHT = 700
PADDING = 10
DISPLAYSURFACE = pygame.display.set_mode((WIDTH, HEIGHT))


def main(score=None):
    menu = go.Menu(DISPLAYSURFACE)
    if score is not None:
        menu.end_menu(score)
    while menu.in_menu:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                os.sys.exit()
        menu.update()
        pygame.display.update()
    status = play(menu.level, menu.mode)
    main(score=status)


def play(level, mode):
    playing = 1
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Tanki!')
    game_manager = GameManager(10, mode)
    game_handler = GameHandler(DISPLAYSURFACE, game_manager, lb.build_level('levels/{}.lvl'.format(level)))
    last_time = 0
    passed = 0
    frames = 0

    while playing == 1:
        frames += 1
        DISPLAYSURFACE.fill((0, 0, 0))
        game_handler.render(DISPLAYSURFACE)
        t = pygame.time.get_ticks()
        delta = (t - last_time) / 1000.0
        last_time = t
        game_handler.update(delta)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                os.sys.exit()
        playing = game_manager.status
        pygame.display.update()
        clock.tick(FPS)
        passed += delta
        if passed > 1:
            passed = 0
            print(frames)
            frames = 0
    return playing


if __name__ == "__main__":
    pygame.mixer.pre_init(34100, -16, 1, 1024)
    pygame.mixer.init()
    pygame.mixer.music.load('Music/button1.wav')
    main()
