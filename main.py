
from map import Map
from ship import Ship
from orientation import Orientation


def main():
    s1 = Ship(4, Orientation.HORIZONTAL)
    print(s1)
    print(s1.parts[2].ship)

    m = Map()
    m.show()


if __name__ == "__main__":
    main()

