"""
Module for the Player class which represents a player in the game.
"""

import pygame
from character import Character
from controls import Controls
import math

class Player(Character):
    """
    Represents a player in the game.

    Attributes:
        controls (dict): The controls for the player.
        name (str): The name of the player.
        moving (bool): Whether the player is moving.
    """

    def __init__(self, pos, controls, name):
        """
        Initializes a Player object.

        Args:
            pos (tuple): The initial position of the player.
            controls (dict): The controls for the player.
            name (str): The name of the player.
        """
        super().__init__(pos)
        self.controls = controls
        self.name = name
        self.moving = False

    def stop(self):
        """
        Stops the player's movement.
        """
        self.moving = False

    def change_direction(self, direction):
        """
        Changes the player's direction.

        Args:
            direction (int): The new direction.
        """
        self.direction = direction
        self.frame = 0
        self.moving = True

    def step(self, new_direction, grid, ene_blocks):
        """
        Moves the player one step in the new direction.

        Args:
            new_direction (int): The new direction.
            grid (list): The game grid.
            ene_blocks (list): The list of enemy blocks.
        """
        if new_direction != self.direction:
            self.change_direction(new_direction)
        if self.direction == 0:
            self.move(0, 1, grid, ene_blocks)
            self.next_frame()
        elif self.direction == 1:
            self.move(1, 0, grid, ene_blocks)
            self.next_frame()
        elif self.direction == 2:
            self.move(0, -1, grid, ene_blocks)
            self.next_frame()
        elif self.direction == 3:
            self.move(-1, 0, grid, ene_blocks)
            self.next_frame()

    def move(self, dx, dy, grid, enemys):
        """
        Moves the player in the specified direction.

        Args:
            dx (int): The x-direction.
            dy (int): The y-direction.
            grid (list): The game grid.
            enemys (list): The list of enemies.
        """
        tempx = int(self.posX / 4)
        tempy = int(self.posY / 4)

        map = [[cell for cell in row] for row in grid]

        for x in enemys:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                map[int(x.posX / 4)][int(x.posY / 4)] = 2

        if self.posX % 4 != 0 and dx == 0:
            if self.posX % 4 == 1:
                self.posX -= 1
            elif self.posX % 4 == 3:
                self.posX += 1
            return
        if self.posY % 4 != 0 and dy == 0:
            if self.posY % 4 == 1:
                self.posY -= 1
            elif self.posY % 4 == 3:
                self.posY += 1
            return

        # right
        if dx == 1:
            if map[tempx + 1][tempy] in [0, 4]:
                self.posX += 1
        # left
        elif dx == -1:
            tempx = math.ceil(self.posX / 4)
            if map[tempx - 1][tempy] in [0, 4]:
                self.posX -= 1

        # bottom
        if dy == 1:
            if map[tempx][tempy + 1] in [0, 4]:
                self.posY += 1
        # top
        elif dy == -1:
            tempy = math.ceil(self.posY / 4)
            if map[tempx][tempy - 1] in [0, 4]:
                self.posY -= 1

    def load_animations(self, scale, secondPlayer):
        """
        Loads the player's animations.

        Args:
            scale (int): The scale of the animations.
            secondPlayer (bool): Whether this is the second player.
        """
        image_path = "images/hero/p"
        if secondPlayer:
            image_path += "2/p"
        else:
            image_path += "1/p"

        super().load_animations(scale, image_path)

    def next_frame(self):
        """
        Advances to the next frame in the animation.
        """
        if self.frame == 2:
            self.frame = 0
        else:
            self.frame += 1
