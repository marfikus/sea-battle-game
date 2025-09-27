
from cell import Cell
from ship_part import ShipPart
from miss import Miss
from orientation import Orientation


class Map:
    def __init__(self, w=10, h=10):
        self.width = w
        self.height = h
        self.map = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        self.ships = []


    def show(self):
        border = " " + "-=-" * len(self.map[0])
        print(border)
        for y in range(self.height):
            print("|", end="")
            num_line = " "
            for x in range(self.width):
                num_line += f" {x} "
                content = self.map[y][x].content
                if content is None:
                    print("   ", end="")
                elif isinstance(content, ShipPart):
                    print(" s ", end="")
                elif isinstance(content, Miss):
                    print(" o ", end="")
            print("|", y)
        print(border)
        print(num_line)


    def add_ship(self, ship, y, x, orientation):
        if ship in self.ships:
            print("This ship already added!")
            return

        if (y < 0) or (y >= self.height):
            print("Invalid position 'y'!", y)
            return

        if (x < 0) or (x >= self.width):
            print("Invalid position 'x'!", x)
            return

        inc_x = 0
        inc_y = 0
        if orientation == Orientation.HORIZONTAL:
            inc_x = 1
            max_x = x + (len(ship.parts) - 1)
            if max_x >= self.width:
                print("Very long ship!")
                return
        elif orientation == Orientation.VERTICAL:
            inc_y = 1
            max_y = y + (len(ship.parts) - 1)
            if max_y >= self.height:
                print("Very long ship!")
                return

        _y = y
        _x = x
        for part in ship.parts:
            if self.map[_y][_x].content is not None:
                print("Busy cell!")
                return

            self.map[_y][_x].content = part
            _y += inc_y
            _x += inc_x

        self.ships.append(ship)
        ship.orientation = orientation

