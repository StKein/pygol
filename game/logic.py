class GameSettings:
    __slots__ = ('players_number', 'generations_per_round', 'new_cells_per_round')

    def __init__(self, players_number: int=2, generations_per_round: int=0, new_cells_per_round: int=20):
        self.players_number = players_number if 1 <= players_number <= 5 else 1;
        self.new_cells_per_round = new_cells_per_round if 10 <= new_cells_per_round <= 100 else 10;
        # TODO: remove infinite generations possibility when game gets to required format
        self.generations_per_round = generations_per_round if 0 <= generations_per_round <= 50 else 0


class GameOfLife:
    __slots__ = ('settings', 'cols', 'rows', 'prev2_generation', 'prev_generation', 'cur_generation', 'cur_generation_num', 'cur_player')

    def __init__(self, size: (int, int)=(20,20), settings: GameSettings=GameSettings()):
        self.settings = settings
        self.cols, self.rows = size
        # if field is too small, increase it
        while self.cols * self.rows < self.settings.players_number * self.settings.new_cells_per_round:
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
        for p in range(1, self.settings.players_number + 1):
            self.cur_player = p
            self.__playerMove()
        self.cur_generation_num += 1
        pass
    
    
    def __createGrid(self, auto_fill: bool=False):
        """
            Creates new board grid
            TODO: move filling part to 'addNewCells'
            TODO: when manual start cells setup ready, remove auto_fill
        """
        grid = []
        for y in range(self.rows):
            grid.append([])
            for x in range(self.cols):
                grid[y].append(0)
        if auto_fill:
            import random
            for player in range(1, self.settings.players_number + 1):
                x = -1
                y = -1
                for n in range(self.settings.new_cells_per_round):
                    while x == -1 or grid[y][x] != 0:
                        x = random.randint(0, self.cols - 1)
                        y = random.randint(0, self.rows - 1)
                    grid[y][x] = player
        return grid
    
    # ACCP = Alive Cell of Current Player
    """ Get count of cell's neighbors that are ACCP """
    def __getACCPNeighborsCount(self, cell_x, cell_y) -> int:
        count = 0
        for y in range(cell_y - 1, cell_y + 2):
            for x in range(cell_x - 1, cell_x + 2):
                if x != cell_x or y != cell_y:
                    count += (self.cur_generation[y % self.rows][x % self.cols] == self.cur_player)
        return count
    
    """ Get status of cell after current player's move """
    def __getCellNewStatus(self, cell_x, cell_y):
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
    
    """ Process move of current playe, update curgen grid accordingly """
    def __playerMove(self):
        grid = []
        for y in range(self.rows):
            grid.append([])
            for x in range(self.cols):
                grid[y].append(self.__getCellNewStatus(x, y))
        self.cur_generation = grid
    
    
    @property
    def IsNotEnded(self) -> bool:
        return not (self.__maxGenerationsExceeded or not self.__generationIsChanging)
    
    @property
    def __maxGenerationsExceeded(self) -> bool:
        return self.settings.generations_per_round != 0 and self.cur_generation_num > self.settings.generations_per_round
    
    @property
    def __generationIsChanging(self) -> bool:
        return self.cur_generation != self.prev_generation and self.cur_generation != self.prev2_generation