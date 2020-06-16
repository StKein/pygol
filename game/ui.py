import abc
from logic import GameOfLife

class UI(abc.ABC):

    def __init__(self, game: GameOfLife):
        self.game = game
    
    def run(self):
        pass


import pygame
from pygame.locals import *

class GUI(UI):

    def __init__(self,
                game: GameOfLife,
                cell_size: int=20,
                speed: int=10):
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
                #running = not self.game.IsOver
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
                pygame.draw.rect(self.screen,
                                self.__getCellColor(self.game.grid[y][x]),
                                (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
    
    def __getCellColor(self, cell_value):
        colors = ['black', 'red', 'green', 'blue', 'yellow', 'purple']
        return pygame.Color(colors[cell_value])