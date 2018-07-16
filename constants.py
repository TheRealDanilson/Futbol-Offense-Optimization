from enum import Enum, auto

GOAL_POS = (0, 0)
FIELD_BOUNDS = (-45, 45, 0, 60)
MAX_SPEED = 0.03
RECEIVE_THRESHOLD = MAX_SPEED*.9
OPENNESS = 6
FORWARDNESS = 6
LENGTHINESS = 2
RANDOM_TIME = 100
ZONE_THRESHOLD = 10
dcel = -.00005
shift = 6
pass_factor = 20
opt_pass = 5
class Objectives(Enum):
    GOAL = auto()
    TEAMMATES = auto()
    OPPONENTS = auto()
    BALL = auto()
    ZONE_CENTER = auto()
    Shift = auto()
    RANDOM = auto()
    OFF_SIDES = auto()
