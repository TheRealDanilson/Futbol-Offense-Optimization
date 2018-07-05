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
    self.passes = 0 #Init pass count
    self.oldholder = self.players[0] #Same as player who starts with ball


def PassCount(self):
    """
        When the ball's possessor changes from None to Player or
        Player to Player, this counts as a pass.

        Since a player kicking the ball into the field is not
        necessarily a successful pass, Player to None doesn't
        count as a pass. Also, a Player 'passing' to himself doesn't
        count.
    """
    if (self.oldholder != self.ball.getPossession) and (self.ball.getPossession != None):
        self.passes += 1

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
    self.Passcount()#Adds 1 to self.passes if a pass happened in the above loop
    self.ball.update()
    self.ball.move()
    self.oldholder = self.ball.getPossession() #Checks who has the ball at the end of this step
    self.printFieldNested()
