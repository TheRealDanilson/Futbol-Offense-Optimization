from enum import Enum, auto

GOAL_POS = (0, 0)
FIELD_BOUNDS = (-35, 35, 0, 50)
MAX_SPEED = 1
RECEIVE_THRESHOLD = .5
CAREFULLNESS = 0.7

class Objectives(Enum):
    GOAL = auto()
    TEAMMATES = auto()
    OPPONENTS = auto()
    BALL = auto()
    ZONE_CENTER = auto()