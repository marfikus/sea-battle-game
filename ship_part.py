
class ShipPart:
    def __init__(self, ship=None, alive=True):
        self.ship = ship
        self.alive = alive


    def kill(self):
        self.alive = False
        self.ship.update_state()


