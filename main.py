
from map import Map
from ship import Ship
from orientation import Orientation


def main():
    s1 = Ship(4, Orientation.VERTICAL)

    m = Map()
    m.show()

    m.add_ship(s1, 1, 1)
    m.add_ship(Ship(4, Orientation.HORIZONTAL), 1, 3)
    m.show()


if __name__ == "__main__":
    main()

