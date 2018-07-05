from constants import *
from random import uniform, choice
from math import exp



def expcdf(x, mu):
    return 1 - exp(-x/mu)


class Player(object):
    """
    game        Stores the currently running game
    
    velocity    List containing the velocities in the x and y directions.
                X-velocity is stored as the first element of the list, and the
                y-velocity is stored as the second element of the list
                
    position    List containing the position in the x and y axes. X position
                is stored as the first element of the list, and the y positoin
                is stored as the second element of the list
                
    ball        Stores the game's ball
    
    bounds      Four element tuple storing the minimum and maximum bounds in the
                x and y directions
            
    passFactor  Constant number between LOWER and UPPER inclusive, represents
                the tendency to pass
        
    carefulness Constant number between 1 and 4 inclusive, represents how 
                reserved a player is when making a pass
                
    optPassDist Constant number that represents the optimal distance from a
                teammate the offense will pass either short, medium or long
    """
    
    def __init__(self, position, game, bounds = FIELD_BOUNDS):
        self.game = game
        self.ball = None
        self.position = position.copy()
        self.bounds = list(bounds)
        self.velocity = [0, 0]
        self.receiving = False
        self.justShot = False
        
    def getPosition(self):
        return self.position.copy()
    
    def getVelocity(self):
        return self.velocity.copy()
    
    def getBounds(self):
        return self.bounds.copy()
    
    def getPossession(self, ball):
        self.ball = ball
        
    def setToReceive(self):
        self.receiving = True
    
    
    def removePossession(self):
        self.ball = None
    
    def justShotBall(self):
        return self.justShot
    
    def shoot(self, position):
        """
        position    position of the player instance
        Removes possession from player and shoots the ball to center of goal
        """
        dX = position[0] - self.position[0]
        dY = position[1] - self.position[1]
        magnitude = (dX**2 + dY**2)**(0.5)
        direction = (dX/magnitude, dY/magnitude)
        self.ball.shoot(direction)
        self.removePossession()
        self.justShot = True
        print("test")
        
    def move(self):
        """
        Stores current position to old position and adds velocity to current
        position
        """
        self.oldPosition = self.position.copy()
        self.position[0] = self.position[0] + self.velocity[0]
        self.position[1] = self.position[1] + self.velocity[1]
        
    def genWeight(self, objective):
        return uniform(0, 1)                     #Dummy Weight
    
    def pickPlayer(self):
        """
        Returns a Player instance to pass to
        """
        return choice(self.game.playerTeam(self))
            
    def calcShootProb(self):
        """
        Returns the probability of shooting
        """
        x = self.position[0]
        y = self.position[1]
        z = (x**2)/150 +(y**2)/300;
        if z >= 4.5 or (x**2)/y > 30:
            p = 0.0
        elif (x**2 + y**2)**(0.5) <= 5:
            p = 1.0
        else:
            p = expcdf((4.5-z),1)
        return p
    
    
    def receive(self, ball):
        self.ball = ball
        self.receiving = False
    
    
    def hasBall(self):
        return self.ball is not None
    
    
    def passBall(self, player):
        # player - player instance of class Player
        
        print("passTest")
        if self is not player:
            player.setToReceive()
            self.shoot(player.getPosition())
    
        
    def shootPassKeep(self):
        """
        Decides if player shoots the ball, passes the ball, or keeps the ball
        and performs the chosen action
        """
        if self.ball is not None:       #Making sure player has the ball
            shootProb = self.calcShootProb()
            rand = uniform(0, 1)                   #Randon decimal between 0 and 1
            if rand <= shootProb:       #Decides if to shoot
                self.shoot(GOAL_POS)      
            else:                       #Decides which Player instance to pass to
                player = self.pickPlayer()
                self.passBall(player)    
    
    
    def createVector(self, weight, vector):
        """
        vector - list of length 2.  Entry 0 is x and entry 1 is y
        weight - real number
        Returns  list (vector x weight) of length 2, entry 0 is x and entry y is 1
        """
        dummy = [0, 0]
        dummy[0] = vector[0] * weight 
        dummy[1] = vector[1] * weight
        return dummy
    
    
    def calcVector(self, objective):
        """
        objective - enumerations from the Objectives Class in constants.py
        Returns a list of length 2 that corresponds to the weighted vector
        between a player and the objective.  Entry 0 is x and entry 1 is y.
        """
        weight = self.genWeight(objective)
        if objective is Objectives.GOAL:
            return self.createVector(weight, self.game.playerDistGoal(self))
        elif objective is Objectives.TEAMMATES:
            team = self.game.playerTeam(self)
            vector = [0, 0]
            for teammate in team:
                mateVector = self.createVector(-weight, self.game.playerDistPlayer(self, teammate))
                self.addVectors(vector, mateVector)
            return vector
        elif objective is Objectives.ZONE_CENTER:
            return self.createVector(3*weight, self.game.playerDistZone(self))
        return [0, 0]
                
    def addVectors(self, finalVector, vector):
        """
        Adds vector (list length 2) to finalVector (list length 2)
        """
        finalVector[0] = finalVector[0] + vector[0]
        finalVector[1] = finalVector[1] + vector[1]
    
    
    def update(self):
        """
        First decides a players action (shoot, pass, keep) then updates the
        player's velocity if they are not receiving the ball.
        """
        self.justShot = False
        self.shootPassKeep()
        finalVector = [0, 0]
        if self.receiving is not True:
            for objective in Objectives:
                vector = self.calcVector(objective)
                self.addVectors(finalVector, vector)
            speed = (finalVector[0]**2 + finalVector[1]**2)**(0.5)
            if speed > MAX_SPEED:
                finalVector[0] *= MAX_SPEED/speed
                finalVector[1] *= MAX_SPEED/speed
        self.velocity = finalVector
        
            
   
    # test for push pull
    # can you guys read this
    


class Offender(Player):
    """ Subclass of Player
            
    """
    
    def __init__(self, position, game, bounds = FIELD_BOUNDS):
        super().__init__(position, game, bounds)
