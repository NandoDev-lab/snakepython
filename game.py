# game.py
from PyQt5.QtGui import QColor

class SnakeGame:
    def __init__(self):
        self.grid_size = 20
        self.board_width = 30
        self.board_height = 30

        # Inicializar cobras e direções
        self.snakes = [[(10, 10)], [(20, 20)]]
        self.directions = [None, None]  # Inicialmente, sem direção
        self.snake_colors = [QColor("green"), QColor("blue")]  # Adiciona cores para as cobras

    def move_snake(self, player_index):
        """Move a cobra do jogador para a próxima posição baseada na direção."""
        if not self.directions[player_index]:
            return

        head_x, head_y = self.snakes[player_index][0]
        if self.directions[player_index] == "UP":
            new_head = (head_x, head_y - 1)
        elif self.directions[player_index] == "DOWN":
            new_head = (head_x, head_y + 1)
        elif self.directions[player_index] == "LEFT":
            new_head = (head_x - 1, head_y)
        elif self.directions[player_index] == "RIGHT":
            new_head = (head_x + 1, head_y)
        else:
            return

        self.snakes[player_index].insert(0, new_head)
        self.snakes[player_index].pop()

    def check_collision(self, player_index):
        """Verifica se a cobra colidiu com os limites ou consigo mesma."""
        head = self.snakes[player_index][0]
        # Verifica limites do tabuleiro
        if not (0 <= head[0] < self.board_width and 0 <= head[1] < self.board_height):
            return True
        # Verifica colisão consigo mesma
        if head in self.snakes[player_index][1:]:
            return True
        return False
