from Ball import Ball
from Game import Game

# passes complete (by each player/all), shot from where, time posession
# (each player/all), which defender intercepted the most, number of decisions
# to keep (player), no. goals, no. shots, distance moved by offenders, distance
# moved by defenders.

class Data:
    """
    ballDist        Total units of distance that the ball has traveled.
    ballDistAlone   Total units of distance the ball has traveled while not
                    being possessed by a player.
    ballDistHeld    Total distance the ball has traveled while being possessed
                    by a player.
    ballTimeAlone   Total number of timesteps the ball has not been possessed by
                    a player.
    ballTimeHeld    Total number of timesteps the ball has been possessed by a
                    player.
    whoDist         List of total units of distances moved by each player.
    whoDistAlone    List of total units of distances moved by each offender
                    while not possessing the ball.
    whoDistHeld     List of total units of distances moved by each offender
                    while possessing the ball.
    whoTimeAlone    List of total number of timesteps the ball has not been in
                    possession for each offender.
    whoTimeHeld     List of total number of timesteps the ball has been in
                    possession for each offender.
    """
    
    def __init__(self):
        self.ballDist = 0
        self.ballDistAlone = 0
        self.ballDistHeld = 0
        self.ballTimeAlone = 0
        self.ballTimeHeld = 0 
        
        self.whoDist = []
        self.whoDistAlone = []
        self.whoDistHeld = []
        self.whoTimeAlone = []
        self.whoTimeHeld = []


    #-----------
    # Getter methods
    #-----------
    
    
    def get_ballDist(self):
        return self.BallDist
    
    def get_ballDistAlone(self):
        return self.BallDistAlone
    
    def get_ballDistHeld(self):
        return self.ballDistHeld
    
    def get_ballTimeAlone(self):
        return self.ballTimeAlone
    
    def get_ballTimeHeld(self):
        return self.ballTimeHeld
    
    
    # Note: Made the following methods assuming they would be placed right
    # after game.update() in runGame.py
    
    
    def ball_DistTime(self, ball):
        """
        Adds on time and distance traveled by the ball while being possessed by
        a player or not. Also adds on total distance traveled by ball.
        
        Parameter ball: Ball object
        """
        
        x_moved = abs(ball.getPosition[0] - ball.getOldPosition[0])
        y_moved = abs(ball.getPosition[1] - ball.getOldPosition[1])
        hyp = (x_moved**2 + y_moved**2)**(1/2)
        
        self.ballDist += hyp
        
        if ball.getPossession == None:
            self.ballDistAlone += hyp
            self.ballTimeAlone += 1
        else:
            self.ballDistHeld += hyp
            self.ballTimeHeld += 1
    
    
    def player_DistTime(self,game):
        """
        Parameter game: Game object
        (Unfinished)
        """