import os
import pygame
from pygame.locals import QUIT
from tkinter import Tk, Menu, Frame
from logic import GameSettings, GameOfLife

class GUI():

    def __init__(self):
        self.width = 640
        self.height = 480
        self.root = Tk()
        self.root.title('Game of Life')
        menu = Menu(self.root)
        menu.add_command(label='New game', command=self.NewGame)
        menu.add_command(label='Exit', command=self.__appQuit)
        self.root.config(menu=menu)
    
    def Run(self):
        frame = Frame(self.root, width=self.width, height=self.height)
        frame.pack()
        os.environ['SDL_WINDOWID'] = str(frame.winfo_id())
        self.root.update()
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.root.protocol('WM_DELETE_WINDOW', self.__appQuit)
        self.app_running = True
        while self.app_running:
            self.root.update_idletasks()
            self.root.update()
    
    def NewGame(self):
        self.__setGameSettings()
        self.__setupNewGame()
        clock = pygame.time.Clock()
        self.__drawLines()
        self.game.Start()
        self.__drawGrid()
        self.game_in_process = True
        while self.game_in_process:
            for event in pygame.event.get():
                # event.type == MOUSEBUTTONDOWN; event.pos: (x,y)
                if event.type == QUIT:
                    self.__appQuit()
                    return
            self.game.Move()
            self.__drawGrid()
            self.__drawLines()
            pygame.display.flip()
            self.root.update_idletasks()
            self.root.update()
            clock.tick(self.speed)
            self.game_in_process = not self.game.IsOver
            self.root.update_idletasks()
            self.root.update()
    
    
    def __setGameSettings(self):
        # TODO: modify 'new game' button for game settings popup before start
        self.game_settings = GameSettings(players_number=5, new_cells_per_round=50)
    
    """ Create new app game """
    def __setupNewGame(self):
        self.cell_size = 20
        self.speed = 10
        self.game = GameOfLife(size=(int(self.width / self.cell_size), int(self.height / self.cell_size)), settings=self.game_settings)
    
    """ Draw lines to outline cells """
    def __drawLines(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))
    
    """ Paint game grid to show its current state """
    def __drawGrid(self):
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                pygame.draw.rect(self.screen,
                                self.__getCellColor(self.game.grid[y][x]),
                                (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
    
    def __getCellColor(self, cell_value):
        colors = ['black', 'red', 'green', 'blue', 'yellow', 'purple']
        return pygame.Color(colors[cell_value])
    
    def __appQuit(self):
        self.app_running = False
        self.game_in_process = False
        pygame.quit()