from django.apps import AppConfig


class GameConfig(AppConfig):
    name = 'game'


class GameOfLife:

    def __init__(self, size: (int, int)=(20,15), max_generations: int=0, players_number: int=2, player_start_cells: int=20):
        self.players_number = players_number if 1 <= players_number <= 5 else 1;
        self.player_start_cells = player_start_cells if 10 <= player_start_cells <= 100 else 10;
        self.max_generations = max_generations
        self.cols, self.rows = size
        # if field is too small, increase it
        while self.cols * self.rows < self.players_number * self.player_start_cells:
            self.cols += 1
            self.rows += 1
    
    def Start(self):
        """
            Game startup preparations:
                * create "dead" prevgen grid
                * create active grid
                * set startup generation number
        """
        self.prev2_generation = self.__createGrid()
        self.prev_generation = self.prev2_generation
        self.cur_generation = self.__createGrid(auto_fill=True)
        self.cur_generation_num = 1
    
    def Move(self):
        """
            Generation step
            Each player's cells make a move
            Then the board is refreshed to show new state
        """
        self.prev2_generation = self.prev_generation
        self.prev_generation = self.cur_generation
        for p in range(1, self.players_number + 1):
            self.cur_player = p
            self.__playerMove()
        self.cur_generation_num += 1
        pass
    
    
    def __createGrid(self, auto_fill: bool=False):
        """
            Creates new board grid
            TODO: when manual start cells setup ready, remove auto_fill
        """
        grid = []
        for y in range(self.rows):
            grid.append([])
            for x in range(self.cols):
                grid[y].append(0)
        if auto_fill:
            import random
            for player in range(1, self.players_number + 1):
                x = -1
                y = -1
                for n in range(self.player_start_cells):
                    while x == -1 or grid[y][x] != 0:
                        x = random.randint(0, self.cols - 1)
                        y = random.randint(0, self.rows - 1)
                    grid[y][x] = player
        return grid
    
    # ACCP = Alive Cell of Current Player
    def __getACCPNeighborsCount(self, cell_x, cell_y) -> int:
        """
            Get count of cell's neighbors that are alive cells of current player
        """
        count = 0
        for y in range(cell_y - 1, cell_y + 2):
            for x in range(cell_x - 1, cell_x + 2):
                if x != cell_x or y != cell_y:
                    count += (self.cur_generation[y % self.rows][x % self.cols] == self.cur_player)
        return count
    
    def __getCellNewStatus(self, cell_x, cell_y):
        """
            Get status of cell after current player's move
        """
        c = self.cur_generation[cell_y][cell_x]
        neighbors = self.__getACCPNeighborsCount(cell_x, cell_y)
        """
            if cell is ACCP:
                if it has 2 or 3 ACCP neighbors:
                    * it remains unchanged
                else:
                    * it dies
            else:
                if it has 3 ACCP neighbors:
                    * it becomes ACCP
                else:
                    * it remains unchanged
        """
        if c == self.cur_player:
            if not 2 <= neighbors <= 3:
                c = 0
        else:
            if neighbors == 3:
                c = self.cur_player
        return c
    
    def __playerMove(self):
        """
            Process move of current player
            Update curgen grid accordingly
        """
        grid = []
        for y in range(self.rows):
            grid.append([])
            for x in range(self.cols):
                grid[y].append(self.__getCellNewStatus(x, y))
        self.cur_generation = grid
    
    
    @property
    def IsNotEnded(self) -> bool:
        return not (self.__maxGenerationsExceeded or not self.__generationHasChanged)
    
    @property
    def __maxGenerationsExceeded(self) -> bool:
        return self.max_generations != 0 and self.cur_generation_num > self.max_generations
    
    @property
    def __generationHasChanged(self) -> bool:
        return self.cur_generation != self.prev_generation and self.cur_generation != self.prev2_generation


import abc

class UI(abc.ABC):

    def __init__(self, game: GameOfLife):
        self.game = game
    
    def run(self):
        pass


import pygame
from pygame.locals import *

class GUI(UI):

    def __init__(self, game: GameOfLife, cell_size: int=20, speed: int=10):
        self.game = game
        self.cell_size = cell_size if 10 <= cell_size <= 40 else 20
        self.width = self.game.cols * self.cell_size
        self.height = self.game.rows * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.speed = speed

        super().__init__(game)
    
    def Run(self):
        """
            TODO:
                * make manual startup cells creation
                * make new game event
                * don't close window when game ends
                * print endgame message
        """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.__drawLines()
        self.game.Start()
        self.__drawGrid()
        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                # event.type == MOUSEBUTTONDOWN; event.pos: (x,y)
                if event.type == KEYDOWN and event.key == 112:
                    paused = not paused
                if event.type == QUIT:
                    pygame.quit()
                    return
            if not paused:
                self.game.Move()
                self.__drawGrid()
                self.__drawLines()
                pygame.display.flip()
                clock.tick(self.speed)
                running = self.game.IsNotEnded
        pygame.quit()
    

    def __drawLines(self):
        """
            Draw lines to outline cells
        """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))
    
    def __drawGrid(self):
        """
            Paint grid to show board current state
        """
        color = ""
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                pygame.draw.rect(self.screen, self.__getCellColor(self.game.cur_generation[y][x]), (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
    
    def __getCellColor(self, cell_value):
        colors = ['black', 'red', 'green', 'blue', 'yellow', 'purple']
        return pygame.Color(colors[cell_value])