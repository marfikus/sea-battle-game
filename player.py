
import random
import time
from map import Map
from ship import Ship
from orientation import Orientation
from player_type import PlayerType
from action_type import ActionType
from step_data import StepData
from step_response_type import StepResponseType
from miss import Miss
from ship_part import ShipPart
from wounded import Wounded


class Player:
    def __init__(self, type, game):
        self.type = type
        self.game = game
        self.main_screen = None
        self.strings = self.game.settings.strings
        self.own_map = self.init_own_map()
        self.opponent_map = Map(self)


    def init_own_map(self):
        m = Map(self)
        # generation ship list
        ships = []
        max_ = 5
        for i in range(1, max_):
            for j in range(i):
                ships.append(Ship(max_ - i))

        # fill map
        max_attempts = 100
        for ship in ships:
            for attempt in range(max_attempts):
                y = random.randint(0, m.height - 1)
                x = random.randint(0, m.width - 1)
                orientation = random.choice(list(Orientation))

                if m.add_ship(ship, y, x, orientation, True):
                    break
                elif attempt == max_attempts - 1:
                    raise RuntimeError("Ship not added!")
        return m


    def input_coordinates(self):
        letters = self.strings["letters"][:self.opponent_map.height]
        min_value = 1
        max_value = self.opponent_map.width
        y = None 
        x = None

        while True:
            val = input(self.strings["enter_your_step"])

            if len(val) < 2:
                print(self.strings["invalid_input"])
                continue

            if val[0].upper() in letters:
                y = letters.index(val[0].upper())
            else:
                print(self.strings["invalid_letter"])
                continue

            try:
                x = int(val[1:])
            except ValueError:
                print(self.strings["incorrect_digit"])
                continue

            if min_value <= x <= max_value:
                break
            else:
                msg = self.strings["digit_out_of_range"]
                print(f"{msg} {min_value}...{max_value}!")

        return y, x - 1


    def make_step(self):
        # print("make step by", self.type)
        self.send_waiting_opponent_step()

        y = None
        x = None
        if self.type == PlayerType.HUMAN:
            if self.game.gui:
                self.main_screen.make_step()
                return
            else:
                self.show_own_maps()
                print(self.strings["state_your_step"])

                while True:
                    y, x = self.input_coordinates()
                    content = self.opponent_map.map[y][x].content
                    if content is None:
                        break
                    else:
                        print(self.strings["repeated"])

        elif self.type == PlayerType.COMPUTER:
            time.sleep(random.randint(2, 4))

            while True:
                y = random.randint(0, self.opponent_map.height - 1)
                x = random.randint(0, self.opponent_map.width - 1)
                content = self.opponent_map.map[y][x].content
                if content is None:
                    break

        self.send_step_request(y, x)


    def step_request(self, data):
        # print("step request to", self.type, data.coords)
        y = data.coords["y"]
        x = data.coords["x"]
        content = self.own_map.map[y][x].content
        response_type = None
        killed_ship = None

        if content is None:
            # away
            self.own_map.map[y][x].content = Miss()
            response_type = StepResponseType.AWAY
            self.step_request_away(y, x)

        elif isinstance(content, ShipPart):
            if content.alive:
                content.kill()

                if content.ship.alive:
                    # wounded
                    response_type = StepResponseType.WOUNDED
                    self.step_request_wounded(y, x)
                else:
                    # killed
                    response_type = StepResponseType.KILLED
                    killed_ship = content.ship
                    self.step_request_killed(y, x, killed_ship)
            else:
                # repeated
                response_type = StepResponseType.REPEATED
                self.step_request_repeated(y, x)

        elif isinstance(content, Miss):
            # repeated
            response_type = StepResponseType.REPEATED
            self.step_request_repeated(y, x)

        time.sleep(1)
        step_data = StepData(y, x, response_type, killed_ship)
        self.send_step_response(step_data)


    def step_request_away(self, y, x):
        if self.type == PlayerType.HUMAN:
            text = "{}{}: {}".format(
                self.strings["state_opponent_shot_on"],
                self.coords_to_code(y, x),
                self.strings["away"]
            )
            if self.game.gui:
                self.main_screen.step_request_away(y, x, text)
            else:
                print(text)


    def step_request_wounded(self, y, x):
        if self.type == PlayerType.HUMAN:
            text = "{}{}: {}".format(
                self.strings["state_opponent_shot_on"],
                self.coords_to_code(y, x),
                self.strings["wounded"]
            )
            if self.game.gui:
                self.main_screen.step_request_wounded(y, x, text)
            else:
                print(text)


    def step_request_killed(self, y, x, killed_ship):
        if self.type == PlayerType.HUMAN:
            text = "{}{}: {}".format(
                self.strings["state_opponent_shot_on"],
                self.coords_to_code(y, x),
                self.strings["killed"]
            )
            if self.game.gui:
                self.main_screen.step_request_killed(y, x, killed_ship, text)
            else:
                print(text)


    def step_request_repeated(self, y, x):
        if self.type == PlayerType.HUMAN:
            text = "{}{}: {}".format(
                self.strings["state_opponent_shot_on"],
                self.coords_to_code(y, x),
                self.strings["repeated"]
            )
            if self.game.gui:
                self.main_screen.step_request_repeated(y, x, text)
            else:
                print(text)


    def step_response(self, data):
        # print("step response to", self.type, data.coords, data.step_response_type)
        y = data.coords["y"]
        x = data.coords["x"]
        response = data.step_response_type

        if response == StepResponseType.AWAY:
            self.opponent_map.map[y][x].content = Miss()
            self.step_response_away(y, x)
            self.send_make_step()
        elif response == StepResponseType.WOUNDED:
            self.opponent_map.map[y][x].content = Wounded()
            self.step_response_wounded(y, x)
            self.make_step()
        elif response == StepResponseType.KILLED:
            # добавляем убитый корабль на карту
            ship = Ship(alive=False)
            ship.orientation = data.killed_ship.orientation
            for p in data.killed_ship.parts:
                part = ShipPart(ship, False, p.map_y, p.map_x)
                ship.parts.append(part)
                self.opponent_map.map[p.map_y][p.map_x].content = part
            self.opponent_map.ships.append(ship)

            self.step_response_killed(y, x, ship)
            # проверить оставшиеся корабли противника, возможен конец игры
            if self.opponent_has_alive_ships():
                self.make_step()
            else:
                self.game.end(self)
            
        elif response == StepResponseType.REPEATED:
            self.step_response_repeated(y, x)


    def step_response_away(self, y, x):
        if self.type == PlayerType.HUMAN:
            text = "{}{}: {}".format(
                self.strings["state_your_shot_on"],
                self.coords_to_code(y, x),
                self.strings["away"]
            )
            if self.game.gui:
                self.main_screen.step_response_away(y, x, text)
            else:
                print(text)


    def step_response_wounded(self, y, x):
        if self.type == PlayerType.HUMAN:
            text = "{}{}: {}".format(
                self.strings["state_your_shot_on"],
                self.coords_to_code(y, x),
                self.strings["wounded"]
            )
            if self.game.gui:
                self.main_screen.step_response_wounded(y, x, text)
            else:
                print(text)


    def step_response_killed(self, y, x, ship):
        if self.type == PlayerType.HUMAN:
            text = "{}{}: {}".format(
                self.strings["state_your_shot_on"],
                self.coords_to_code(y, x),
                self.strings["killed"]
            )
            if self.game.gui:
                self.main_screen.step_response_killed(y, x, ship, text)
            else:
                print(text)


    def step_response_repeated(self, y, x):
        if self.type == PlayerType.HUMAN:
            text = "{}{}: {}".format(
                self.strings["state_your_shot_on"],
                self.coords_to_code(y, x),
                self.strings["repeated"]
            )
            if self.game.gui:
                self.main_screen.step_response_repeated(y, x, text)
            else:
                print(text)


    def opponent_has_alive_ships(self):
        # print("opponent ships:", len(self.opponent_map.ships))
        # print("own ships:", len(self.own_map.ships))
        if len(self.opponent_map.ships) < len(self.own_map.ships):
            return True
        return False


    def opponent_first_step(self):
        if self.type == PlayerType.HUMAN:
            if self.game.gui:
                self.main_screen.opponent_first_step()
            else:
                self.show_own_maps()
                print(self.strings["state_opponent_first_step"])
            time.sleep(2)


    def waiting_opponent_step(self):
        if self.type == PlayerType.HUMAN:
            if self.game.gui:
                self.main_screen.waiting_opponent_step()
            else:
                print(self.strings["state_waiting_opponent_step"])


    def show_own_maps(self):
        print(self.strings["your_ships_map"])
        self.own_map.show()
        print(self.strings["opponent_ships_map"])
        self.opponent_map.show()


    def send_step_request(self, y, x):
        self.game.send(self, ActionType.STEP_REQUEST, StepData(y, x))


    def send_step_response(self, data):
        self.game.send(self, ActionType.STEP_RESPONSE, data)


    def send_make_step(self):
        self.game.send(self, ActionType.MAKE_STEP)


    def send_waiting_opponent_step(self):
        self.game.send(self, ActionType.WAITING_OPPONENT_STEP)


    def coords_to_code(self, y, x):
        letters = self.strings["letters"]
        return f"{letters[y]}{x + 1}"


