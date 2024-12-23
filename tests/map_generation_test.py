import unittest
from game import Game

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.game_instance = Game()  # Create an instance of the Game class

    def test_map_generation_corners(self):
        self.game_instance.generate_map()  # Call the method from the instance
        grid = self.game_instance.grid  # Access the grid from the instance

        self.assertEqual(0, grid[1][1])
        self.assertEqual(0, grid[1][2])
        self.assertEqual(0, grid[2][1])

        l = len(grid)

        self.assertEqual(0, grid[l - 2][1])
        self.assertEqual(0, grid[l - 2][2])
        self.assertEqual(0, grid[l - 3][1])

        self.assertEqual(0, grid[1][l - 2])
        self.assertEqual(0, grid[1][l - 3])
        self.assertEqual(0, grid[2][l - 2])

        self.assertEqual(0, grid[l - 2][l - 2])
        self.assertEqual(0, grid[l - 2][l - 3])
        self.assertEqual(0, grid[l - 3][l - 2])

if __name__ == '__main__':
    unittest.main()
