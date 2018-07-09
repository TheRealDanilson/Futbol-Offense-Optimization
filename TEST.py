import sys
import sdl2.ext
from Game import Game
from Player import *
from constants import *
from math import floor
from Ball import *

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
x_min = FIELD_BOUNDS[0]
x_max = FIELD_BOUNDS[1]
y_min = FIELD_BOUNDS[2] 
y_max = FIELD_BOUNDS[3]
while True:
    events = sdl2.ext.get_events()
    for event in events:                #This for loop is not working
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
    
    for player in players:
        if type(player) is Offender:
            sprite = factory.from_image(RESOURCES.get_path("redPlayer.png"))
        else:           #What about ball?
            sprite = factory.from_image(RESOURCES.get_path("bluePlayer.png"))
        (x, y) = player.getPosition()
        sprite.position = (floor((x + x_max)*10), floor((-y + y_max)*10)   ) #We need to fix this so that the origin is at the center of each image
        player_sprites[player] = sprite
        spriterenderer.render(sprite)
    soccerball = factory.from_image(RESOURCES.get_path("ball.png"))
    (x,y) = game.ball.getPosition()
    soccerball.position = (floor((x + x_max)*10), floor((-y + y_max)*10)   )
    spriterenderer.render(soccerball)
    processor = sdl2.ext.TestEventProcessor()
    #processor.run(window)
    #window.refresh()
    game.update()
    #sleep(0.05)    
    
if __name__ == "__main__":
    sys.exit(run())   


