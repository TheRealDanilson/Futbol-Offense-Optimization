from constants import *

class Player(object):
    """
    game - Stores the currently running game
    velocity - List containing the velocities in the x and y directions. X-velocity
                is stored as the first element of the list, and the y-velocity is
                stored as the second element of the list
    position - List containing the position in the x and y axes. X position
                is stored as the first element of the list, and the y positoin is
                stored as the second element of the list
    ball - Stores the game's ball
    bounds - Four element tuple storing the minimum and maximum bounds in the
            x and y directions
    passFactor - Constant number between LOWER and UPPER inclusive, represents the
        tendency to pass
    carefulness - Constant number between 1 and 4 inclusive, represents how 
                reserved a player is when making a pass
    optPassDist -  Constant number that represents the optimal distance 
               from a teammate the offense will pass either short, medium or long
    """
    
    def __init__(self, position, game, bounds = FIELD_BOUNDS):
        self.game = game
        self.ball = None
        self.position = position
        self.bounds = bounds
        self.velocity = [0, 0]
        
    def getPosition(self):
        return self.position
    
    def getVelocity(self):
        return self.velocity
    
    def getBounds(self):
        return self.bounds
    
    def removePossession(self):
        self.ball = None
        
    def getPossession(self, ball):
        self.ball = ball
    
    def shoot(self, position):
        """
            Attempts to shoot the ball to a specified location
            Returns True if the shot was made, returns False otherwise
        """
        if self.ball is None:
            return False
        self.ball.shoot(self, position)
        self.ball = None
        return True
    
    def move(self):
        self.oldPosition = self.position
        self.position[0] = self.position[0] + self.velocity[0]
        self.position[1] = self.position[1] + self.velocity[1]
        
    def genWeight(self, objective):
        return 0.5
        
    def update(self):
        Vx = self.velocity[0]
        Vy = self.velocity[1]
        dVx = 0
        dVy = 0
        for objective in Objectives:
            weight = self.genWeight(objective)
            if objective is Objectives.GOAL:
                vector = self.game.playerDistGoal(self)
                dVx += weight * vector[0]
                dVy += weight * vector[1]
        Vx += dVx
        Vy += dVy
        speed = (Vx**2 + Vy **2)**(0.5)
        if speed > MAX_SPEED:
            Vx *= MAX_SPEED/speed
            Vy *= MAX_SPEED/speed
        self.velocity = [Vx, Vy]
            
    
        
    

