from django.apps import AppConfig


class GameConfig(AppConfig):
    name = 'game'


class GameOfLife:

    def __init__(self, size: (int, int), max_generations: int=0) -> None:
        self.cols, self.rows = size
        self.max_generations = max_generations
    
    def create_grid(self, randomize: bool=False):
        """
            Create grid
            TODO: when manual start cells setup ready, remove randomize
        """
        grid = []
        if randomize:
            import random
        for y in range(self.rows):
            grid.append([])
            for x in range(self.cols):
                if randomize:
                    grid[y].append(random.randint(0, 1))
                else:
                    grid[y].append(0)
        return grid
    
    def get_alive_neighbors_count(self, cell_x, cell_y) -> int:
        # TODO: when implementing 2 players mode rework the algorithm
        #       to find count of nearby cells with value X
        top_x = (cell_x + 1) % self.cols
        top_y = (cell_y + 1) % self.rows
        return self.cur_generation[cell_y - 1][cell_x - 1] + self.cur_generation[cell_y - 1][cell_x] + self.cur_generation[cell_y - 1][top_x] + self.cur_generation[cell_y][cell_x - 1] + self.cur_generation[cell_y][top_x] + self.cur_generation[top_y][cell_x - 1] + self.cur_generation[top_y][cell_x] + self.cur_generation[top_y][top_x]
    
    def cell_gets_to_live(self, x, y) -> bool:
        neighbors = self.get_alive_neighbors_count(x, y)
        return neighbors == 3 or (neighbors == 2 and self.cur_generation[y][x] == 1)
    
    def step(self) -> None:
        grid = []
        for y in range(self.rows):
            grid.append([])
            for x in range(self.cols):
                if self.cell_gets_to_live(x, y):
                    grid[y].append(1)
                else:
                    grid[y].append(0)
        self.prev_generation = self.cur_generation
        self.cur_generation = grid
        self.cur_generation_num += 1
        pass
    
    def start(self) -> None:
        self.prev_generation = self.create_grid()
        self.cur_generation = self.create_grid(randomize=True)
        self.cur_generation_num = 1
    
    @property
    def is_not_ended(self) -> bool:
        return not (self.__max_generations_exceeded or not self.__generation_has_changed)
    
    @property
    def __max_generations_exceeded(self) -> bool:
        return self.max_generations != 0 and self.cur_generation_num > self.max_generations
    
    @property
    def __generation_has_changed(self) -> bool:
        return self.prev_generation != self.cur_generation


import abc

class UI(abc.ABC):

    def __init__(self, game: GameOfLife) -> None:
        self.game = game
    
    def run(self) -> None:
        pass


import pygame
from pygame.locals import *

class GUI(UI):

    def __init__(self, game: GameOfLife, cell_size: int=20, speed: int=10) -> None:
        self.game = game
        self.cell_size = cell_size
        self.width = self.game.cols * self.cell_size
        self.height = self.game.rows * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.speed = speed

        super().__init__(game)
    
    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))
    
    def draw_grid(self) -> None:
        color = ""
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                if self.game.cur_generation[y][x] == 1:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('black')
                pygame.draw.rect(self.screen, color, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
    
    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.draw_lines()
        self.game.start()
        self.draw_grid()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
            self.game.step()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
            running = self.game.is_not_ended
        pygame.quit()