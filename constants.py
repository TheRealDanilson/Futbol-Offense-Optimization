from enum import Enum, auto

GOAL_POS = (0, 0)
FIELD_BOUNDS = (-45, 45, 0, 60)
MAX_SPEED = 0.05
RECEIVE_THRESHOLD = MAX_SPEED*3/4
OPENNESS = 10
ZONE_THRESHOLD = 20

class Objectives(Enum):
    GOAL = auto()
    TEAMMATES = auto()
    OPPONENTS = auto()
    BALL = auto()
    ZONE_CENTER = auto()
