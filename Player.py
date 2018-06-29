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
            Notifies the player being s
        """
       
    
    def move(self):
        self.oldPosition = self.position
        self.position[0] = self.position[0] + self.velocity[0]
        self.position[1] = self.position[1] + self.velocity[1]
        
    def genWeight(self, objective):
        return 0.5
        
    def update(self):
        Vx = 0
        Vy = 0
        
        for objective in Objectives:
            weight = self.genWeight(objective)
            if objective is Objectives.GOAL:
                vector = self.game.playerDistGoal(self)
                Vx += weight * vector[0]
                Vy += weight * vector[1]
            elif objective is Objectives.TEAMMATES:
                team = self.game.playerTeam(self)
                for teammate in team:
                    vector = self.game.playerDistPlayer(self, teammate)
                    Vx += weight * -vector[0]
                    Vy += weight * -vector[1]
                
        speed = (Vx**2 + Vy**2)**(0.5)
        if speed > MAX_SPEED:
            Vx *= MAX_SPEED/speed
            Vy *= MAX_SPEED/speed
        self.velocity = [Vx, Vy]
            
    def shootPassKeep(self):
        "Decides if player shoots the ball, passes the ball, or keeps the ball"
        #Making sure player has the ball
        if self.ball is not None:
            
            shootProb = self.calcShootProb()
            passProb = self.calcPassProb()
            rand = .3 #selecting randon number
            
                if rand <= shootProb:
                    
                    self.shoot(GOAL_POS)
                    
                else
                    player = self.pickPlayer()
                    self.pass(player)
                    
    def calcPassingProb
        "Returns a list of length TEAM_SIZE with the probabilities range of passing to each player, including the player with the ball"
        return (.2,.4,.6,.8,1)
                    
    def calcPassProb(self)
        "Returns the probability of passing"
        return .5
            
    def calcShootProb(self):
        "Returns the probability of shooting"
        probability = .5
        return probability
    
        
    

