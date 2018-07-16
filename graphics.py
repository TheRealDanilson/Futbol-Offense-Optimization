import sys
import sdl2.ext
from Game import Game
from Player import *
from constants import *
from math import floor
from Ball import *

class Graphics(object):
    
    def __init__(self, game):
        self.game = game
        RESOURCES = sdl2.ext.Resources(__file__, "Images")

        sdl2.ext.init()

        window = sdl2.ext.Window("Futbol Offense Optimization", size=(910, 610))
        window.show()

        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        background = factory.from_image(RESOURCES.get_path("soccerField.png"))
        self.sprites = [background]