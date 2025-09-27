
from map import Map
from ship import Ship
from orientation import Orientation


def main():
    s1 = Ship(4)

    m = Map()
    m.show()

    m.add_ship(s1, 1, 0, Orientation.VERTICAL, True)
    m.add_ship(Ship(4), 3, 2, Orientation.HORIZONTAL, True)
    m.show()

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


if __name__ == "__main__":
    main()

