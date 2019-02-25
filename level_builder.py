import main_game as mg
import pygame
import game_objects as go


def build_level(level_path):
    with open(level_path) as file:
        level = file.read()

    x = mg.PADDING
    y = mg.PADDING
    neutral_group = pygame.sprite.Group([])
    enemy_group = pygame.sprite.Group([])
    player_group = pygame.sprite.Group([])
    plate_group = pygame.sprite.Group([])
    bush_group = pygame.sprite.Group([])
    base_group = pygame.sprite.Group([])
    water_group = pygame.sprite.Group([])
    for ch in level:
        if ch == "X":
            neutral_group.add(go.NormalBricksBlock(x, y, 1))
            neutral_group.add(go.NormalBricksBlock(x + 25, y, 1))
            neutral_group.add(go.NormalBricksBlock(x, y + 25, 1))
            neutral_group.add(go.NormalBricksBlock(x + 25, y + 25, 1))
        elif ch == 'U':
            neutral_group.add(go.WhiteBricksBlock(x, y, 300))
        elif ch == "S":
            neutral_group.add(go.NormalBricksBlock(x + 25, y + 25, 1))
            base_group.add(go.Base(x + 50, y + 50))
            neutral_group.add(go.NormalBricksBlock(x + 50, y + 25, 1))
            neutral_group.add(go.NormalBricksBlock(x + 75, y + 25, 1))
            neutral_group.add(go.NormalBricksBlock(x + 100, y + 25, 1))
            neutral_group.add(go.NormalBricksBlock(x + 25, y + 50, 1))
            neutral_group.add(go.NormalBricksBlock(x + 25, y + 75, 1))
            neutral_group.add(go.NormalBricksBlock(x + 100, y + 50, 1))
            neutral_group.add(go.NormalBricksBlock(x + 100, y + 75, 1))

        elif ch == "B":
            bush_group.add(go.Bush(x, y))
            bush_group.add(go.Bush(x + 25, y))
            bush_group.add(go.Bush(x, y + 25))
            bush_group.add(go.Bush(x + 25, y + 25))
        elif ch == "E":
            enemy_group.add(go.Enemy(x, y, 2, 150, 0.1, 400))
        elif ch == "L":
            plate_group.add(go.Plate(x, y))
        elif ch == "W":
            water_group.add(go.Water(x, y))
        elif ch == "P":
            player_group.add(pygame.sprite.Group([go.Player(x, y, 5, 200, 1)]))
        if (x + mg.BLOCK_SIZE) > mg.FIELD_WIDTH + mg.PADDING:
            x = mg.PADDING
            y += mg.BLOCK_SIZE
        else:
            x += mg.BLOCK_SIZE

            # groups: 0-player 1-neutral, 2-enemy, 3-bullets, 4-boom 5-bushes , 6-plates, 7-base,
            # 8-gui, 9-spawner 10 - water 12-items
    return [player_group, neutral_group, enemy_group, pygame.sprite.Group([]),
            pygame.sprite.Group([]), bush_group, plate_group, base_group, pygame.sprite.Group([go.Frame()]),
            pygame.sprite.Group([]), water_group, pygame.sprite.Group([]), pygame.sprite.Group([])]

