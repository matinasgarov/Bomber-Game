from random import choice
from bonus import Bonus

class Explosion:
    def __init__(self, x, y, bonuses):
        self.sourceX = x
        self.sourceY = y
        self.time = 300
        self.frame = 0
        self.bonuses = bonuses
        self.sectors = set()

    def explode(self, grid, bombs, b):
        self.sectors.update(set(map(tuple, b.get_range(grid, self.bonuses))))
        bombs.remove(b)
        sectors_to_check = list(self.sectors)
        checked_sectors = []
        while sectors_to_check:
            curr_sector = sectors_to_check.pop()
            checked_sectors.append(curr_sector)
            for x in bombs:
                if x.posX == curr_sector[0] and x.posY == curr_sector[1]:
                    grid[x.posX][x.posY] = 0
                    x.bomber.bomb_limit += 1
                    bombs.remove(x)
                    self.sectors.update(set(map(tuple, x.get_range(grid, self.bonuses))))
                    sectors_to_check = [sector for sector in list(self.sectors) if sector not in checked_sectors]

    def clear_sectors(self, map, bonuses):

        for i in self.sectors:
            for bonus in bonuses:
                if (bonus.x == i[0]) and (bonus.y == i[1]):
                    bonuses.remove(bonus)

            if map[i[0]][i[1]] != 0:
                map[i[0]][i[1]] = 0
                rand_bonus = choice([0, 0, 0, 0, 0, 0, 1, 1, 2, 2])
                if rand_bonus != 0:
                    bonuses.append(Bonus(i[0], i[1], rand_bonus))

    def update(self, dt):

        self.time = self.time - dt

        if self.time < 100:
            self.frame = 2
        elif self.time < 200:
            self.frame = 1