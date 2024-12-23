import sys
import pygame
import pygame_menu
import cfg
from game import Game
from algorithm import Algorithm
from controls import Controls

class Menu:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.show_path = False
        self.game = Game()
        self.surface = pygame.display.set_mode(cfg.WINDOW_SIZE)
        self.players_alg = [Algorithm.PLAYER, Algorithm.PLAYER, Algorithm.DIJKSTRA, Algorithm.DFS]

        # Controllers initialization
        self.control_list_select1 = [("Key1", 0)]
        self.control_list_select2 = [("Key2", 1)]
        pygame.joystick.init()
        self.num_of_gamepads = pygame.joystick.get_count()
        self.controllers = [
            Controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL),
            Controls(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LCTRL)
        ]
        for i in range(self.num_of_gamepads):
            gamepad = pygame.joystick.Joystick(i)
            gamepad.init()
            self.controllers.append(gamepad)
            if i % 2 == 0:
                self.control_list_select1.append((f"Joy{i+1}", i+2))
            else:
                self.control_list_select2.append((f"Joy{i+1}", i+2))

        self.player_controls = [
            self.controllers[0],
            self.controllers[1]
        ]

    def change_controls_player(self, value, control_num, player_num):
        self.player_controls[player_num] = self.controllers[control_num]

    def change_controls_player1(self, value, control_num):
        self.change_controls_player(value, control_num, 0)

    def change_controls_player2(self, value, control_num):
        self.change_controls_player(value, control_num, 1)

    def change_path(self, value, c):
        self.show_path = c

    def change_player(self, value, c, player_num):
        self.players_alg[player_num] = c

    def run_game(self, terrain_type='grass'):
        print(f"Starting game with {terrain_type} terrain.")
        self.game.game_init(self.show_path, self.players_alg, cfg.TILE_SIZE, self.player_controls, terrain_type)

       
    def main_background(self):
        self.surface.fill(cfg.COLOR_BACKGROUND)

    def map_selection_menu(self):
        map_selection_theme = pygame_menu.themes.Theme(
            selection_color=cfg.COLOR_WHITE,
            widget_font=pygame_menu.font.FONT_BEBAS,
            title_font_size=int(cfg.TILE_SIZE*0.8),
            title_font_color=cfg.COLOR_WHITE,
            title_font=pygame_menu.font.FONT_BEBAS,
            widget_font_color=cfg.COLOR_WHITE,
            widget_font_size=int(cfg.TILE_SIZE*0.7),
            background_color=cfg.MENU_BACKGROUND_COLOR,
            title_background_color=cfg.MENU_TITLE_COLOR,
        )
        map_menu = pygame_menu.Menu('Select Map', 512, 512, theme=map_selection_theme)
        map_menu.add.button('Grass Map', lambda: self.run_game('grass'))
        map_menu.add.button('Snow Map', lambda: self.run_game('snow'))
        map_menu.add.button('Desert Map', lambda: self.run_game('desert'))
        map_menu.add.button('Back', pygame_menu.events.BACK)
        return map_menu

    def menu_loop(self):
        pygame.init()
        pygame.display.set_caption('Bomberman')
        menu_theme = pygame_menu.themes.Theme(
            selection_color=cfg.COLOR_WHITE,
            widget_font=pygame_menu.font.FONT_BEBAS,
            title_font_size=int(cfg.TILE_SIZE*0.8),
            title_font_color=cfg.COLOR_WHITE,
            title_font=pygame_menu.font.FONT_BEBAS,
            widget_font_color=cfg.COLOR_WHITE,
            widget_font_size=int(cfg.TILE_SIZE*0.7),
            background_color=cfg.MENU_BACKGROUND_COLOR,
            title_background_color=cfg.MENU_TITLE_COLOR,
        )

        play_menu = pygame_menu.Menu('Play Menu', 512,512, theme=menu_theme)
        play_options = pygame_menu.Menu('Play Options', 512,512, theme=menu_theme)

        player_options = pygame_menu.Menu('Characters', 512,512, theme=menu_theme)
        
        control_options = pygame_menu.Menu('Controls', 512,512, theme=menu_theme)

        play_options.add.button('Characters', player_options)
        play_options.add.button('Controls', control_options)
        play_options.add.button('Back', pygame_menu.events.BACK)

        
        player_options.add.selector("Character 1", [("Player 1", Algorithm.PLAYER, 0), ("DFS", Algorithm.DFS, 0),
                                                ("DIJKSTRA", Algorithm.DIJKSTRA, 0), ("None", Algorithm.NONE, 0)], onchange=self.change_player)
        player_options.add.selector("Character 2", [("Player 2", Algorithm.PLAYER, 1), ("DFS", Algorithm.DFS, 1),
                                                ("DIJKSTRA", Algorithm.DIJKSTRA, 1), ("None", Algorithm.NONE, 1)], onchange=self.change_player)
        player_options.add.selector("Character 3", [("DFS", Algorithm.DIJKSTRA, 2),
                                                ("DIJKSTRA", Algorithm.DFS, 2), ("None", Algorithm.NONE, 2)], onchange=self.change_player)
        player_options.add.selector("Character 3", [("DFS", Algorithm.DFS, 3),
                                                ("DIJKSTRA", Algorithm.DIJKSTRA, 3), ("None", Algorithm.NONE, 3)], onchange=self.change_player)
        player_options.add.selector("Show AI path", [("No", False), ("Yes", True)], onchange=self.change_path)
        player_options.add.button('Back', pygame_menu.events.BACK)

        control_options.add.selector("Player 1", self.control_list_select1, onchange=self.change_controls_player1)
        control_options.add.selector("Player 2", self.control_list_select2, onchange=self.change_controls_player2)
        control_options.add.button('Back', pygame_menu.events.BACK)
        control_options.add.vertical_margin(50)
        control_options.add.label("Key1: Move - Arrows, Bomb - RCtrl", font_size=int(cfg.TILE_SIZE*0.4))
        control_options.add.label("Key2: Move - WSAD, Bomb - LCtrl", font_size=int(cfg.TILE_SIZE*0.4))
        
        play_menu.add.button('Start',self.map_selection_menu())

        play_menu.add.button('Options', play_options)
        play_menu.add.button('Return  to  main  menu', pygame_menu.events.BACK)

        about_menu_theme = pygame_menu.themes.Theme(
            selection_color=cfg.COLOR_WHITE,
            widget_font=pygame_menu.font.FONT_BEBAS,
            title_font_size=cfg.TILE_SIZE,
            title_font_color=cfg.COLOR_WHITE,
            title_font=pygame_menu.font.FONT_BEBAS,
            widget_font_color=cfg.COLOR_WHITE,
            widget_font_size=int(cfg.TILE_SIZE*0.4),
            background_color=cfg.MENU_BACKGROUND_COLOR,
            title_background_color=cfg.MENU_TITLE_COLOR,
        )

        about_menu = pygame_menu.Menu('About', 512,512, theme=about_menu_theme)
        about_menu.add.vertical_margin(15)
        about_menu.add.label("Author:")
        about_menu.add.label("Matin Asgarov")
        about_menu.add.label("ELTE")
        about_menu.add.vertical_margin(15)

    

        main_menu = pygame_menu.Menu('Menu', 512,512, theme=menu_theme)

        main_menu.add.button('Play', play_menu)
        main_menu.add.button('About', about_menu)
        main_menu.add.button('Quit', pygame_menu.events.EXIT)
        
        while True:
            self.clock.tick(60)
            self.main_background()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            main_menu.mainloop(self.surface, self.main_background, disable_loop=False, fps_limit=0)
            pygame.display.flip()

            main_menu.mainloop(self.surface, self.main_background, disable_loop=False, fps_limit=0)
            main_menu.update(events)
            main_menu.draw(self.surface)

            pygame.display.flip()

    def run(self):
        self.menu_loop()


    