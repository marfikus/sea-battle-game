
class ShipPart:
    def __init__(self, ship):
        self.ship = ship
        self.alive = True


    def kill(self):
        self.alive = False
        self.ship.update_state()


