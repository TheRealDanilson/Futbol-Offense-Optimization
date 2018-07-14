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
        print(randNumber)
        print(p)
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
        self.oldPosition = position.copy()
        
        
        
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
        b = playerPos[0]**2/300 + playerPos[1]**2/150
        for teammate in team:
            if teammate is not self:
                matePos = teammate.getPosition()
                a = matePos[0]**2/300 + playerPos[1]**2/150
                dist = self.game.playerDistPlayer(self, teammate)
                d = (dist[0]**2 + dist[1]**2)**(0.5)
                z = (b - a + 25)/25 - abs(d - opt_pass)/(((2*FIELD_BOUNDS[1])**2 + FIELD_BOUNDS[3]**2)**.5 - opt_pass)
                p = expcdf((z),.5)
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
                print("M is: " + str(m))
                print("P is: " + str(p))
                print("U is: " + str(u))
                try:
                    #z = m*p/u**2
                    z = p*(m - u + 10)/pass_factor
                    #z = p/u
                    #z = u**2/(m*p)
                    print('Z is: ' + str(z))
                    if z > 0:
                        o = expcdf((z),.5)
                    else:
                        o = 0
                except:
                    print('Set o to 0')
                    o = 0
                print('O is: ' + str(o))
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
        P = sum(probabilities.values())
        probabilities[self] = 1 - P/((len(team) - 1)**2)
        #probabilities[self] = 0
        #Debugging
        print(team)
        print(list(probabilities.values()))
        #a = choices(team, weights=list(probabilities.values()), k=1)[0]
        a = randSelect(probabilities)
        print(a is self)
        return a
        
        
    def calcShootProb(self):
        """
        Returns the probability of shooting (real number between 0 and 1)
        """
        x = self.position[0]
        y = self.position[1]
        z = (x**2)/150 +(y**2)/300;
        if z >= 3.5 or (x**2)/y > 30:
            p = 0.0
        elif (x**2 + y**2)**(0.5) <= 5:
            p = 1.0
        else:
            p = expcdf((3.5 - z),.25)/3
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
        self.shootPassKeep()
        finalVector = self.velocity
        if self.receiving:
            ballDist = self.game.playerDistBall(self)
            (dist, direction) = self.magnitudeAndDirection(ballDist)
            weight = .1
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

    
    def __init__(self, position, game, bounds = FIELD_BOUNDS):
        """
        Constructor method for offender
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
            weight = (dist/10)**2
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
                weight *= 10
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
            #weight = 15/(dist + 1)
            # if dist <= 2*ZONE_THRESHOLD:
            #     weight = 15 
            # if self.receiving:
            #     weight = 2
            #     #weight = 10
            return self.createVector(weight, direction)
        elif objective is Objectives.TEAMMATES:
            Team = self.game.playerTeam(self)
            vector = [0, 0]
            nearestTeammate = self.game.nearestTeammate(self)[0]
            for mate in Team:
                    (dist, direction) = self.magnitudeAndDirection(self.game.playerDistPlayer(self, mate))
                    weight = -(75/(dist + 1))**2
                    if mate is nearestTeammate:
                        weight *= 2
                    if self.hasBall():
                        weight *= 10
                    mateVector = self.createVector(weight, direction)
                    self.addVectors(vector, mateVector)
            return (vector[0], vector[1])
        # elif objective is Objectives.Shift:
        #     # shift belongs to both offender and defender and shifts there formation to
        #     # the side the ball is on either left,right,up or a combination of them
        #     ball = self.getPosition()
        #     direction = ball
        #     if ball[0] > 20:
        #         direction[0] = 2
        #     elif ball[0] < -20:
        #         direction[0] = 2
        #     else:
        #          direction[0] = 0
        #     if ball[1] > 30:
        #         direction[1] = 2
        #     elif ball[1] < 20:
        #         direction[1] = 0
        #     else:
        #         direction[1] = 0
        #     weight = 20
        #     return self.createVector(weight, direction)
        return (0, 0)


class Defender(Player):
    """
    Subclass of Player
    """
    
    
    def __init__(self, position, game, bounds = FIELD_BOUNDS):
        """
        Constructor method for defender
        """
        super().__init__(position, game, bounds)


    def shootPassKeep(self):
        pass
    
        
    def calcVector(self, objective):
        """
        objective - enumerations from the Objectives Class in constants.py
        Returns a list of length 2 that corresponds to the weighted vector
        between a player and the objective.  Entry 0 is x and entry 1 is y.
        """
        weight = self.genWeight(objective)
        ballDist = self.game.playerDistBall(self)
        (forget, direction) = self.magnitudeAndDirection(ballDist)
        if forget <= 3:
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
                        weight = -10/(dist + 1)
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
            # elif objective is Objectives.Shift:
            # # shift belongs to both offender and defender and shifts there formation to
            # # the side the ball is on either left,right,up or a combination of them
            #     ball = self.getPosition()
            #     direction = ball
            #     if ball[0] > 20:
            #         direction[0] = 2
            #     elif ball[0] < -20:
            #         direction[0] = 2
            #     else:
            #          direction[0] = 0
            #     if ball[1] > 30:
            #         direction[1] = 2
            #     elif ball[1] < 20:
            #         direction[1] = 0
            #     else:
            #         direction[1] = 0
            #     weight = 20
            #     return self.createVector(weight, direction)
            return (0, 0)
        
