
from map import Map
from ship import Ship
from orientation import Orientation
import random


def main():
    s1 = Ship(4)

    m = Map()
    m.show()

    # m.add_ship(s1, 1, 0, Orientation.VERTICAL, True)
    # m.add_ship(Ship(4), 3, 2, Orientation.HORIZONTAL, True)
    # m.show()

    # print(s1.parts[2])
    # print(m.map[3][1].content)

    # generation ship list
    ships = []
    max_ = 5
    for i in range(1, max_):
        for j in range(i):
            ships.append(Ship(max_ - i))
    # print(len(ships))
    # for s in ships:
    #     print(len(s.parts))

    # fill map
    max_attempts = 100
    # max_add_attempt = 0
    for ship in ships:
        for attempt in range(max_attempts):
            y = random.randint(0, m.height)
            x = random.randint(0, m.width)
            orientation = random.choice(list(Orientation))

            if m.add_ship(ship, y, x, orientation, True):
                # print("Ship added, attempt:", attempt)
                # if attempt > max_add_attempt: max_add_attempt = attempt
                break
            elif attempt == max_attempts - 1:
                print("Ship not added!")

    m.show()
    # print(len(m.ships))
    # print(max_add_attempt)


if __name__ == "__main__":
    main()

