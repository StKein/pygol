import pygame
import random
from pygame.locals import *


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Скорость протекания игры
        self.speed = speed
    
    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))
    
    def create_grid(self, randomize: bool=False) -> None:
        """
            Create starting grid
        """
        self.grid = []
        for y in range(self.height // self.cell_size):
            self.grid.append([])
            for x in range(self.width // self.cell_size):
                if randomize:
                    self.grid[y].append(random.randint(0, 1))
                else:
                    self.grid[y].append(0)
        pass
    
    def draw_grid(self) -> None:
        color = ""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == 1:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('black')
                pygame.draw.rect(self.screen, color, (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
        pass
    
    def get_alive_neighbors_count(self, cell_x, cell_y) -> int:
        top_x = (cell_x + 1) % len(self.grid[0])
        top_y = (cell_y + 1) % len(self.grid)
        return self.grid[cell_y - 1][cell_x - 1] + self.grid[cell_y - 1][cell_x] + self.grid[cell_y - 1][top_x] + self.grid[cell_y][cell_x - 1] + self.grid[cell_y][top_x] + self.grid[top_y][cell_x - 1] + self.grid[top_y][cell_x] + self.grid[top_y][top_x]
    
    def cell_gets_to_live(self, x, y) -> bool:
        neighbors = self.get_alive_neighbors_count(x, y)
        return neighbors == 3 or (neighbors == 2 and self.grid[y][x] == 1)
    
    def generation_step(self) -> None:
        grid = []
        for y in range(len(self.grid)):
            grid.append([])
            for x in range(len(self.grid[0])):
                if self.cell_gets_to_live(x, y):
                    grid[y].append(1)
                else:
                    grid[y].append(0)
        self.grid = grid
        pass
    
    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.draw_lines()
        self.create_grid(True)
        self.draw_grid()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.generation_step()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    game = GameOfLife(640, 480, 40)
    game.run()