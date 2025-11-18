
from enum import Enum


class ActionType(Enum):
    MAKE_STEP = 0
    STEP_REQUEST = 1
    STEP_RESPONSE = 2
    WAITING_OPPONENT_STEP = 3
