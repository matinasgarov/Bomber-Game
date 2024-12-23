import pygame
from bomb import Bomb

class Character:
    def __init__(self, pos):
        self.life = True
        self.posX = pos[0] * 4
        self.posY = pos[1] * 4
        self.direction = 0
        self.frame = 0
        self.animation = []
        self.bomb_range = 2
        self.bomb_limit = 1

    def plant_bomb(self, map, time, bombs, bonuses):
        if self.bomb_limit > 0:
            bomb_posX = round(self.posX / 4)
            bomb_posY = round(self.posY / 4)
            # Do not plant bomb on existing bomb
            for bomb in bombs:
                if bomb.posX == bomb_posX and bomb.posY == bomb_posY:
                    return None
            # Prevent bomb being planted in front of character
            if self.direction == 0 and self.posY / (4 * bomb_posY) < 1:
                return None
            elif self.direction == 1 and self.posX / (4 * bomb_posX) < 1:
                return None
            elif self.direction == 2 and self.posY / (4 * bomb_posY) > 1:
                return None
            elif self.direction == 3 and self.posX / (4 * bomb_posX) > 1:
                return None

            bomb = Bomb(self.bomb_range, bomb_posX, bomb_posY, map, self, time, bonuses)
            self.bomb_limit -= 1
            bombs.append(bomb)
            map[bomb.posX][bomb.posY] = 3  # Mark the map grid as occupied by a bomb
            return bomb
        return None
    def check_death(self, exp):
        for e in exp:
            for s in e.sectors:
                if int(self.posX / 4) == s[0] and int(self.posY / 4) == s[1]:
                    self.life = False

    def check_bonus(self, bonuses):
        to_remove = []
        for bonus in bonuses:
            if int(self.posX/4) == bonus.x and int(self.posY/4) == bonus.y:
                if bonus.type == 1:
                    self.bomb_range += 1
                elif bonus.type == 2:
                    self.bomb_limit += 1
                to_remove.append(bonus)
        for bonus in to_remove:
            bonuses.remove(bonus)

    def load_animations(self, scale, image_path):
        front = []
        back = []
        left = []
        right = []
        resize_width = scale
        resize_height = scale

        f1 = pygame.image.load(image_path + 'f0.png')
        f2 = pygame.image.load(image_path + 'f1.png')
        f3 = pygame.image.load(image_path + 'f2.png')

        f1 = pygame.transform.scale(f1, (resize_width, resize_height))
        f2 = pygame.transform.scale(f2, (resize_width, resize_height))
        f3 = pygame.transform.scale(f3, (resize_width, resize_height))

        front.append(f1)
        front.append(f2)
        front.append(f3)

        r1 = pygame.image.load(image_path + 'r0.png')
        r2 = pygame.image.load(image_path + 'r1.png')
        r3 = pygame.image.load(image_path + 'r2.png')

        r1 = pygame.transform.scale(r1, (resize_width, resize_height))
        r2 = pygame.transform.scale(r2, (resize_width, resize_height))
        r3 = pygame.transform.scale(r3, (resize_width, resize_height))

        right.append(r1)
        right.append(r2)
        right.append(r3)

        b1 = pygame.image.load(image_path + 'b0.png')
        b2 = pygame.image.load(image_path + 'b1.png')
        b3 = pygame.image.load(image_path + 'b2.png')

        b1 = pygame.transform.scale(b1, (resize_width, resize_height))
        b2 = pygame.transform.scale(b2, (resize_width, resize_height))
        b3 = pygame.transform.scale(b3, (resize_width, resize_height))

        back.append(b1)
        back.append(b2)
        back.append(b3)

        l1 = pygame.image.load(image_path + 'l0.png')
        l2 = pygame.image.load(image_path + 'l1.png')
        l3 = pygame.image.load(image_path + 'l2.png')

        l1 = pygame.transform.scale(l1, (resize_width, resize_height))
        l2 = pygame.transform.scale(l2, (resize_width, resize_height))
        l3 = pygame.transform.scale(l3, (resize_width, resize_height))

        left.append(l1)
        left.append(l2)
        left.append(l3)

        self.animation.append(front)
        self.animation.append(right)
        self.animation.append(back)
        self.animation.append(left)