
from ship_part import ShipPart


class Ship:
    def __init__(self, parts_num=0, alive=True):
        self.parts = []
        self.orientation = None
        self.alive = alive
        self.screen_coords = None

        for _ in range(parts_num):
            self.parts.append(ShipPart(ship=self))


    def update_state(self):
        for part in self.parts:
            if part.alive:
                return
        self.alive = False

