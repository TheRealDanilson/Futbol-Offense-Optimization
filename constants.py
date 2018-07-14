from enum import Enum, auto

GOAL_POS = (0, 0)
FIELD_BOUNDS = (-45, 45, 0, 60)
MAX_SPEED = 0.03
RECEIVE_THRESHOLD = MAX_SPEED*.9
OPENNESS = 2
ZONE_THRESHOLD = 10
dcel = .999
shift = 5
pass_factor = 40
opt_pass = 10
class Objectives(Enum):
    GOAL = auto()
    TEAMMATES = auto()
    OPPONENTS = auto()
    BALL = auto()
    ZONE_CENTER = auto()
    Shift = auto()
    RANDOM = auto()
