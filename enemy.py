import pygame
import random
from node import Node
from algorithm import Algorithm
from character import Character

class Enemy(Character):

    dire = [[1, 0, 1], [0, 1, 0], [-1, 0, 3], [0, -1, 2]]

    def __init__(self, pos, alg):
        Character.__init__(self, pos)
        self.path = []
        self.movement_path = []
        self.plant = False
        self.algorithm = alg

    def move(self, map, bombs, explosions, enemy, powerUp):
        if self.direction == 0:
            self.posY += 1
        elif self.direction == 1:
            self.posX += 1
        elif self.direction == 2:
            self.posY -= 1
        elif self.direction == 3:
            self.posX -= 1

        if self.posX % 4 == 0 and self.posY % 4 == 0:
            self.movement_path.pop(0)
            self.path.pop(0)
            if len(self.path) > 1:
                grid = self.create_grid(map, bombs, explosions, enemy, powerUp)
                next = self.path[1]
                if grid[next[0]][next[1]] > 1:
                    self.movement_path.clear()
                    self.path.clear()

        if self.frame == 2:
            self.frame = 0
        else:
            self.frame += 1

    def make_move(self, map, bombs, explosions, enemy, bomb_time, powerUp):

        if not self.life:
            return
        if len(self.movement_path) == 0:
            if self.plant:
                bomb_planted = self.plant_bomb(map, bomb_time, bombs, powerUp)
                if bomb_planted:
                    self.plant = False
            if self.algorithm is Algorithm.DFS:
                self.dfs(self.create_grid(map, bombs, explosions, enemy, powerUp))
            else:
                self.dijkstra(self.create_grid_dijkstra(map, bombs, explosions, enemy, powerUp))

        else:
            self.direction = self.movement_path[0]
            self.move(map, bombs, explosions, enemy, powerUp)

    def dfs(self, grid):

        new_path = [[int(self.posX / 4), int(self.posY / 4)]]
        depth = 0
        if self.bomb_limit == 0:
            self.dfs_rec(grid, 0, new_path, depth)
        else:
            self.dfs_rec(grid, 2, new_path, depth)

        self.path = new_path

    def dfs_rec(self, grid, end, path, depth):
            last = path[-1]
            if depth > 200:
                return
            if grid[last[0]][last[1]] == 0 and end == 0:
                return
            elif end == 2:
                if (last[0] + 1 < len(grid) and grid[last[0] + 1][last[1]] == end) or \
                (last[0] - 1 >= 0 and grid[last[0] - 1][last[1]] == end) or \
                (last[1] + 1 < len(grid[0]) and grid[last[0]][last[1] + 1] == end) or \
                (last[1] - 1 >= 0 and grid[last[0]][last[1] - 1] == end):
                    if len(path) == 1 and end == 2:
                        self.plant = True
                    return

            grid[last[0]][last[1]] = 9

            random.shuffle(self.dire)

            # safe
            for direction in self.dire:
                nx, ny = last[0] + direction[0], last[1] + direction[1]
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
                    path.append([nx, ny])
                    self.movement_path.append(direction[2])
                    self.dfs_rec(grid, end, path, depth + 1)
                    return

            # unsafe
            for direction in self.dire:
                nx, ny = last[0] + direction[0], last[1] + direction[1]
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 1:
                    path.append([nx, ny])
                    self.movement_path.append(direction[2])
                    self.dfs_rec(grid, end, path, depth + 1)
                    return

            if len(self.movement_path) > 0:
                path.pop()
                self.movement_path.pop()

            self.dfs_rec(grid, end, path, depth + 1)

    def dijkstra(self, grid):

        end = 1
        if self.bomb_limit == 0:
            end = 0

        visited = []
        open_list = []
        current = grid[int(self.posX / 4)][int(self.posY / 4)]
        current.weight = current.base_weight
        new_path = []
        while True:
            visited.append(current)
            random.shuffle(self.dire)
            if (current.value == end and end == 0) or\
                    (end == 1 and (grid[current.x+1][current.y].value == 1 or grid[current.x-1][current.y].value == 1 or
                grid[current.x][current.y+1].value == 1 or grid[current.x][current.y-1].value == 1)):
                new_path.append([current.x, current.y])
                while True:
                    if current.parent is None:
                        break
                    current = current.parent
                    new_path.append([current.x, current.y])
                new_path.reverse()
                for xd in range(len(new_path)):
                    if new_path[xd] is not new_path[-1]:
                        if new_path[xd][0] - new_path[xd+1][0] == -1:
                            self.movement_path.append(1)
                        elif new_path[xd][0] - new_path[xd + 1][0] == 1:
                            self.movement_path.append(3)
                        elif new_path[xd][1] - new_path[xd + 1][1] == -1:
                            self.movement_path.append(0)
                        elif new_path[xd][1] - new_path[xd + 1][1] == 1:
                            self.movement_path.append(2)
                if len(new_path) == 1 and end == 1:
                    self.plant = True
                self.path = new_path
                return

            for i in range(len(self.dire)):
                if current.x + self.dire[i][0] < len(grid) and current.y + self.dire[i][1] < len(grid):
                    if grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].reach \
                            and grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]] not in visited:
                        if grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]] in open_list:
                            if grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].weight >\
                                    grid[current.x][current.y].weight \
                                    + grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].base_weight:
                                grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].parent = current
                                grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].weight = current.weight + grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].base_weight
                                grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].direction = self.dire[i][2]

                        else:
                            grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].parent = current
                            grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].weight =\
                                current.weight + grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].base_weight
                            grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].direction = self.dire[i][2]
                            open_list.append(grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]])

            if len(open_list) == 0:
                self.path = [[int(self.posX / 4), int(self.posY / 4)]]
                return

            next_node = open_list[0]
            for n in open_list:
                if n.weight < next_node.weight:
                    next_node = n
            open_list.remove(next_node)
            current = next_node


    def create_grid(self, map, bombs, explosions, enemys, powerUp):
        grid = [[0] * len(map) for r in range(len(map))]

        # 0 - safe
        # 1 - unsafe
        # 2 - destryable
        # 3 - unreachable

        for b in bombs:
            for x in b.get_range(map, powerUp):
                grid[x[0]][x[1]] = 1
            grid[b.posX][b.posY] = 3

        for e in explosions:
            for s in e.sectors:
                grid[s[0]][s[1]] = 3

        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 1:
                    grid[i][j] = 3
                elif map[i][j] == 2:
                    grid[i][j] = 2

        for x in enemys:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                grid[int(x.posX / 4)][int(x.posY / 4)] = 2

        return grid

    def create_grid_dijkstra(self, map, bombs, explosions, enemys, powerUp):
        grid = [[None] * len(map) for r in range(len(map))]

        # 0 - safe
        # 1 - destroyable
        # 2 - unreachable
        # 3 - unsafe
        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == 0:
                    grid[i][j] = Node(i, j, True, 2, 0)
                elif map[i][j] == 2:
                    grid[i][j] = Node(i, j, False, 999, 1)
                elif map[i][j] == 1:
                    grid[i][j] = Node(i, j, False, 999, 2)
                elif map[i][j] == 3:
                    grid[i][j] = Node(i, j, False, 999, 2)

        for b in bombs:
            for x in b.get_range(map, powerUp):
                grid[x[0]][x[1]].weight = 5
                grid[x[0]][x[1]].value = 3
            grid[b.posX][b.posY].reach = False

        for e in explosions:
            for s in e.sectors:
                grid[s[0]][s[1]].reach = False
            
        for bonus in powerUp:
            grid[bonus.x][bonus.y].weight = 1

        for x in enemys:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                grid[int(x.posX / 4)][int(x.posY / 4)].reach = False
                grid[int(x.posX / 4)][int(x.posY / 4)].value = 1
        return grid

    def load_animations(self, en, scale):

        image_path = f'images/enemy/e{en}'
        if en == 0:
            image_path = 'images/hero/p1/p'

        Character.load_animations(self, scale, image_path)
        

        

