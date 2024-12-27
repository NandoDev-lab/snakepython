# main.py
import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QTimer
from game import SnakeGame
from controls import Controls
from client import SnakeClient

class SnakeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.controls = Controls()
        self.game = SnakeGame()
        self.client = SnakeClient("ws://localhost:6789")
        self.game_running = False  # Estado do jogo (iniciado ou não)
        
        # Inicializar loop de eventos para WebSocket
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.client.connect())
        self.client.set_on_message_callback(self.handle_remote_move)

    def initUI(self):
        self.setWindowTitle("Snake Multiplayer")
        self.setGeometry(100, 100, 600, 600)
        
        # Adicionar botão "Play"
        self.play_button = QPushButton("Play", self)
        self.play_button.setGeometry(250, 275, 100, 50)
        self.play_button.clicked.connect(self.start_game)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.show()

    def start_game(self):
        """Inicia o jogo ao clicar no botão Play."""
        self.game_running = True
        self.play_button.hide()  # Esconde o botão Play
        self.timer.start(200)  # Inicia o loop do jogo

    def keyPressEvent(self, event):
        """Manipula os comandos de movimento dos jogadores."""
        if self.game_running:  # Só processa comandos se o jogo estiver em execução
            for player_index in range(len(self.game.snakes)):
                new_direction = self.controls.handle_key_press(
                    event.key(), player_index, self.game.directions[player_index]
                )
                if new_direction != self.game.directions[player_index]:
                    self.game.directions[player_index] = new_direction
                    self.loop.create_task(self.client.send(f"{player_index}:{new_direction}"))

    def handle_remote_move(self, message):
        """Recebe e processa movimentos de jogadores remotos."""
        player_index, direction = map(str, message.split(":"))
        player_index = int(player_index)
        self.game.directions[player_index] = direction

    def game_loop(self):
        """Loop principal do jogo."""
        if self.game_running:
            # Movimenta apenas cobras que possuem direções válidas
            for i in range(len(self.game.snakes)):
                if self.game.directions[i] is not None:
                    self.game.move_snake(i)
                    if self.game.check_collision(i):
                        self.timer.stop()
                        print(f"Player {i+1} lost!")
                        self.game_running = False
                        self.play_button.show()  # Mostra o botão Play novamente para reiniciar
            self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnakeApp()
    sys.exit(app.exec_())
