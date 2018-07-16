import sys
import sdl2.ext
from Game import Game
from Player import *
from constants import *
from math import floor
from Ball import *

class Graphics(object):
    
    def __init__(self, game):
        RESOURCES = sdl2.ext.Resources(__file__, "Images")
        sdl2.ext.init()
        window = sdl2.ext.Window("Futbol Offense Optimization", size=(910, 610))
        window.show()
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        background = factory.from_image(RESOURCES.get_path("soccerField.png"))
        
        self.game = game
        self.players = self.game.playerList()
        self.player_sprites = {}
        self.sprites = [background]
        self.ball = factory.from_image(RESOURCES.get_path("ball.png"))
        self.running = True
        
        self.createSprites(players)
        self.addSprite(ball)
        
        spriterenderer = factory.create_sprite_render_system(window)       
        spriterenderer.render(self.sprites)
        
        
        while running:
            game.update()
            ###
            self.update()
            
            
    def getSize(self, sprite):
        """ Returns a 2 element list with the width and height in first and second
            entry, respectively
        """
        xSize = sprite.size[0]
        ySize = sprite.size[1]
        return[xSize, ySize]
    
    def move(self, sprite, x = None, y = None):
        """Changes a sprite's position to the input X and Y
        """
        if x is None and y is None:
            (x, y) = sprite.getPosition()
        (xSize, ySize) = getSize(sprite)
        
        x_min = FIELD_BOUNDS[0]
        x_max = FIELD_BOUNDS[1]
        y_min = FIELD_BOUNDS[2] 
        y_max = FIELD_BOUNDS[3]
            
        sprite.position = (floor(( x + x_max)*10-xSize/2), \
                           floor((-y + y_max)*10-ySize/2)  )
        
    def addSprite(self, sprite):
        self.sprites += [sprite]
        
        
    def createSprites(self, players):
        for player in players:
            if type(i) is Offender:
                sprite = factory.from_image(RESOURCES.get_path("redPlayer.png"))
            else: 
                sprite = factory.from_image(RESOURCES.get_path("bluePlayer.png"))
                
            self.player_sprites[player] = sprite
            self.addSprite(sprite)
            
    def update(self):
        events = sdl2.ext.get_events()
        for event in events:                #This for loop is not working
            if event.type == sdl2.SDL_QUIT:
                self.running = False
                break
            
        for player in self.players:
            sprite = self.player_sprites[player]
            (x, y) = player.getPosition()
            self.move(sprite, x, y)
            
        (x, y) = game.ball.getPosition()    
        self.move(self.ball, x, y)
        spriterenderer.render(sprites)
