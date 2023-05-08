from dice import Dice

class Game:
    def __init__(self, players, board):
        self.players = players
        self.board = board
        self.history = []

    def play(self):
        player_count = len(self.players)
        current_player = 0

        while True:
            player = self.players[current_player]
            dice_1, dice_2 = Dice.roll(), Dice.roll()
            move_info = {
                "player": player.name,
                "color": player.color,
                "dice": (dice_1, dice_2),
                "snake": False,
                "ladder": False,
                "overshoot": False,
                "winner": False,
                "position": 1,
            }

            move = dice_1 + dice_2
            new_position = player.position + move

            if new_position > 100:
                overshoot = new_position - 100
                new_position = 100 - overshoot
                move_info["overshoot"] = True

            if new_position in self.board.snakes_and_ladders:
                if new_position < self.board.snakes_and_ladders[new_position]:
                    move_info["ladder"] = True
                else:
                    move_info["snake"] = True

                new_position = self.board.snakes_and_ladders[new_position]

            player.position = new_position
            move_info["position"] = new_position

            if new_position == 100:
                move_info["winner"] = True
                self.history.append(move_info)
                break

            self.history.append(move_info)

            if dice_1 != dice_2:
                current_player = (current_player + 1) % player_count
