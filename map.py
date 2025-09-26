from cell import Cell
from ship_part import ShipPart
from miss import Miss


class Map:
    def __init__(self, w=10, h=10):
        self.width = w
        self.height = h
        self.map = [[Cell() for _ in range(self.width)] for _ in range(self.height)]


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
