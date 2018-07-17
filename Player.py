from constants import *
from random import uniform, choices, seed
from math import exp
from time import sleep

    
def expcdf(x, mu):
    return 1 - exp(-x/mu)


def randSelect(dct):
    seed()
    temp = dct.copy()
    W = sum(temp.values())
    for key in temp:
        temp[key] /= W
    randNumber = uniform(0, 1)
    for key in temp:
        p = temp[key]
        if randNumber <= p:
            return key
        randNumber -= p
    return key


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
                
    oldPosition 2 element list storing position from previous timestep with
                position(0) being position in the x-direction, and position(1)
                being position in the y-direction.
    """
    
    
    def __init__(self, position, game, bounds = FIELD_BOUNDS, name = 'N/A'):
        """
        Constructor Method for player class
        """
        self.game = game
        self.name = name
        self.ball = None
        self.position = position.copy()
        self.bounds = list(bounds)
        self.velocity = [0, 0]
        self.receiving = False
        self.justShot = False
        self.oldPosition = position.copy()
        self.keeping = 0
        self.randomCount = 0
        self.randomVector = [1,1]
        self.players = []
        
    # def getRandonVector(self):
    #     return self.randomVector
    # 
    # def setRandomVector(self, vector):
    #     self.randomVector = vector
    #     
    # def getRandom(self):
    #     return self.random
    # 
    # def setRandom(self, integer):
    #     self.random = integer
    def setPlayers(self,playerlist):
        self.players = playerlist
        
    def getPosition(self):
        """
        Returns a copy of the position attribute (list of length 2) 
        """
        return self.position.copy()
    
    def getOldPosition(self):
        """
        Returns a copy of the oldPosition attribute (list of length 2)
        """
        return self.oldPosition.copy()
    
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
        if position[1] == 0 and abs(position[0]) < 4:
            dX = position[0] - self.position[0] + (self.position[0]/7.5 + uniform(-5,5))
            dY = position[1] - self.position[1]
            magnitude = .5*(dX**2 + dY**2)**(0.5)
            direction = (dX/magnitude, dY/magnitude)
            self.ball.towardGoal = True
        else:
            dX = position[0] - self.position[0]
            dY = position[1] - self.position[1]
            magnitude = (dX**2 + dY**2)**(0.5)
            direction = (dX/magnitude, dY/magnitude)
        self.ball.shoot(direction)
        self.removePossession()
        self.justShot = True
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
        b = playerPos[0]**2/300 + playerPos[1]**2/150
        for teammate in team:
            if teammate is not self:
                matePos = teammate.getPosition()
                a = matePos[0]**2/300 + playerPos[1]**2/150
                dist = self.game.playerDistPlayer(self, teammate)
                d = (dist[0]**2 + dist[1]**2)**(0.5)
                f = (b - a + 7)/7
                l = 2 - 4*abs(d - opt_pass)/(((2*FIELD_BOUNDS[1])**2 + FIELD_BOUNDS[3]**2)**.5 - opt_pass) 
                p = FORWARDNESS*expcdf((f),1.44) + LENGTHINESS*expcdf((l),1.44)
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
                m = self.game.nearestOpponent(teammate)[1]
                p = self.game.nearestOpponentToLine(type(self),\
                    self.getPosition(), teammate.getPosition())[1]
                try:
                    #z = m*p/u**2
                    z = p*(m - u + 20)/pass_factor
                    #z = p/u
                    #z = u**2/(m*p)
                    if z > 0:
                        o = expcdf((z),1.44)
                    else:
                        o = 0
                except:
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
                                           [teammate])/(LENGTHINESS + OPENNESS + FORWARDNESS)
        P = sum(probabilities.values())
        probabilities[self] = len(team)-P
        #probabilities[self] = 0
        #Debugging
        #a = choices(team, weights=list(probabilities.values()), k=1)[0]
        a = randSelect(probabilities)
        return a
        
        
    def calcShootProb(self):
        """
        Returns the probability of shooting (real number between 0 and 1)
        """
        defendMinY = float('inf')
        for member in self.players:
            if isinstance(member, Defender):
                memberY = member.getPosition()[1]
                if memberY < defendMinY:
                    defendMinY = memberY
                if  self.hasBall() and self.getPosition()[1] < defendMinY:
                    p = 1
        x = self.position[0]
        y = self.position[1]
        z = (x**2)/300 +(y**2)/150;
        if z >= 5.5 or (x**2)/y > 50:
            p = 0.0
        elif (x**2 + y**2)**(0.5) <= 10:
            p = 1.0
        else:
            p = expcdf((5.5 - z),4.3)/2.75
        return p
     
    
    def receive(self, ball):
        """
        ball - current game's ball instance
        
        Sets ball attribute to the game's ball instance and the receiving
        attribute to False
        """
        if self.ball is None:
            self.ball = ball
        if ball is not None:
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
                if player is self:
                    self.keeping = int(uniform(50, 150))
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
       #  weight = self.genWeight(objective)
       #  #if objective is Objectives.GOAL:
       #   #   (dist, direction) = self.magnitudeAndDirection(self.game.playerDistGoal(self))
       #  #    weight = uniform(0,1)*dist
       # #     return self.createVector(weight, direction)
       #  if objective is Objectives.ZONE_CENTER:
       #      (dist, direction) = self.magnitudeAndDirection(self.game.playerDistZone(self))
       #      weight = dist
       #      return self.createVector(weight, direction)
       #  elif objective is Objectives.OPPONENTS:
       #      opponentTeam = self.game.playerOpponentTeam(self)
       #      vector = [0, 0]
       #      for opponent in opponentTeam:
       #              (dist, direction) = self.magnitudeAndDirection(self.game.playerDistPlayer(self, opponent))
       #              weight = -10/(dist + 1)
       #              if self.hasBall():
       #                  weight *= 10
       #              mateVector = self.createVector(weight, direction)
       #              self.addVectors(vector, mateVector)
       #      return (vector[0], vector[1])
       #  elif objective is Objectives.BALL:
       #      ballDist = self.game.playerDistBall(self)
       #      (dist, direction) = self.magnitudeAndDirection(ballDist)
       #      weight = 15/(dist + 1)
       #      if self.receiving:
       #          weight *= 10
       #      return self.createVector(weight, direction)
       #  elif objective is Objectives.Shift:
       #      ballPos = self.ball.getPosition()
       #      if ballPos[0] > 10:
       #          direction[0] = 4
       #      elif ballPos[0] < -10:
       #          direction[0] = -4 
       #      else:
       #           direction[0] = 0
       #      if ballPos[1] > 30:
       #          direction[1] = 4
       #      else:
       #          direction[1] = 0
       #      weight = 100
       #      return self.createVector(weight, direction)
       #  
       #  return (0, 0)
              
                
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
        if self.keeping > 0:
            self.keeping -= 1
        else:
            self.shootPassKeep()

        finalVector = self.velocity
        (dist, direction) = self.magnitudeAndDirection(self.game.playerDistBall(self))
        if self.receiving:
             if dist < ZONE_THRESHOLD:
                 weight = .01
                 finalVector = [weight*direction[0], weight*direction[1]]
             else:
                 weight = .9
                 finalVector = [weight*direction[0], weight*direction[1]]
        else:
            for objective in Objectives:
                vector = self.calcVector(objective)
                self.addVectors(finalVector, vector)
                
        speed = (finalVector[0]**2 + finalVector[1]**2)**(0.5)
        if speed > MAX_SPEED:
            finalVector[0] *= MAX_SPEED/speed
            finalVector[1] *= MAX_SPEED/speed
            
        #if speed <= MAX_SPEED*.2:
        #    finalVector[0] += 100*MAX_SPEED
        #    finalVector[1] += 100*MAX_SPEED
        
        futureX = self.position[0] + finalVector[0]
        futureY = self.position[1] + finalVector[1]
        
        if futureX < FIELD_BOUNDS[0] or futureX > FIELD_BOUNDS[1]:
            finalVector[0] = -finalVector[0]
        elif futureY < FIELD_BOUNDS[2] or futureY > FIELD_BOUNDS[3]:
            finalVector[1] = -finalVector[1]
    
        self.velocity = finalVector


class Offender(Player):
    """
    Subclass of Player    
    """

    
    def __init__(self, position, game, bounds = FIELD_BOUNDS, name = 'N/A'):
        """
        Constructor method for offender
        """
        super().__init__(position, game, bounds, name)
        
        
        
    def calcVector(self, objective):
        """
        objective - enumerations from the Objectives Class in constants.py
        Returns a list of length 2 that corresponds to the weighted vector
        between a player and the objective.  Entry 0 is x and entry 1 is y.
        """
        weight = self.genWeight(objective)
        ball = self.getPosition()
        playerPos = self.getPosition()
        if self.game.getBlocked():
            ballDist = self.game.playerDistBall(self)
            (forget, direction) = self.magnitudeAndDirection(ballDist)
            if forget <= 5:
                weight = 10
                return self.createVector(weight, direction)
            elif objective is Objectives.ZONE_CENTER:
                (dist, direction) = self.magnitudeAndDirection(self.game.playerDistZone(self))
                # if dist < ZONE_THRESHOLD/2:
                #    weight = 0
                # else:
                weight = dist**2
                return self.createVector(weight, direction)
            elif objective is Objectives.BALL:
                ballDist = self.game.playerDistBall(self)
                (dist, direction) = self.magnitudeAndDirection(ballDist)
                if dist <= ZONE_THRESHOLD:
                    weight = 15
                return self.createVector(weight, direction)
            if self.hasBall():
                self.game.blocked = False
        else:
            if objective is Objectives.GOAL:
                (dist, direction) = self.magnitudeAndDirection(self.game.playerDistGoal(self))
                weight = dist
                return self.createVector(weight, direction)
            if objective is Objectives.ZONE_CENTER:
                (dist, direction) = self.magnitudeAndDirection(self.game.playerDistZone(self))
                # if dist < ZONE_THRESHOLD/2:
                #    weight = 0
                # else:
                weight = dist**2
                return self.createVector(weight, direction)
            elif objective is Objectives.OPPONENTS:
                #opponentTeam = self.game.playerOpponentTeam(self)
                nearestOpponent = self.game.nearestOpponent(self)[0]
                (dist, direction) = self.magnitudeAndDirection(self.game.playerDistPlayer(self, nearestOpponent))
                weight = -20/(dist + 1)
                if self.hasBall():
                    weight *= 20
                return (direction[0] * weight, direction[1] * weight)
                # for opponent in opponentTeam:
                #         (dist, direction) = self.magnitudeAndDirection(self.game.playerDistPlayer(self, opponent))
                #         weight = -10/(dist + 1)
                #         if opponent is nearestOpponent:
                #             weight *= 2
                #         if self.hasBall():
                #             weight *= 10
                #         mateVector = self.createVector(weight, direction)
                #         self.addVectors(vector, mateVector)
                # return (vector[0], vector[1])
            elif objective is Objectives.BALL:
                ballDist = self.game.playerDistBall(self)
                (dist, direction) = self.magnitudeAndDirection(ballDist)
                weight = 15/(dist + 1)
                if dist <= 2*ZONE_THRESHOLD:
                    weight = 15 
                if self.receiving:
                    weight = 10 
            elif objective is Objectives.TEAMMATES:
                Team = self.game.playerTeam(self)
                vector = [0, 0]
                nearestTeammate = self.game.nearestTeammate(self)[0]
                for mate in Team:
                        (dist, direction) = self.magnitudeAndDirection(self.game.playerDistPlayer(self, mate))
                        weight = -1*(75/(dist + 1))**2
                        if mate is nearestTeammate:
                            weight *= 20
                        if self.hasBall():
                            weight *= 20
                        mateVector = self.createVector(weight, direction)
                        self.addVectors(vector, mateVector)
                return (vector[0], vector[1])
            elif ball[0] > 25 and playerPos[0] > 25:
                direction = (0,-1)
                weight = 50
                return self.createVector(weight, direction)
            elif ball[0] < -25 and playerPos[0] < -25:
                direction = (0,-1)
                weight = 50
                return self.createVector(weight, direction)
            elif objective is Objectives.RANDOM:
                if self.randomCount > RANDOM_TIME:
                    vector = (uniform(-1,1),uniform(-1,1))
                    weight = 60
                    self.randomVector = self.createVector(weight, vector)
                    self.randomCount = 0
                    return self.randomVector
                else:
                    self.randomCount += 1
                if abs(playerPos[0]) > 40 or playerPos[1] > 55 and self.hasBall():
                    weight *= 5
                    return(self.randomVector)
            elif objective is Objectives.OFF_SIDES:
                defendMinY = float('inf')
                for member in self.players:
                    if isinstance(member, Defender):
                        memberY = member.getPosition()[1]
                        if memberY < defendMinY:
                            defendMinY = memberY
                if  not self.receiving and not self.hasBall() and self.getPosition()[1] < defendMinY:
                    weight = 100
                    vector = [0, weight]
                    return(vector)
                
        return (0, 0)

class Defender(Player):
    """
    Subclass of Player
    """
    
    
    def __init__(self, position, game, bounds = FIELD_BOUNDS, name = 'N/A'):
        """
        Constructor method for defender
        """
        super().__init__(position, game, bounds, name)


    def shootPassKeep(self):
        pass
        # rand = uniform(0,100)
        # if self.hasBall():
        #     if self.ball.getSpeed() > 3*MAX_SPEED:
        #         self.shoot(uniform(-35,35),uniform(0,60))
        #     elif self.ball.getSpeed() >= 2*MAX_SPEED and rand >= 50:
        #         self.shoot(uniform(-35,35),uniform(0,60))
        #     else:
        #         self.keeping = int(uniform(50, 150))
            
    
        
    def calcVector(self, objective):
        """
        objective - enumerations from the Objectives Class in constants.py
        Returns a list of length 2 that corresponds to the weighted vector
        between a player and the objective.  Entry 0 is x and entry 1 is y.
        """
        weight = self.genWeight(objective)
        ballDist = self.game.playerDistBall(self)
        (forget, direction) = self.magnitudeAndDirection(ballDist)
        if forget <= 5:
            weight = 10
            return self.createVector(weight, direction)
        else:
            if objective is Objectives.GOAL:
                (dist, direction) = self.magnitudeAndDirection(self.game.playerDistGoal(self))
                weight = (dist/10)**2
                return self.createVector(weight, direction)
            elif objective is Objectives.ZONE_CENTER:
                (dist, direction) = self.magnitudeAndDirection(self.game.playerDistZone(self))
                weight = dist**2
                return self.createVector(weight, direction)
            elif objective is Objectives.OPPONENTS:
                opponentTeam = self.game.playerOpponentTeam(self)
                vector = [0, 0]
                nearestOpponent = self.game.nearestOpponent(self)[0]
                for opponent in opponentTeam:
                        (dist, direction) = self.magnitudeAndDirection(self.game.playerDistPlayer(self, opponent))
                        weight = -15/(dist + 1)
                        if opponent is nearestOpponent:
                            weight *= -4
                        if self.hasBall():
                            weight *= -10
                        mateVector = self.createVector(weight, direction)
                        self.addVectors(vector, mateVector)
                return (vector[0], vector[1])           
            elif objective is Objectives.BALL:
                ballDist = self.game.playerDistBall(self)
                (dist, direction) = self.magnitudeAndDirection(ballDist)
                if dist <= 2*ZONE_THRESHOLD:
                    weight = 15
                # else:    
                #     weight = 15/(dist + 1)
                return self.createVector(weight, direction)
            elif objective is Objectives.TEAMMATES:
                Team = self.game.playerTeam(self)
                vector = [0, 0]
                nearestTeammate = self.game.nearestTeammate(self)[0]
                for mate in Team:
                        (dist, direction) = self.magnitudeAndDirection(self.game.playerDistPlayer(self, mate))
                        weight = -(30/(dist + 1))**2
                        if mate is nearestTeammate:
                            weight *= 2
                        if self.hasBall():
                            weight *= 10
                        mateVector = self.createVector(weight, direction)
                        self.addVectors(vector, mateVector)
                return (vector[0], vector[1])   
            return (0, 0)
        
