from logic import GameSettings, GameOfLife
from ui import GUI

GUI(game=GameOfLife(size=(20, 15), settings=GameSettings(players_number=5, new_cells_per_round=100)), speed=10).Run()