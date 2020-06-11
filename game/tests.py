from django.test import TestCase
from .proto import GameOfLife

# Create your tests here.
class GameOfLifeTestCase(TestCase):
    """
    def test_create_grid(self):
        self.game.create_grid(True)
        for y in range(self.game.grid):
            for x in range(self.game.grid[0]):
                self.
    """
    def set_game(self):
        """
            1 0 0 0 1 0
            0 1 1 0 1 0
            1 1 0 1 0 1
            0 0 1 0 1 1
        """
        self.game = GameOfLife(60, 40, 10)
        self.game.grid = [[1,0,0,0,1,0],[0,1,1,0,1,0],[1,1,0,1,0,1],[0,0,1,0,1,1]]
        pass

    def test_get_alive_neighbors_count(self):
        self.set_game()
        """
            2 4 3 5 3 5
            5 4 3 4 3 5
            4 4 5 4 5 4
            5 4 2 4 4 5
        """
        neighbors_count = [[2,4,3,5,3,5],[5,4,3,4,3,5],[4,4,5,4,5,4],[5,4,2,4,4,5]]
        for y in range(4):
            for x in range(6):
                self.assertEqual(self.game.get_alive_neighbors_count(x,y), neighbors_count[y][x])
    
    def test_generation_step(self):
        self.set_game()
        self.game.generation_step()
        """
            1 0 1 0 1 0
            0 0 1 0 1 0
            0 0 0 0 0 0
            0 0 1 0 0 0
        """
        new_grid = [[1,0,1,0,1,0],[0,0,1,0,1,0],[0,0,0,0,0,0],[0,0,1,0,0,0]]
        self.assertEqual(self.game.grid, new_grid)
        self.game.generation_step()
        """
            0 0 1 0 0 1
            0 1 0 0 0 1
            0 0 0 1 0 0
            0 1 0 1 0 0
        """
        new_grid = [[0,0,1,0,0,1],[0,1,0,0,0,1],[0,0,0,1,0,0],[0,1,0,1,0,0]]
        self.assertEqual(self.game.grid, new_grid)