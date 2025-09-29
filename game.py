
from player import Player
from player_type import PlayerType


class Game:
    def __init__(self):
        self.player1 = Player(type=PlayerType.HUMAN)
        self.player2 = Player(type=PlayerType.COMPUTER)


    def start(self):
        self.player1.own_map.show()
        self.player2.own_map.show()
