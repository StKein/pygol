from apps import GameOfLife, GUI
game = GUI(game=GameOfLife(size=(20, 15), players_number=5, player_start_cells=100), speed=10)
game.Run()