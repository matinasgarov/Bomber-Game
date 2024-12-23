
import unittest
from game import Game
from player import Player

class PlayerMovementTest(unittest.TestCase):

    def setUp(self):
        self.game_instance = Game()
        self.game_instance.players = [Player((2, 2), None, "TestPlayer")]
        self.game_instance.grid = [[0] * 13 for _ in range(13)]

    def test_move_down(self):
        player = self.game_instance.players[0]
        initial_position = (player.posX, player.posY)
        player.step(0, self.game_instance.grid, self.game_instance.enemy_list)  # Move down
        self.assertNotEqual(initial_position, (player.posX, player.posY), "Player should move down.")

    def test_move_right(self):
        player = self.game_instance.players[0]
        initial_position = (player.posX, player.posY)
        player.step(1, self.game_instance.grid, self.game_instance.enemy_list)  # Move right
        self.assertNotEqual(initial_position, (player.posX, player.posY), "Player should move right.")

    def test_move_up(self):
        player = self.game_instance.players[0]
        initial_position = (player.posX, player.posY)
        player.step(2, self.game_instance.grid, self.game_instance.enemy_list)  # Move up
        self.assertNotEqual(initial_position, (player.posX, player.posY), "Player should move up.")

    def test_move_left(self):
        player = self.game_instance.players[0]
        initial_position = (player.posX, player.posY)
        player.step(3, self.game_instance.grid, self.game_instance.enemy_list)  # Move left
        self.assertNotEqual(initial_position, (player.posX, player.posY), "Player should move left.")

if __name__ == '__main__':
    unittest.main()
