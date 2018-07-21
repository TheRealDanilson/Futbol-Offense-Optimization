from constants import *

class Ball(object):
    """
    velocity     2 element list storing velocity with velocity(0) being velocity
                 in the x-direction, and velocity(1) being velocity in the
                 y-direction. Starting velocity is [0,0]
                 
    position     2 element list storing position with position(0) being position
                 in the x-direction, and position(1) being position in the
                 y-direction.
                 
    oldPosition  2 element list storing position from previous timestep with
                 position(0) being position in the x-direction, and position(1)
                 being position in the y-direction.

    possession   The instance of player who possesses the ball

    bounds       4 element tuple with bounds(0) being the min x coord (-35),
                 bounds(1) being the max x coord (35), bounds(2) being the min
                 y coord (0), and bounds(3) being the max y coord (50).
                 Note: Goal Post positions are x = -4 and 4 y = 0.
                 
    shooter     To add
    """


    def __init__(self, player):
        """
        Constructor method for Ball
        """
        self.position = player.position
        self.possession = player
        self.velocity = [0,0]
        self.bounds = FIELD_BOUNDS
        self.oldPosition = self.position
        self.receiving = False
        self.shooter = None
        self.towardGoal = False
        
        
    def getPosition(self):
        """
        Returns a copy of the ball's position attribute (2 element list)
        """
        return self.position.copy()
    
    def getSpeed(self):
        speed = (self.velocity[0]**2 + self.velocity[1]**2)**(0.5)
        return speed
    
    def getOldPosition(self):
        return self.oldPosition.copy()

    def getPossession(self):
        """
        Returns ball's possession attribute (player instance)
        """
        return self.possession
    
    
    def getShooter(self):
        return self.shooter
    
    
    def setPossession(self, player):
        """
        Changes ball's possession attribute to the input player instance
        """
        self.possession = player
        self.velocity = player.getVelocity()
        self.position = player.position
        self.shooter = None
    
          
    def isOutBounds(self):
        """
        Returns True if ball is out of bounds or False if ball is in bounds. 
        This is done by checking to see if the ball's x and y coordinates are
        within the min and max x and y coordinates stored in the bounds attribute
        """
        return self.position[0] < self.bounds[0] \
            or self.position[0] > self.bounds[1] \
            or self.position[1] < self.bounds[2] \
            or self.position[1] > self.bounds[3] 
            
    
    def update(self):
        """
        If the ball is possessed, this method changes the ball's velocity to the
        velocity of the player instance that possesses it
        """
        
        if self.possession is not None:
            self.velocity = self.possession.getVelocity()
        else:
            try:
                speed = (self.velocity[0]**2 + self.velocity[1]**2)**(0.5)
                accel = self.velocity[0]*dcel/speed, self.velocity[1]*dcel/speed
                self.velocity[0] = self.velocity[0] + accel[0]
                self.velocity[1] = self.velocity[1] + accel[1]
            except:
                pass
        
        
        
    def move(self):
        """
        Changes ball's position by adding velocity x to position x and
        velocity y to position y
        """
        self.oldPosition = self.position.copy()
        if self.possession is None:
            self.position[0] = self.position[0] + self.velocity[0] #changing x
            self.position[1] = self.position[1] + self.velocity[1] #changing y
    

    def isGoal(self):
        """
        Returns True if the ball is a goal or False if it is not
        """
        oldx = self.oldPosition[0]
        oldy = self.oldPosition[1]
        newx = self.position[0]
        newy = self.position[1]
        
        try:
            slope = (newy - oldy)/(newx - oldx) #Calculating slope (m) in y=mx+b 
            b = oldy - slope*oldx               #Calculating b in y=mx+b
            travelx = -b/slope                  #Calculate x when y = 0
            return -4 < travelx and travelx < 4 and newy <= 0 #True if ball is between goal posts
        except:
            return -4 < newx and newx < 4 and newy <= 0
    
    
    def shoot(self, direction, blocked = False):
        """
        Changes ball's possession to None and changes the ball velocity to
        input velocity
        """
        if not blocked:
            self.shooter = self.possession
        self.possession = None
        self.position = self.position.copy()
        self.velocity = [direction[0] * 2*MAX_SPEED, direction[1] * 2*MAX_SPEED]
        
        
    
     
