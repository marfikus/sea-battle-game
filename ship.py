
from ship_part import ShipPart


class Ship:
    def __init__(self, parts_num, orientation):
        self.parts = []
        self.orientation = orientation
        self.alive = True

        for _ in range(parts_num):
            self.parts.append(ShipPart(self))
