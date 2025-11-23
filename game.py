
import random
from settings import Settings
from main_screen import MainScreen
from player import Player
from player_type import PlayerType
from action_type import ActionType


class Game:
    def __init__(self):
        self.settings = Settings()
        self.gui = None
        self.main_screen = None

        self.player1 = Player(PlayerType.HUMAN, self)
        self.player2 = Player(PlayerType.COMPUTER, self)
        self.opponents = {
            self.player1: self.player2,
            self.player2: self.player1,
        }
        self.game_is_active = False


    def select_version(self):
        cmd = input("Select version please (1 - console, 2 - gui): ")
        # cmd = "1"
        if cmd == "1":
            self.gui = False
            self.start()
        elif cmd == "2":
            self.gui = True
            self.main_screen = MainScreen(self.settings, self, self.player1)
            self.main_screen.start_gui()
        else:
            print("Unknown command!")
            return


    def start(self):
        # self.player1.own_map.show()
        # self.player2.own_map.show()
        self.game_is_active = True
        player = random.choice(list(self.opponents))
        if player.type == PlayerType.COMPUTER:
            if self.gui:
                pass
                # вывести сообщение о первом ходе соперника
            else:
                self.opponents[player].show_own_maps()
                print("First step make opponent!")
        player.make_step()


    def send(self, player, action_type, data=None):
        if action_type == ActionType.MAKE_STEP:
            self.opponents[player].make_step()
        elif action_type == ActionType.STEP_REQUEST:
            self.opponents[player].step_request(data)
        elif action_type == ActionType.STEP_RESPONSE:
            self.opponents[player].step_response(data)
        elif action_type == ActionType.WAITING_OPPONENT_STEP:
            self.opponents[player].waiting_opponent_step()


    def end(self, player):
        print("Game over! Winner is", player.type)
        self.game_is_active = False
        # надо сообщить противнику тоже...
        # еще вариант когда кто-то сдаётся... наверное добавить в ActionType...


