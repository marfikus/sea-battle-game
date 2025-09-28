
import random
from map import Map
from ship import Ship
from orientation import Orientation


class Player:
    def __init__(self):
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
                y = random.randint(0, m.height)
                x = random.randint(0, m.width)
                orientation = random.choice(list(Orientation))

                if m.add_ship(ship, y, x, orientation, True):
                    break
                elif attempt == max_attempts - 1:
                    print("Ship not added!")

        return m


    def shoot(self):
        pass

