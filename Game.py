from constants import *
from Player import Player
from Ball import Ball
from math import floor
from random import seed


class Game(object):
    
    def __init__(self):
        seed()
        self.players = []
        self.createPlayer([-10, 50])
        self.createPlayer([-20, 35])
        self.createBall(self.players[0])
    
    
    def createPlayer(self, position):
        player = Player(position, self)
        self.players += [player]
    
    
    def createBall(self, player):
        self.ball = Ball(player)
        player.getPossession(self.ball)
    
    
    def playerDistBall(self, player):
        playerPos = player.getPosition()
        ballPos = self.ball.getPosition()
        dx = ballPos[0] - playerPos[0]
        dy = ballPos[1] - playerPos[1]
        return (dx, dy)
        
        
    def playerDistGoal(self, player):
        playerPos = player.getPosition()
        dx = GOAL_POS[0] - playerPos[0]
        dy = GOAL_POS[1] - playerPos[1]
        return (dx, dy)
    
    
    def playerDistPlayer(self, player1, player2):
        player1Pos = player1.getPosition()
        player2Pos = player2.getPosition()
        dx = player2Pos[0] - player1Pos[0]
        dy = player2Pos[0] - player1Pos[0]
        return (dx, dy)
    
        
    def changePossession(self, player):
        oldPlayer = self.ball.getPossession()
        if oldPlayer is not None:
            oldPlayer.removePossession()
        player.getPossession(ball)
        self.ball.setPossession(player)
        
    
    def playerTeam(self, player):
        return self.players
    
    
    def update(self):
#        ballPlayer = self.ball.getPossession()
        for player in self.players:
            player.update()
            player.move()
            distBall = self.playerDistBall(player)
            dist = (distBall[0]**2 + distBall[1]**2)**(0.5)
            if dist <= RECEIVE_THRESHOLD:
                player.receive(self.ball)
                self.ball.setPossession(player)
        self.ball.update()
        self.ball.move()
        self.printField()
    
    
    def printField(self):
        field = []
        x_min = FIELD_BOUNDS[0]
        x_max = FIELD_BOUNDS[1]
        y_min = FIELD_BOUNDS[2]
        y_max = FIELD_BOUNDS[3]
        xLength = x_max - x_min + 1
        yLength = y_max - y_min + 1
        field_size = xLength*yLength
        ballPos = self.ball.getPosition()
        for i in range(field_size):
            field += ['.']
        goalIndex = (xLength)*(y_max - GOAL_POS[1]) + GOAL_POS[0] - x_min
        ballIndex = (xLength)*(y_max - floor(ballPos[1])) + floor(ballPos[0]) - x_min
        field[goalIndex] = 'G'
        if ballIndex >= 0 and ballIndex < field_size - 1 and ballPos[0] >= x_min and ballPos[0] <= x_max:
            field[ballIndex] = 'o'
        for player in self.players:
            pos = player.getPosition()
            x = floor(pos[0])
            y = floor(pos[1])
            index = (xLength)*(y_max - y) + x - x_min
            if index >= 0 and index < field_size - 1 and x >= x_min and x <= x_max:
                if player.hasBall():
                    field[index] = 'Xo'
                else:
                    field[index] = 'X'
        for y in range(yLength):
            line = ''
            for x in range(xLength):
                line += field[xLength*y + x]
            print(line)


        