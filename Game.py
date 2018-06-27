import Player
import Ball

class Game(object):
    
    def createPlayer(self, position):
        player = Player.Player(position, self)
        self.players += [player]
    
        
    def createBall(self, player):
        self.ball = Ball.Ball(player)
    
    
    def playerDistBall(self, player):
        playerPos = player.getPosition()
        ballPos = self.ball.getPosition()
        dx = playerPos[0] - ballPos[0]
        dy = playerPos[1] - ballPos[1]
        dist = (dx**2 + dy**2)**(0.5)
        
        
    def changePossession(self, player):
        oldPlayer = self.ball.getPossession()
        if oldPlayer is not None:
            oldPlayer.removePossession()
        player.getPossession(ball)
        self.ball.setPossession(player)
    
        
    def update(self):
        self.ball.move()
        for player in self.players:
            player.move()
            if self.ball.getPossession() is None:
                dist = self.playerDistBall(player)
                if dist <= self.threshold:
                    self.changePossession(player)

                            
        