
import random
from map import Map
from ship import Ship
from orientation import Orientation
from player_type import PlayerType
from action_type import ActionType
from step_data import StepData
from step_response_type import StepResponseType
from miss import Miss
from ship_part import ShipPart


class Player:
    def __init__(self, type, game):
        self.type = type
        self.game = game
        self.own_map = self.init_own_map()
        self.opponent_map = Map()


    def init_own_map(self):
        m = Map()
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
                    print("Ship not added!")

        return m


    def input_coordinate(self, axis, min_value, max_value):
        while True:
            c = input(f"Enter '{axis}' coordinate please: ")
            try:
                c = int(c)
            except ValueError:
                print("Incorrect value!")
                continue

            if min_value <= c <= max_value:
                break
            else:
                print(f"Value is out of range: {min_value}...{max_value}")

        return c


    def make_step(self):
        y = None
        x = None
        if self.type == PlayerType.HUMAN:
            #cli version
            while True:
                y = self.input_coordinate("Y", 0, self.opponent_map.height - 1)
                x = self.input_coordinate("X", 0, self.opponent_map.width - 1)
                content = self.opponent_map.map[y][x].content
                if content is None:
                    break
                else:
                    print("This point is already used!")

        elif self.type == PlayerType.COMPUTER:
            while True:
                y = random.randint(0, self.opponent_map.height - 1)
                x = random.randint(0, self.opponent_map.width - 1)
                content = self.opponent_map.map[y][x].content
                if content is None:
                    break

        print(y, x)
        self.game.send(self, ActionType.STEP_REQUEST, StepData(y, x))


    def step_request(self, data):
        print(self.type, data.coords)
        y = data.coords["y"]
        x = data.coords["x"]
        content = self.own_map.map[y][x].content
        response_type = None

        if content is None:
            self.own_map.map[y][x].content = Miss()
            response_type = StepResponseType.AWAY
            print("Away!")

        elif isinstance(content, ShipPart):
            if content.alive:
                content.kill()

                if content.ship.alive:
                    # wounded
                    response_type = StepResponseType.WOUNDED
                    print("Wounded!")
                else:
                    # killed
                    response_type = StepResponseType.KILLED
                    print("Killed!")
            else:
                # repeated
                response_type = StepResponseType.REPEATED
                print("Repeated!")

        elif isinstance(content, Miss):
            # repeated
            response_type = StepResponseType.REPEATED
            print("Repeated!")

        self.game.send(
            self, 
            ActionType.STEP_RESPONSE, 
            StepData(y, x, response_type)
        )


    def step_response(self, data):
        pass



