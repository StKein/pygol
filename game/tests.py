from django.test import TestCase
from .apps import GameOfLife

# Create your tests here.
class GameOfLifeTestCase(TestCase):
    def setUp(self):
        self.game = GameOfLife(size=(10,6), players_number=4, player_start_cells=20)
    
    def test_createGrid(self):
        self.game.Start()
        cells = []
        for i in range(self.game.players_number + 1):
            cells.append(0)
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                cells[self.game.cur_generation[y][x]] += 1
        for i in range(1, len(cells)):
            self.assertEqual(cells[i], self.game.player_start_cells)
        for i in range(self.game.rows):
            print(self.game.cur_generation[i])

    def test_getACCPNeighborsCount(self):
        self.__setManualGrid()
        neighbors_count = [
            [1,3,2,1,0,0,0,0,0,1],
            [4,4,2,1,0,1,1,1,0,2],
            [2,3,3,1,0,1,1,3,2,2],
            [2,2,1,0,0,2,4,4,2,2],
            [0,0,0,0,0,1,2,3,3,1],
            [1,1,0,0,0,1,2,2,1,1],
        ]
        self.game.cur_player = 1
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                self.assertEqual(self.game._GameOfLife__getACCPNeighborsCount(x,y), neighbors_count[y][x])
        neighbors_count = [
            [0,1,1,1,1,3,3,2,1,0],
            [0,0,0,0,1,2,4,4,2,0],
            [1,2,2,1,1,2,3,1,1,0],
            [3,3,2,1,0,0,1,1,1,1],
            [2,4,4,2,0,0,0,0,0,1],
            [2,3,1,1,0,1,2,2,1,1],
        ]
        self.game.cur_player = 2
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                self.assertEqual(self.game._GameOfLife__getACCPNeighborsCount(x,y), neighbors_count[y][x])
    
    def test_getCellNewStatus(self):
        self.__setManualGrid()
        grid_next_state = [
            [0,1,0,0,0,0,2,2,0,0],
            [0,0,1,0,0,2,2,0,0,0],
            [1,1,1,0,0,0,0,1,0,0],
            [0,2,2,0,0,0,0,0,1,0],
            [2,2,0,0,0,0,1,1,1,0],
            [0,0,2,0,0,0,0,0,0,0],
        ]
        self.game.cur_player = 1
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                self.assertEqual(self.game._GameOfLife__getCellNewStatus(x, y), grid_next_state[y][x])
        grid_next_state = [
            [0,1,0,0,0,2,2,2,0,0],
            [0,0,1,0,0,2,2,2,0,0],
            [1,1,1,0,0,0,0,1,0,0],
            [2,2,2,0,0,0,0,0,1,0],
            [2,0,0,0,0,0,1,1,1,0],
            [0,2,0,0,0,0,0,0,0,0],
        ]
        self.game._GameOfLife__playerMove()
        self.game.cur_player = 2
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                self.assertEqual(self.game._GameOfLife__getCellNewStatus(x, y), grid_next_state[y][x])
    
    def test_ManualCases(self):
        game = GameOfLife(size=(5,5), players_number=1, player_start_cells=5)
        game.cur_generation_num = 1
        game.cur_generation = [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ]
        game.Move()
        cur_gen = [
            [0,0,0,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
        ]
        self.assertEqual(game.cur_generation, cur_gen)
        game.Move()
        cur_gen = [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ]
        self.assertEqual(game.cur_generation, cur_gen)

        game.cols = 6
        game.cur_generation = [
            [0,0,0,0,0,0],
            [0,0,1,1,0,0],
            [0,1,0,0,1,0],
            [0,0,1,1,0,0],
            [0,0,0,0,0,0],
        ]
        game.Move()
        cur_gen = [
            [0,0,0,0,0,0],
            [0,0,1,1,0,0],
            [0,1,0,0,1,0],
            [0,0,1,1,0,0],
            [0,0,0,0,0,0],
        ]
        self.assertEqual(game.cur_generation, cur_gen)
    
    
    def __setManualGrid(self):
        self.game.cur_generation = [
            [1,0,0,0,0,0,2,2,0,0],
            [0,1,1,0,0,2,2,0,0,0],
            [1,1,0,0,0,0,1,2,0,0],
            [0,2,2,0,0,0,0,1,1,0],
            [2,2,0,0,0,0,1,1,0,0],
            [0,0,2,0,0,0,0,0,0,0],
        ]
        self.game.rows = 6
        self.game.cols = 10
        pass


"""
    DIAGRAMS (or whatever)

    Manual start grid:
        1 0 0 0 0 0 2 2 0 0
        0 1 1 0 0 2 2 0 0 0
        1 1 0 0 0 0 1 2 0 0
        0 2 2 0 0 0 0 1 1 0
        2 2 0 0 0 0 1 1 0 0
        0 0 2 0 0 0 0 0 0 0
    
    P1 neighbors:
        1 3 2 1 0 0 0 0 0 1
        4 4 2 1 0 1 1 1 0 2
        2 3 3 1 0 1 1 3 2 2
        2 2 1 0 0 2 4 4 2 2
        0 0 0 0 0 1 2 3 3 1
        1 1 0 0 0 1 2 2 1 1
    
    P2 neighbors:
        0 1 1 1 1 3 3 2 1 0
        0 0 0 0 1 2 4 4 2 0
        1 2 2 1 1 2 3 1 1 0
        3 3 2 1 0 0 1 1 1 1
        2 4 4 2 0 0 0 0 0 1
        2 3 1 1 0 1 2 2 1 1
    
    P1 first mode:
        0 1 0 0 0 0 2 2 0 0
        0 0 1 0 0 2 2 0 0 0
        1 1 1 0 0 0 0 1 0 0
        0 2 2 0 0 0 0 0 1 0
        2 2 0 0 0 0 1 1 1 0
        0 0 2 0 0 0 0 0 0 0
        
    P2 first move:
        0 1 0 0 0 2 2 2 0 0
        0 0 1 0 0 2 2 2 0 0
        1 1 1 0 0 0 0 1 0 0
        2 2 2 0 0 0 0 0 1 0
        2 0 0 0 0 0 1 1 1 0
        0 2 0 0 0 0 0 0 0 0
"""