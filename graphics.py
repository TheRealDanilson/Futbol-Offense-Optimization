import sys
import sdl2.ext
from Game import Game
from Player import *
from constants import *
from math import floor
from Ball import *

RESOURCES = sdl2.ext.Resources(__file__, "Images")

class Graphics(object):
    
    def __init__(self, game):
        #SDL2 Specific
        sdl2.ext.init()
        window = sdl2.ext.Window("Futbol Offense Optimization", size=(910, 610))
        window.show()
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        # Creating Attributes
        self.game = game
        self.players = self.game.playerList()
        self.player_sprites = {}
        self.sprites = []
        self.background = factory.from_image(RESOURCES.get_path("soccerField.png"))
        self.ball = factory.from_image(RESOURCES.get_path("ball.png"))
        self.running = True
        # Creating and Adding Sprites
        self.addSprite(self.background)
        self.createSprites(self.players, factory)
        self.addSprite(self.ball)
        # Rendering
        self.spriterenderer = factory.create_sprite_render_system(window)       
            
            
    def getSize(self, sprite):
        """
        sprite - object used to represent an image
        Returns a 2 element tuple with the width and height in first and second
        entry, respectively
        """
        width = sprite.size[0]
        height = sprite.size[1]
        return (width, height)
    
    
    def move(self, sprite, x, y):
        """
        sprite - object used to represent an image
        x - real number
        y - real number
        Changes a sprite's position to the input x and y and uses the size of
        the sprite to realign sprite so it is printed in it's "center"
        """
        (xSize, ySize) = self.getSize(sprite)
        
        x_min = FIELD_BOUNDS[0]
        x_max = FIELD_BOUNDS[1]
        y_min = FIELD_BOUNDS[2] 
        y_max = FIELD_BOUNDS[3]
            
        sprite.position = (floor(( x + x_max)*10-xSize/2), \
                           floor((-y + y_max)*10-ySize/2)  )
        
        
    def addSprite(self, sprite):
        """
        sprite - object used to represent an image
        Adds the input sprite (sprite) to the sprites attribute (list)
        """
        self.sprites += [sprite]
        
        
    def createSprites(self, players, factory):
        """
        players - list of players
        factory - special object that creates sprite from image
        Assigns a sprite depending on if player is offender or defender and then
        adds the sprite to the player_sprites attribute (dictionary) and to
        sprite attribute (list)
        """
        for player in players:
            if type(player) is Offender:
                sprite = factory.from_image(RESOURCES.get_path("redPlayer.png"))
            else: 
                sprite = factory.from_image(RESOURCES.get_path("bluePlayer.png"))
                
            self.player_sprites[player] = sprite
            self.addSprite(sprite)
           
            
    def update(self):
        """
        First for loop is used to check if user closes application window, and
        if so then quits.
        Second for loop moves each sprite to their associated player's position.
        At the end all sprites are rendered.
        """
        events = sdl2.ext.get_events()
        for event in events:                #This for loop is not working
            if event.type == sdl2.SDL_QUIT:
                self.running = False
                break
            
        for player in self.players:
            sprite = self.player_sprites[player]
            (x, y) = player.getPosition()
            self.move(sprite, x, y)
            
        (x, y) = self.game.ball.getPosition()    
        self.move(self.ball, x, y)
        self.spriterenderer.render(self.sprites)
