import os
import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT
from tkinter import Tk, Menu, Frame, Toplevel, Label, Entry, Button
from logic import GameSettings, GameOfLife

class GUI():

    def __init__(self):
        self.width = 640
        self.height = 480
        self.root = Tk()
        self.root.title('Game of Life')
        self.need_con = False
        menu = Menu(self.root)
        menu.add_command(label='New game', command=self.__newGamePopup)
        menu.add_command(label='Exit', command=self.__appQuit)
        # Space to separate status. Not the most elegant solution, I know
        menu.add_command(label='                ')
        # Status label
        menu.add_command(label=' ')
        self.root.config(menu=menu)
        self.menu = menu
    
    def Run(self):
        frame = Frame(self.root, width=self.width, height=self.height)
        frame.pack()
        os.environ['SDL_WINDOWID'] = str(frame.winfo_id())
        self.root.update()
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.root.protocol('WM_DELETE_WINDOW', self.__appQuit)
        self.game_settings = GameSettings()
        self.ng_window = None
        self.app_running = True
        self.game_in_process = False
        while self.app_running:
            self.root.update_idletasks()
            self.root.update()
    

    def __newGamePopup(self):
        if self.game_in_process:
            return
        if not self.ng_window is None:
            self.ng_window.destroy()
        self.ng_window = Toplevel(self.root)
        grid_row = 0
        self.game_params_entries = {}
        for param in self.game_settings.__slots__:
            Label(self.ng_window, text = param).grid(row = grid_row,column = 0)
            param_entry = Entry(self.ng_window)
            param_entry.grid(row = grid_row, column = 1)
            param_entry.insert(0, self.game_settings.__getattribute__(param))
            self.game_params_entries[param] = param_entry
            grid_row += 1
        Button(self.ng_window, text="Start", command=self.__newGame).grid(row = grid_row, column = 0)
        Button(self.ng_window, text="Close", command=self.ng_window.destroy).grid(row = grid_row, column = 1)
    
    def __newGame(self):
        self.__setGameSettings()
        self.__setupNewGame()
        self.__setStatus('New game started')
        self.clock = pygame.time.Clock()
        self.ng_window.destroy()
        self.__drawLines()
        self.game.Start()
        self.__drawGrid()
        self.game_in_process = True
        while self.game_in_process:
            # Start of new round
            if self.game.cur_round_generation == 1:
                self.__addNewCells()
                self.__setStatus('Round {}'.format(self.game.cur_round))
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__appQuit()
                    return
            self.game.Move()
            self.game_in_process = not self.game.IsOver
            self.__drawGrid()
            self.__drawLines()
            self.__refreshFrame()
        self.__setStatus(self.game.Winner)
    
    def __setGameSettings(self):
        for param in self.game_params_entries:
            self.game_settings.__setattr__(param, self.game_params_entries[param].get())
    
    """ Create new app game """
    def __setupNewGame(self):
        self.cell_size = 20
        self.speed = 10
        self.game = GameOfLife(size=(int(self.width / self.cell_size), int(self.height / self.cell_size)), settings=self.game_settings)
    
    """ Draw lines to outline cells """
    def __drawLines(self, color_is_white: bool=False):
        color = pygame.Color('white') if color_is_white else pygame.Color('black')
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, color, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))
    
    """ Paint game grid to show its current state """
    def __drawGrid(self):
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                self.__drawCell(self.game.grid[y][x], x, y)
    
    def __drawCell(self, player, x, y):
        pygame.draw.rect(self.screen,
                        self.__getCellColor(player),
                        (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
    
    def __getCellColor(self, cell_value):
        colors = ['black', 'red', 'green', 'blue', 'yellow', 'purple']
        return pygame.Color(colors[cell_value])
    
    def __appQuit(self):
        self.app_running = False
        self.game_in_process = False
        pygame.quit()
    
    def __addNewCells(self):
        self.__drawLines(True)
        for p in self.game.players_queue:
            added_cells = 0
            while added_cells < self.game_settings.new_cells_per_round:
                self.__setStatus('Round {}. Player {} adding cells: {} left'.format(self.game.cur_round, p, self.game_settings.new_cells_per_round - added_cells))
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        x = event.pos[0] // self.cell_size
                        y = event.pos[1] // self.cell_size
                        if self.game.AddCell(p, x, y):
                            added_cells += 1
                            pygame.draw.rect(self.screen,
                                            self.__getCellColor(p),
                                            (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
                self.__refreshFrame()
    
    def __setStatus(self, status):
        self.menu.entryconfigure(4, label=status)
    
    def __refreshFrame(self):
        pygame.display.flip()
        self.root.update_idletasks()
        self.root.update()
        self.clock.tick(self.speed)