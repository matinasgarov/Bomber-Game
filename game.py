"""
Module for the Game class which handles the main game logic and states.
"""

import sys
import random
import time
import copy
import pygame.font
import pygame
import cfg
from player import Player
from explosion import Explosion
from enemy import Enemy
from algorithm import Algorithm

class Game:
    """
    Represents the game.

    Attributes:
        surf (pygame.Surface): The game surface.
        show_path (bool): Whether to show the path.
        clock (pygame.time.Clock): The game clock.
        player_controls (list): The list of player controls.
        players (list): The list of players.
        enemy_list (list): The list of enemies.
        ene_blocks (list): The list of enemy blocks.
        bombs (list): The list of bombs.
        explosions (list): The list of explosions.
        bonuses (list): The list of bonuses.
        grid (list): The game grid.
        terrain_images (list): The list of terrain images.
        bomb_images (list): The list of bomb images.
        explosion_images (list): The list of explosion images.
        bonus_images (list): The list of bonus images.
        joysticks (list): The list of joysticks.
    """

    def __init__(self):
        """
        Initializes the Game object.
        """
        self.surf = None
        self.show_path = True
        self.clock = None
        self.player_controls = []
        self.players = []
        self.enemy_list = []
        self.ene_blocks = []
        self.bombs = []
        self.explosions = []
        self.bonuses = []
        self.grid = copy.deepcopy(cfg.GRID)
        self.terrain_images = []
        self.bomb_images = []
        self.explosion_images = []
        self.bonus_images = []
        self.joysticks = []

        pygame.font.init()
        self.font = pygame.font.SysFont(cfg.FONT_TYPE, cfg.FONT_SIZE)
        self.text_lose = self.font.render(cfg.TEXT_LOSE, False, (0, 0, 0))
        self.text_win = self.font.render(cfg.TEXT_WIN, False, (0, 0, 0))

    def game_init(self, path, players_alg, scale, controls, terrain_type):
        """
        Initializes the game.

        Args:
            path (bool): Whether to show the path.
            players_alg (list): The list of player algorithms.
            scale (int): The scale of the game.
            controls (list): The list of player controls.
            terrain_type (str): The type of terrain.
        """
        self.player_controls = controls
        self.grid = copy.deepcopy(cfg.GRID)
        cfg.TILE_SIZE = scale
        self.font = pygame.font.SysFont('Bebas', scale)
        self.show_path = path
        self.surf = pygame.display.set_mode((13 * cfg.TILE_SIZE, 13 * cfg.TILE_SIZE))
        pygame.display.set_caption('Bomberman')
        self.clock = pygame.time.Clock()
        self.game_speed = cfg.GAME_SPEED
        self.bomb_time = cfg.BOMB_TIME * cfg.GAME_SPEED / self.game_speed

        self.enemy_list = []
        self.ene_blocks = []
        self.bombs.clear()
        self.explosions.clear()
        self.bonuses.clear()

        player_pos = [[1, 1], [11, 11], [1, 11], [11, 1]]

        for i, alg in enumerate(players_alg):
            if alg is Algorithm.PLAYER:
                self.players.append(Player(player_pos[i], self.player_controls[i], f"Player {i + 1}"))
                self.players[-1].load_animations(scale, (len(self.players) > 0))
                self.ene_blocks.append(self.players[-1])
            elif alg is not Algorithm.NONE:
                en1 = Enemy(player_pos[i], alg)
                en1.load_animations(i, scale)
                self.enemy_list.append(en1)
                self.ene_blocks.append(en1)

        terrain_image_path = f'images/terrain/{terrain_type}.png'
        self.grass_img = pygame.image.load(terrain_image_path)
        self.grass_img = pygame.transform.scale(self.grass_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))

        self.block_img = pygame.image.load('images/terrain/block.png')
        self.block_img = pygame.transform.scale(self.block_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.box_img = pygame.image.load('images/terrain/box.png')
        self.box_img = pygame.transform.scale(self.box_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.bonus_fire_img = pygame.image.load('images/power_up/fire.png')
        self.bonus_fire_img = pygame.transform.scale(self.bonus_fire_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.bonus_bomb_img = pygame.image.load('images/power_up/bomb.png')
        self.bonus_bomb_img = pygame.transform.scale(self.bonus_bomb_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.bomb1_img = pygame.image.load('images/bomb/1.png')
        self.bomb1_img = pygame.transform.scale(self.bomb1_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.bomb2_img = pygame.image.load('images/bomb/2.png')
        self.bomb2_img = pygame.transform.scale(self.bomb2_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.bomb3_img = pygame.image.load('images/bomb/3.png')
        self.bomb3_img = pygame.transform.scale(self.bomb3_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.explosion1_img = pygame.image.load('images/explosion/1.png')
        self.explosion1_img = pygame.transform.scale(self.explosion1_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.explosion2_img = pygame.image.load('images/explosion/2.png')
        self.explosion2_img = pygame.transform.scale(self.explosion2_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.explosion3_img = pygame.image.load('images/explosion/3.png')
        self.explosion3_img = pygame.transform.scale(self.explosion3_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.terrain_images = [self.grass_img, self.block_img, self.box_img, self.grass_img]
        self.bomb_images = [self.bomb1_img, self.bomb2_img, self.bomb3_img]
        self.explosion_images = [self.explosion1_img, self.explosion2_img, self.explosion3_img]
        self.bonus_images = [self.bonus_fire_img, self.bonus_bomb_img]
        self.terrain_images = [self.grass_img, self.block_img, self.box_img, self.grass_img]
        self.main()

    def draw(self):
        """
        Draws the game elements on the surface.
        """
        self.surf.fill(cfg.GAME_BACKGROUND)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.surf.blit(self.terrain_images[self.grid[i][j]], (i * cfg.TILE_SIZE, j * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE))

        for x in self.bombs:
            self.surf.blit(self.bomb_images[x.frame], (x.posX * cfg.TILE_SIZE, x.posY * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE))

        for y in self.explosions:
            for x in y.sectors:
                self.surf.blit(self.explosion_images[y.frame], (x[0] * cfg.TILE_SIZE, x[1] * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE))

        for bonus in self.bonuses:
            self.surf.blit(self.bonus_images[bonus.type - 1], (bonus.x * cfg.TILE_SIZE, bonus.y * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE))

        for player in self.players:
            if player.life:
                self.surf.blit(player.animation[player.direction][player.frame],
                               (player.posX * (cfg.TILE_SIZE / 4), player.posY * (cfg.TILE_SIZE / 4), cfg.TILE_SIZE, cfg.TILE_SIZE))
        for en in self.enemy_list:
            if en.life:
                self.surf.blit(en.animation[en.direction][en.frame],
                               (en.posX * (cfg.TILE_SIZE / 4), en.posY * (cfg.TILE_SIZE / 4), cfg.TILE_SIZE, cfg.TILE_SIZE))
                if self.show_path:
                    if en.algorithm == Algorithm.DFS:
                        for sek in en.path:
                            pygame.draw.rect(self.surf, (255, 0, 0, 240), [sek[0] * cfg.TILE_SIZE, sek[1] * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE], 1)
                    else:
                        for sek in en.path:
                            pygame.draw.rect(self.surf, (255, 0, 255, 240), [sek[0] * cfg.TILE_SIZE, sek[1] * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE], 1)

        pygame.display.update()

    def generate_map(self):
        """
        Generates the game map with destructible boxes.
        """
        for i in range(1, len(self.grid) - 1):
            for j in range(1, len(self.grid[i]) - 1):
                if self.grid[i][j] != 0:
                    continue
                elif (i < 3 or i > len(self.grid) - 4) and (j < 3 or j > len(self.grid[i]) - 4):
                    continue
                if random.randint(0, 9) < 7:
                    self.grid[i][j] = 2

    def game_end_check(self):
        """
        Checks if the game should end.

        Returns:
            bool: True if the game should end, False otherwise.
        """
        num_alive = 0
        for player in self.players:
            if player.life:
                num_alive += 1

        if num_alive == 0:
            self.game_speed = cfg.GAME_SPEED_AI_ONLY
            self.bomb_time = cfg.BOMB_TIME * cfg.GAME_SPEED / self.game_speed

        for enemy in self.enemy_list:
            if enemy.life:
                num_alive += 1

        if num_alive > 1:
            return False
        return True

    def changeDirIfDifferent(self, direction, player):
        """
        Changes the direction of the player if it is different from the current direction.

        Args:
            direction (int): The new direction.
            player (Player): The player object.
        """
        if direction != player.direction:
            player.change_direction(direction)

    def main(self):
        """
        The main game loop.
        """
        self.generate_map()
        end_game = False
        while not self.game_end_check() and not end_game:
            dt = self.clock.tick(self.game_speed)
            for en in self.enemy_list:
                en.make_move(self.grid, self.bombs, self.explosions, self.ene_blocks, self.bomb_time, self.bonuses)

            keys = pygame.key.get_pressed()
            events = pygame.event.get()

            for player in self.players:
                if not player.life:
                    continue
                if not isinstance(player.controls, pygame.joystick.JoystickType):
                    if keys[player.controls.down]:  # moving down
                        player.step(0, self.grid, self.ene_blocks)
                    elif keys[player.controls.right]:  # moving right
                        player.step(1, self.grid, self.ene_blocks)
                    elif keys[player.controls.up]:  # moving up
                        player.step(2, self.grid, self.ene_blocks)
                    elif keys[player.controls.left]:  # moving left
                        player.step(3, self.grid, self.ene_blocks)
                    if keys[player.controls.bomb]:  # planting bomb
                        player.plant_bomb(self.grid, self.bomb_time, self.bombs, self.bonuses)
                else:
                    joy_id = player.controls.get_id()
                    joystick_state = self.joysticks[joy_id]

                    axis0 = joystick_state.axes[0]
                    axis1 = joystick_state.axes[1]

                    if axis0 < 0:
                        player.step(3, self.grid, self.ene_blocks)
                    elif axis0 > 0:
                        player.step(1, self.grid, self.ene_blocks)
                    elif axis1 < 0:
                        player.step(2, self.grid, self.ene_blocks)
                    elif axis1 > 0:
                        player.step(0, self.grid, self.ene_blocks)

                    if joystick_state.buttons[2]:
                        player.plant_bomb(self.grid, self.bomb_time, self.bombs, self.bonuses)

            self.draw()
            for e in events:
                if e.type == pygame.QUIT:
                    sys.exit(0)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        end_game = self.pause()

            self.update_bombs(dt)
        self.game_over()

    def update_bombs(self, dt):
        """
        Updates the state of all bombs in the game.

        Args:
            dt (int): The delta time since the last update.
        """
        for b in self.bombs:
            b.update(dt)
            if b.time < 1:
                b.bomber.bomb_limit += 1
                self.grid[b.posX][b.posY] = 0
                exp_temp = Explosion(b.posX, b.posY, self.bonuses)
                exp_temp.explode(self.grid, self.bombs, b)
                exp_temp.clear_sectors(self.grid, self.bonuses)
                self.explosions.append(exp_temp)
        for player in self.players:
            if player not in self.enemy_list:
                player.check_death(self.explosions)
                player.check_bonus(self.bonuses)
        for en in self.enemy_list:
            en.check_death(self.explosions)
            en.check_bonus(self.bonuses)
        for e in self.explosions:
            e.update(dt)
            if e.time < 1:
                self.explosions.remove(e)

    def game_over(self):
        """
        Handles the game over state.
        """
        while True:
            dt = self.clock.tick(15)
            self.update_bombs(dt)
            count = 0
            winner = ""

            print("Starting game over loop. Initial conditions:")
            print(f"Enemy list: {len(self.enemy_list)}, Players: {len(self.players)}")

            # Correctly access posX and posY attributes for enemy position
            for en in self.enemy_list:
                print(f"Enemy {en} life: {en.life}, position: ({en.posX}, {en.posY})")
                en.make_move(self.grid, self.bombs, self.explosions, self.ene_blocks, self.bomb_time, self.bonuses)
                if en.life:
                    count += 1
                    winner = en.algorithm.name if hasattr(en.algorithm, 'name') else "Enemy"

            for player in self.players:
                print(f"Player {player.name} life: {player.life}, position: ({player.posX}, {player.posY})")
                if player.life:
                    count += 1
                    winner = player.name

            print(f"Total count: {count}, Current winner: {winner}")

            if count > 1:
                print("Game ended prematurely")
                self.draw()
                textsurface = self.font.render("Game ended prematurely", False, (0, 0, 0))
                font_w = textsurface.get_width()
                font_h = textsurface.get_height()
                self.surf.blit(textsurface, (self.surf.get_width() // 2 - font_w // 2, self.surf.get_height() // 2 - font_h // 2))
                pygame.display.update()
                time.sleep(2)
                break

            if count == 1:
                print(f"Winner is {winner}")
                self.surf.fill(cfg.PAUSE_BACKGROUND_COLOR)
                textsurface = self.font.render(winner + " wins", False, (255, 255, 255))
                gameOverRect = textsurface.get_rect(center=(self.surf.get_width() // 2, self.surf.get_height() // 3))
                self.surf.blit(textsurface, gameOverRect)
                pygame.display.update()
                time.sleep(2)
                break

            if count == 0:
                print("Game resulted in a draw")
                self.draw()
                textsurface = self.font.render("Draw", False, (0, 0, 0))
                font_w = textsurface.get_width()
                font_h = textsurface.get_height()
                self.surf.blit(textsurface, (self.surf.get_width() // 2 - font_w // 2, self.surf.get_height() // 2 - font_h // 2))
                pygame.display.update()
                time.sleep(2)
                break

            self.draw()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)

        self.explosions.clear()
        self.enemy_list.clear()
        self.ene_blocks.clear()
        self.players.clear()
        self.bombs.clear()

    def pause(self):
        """
        Pauses the game.

        Returns:
            bool: False when the game is resumed.
        """
        pause_font_size = int(cfg.FONT_SIZE_LARGE * 0.6)
        button_font_size = int(cfg.FONT_SIZE * 0.6)
        pause_font = pygame.font.SysFont(cfg.FONT_TYPE, pause_font_size)
        button_font = pygame.font.SysFont(cfg.FONT_TYPE, button_font_size)

        pause_text = pause_font.render('PAUSED', True, cfg.TEXT_COLOR)
        continue_text = button_font.render('CONTINUE (PRESS C)', True, cfg.TEXT_COLOR)
        quit_text = button_font.render('QUIT (PRESS Q)', True, cfg.TEXT_COLOR)

        # Center text on screen
        pause_rect = pause_text.get_rect(center=(self.surf.get_width() // 2, self.surf.get_height() // 3))
        continue_rect = continue_text.get_rect(center=(self.surf.get_width() // 2, self.surf.get_height() // 2))
        quit_rect = quit_text.get_rect(center=(self.surf.get_width() // 2, self.surf.get_height() // 2 + button_font_size + 20))

        paused = True
        while paused:
            # Draw the pause screen
            self.surf.fill(cfg.PAUSE_BACKGROUND_COLOR)
            self.surf.blit(pause_text, pause_rect)
            self.surf.blit(continue_text, continue_rect)
            self.surf.blit(quit_text, quit_rect)

            pygame.display.flip()

            # Event handling
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_c:
                        paused = False
                    elif e.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            self.clock.tick(cfg.FPS)  # Using the FPS from cfg

        self.draw()  # Redraw the game screen when unpaused
