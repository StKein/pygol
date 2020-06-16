""" Game logic module """

""" Game settings """
class GameSettings:
    __slots__ = ('players_number', 'rounds_number', 'generations_per_round', 'new_cells_per_round')

    def __init__(self,
                players_number: int=2,
                generations_per_round: int=10,
                rounds_number = 10,
                new_cells_per_round: int=20):
        self.players_number = players_number
        self.generations_per_round = generations_per_round
        self.rounds_number = rounds_number
        self.new_cells_per_round = new_cells_per_round
    
    """ Overwrite setter for validation """
    def __setattr__(self, name, val):
        if not name in self.__slots__:
            return
        
        try:
            val = int(val)
        except ValueError:
            return
        
        is_valid = False
        if name == 'players_number':
            is_valid = 1 <= val <= 5
        elif name == 'generations_per_round':
            is_valid = 1 <= val <= 50
        elif name == 'rounds_number':
            is_valid = 1 <= val <= 30
        elif name == 'new_cells_per_round':
            is_valid = 5 <= val <= 100
        
        if is_valid:
            super().__setattr__(name, val)


import logging
import random
import time

""" Game logic """
class GameOfLife:
    __slots__ = ('settings', 'cols', 'rows', 'grid', '__winner', 'logger',
                'cur_round', 'cur_round_generation', 'cur_player', 'players_queue')

    def __init__(self,
                size: (int, int)=(30,20),
                settings: GameSettings=GameSettings()):
        self.settings = settings
        self.cols, self.rows = size
        self.__winner = [0]
        self.players_queue = []
        for p in range(1, self.settings.players_number + 1):
            self.players_queue.append(p)
        random.shuffle(self.players_queue)
        self.__setLogger()
    
    """ Start game preparations """
    def Start(self):
        self.logger.info('Game for {} players started'.format(self.settings.players_number))
        self.cur_round = 1
        self.cur_round_generation = 1
        self.__resetGrid()
    
    """ Game move logic """
    def Move(self):
        # Just in case
        if self.IsOver:
            return
        
        """ Each player's cells step to next generation """
        for p in self.players_queue:
            self.cur_player = p
            self.__playerMove()
        self.cur_round_generation += 1

        """ Round generations ended - move to next round """
        if self.cur_round_generation > self.settings.generations_per_round:
            self.__setWinner()
            self.cur_round += 1
            self.cur_round_generation = 1
            """ Or not (if all rounds complete) """
            if self.IsOver:
                self.logger.info('Game over. {}'.format(self.Winner))
                return
            self.logger.info('Round {} ended. Current leader: {}'.format(self.cur_round - 1, self.Winner))
            random.shuffle(self.players_queue)
    
    """ Handler for adding cell on field """
    def AddCell(self, player: int, cell_x: int, cell_y: int) -> bool:
        if self.grid[cell_y][cell_x] != 0:
            return False
        
        self.grid[cell_y][cell_x] = player
        return True
    

    """ Class logger setup """
    def __setLogger(self):
        self.logger = logging.getLogger('GameOfLife')
        handler = logging.FileHandler('logs/game.log')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel('INFO')
        self.logger.propagate = False
    
    """ Reset game grid """
    def __resetGrid(self):
        self.grid = []
        for y in range(self.rows):
            self.grid.append([])
            for x in range(self.cols):
                self.grid[y].append(0)
    
    # ACCP = Alive Cell of Current Player
    """ Get count of cell's neighbors that are ACCP """
    def __getACCPNeighborsCount(self, cell_x, cell_y) -> int:
        count = 0
        for y in range(cell_y - 1, cell_y + 2):
            for x in range(cell_x - 1, cell_x + 2):
                if x != cell_x or y != cell_y:
                    count += (self.grid[y % self.rows][x % self.cols] == self.cur_player)
        return count
    
    """ Get status of cell after current player's move """
    def __getCellNewStatus(self, cell_x, cell_y):
        c = self.grid[cell_y][cell_x]
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
    
    """ Process move of current player, update grid accordingly """
    def __playerMove(self):
        grid = []
        for y in range(self.rows):
            grid.append([])
            for x in range(self.cols):
                grid[y].append(self.__getCellNewStatus(x, y))
        self.grid = grid

    
    """ Set game winner """
    def __setWinner(self):
        counts = [0]
        for p in range(self.settings.players_number):
            counts.append(0)
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] > 0:
                    counts[self.grid[y][x]] += 1
        self.__winner = [0]
        for p in range(1, self.settings.players_number + 1):
            if counts[p] == 0:
                continue
            if counts[p] > counts[self.__winner[0]]:
                self.__winner = [p]
            elif counts[p] == counts[self.__winner[0]]:
                self.__winner.append(p)
    
    
    @property
    def IsOver(self) -> bool:
        return self.cur_round > self.settings.rounds_number
    
    @property
    def Winner(self) -> str:
        if len(self.__winner) > 1:
            return 'Draw between players {}'.format(', '.join(str(p) for p in self.__winner))
        else:
            return 'Winner: player {}'.format(self.__winner[0]) if self.__winner[0] > 0 else 'All life was lost'