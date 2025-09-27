
from map import Map
from ship import Ship
from orientation import Orientation


def main():
    s1 = Ship(4)

    m = Map()
    m.show()

    m.add_ship(s1, 1, 1, Orientation.VERTICAL)
    m.add_ship(Ship(4), 1, 3, Orientation.HORIZONTAL)
    m.show()


if __name__ == "__main__":
    main()

