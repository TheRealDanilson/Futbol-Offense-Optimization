from constants import *
from random import uniform, choices
from math import exp
from time import sleep

    
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
                
    receiving   Boolean: True if player is receiving ball. False otherwise
    
    justShot    Boolean: True if player shot/passed the ball within last
                timestep.  False otherwise.
    """
    
    
    def __init__(self, position, game, bounds = FIELD_BOUNDS):
        """
        Constructor Method for player class
        """
        self.game = game
        self.ball = None
        self.position = position.copy()
        self.bounds = list(bounds)
        self.velocity = [0, 0]
        self.receiving = False
        self.justShot = False
        
        
    def getPosition(self):
        """
        Returns a copy of the position attribute (list of length 2) 
        """
        return self.position.copy()
    
    
    def getVelocity(self):
        """
        Returns a copy of the velocity attribute (list of length 2) 
        """
        return self.velocity.copy()
    
    
    def getBounds(self):
        """
        Returns a copy of the bounds attribute (4 element tuple)
        """
        return self.bounds.copy()
    
    
    def setPossession(self, ball):
        """
        ball - game's ball instance
        
        Changes the ball's attribute to the game's ball instance
        """
        self.ball = ball
        
        
    def setToReceive(self):
        """
        Changes receiving attribute to True
        """
        self.receiving = True
    
    
    def removePossession(self):
        """
        Changes ball attribute to None
        """
        self.ball = None
    
    
    def justShotBall(self):
        """
        Return the attribute justShot (Boolean)
        """
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
        #sleep(3)
        
        
    def move(self):
        """
        Stores current position to old position and adds velocity to current
        position
        """
        self.oldPosition = self.position.copy()
        self.position[0] = self.position[0] + self.velocity[0]
        self.position[1] = self.position[1] + self.velocity[1]
        
           
    def calcDistProbs(self):
        """
        DANIELSON/TOMMYTORNADO PLEASE DO THIS
        """
        probabilities = {}
        team = self.game.playerTeam(self)
        playerPos = self.getPosition()
        b = playerPos[0]**2/150 + playerPos[1]**2/300
        for teammate in team:
            if teammate is not self:
                matePos = teammate.getPosition()
                a = matePos[0]**2/150 + playerPos[1]**2/300
                dist = self.game.playerDistPlayer(self, teammate)
                d = (dist[0]**2 + dist[1]**2)**(0.5)
                z = (a - b + 16)/16 + abs(d - 15)/15
                p = expcdf((6-z),1)
                probabilities[teammate] = p
        
        return probabilities
                
    
    def calcOpenness(self):
        """
        DANIELSON/TOMMYTORNADO PLEASE DO THIS
        """
        openness = {}
        u = self.game.nearestOpponent(self)[1]
        team = self.game.playerTeam(self)
        for teammate in team:
            if teammate is not self:
                m = self.game.nearestOpponent(self)[1]
                p = self.game.nearestOpponentToLine(type(self),\
                    self.getPosition(), teammate.getPosition())[1]
                try:
                    z = m*p/u**2
                    print('Z is: ' + str(z))
                    o = expcdf((4.5-z),1)
                except:
                    print('Set o to 0')
                    o = 0
                openness[teammate] = o
        return openness
        
        
    def pickPlayer(self):
        """
        Returns a Player instance to pass to
        
        This function calculates *who* this player will pass to, if he is about
        to pass.  It uses a Z-score from the distances and positions of other
        players, with respect to this player.

        Note: This chooses who to pass to if and only if this player has chosen
        to pass at all.
        """
        D = self.calcDistProbs()
        O = self.calcOpenness()
        probabilities = {}
        team = self.game.playerTeam(self)
        for teammate in team:
            if teammate is not self:
                probabilities[teammate] = (D[teammate] + OPENNESS*O\
                                           [teammate])/(1 + OPENNESS)
        P = 0.0
        for teammate in probabilities:
            P += probabilities[teammate]
        probabilities[self] = 1 - P/(len(team) - 1)
        #Debugging
        print(team)
        print(list(probabilities.values()))
        a = choices(team, weights=list(probabilities.values()), k=1)[0]
        print(a)
        return a
        
        
    def calcShootProb(self):
        """
        Returns the probability of shooting (real number between 0 and 1)
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
        """
        ball - current game's ball instance
        
        Sets ball attribute to the game's ball instance and the receiving
        attribute to False
        """
        self.ball = ball
        self.receiving = False
    
    
    def hasBall(self):
        """
        Returns True if player has ball and False otherwise
        """
        return self.ball is not None
    
    
    def passBall(self, player):
        """
        player - player instance of class Player who receives the ball
        
        Sets the player input's attribute receiving to True and passes the ball
        to the input player's position
        """
        print("passTest")
        if self is not player:
            player.setToReceive()
            self.shoot(player.getPosition())
    
        
    def shootPassKeep(self):
        """
        Decides if player shoots the ball, passes the ball, or keeps the ball
        and performs the chosen action
        """
        if self.hasBall():              #Making sure player has the ball
            shootProb = self.calcShootProb()
            rand = uniform(0, 1)        #Randon decimal between 0 and 1
            if rand <= shootProb:       #Decides if to shoot
                self.shoot(GOAL_POS)      
            else:                       #Decides which Player inst. to pass to
                player = self.pickPlayer()
                self.passBall(player)    
    
    
    def createVector(self, weight, vector):
        """
        vector - list of length 2.  Entry 0 is x and entry 1 is y
        weight - real number
        Returns list (vector x weight) of length 2, entry 0 is x and entry y is 1
        """
        return (weight * vector[0], weight * vector[1])
    
    
    def genWeight(self, objective):
        """
        Returns random number between 0 and 1
        """
        return uniform(0, 1)
    
    
    def magnitudeAndDirection(self, vector):
        """
        vector - 2 element tuple representing a vector
        
        Returns a 2 element tuple with the magnitude (real number ) and
        direction (unit vector pointing in direction of vector) in the first and
        second entry, respectively.
        """
        magnitude = (vector[0]**2 + vector[1]**2)**(0.5)
        try:
            direction = (vector[0]/magnitude, vector[1]/magnitude)
        except:
            direction = (0, 0)
        return (magnitude, direction)
    
    
    def calcVector(self, objective):
        """
        objective - enumerations from the Objectives Class in constants.py
        Returns a list of length 2 that corresponds to the weighted vector
        between a player and the objective.  Entry 0 is x and entry 1 is y.
        """
        weight = self.genWeight(objective)
        if objective is Objectives.GOAL:
            (dist, direction) = self.magnitudeAndDirection(self.game.playerDistGoal(self))
            weight = uniform(0,1)*dist
            return self.createVector(weight, direction)
#        elif objective is Objectives.TEAMMATES:
#            team = self.game.playerTeam(self)
#            vector = [0, 0]
#            for teammate in team:
#                if teammate is not self:
#                    (dist, direction) = self.magnitudeAndDirection(self.game.playerDistPlayer(self, teammate))
#                    weight = -1/(dist+1)
#                    mateVector = self.createVector(weight, direction)
#                    self.addVectors(vector, mateVector)
            return (vector[0], vector[1])
        elif objective is Objectives.ZONE_CENTER:
            (dist, direction) = self.magnitudeAndDirection(self.game.playerDistZone(self))
            weight = dist**1.35
            return self.createVector(weight, direction)
        elif objective is Objectives.OPPONENTS:
            opponentTeam = self.game.playerOpponentTeam(self)
            vector = [0, 0]
            for opponent in opponentTeam:
                    (dist, direction) = self.magnitudeAndDirection(self.game.playerDistPlayer(self, opponent))
                    weight = -10/(dist + 1)
                    if self.hasBall():
                        weight *= 10
                    mateVector = self.createVector(weight, direction)
                    self.addVectors(vector, mateVector)
            return (vector[0], vector[1])
        elif objective is Objectives.BALL:
            ballDist = self.game.playerDistBall(self)
            (dist, direction) = self.magnitudeAndDirection(ballDist)
            weight = 15/(dist + 1)
            if self.receiving:
                weight *= 10
            return self.createVector(weight, direction)
        
        return (0, 0)
              
                
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
        for objective in Objectives:
            vector = self.calcVector(objective)
            self.addVectors(finalVector, vector)
        speed = (finalVector[0]**2 + finalVector[1]**2)**(0.5)
        if speed > MAX_SPEED:
            finalVector[0] *= MAX_SPEED/speed
            finalVector[1] *= MAX_SPEED/speed
        self.velocity = finalVector


class Offender(Player):
    """
    Subclass of Player    
    """

    
    def __init__(self, position, game, bounds = FIELD_BOUNDS):
        """
        Constructor method for offender
        """
        super().__init__(position, game, bounds)


class Defender(Player):
    """
    Subclass of Player
    """
    
    
    def __init__(self, position, game, bounds = FIELD_BOUNDS):
        """
        Constructor method for defender
        """
        super().__init__(position, game, bounds)
        
        
    def calcVector(self, objective):
        """
        objective - enumerations from the Objectives Class in constants.py
        Returns a list of length 2 that corresponds to the weighted vector
        between a player and the objective.  Entry 0 is x and entry 1 is y.
        """
        weight = self.genWeight(objective)
        if objective is Objectives.GOAL:
            (dist, direction) = self.magnitudeAndDirection(self.game.playerDistGoal(self))
            weight = dist
            return self.createVector(weight, direction)
        elif objective is Objectives.ZONE_CENTER:
            (dist, direction) = self.magnitudeAndDirection(self.game.playerDistZone(self))
            weight = dist**1.15
            return self.createVector(weight, direction)
        elif objective is Objectives.OPPONENTS:
            (nearestOpponent, dist) = self.game.nearestOpponent(self)
            return self.game.playerDistPlayer(self, nearestOpponent)
        elif objective is Objectives.BALL:
            ballDist = self.game.playerDistBall(self)
            (dist, direction) = self.magnitudeAndDirection(ballDist)
            weight = 15/(dist + 1)
            return self.createVector(weight, direction)
        return (0, 0)
