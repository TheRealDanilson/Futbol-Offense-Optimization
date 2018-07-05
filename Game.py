from constants import *
from Player import *
from Ball import Ball
from math import floor
from random import seed


class Game(object):
    """
    players     List of length TEAM_SIZE that stores the player instances
    ball        Instance of ball
    
    """
    def __init__(self):
        seed()
        self.players = []
        self.createPlayer([-10, 45], (-20,  10, 40, 50))
        self.createPlayer([ 30, 35], (-30,  10, 10, 40))
        self.createPlayer([-23, 14], (-30, -10, 10, 20))
        self.createPlayer([  8, 35], (-10,  10, 20, 40))
        self.createPlayer([  3,  7], (-10,  10,  0, 20))
        self.createDefender([-3, 3], FIELD_BOUNDS)
        self.createDefender([10, 30], FIELD_BOUNDS)
        self.createDefender([-10, 24], FIELD_BOUNDS)
        self.createDefender([20, 50], FIELD_BOUNDS)
        self.createDefender([10, 3], FIELD_BOUNDS)
        self.createDefender([30, 3], FIELD_BOUNDS)
        self.createBall(self.players[0])
    
    
    def createPlayer(self, position, bounds):
        player = Offender(position, self, bounds)
        self.players += [player]
        
    
    def createDefender(self, position, bounds):
        player = Defender(position, self, bounds)
        self.players += [player]
    
    
    def createBall(self, player):
        self.ball = Ball(player)
        player.getPossession(self.ball)
    
    
    def playerDistBall(self, player):
        """ Returns 2 element tuple that stores the player's distance to the ball
           Entry 0 is change in x and entry 1 is change in y
        """
        playerPos = player.getPosition()
        ballPos = self.ball.getPosition()
        dx = ballPos[0] - playerPos[0]
        dy = ballPos[1] - playerPos[1]
        return (dx, dy)
        
        
    def playerDistGoal(self, player):
        """ Returns 2 element tuple that stores the player's distance to the goal
           Entry 0 is change in x and entry 1 is change in y
        """
        playerPos = player.getPosition()
        dx = GOAL_POS[0] - playerPos[0]
        dy = GOAL_POS[1] - playerPos[1]
        return (dx, dy)
    
    def playerDistZone(self, player):
        """ Returns a 2 element tuple that represents the player's distance to the center of
            zone, pointing from the player
        """
        bounds = player.getBounds()
        playerPos = player.getPosition()
        center = ((bounds[0] + bounds[1])/2, (bounds[2] + bounds[3])/2)
        dx = center[0] - playerPos[0]
        dy = center[1] - playerPos[1]
        return (dx, dy)
    
    
    def playerDistPlayer(self, player1, player2):
        # Returns 2 element tuple that stores the player instance 1's distance to
        #   player instance 2. Entry 0 is change in x and entry 1 is change in y
        player1Pos = player1.getPosition()
        player2Pos = player2.getPosition()
        dx = player2Pos[0] - player1Pos[0]
        dy = player2Pos[0] - player1Pos[0]
        return (dx, dy)
    
        
    def changePossession(self, player):
        """ Updates which player instance has possession of the ball and updates
           the balls instance of who possesses it
        """
        oldPlayer = self.ball.getPossession()
        if oldPlayer is not None:
            oldPlayer.removePossession()
        player.getPossession(ball)
        self.ball.setPossession(player)
    
    
    def nearestOpponent(self, player):
        team = type(player)
        playerPos = player.getPosition()
        minDist = float('inf')
        closest = None
        for member in self.players:
            if not isinstance(member, team):
                memberPos = member.getPosition()
                dx = memberPos[0] - playerPos[0]
                dy = memberPos[1] - playerPos[1]
                dist = (dx**2 + dy**2)**(0.5)
                if dist < minDist:
                    minDist = dist
                    closest = member
        return (closest, minDist)
    
    
    def nearestOpponentToLine(self, team, pos1, pos2):
        minDist = float('inf')
        closest = None
        (x1, y1) = pos1
        (x2, y2) = pos2
        for member in self.players:
            if not isinstance(member, team):
                (x0, y0) = member.getPosition()
                dist = abs((y2 - y1)*x0 - (x2 - x1)*y0 + x2*y1 - y2*x1)/((y2-y1)**2 + (x2 -x1)**2)**(0.5)
                if dist < minDist:
                    minDist = dist
                    closest = member
        return (closest, minDist)
        
    def playerList(self):
        return self.players.copy()
        
    
    def playerOpponentTeam(self, player):
        team = type(player)
        lst = []
        for member in self.players:
            if not isinstance(member, team):
                lst += [member]
        return lst
    
    
    def playerTeam(self, player):
        """ Returns a TEAM_SIZE length list with all player instances of the same team """
        team = type(player)
        lst = []
        for member in self.players:
            if isinstance(member, team):
                lst += [member]
        return lst
    
    
    def update(self):
        """
            Update method for the whole game. Updates the velocities of each player
            and the ball, and then moves them according to their updated velocities
            
            This method also handles receiving the ball. If a player is within the
            RECEIVE_THRESHOLD, the player will receive the ball
            
            TODO: Change this method to handle stealing
        
        """
        for player in self.players:
            player.update()
            player.move()
            distBall = self.playerDistBall(player)
            dist = (distBall[0]**2 + distBall[1]**2)**(0.5)
            if not player.justShotBall() and dist <= RECEIVE_THRESHOLD:
                player.receive(self.ball)
                self.ball.setPossession(player)
        self.ball.update()
        self.ball.move()
        self.printFieldNested()
            
            
    def inBounds(self, position):
        """
            Returns True if position is in bounds, returns False otherwise
        """
        x_min = FIELD_BOUNDS[0]
        x_max = FIELD_BOUNDS[1]
        y_min = FIELD_BOUNDS[2]
        y_max = FIELD_BOUNDS[3]
        x = position[0]
        y = position[1]
        return (x_min <= x) and (x <= x_max) and (y_min <= y) and (y <= y_max)

    def printFieldNested(self):
        """
            Prints a graphical representation of the field to the screen
        """
        field = []
        x_min = FIELD_BOUNDS[0]
        x_max = FIELD_BOUNDS[1]
        y_min = FIELD_BOUNDS[2]
        y_max = FIELD_BOUNDS[3]
        xLength = x_max - x_min + 1 # Adds the "zero" position for even lengths
        yLength = y_max - y_min + 1 # Adds the "zero" position for even lengths

        
        # Initialize the field using nested lists
        # Benefit of using a nested list: Simpler Syntax
        # To access a point on a field, just use field[x][y]
        # No hard to read equations to calculate indices
        for x in range(xLength):
            field += [[]]
            for y in range(yLength):
                field[x] += ['.']
                
        # For the field data structure, the origin is located on the bottom left corner
        # However, we've defined the origin to be where the center of
        # goal is for our simulation
        # To fix this, we shift our points to the right by x_min so that the positions
        # on the field are correct
        field[GOAL_POS[0] + x_min][GOAL_POS[1]] = 'G'
        ballPos = self.ball.getPosition()
        if self.inBounds(ballPos):
            field[floor(ballPos[0]) + x_min][floor(ballPos[1])] = 'o'
        for player in self.players:
            playerPos = player.getPosition()
            bounds = player.getBounds()
            print(bounds)
            zoneCenter = ((bounds[0] + bounds[1])/2, (bounds[2] + bounds[3])/2)
            field[floor(zoneCenter[0]) + x_min][floor(zoneCenter[1])] = 'C'
            if self.inBounds(playerPos):
                if player.hasBall():
                   field[floor(playerPos[0]) + x_min][floor(playerPos[1])] = 'Xo'
                elif isinstance(player, Defender):
                    field[floor(playerPos[0]) + x_min][floor(playerPos[1])] = 'd'
                else:
                    field[floor(playerPos[0]) + x_min][floor(playerPos[1])] = 'X'
                    
        printNestedList(field)



def printNestedList(lst):
    """
        Prints the contents of a list representing a 2D grid
        The origin of the list will be at the bottom left corner
    """
    x_length = len(lst)
    y_length = len(lst[0])
    for y in range(y_length):
        string = ''
        for x in range(x_length):
            string += lst[x][y_length - 1 - y]
        print(string)
        