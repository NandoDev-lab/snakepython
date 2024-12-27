# controls.py
class Controls:
    def __init__(self):
        self.key_mapping = [
            {  # Player 1
                "UP": "w",
                "DOWN": "s",
                "LEFT": "a",
                "RIGHT": "d",
            },
            {  # Player 2
                "UP": "Up",
                "DOWN": "Down",
                "LEFT": "Left",
                "RIGHT": "Right",
            },
        ]

    def handle_key_press(self, key, player_index, current_direction):
        """Converte as teclas pressionadas em direções válidas."""
        direction_map = self.key_mapping[player_index]
        key_name = key.key()  # Nome da tecla pressionada
        if key_name == direction_map["UP"] and current_direction != "DOWN":
            return "UP"
        if key_name == direction_map["DOWN"] and current_direction != "UP":
            return "DOWN"
        if key_name == direction_map["LEFT"] and current_direction != "RIGHT":
            return "LEFT"
        if key_name == direction_map["RIGHT"] and current_direction != "LEFT":
            return "RIGHT"
        return current_direction
