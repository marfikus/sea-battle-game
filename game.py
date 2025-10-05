
import random
from player import Player
from player_type import PlayerType
from action_type import ActionType


class Game:
    def __init__(self):
        self.player1 = Player(PlayerType.HUMAN, self)
        self.player2 = Player(PlayerType.COMPUTER, self)
        self.opponents = {
            self.player1: self.player2,
            self.player2: self.player1,
        }


    def start(self):
        self.player1.own_map.show()
        self.player2.own_map.show()

        player = random.choice(list(self.opponents))
        self.opponents[player].make_step()


    def send(self, player, action_type, data=None):
        if action_type == ActionType.MAKE_STEP:
            self.opponents[player].make_step()
        elif action_type == ActionType.STEP_REQUEST:
            self.opponents[player].step_request(data)
        elif action_type == ActionType.STEP_RESPONSE:
            self.opponents[player].step_response(data)


