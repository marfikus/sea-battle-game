
class ShipPart:
    def __init__(self, ship=None, alive=True, map_y=None, map_x=None):
        self.ship = ship
        self.alive = alive
        self.map_y = map_y
        self.map_x = map_x


    def kill(self):
        self.alive = False
        self.ship.update_state()


