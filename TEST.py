import sys
import sdl2.ext
from Game import Game
from Player import *
from constants import *
from math import floor

RESOURCES = sdl2.ext.Resources(__file__, "Images")

sdl2.ext.init()

window = sdl2.ext.Window("Futbol Offense Optimization", size=(910, 610))
window.show()

factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
background = factory.from_image(RESOURCES.get_path("soccerField.png"))

game = Game()

players = game.playerList()
spriterenderer = factory.create_sprite_render_system(window)
spriterenderer.render(background)

player_sprites = {}
for player in players:
    x_min = FIELD_BOUNDS[0]
    x_max = FIELD_BOUNDS[1]
    y_min = FIELD_BOUNDS[2] 
    y_max = FIELD_BOUNDS[3]
    if type(player) is Offender:
        sprite = factory.from_image(RESOURCES.get_path("redPlayer.png"))
    else:
        sprite = factory.from_image(RESOURCES.get_path("bluePlayer.png"))
    (x, y) = player.getPosition()
    print(x, y)
    sprite.position = (floor((x + x_max)*10), floor((-y + y_max)*10)   )
    print(sprite.position)
    player_sprites[player] = sprite
    spriterenderer.render(sprite)
    
   


processor = sdl2.ext.TestEventProcessor()
processor.run(window)

sdl2.ext.quit()