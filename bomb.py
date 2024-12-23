"""
Module for the Bomb class which handles bomb behavior and explosions.
"""

class Bomb:
    """
    Represents a bomb in the game.

    Attributes:
        range (int): The range of the bomb explosion.
        posX (int): The x-coordinate of the bomb.
        posY (int): The y-coordinate of the bomb.
        time (int): The time before the bomb explodes.
        bomber (Character): The character who planted the bomb.
        frame (int): The current frame of the bomb animation.
    """

    def __init__(self, r, x, y, map, bomber, time, bonuses):
        """
        Initializes a Bomb object.

        Args:
            r (int): The range of the bomb explosion.
            x (int): The x-coordinate of the bomb.
            y (int): The y-coordinate of the bomb.
            map (list): The game map.
            bomber (Character): The character who planted the bomb.
            time (int): The time before the bomb explodes.
            bonuses (list): The list of bonuses.
        """
        self.range = r
        self.posX = x
        self.posY = y
        self.time = time
        self.bomber = bomber
        self.frame = 0

    def update(self, dt):
        """
        Updates the bomb timer and frame.

        Args:
            dt (int): The delta time since the last update.
        """
        self.time = self.time - dt

        if self.time < 1000:
            self.frame = 2
        elif self.time < 2000:
            self.frame = 1

    def has_bonus(self, x, y, bonuses):
        """
        Checks if there is a bonus at the specified position.

        Args:
            x (int): The x-coordinate to check.
            y (int): The y-coordinate to check.
            bonuses (list): The list of bonuses.

        Returns:
            bool: True if there is a bonus at the position, False otherwise.
        """
        for bonus in bonuses:
            if (bonus.x == x) and (bonus.y == y):
                return True
        return False

    def get_range(self, map, bonuses):
        """
        Gets the explosion range of the bomb.

        Args:
            map (list): The game map.
            bonuses (list): The list of bonuses.

        Returns:
            list: The list of sectors affected by the explosion.
        """
        sectors = [[self.posX, self.posY]]
        max_x, max_y = len(map), len(map[0])

        for x in range(1, self.range):
            if self.posX + x >= max_x or map[self.posX + x][self.posY] == 1:
                break
            elif self.has_bonus(self.posX + x, self.posY, bonuses):
                sectors.append([self.posX + x, self.posY])
                break
            elif map[self.posX + x][self.posY] in [0, 3]:
                sectors.append([self.posX + x, self.posY])
            elif map[self.posX + x][self.posY] == 2:
                sectors.append([self.posX + x, self.posY])
                break

        for x in range(1, self.range):
            if self.posX - x < 0 or map[self.posX - x][self.posY] == 1:
                break
            elif self.has_bonus(self.posX - x, self.posY, bonuses):
                sectors.append([self.posX - x, self.posY])
                break
            elif map[self.posX - x][self.posY] in [0, 3]:
                sectors.append([self.posX - x, self.posY])
            elif map[self.posX - x][self.posY] == 2:
                sectors.append([self.posX - x, self.posY])
                break

        for y in range(1, self.range):
            if self.posY + y >= max_y or map[self.posX][self.posY + y] == 1:
                break
            elif self.has_bonus(self.posX, self.posY + y, bonuses):
                sectors.append([self.posX, self.posY + y])
                break
            elif map[self.posX][self.posY + y] in [0, 3]:
                sectors.append([self.posX, self.posY + y])
            elif map[self.posX][self.posY + y] == 2:
                sectors.append([self.posX, self.posY + y])
                break

        for y in range(1, self.range):
            if self.posY - y < 0 or map[self.posX][self.posY - y] == 1:
                break
            elif self.has_bonus(self.posX, self.posY - y, bonuses):
                sectors.append([self.posX, self.posY - y])
                break
            elif map[self.posX][self.posY - y] in [0, 3]:
                sectors.append([self.posX, self.posY - y])
            elif map[self.posX][self.posY - y] == 2:
                sectors.append([self.posX, self.posY - y])
                break

        return sectors

    def explode(self, map, bombs):
        """
        Explodes the bomb, affecting the map and clearing sectors.

        Args:
            map (list): The game map.
            bombs (list): The list of bombs.
        """
        for sector in self.get_range(map, bombs):
            map[sector[0]][sector[1]] = 0  # clear the sector
        self.time = 0
