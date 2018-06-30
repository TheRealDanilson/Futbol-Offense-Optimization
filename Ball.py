from constants import *

class Ball(object):
    """
    velocity    2 element list storing velocity with velocity(0) being velocity in the
            x-direction, and velocity(1) being velocity in the y-direction.
            Starting velocity is [0,0]
        
    position    2 element list storing position with position(0) being position in the
            x-direction, and position(1) being position in the y-direction.
            
    oldPosition 2 element list storing position from previous timestep with position(0) being
            position in the x-direction, and position(1) being position in the
            y-direction.

    possession  The instance of player who possesses the ball

    bounds      4 element tuple with bounds(0) being the min x coord (-35), bounds(1)
            being the max x coord (35), bounds(2) being the min y coord (0), and
            bounds(3) being the max y coord (50).
            Note: Goal Post positions are x = -4 and 4 y = 0.
    """

    def __init__(self, player):
        # constructor method for Ball
        self.position = player.getPosition()
        self.possession = player
        self.velocity = [0,0]
        self.bound = FIELD_BOUNDS
        self.oldPosition = self.position
        
    def isOutBounds(self):
        # returns True if ball is out of bounds or False if ball is in bounds
        # calculates the balls trajectory
        return self.position[0] < self.bound[0] or self.position[0] > self.bound[1] \
            or self.position[1] < self.bound[2] or self.position[1] > self.bound[3]
    
    def update(self):
        if self.possession is not None:
            self.velocity = self.possession.getVelocity()
        
    def move(self):
        # changes position by adding velocity x to position x and velocity y
        # to position y
        self.position[0] = self.position[0] + self.velocity[0]
        self.position[1] = self.position[1] + self.velocity[1]
    
    
    def getPosition(self):
        return self.position.copy()
        
    def isGoal(self):
        # returns True if the ball is a goal or False if not
        
        oldx = self.oldPosition[0]
        oldy = self.oldPosition[1]
        newx = self.oldPosition[0]
        newy = self.oldPosition[1]
        
        #calculating slope and b for y=mx+b starting with old coordinates
        slope = (newy - oldy)/(newx - oldx)
        b = oldy - slope*oldx
        
        #calculate x when y = 0
        travelx = -b/slope
        
        return -4 < travelx and travelx < 4
    
    
    def getPossession(self):
        # returns player instance who has ball
        return self.possession
    
    def setPossession(self, player):
        # changes player instance who has ball
        self.possession = player
        self.velocity = player.getVelocity()
    
    
    def shoot(self, direction):
        # changes ball's possession to None and changes the ball velocity to
        # input velocity
        self.possession = None
        self.velocity = direction
        
        
    
     
