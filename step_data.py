
class StepData:
    def __init__(self, y, x, step_response_type=None, killed_ship=None):
        self.coords = {
            "y": y,
            "x": x
        }
        self.step_response_type = step_response_type
        self.killed_ship = killed_ship

