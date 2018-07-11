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
        
        x_moved = abs(ball.getPosition()[0] - ball.getOldPosition()[0])
        y_moved = abs(ball.getPosition()[1] - ball.getOldPosition()[1])
        hyp = (x_moved**2 + y_moved**2)**(1/2)
        
        self.ballDist += hyp
        
        if ball.getPossession() == None:
            self.ballDistAlone += hyp
            self.ballTimeAlone += 1
        else:
            self.ballDistHeld += hyp
            self.ballTimeHeld += 1
    
    
    def player_Dist(self,game):
        """
        Adds on distance traveled for *each* player.
        
        -- Assumed that getOldPosition for Players has been implemented.
        
        Parameter game: Game object
        """
        dist = []
        
        for i in game.players:
            x_moved = abs(i.getPosition()[0] - i.getOldPosition()[0])
            y_moved = abs(i.getPosition()[1] - i.getOldPosition()[1])
            dist.append((x_moved**2 + y_moved**2)**(1/2))
        
        if len(self.whoDist) == 0:
            self.whoDist += dist # Make dist the whoDist if whoDist is empty
        else:
            self.whoDist = [sum(x) for x in zip(dist, self.whoDist)] # Element-wise sum
    
    
    def offender_DistTime(self,game):
        """
        Adds on time and distance traveled for *each* offender either with
        or without the ball.
        
        -- This is all assuming game.players list follows an offender-first
        format with half offender and half defender; ex. in [a,b,c,d,e,f]: a,
        b, and c are offenders, d, e, and f are defenders.
        
        Parameter game: Game object
        """
        distHeld = []
        distAlone = []
        timeHeld = []
        timeAlone = []
        offenders = game.players[:len(game.players)//2] # Front-half
        
        for i in offenders:
            x_moved = abs(i.getPosition()[0] - i.getOldPosition()[0])
            y_moved = abs(i.getPosition()[1] - i.getOldPosition()[1])
            hyp = (x_moved**2 + y_moved**2)**(1/2)
            
            if game.ball.getPossession() != i: #If the Offender 'i' is not the one holding the ball, his distance for holding the ball is 0 and his dist. w/o the ball is the formula/
                distHeld.append(0)
                timeHeld.append(0)
                distAlone.append(hyp)
                timeAlone.append(1)
            else:
                distHeld.append(hyp)
                timeHeld.append(1)
                distAlone.append(0)
                timeAlone.append(0)
        
        if len(self.whoDistHeld) == 0:
            self.whoDistHeld += distHeld
        else:
            self.whoDistHeld = [sum(x) for x in zip(distHeld, self.whoDistHeld)]
        
        if len(self.whoTimeHeld) == 0:
            self.whoTimeHeld += timeHeld
        else:
            self.whoTimeHeld = [sum(x) for x in zip(timeHeld, self.whoTimeHeld)]
        
        if len(self.whoDistAlone) == 0:
            self.whoDistAlone += distAlone
        else:
            self.whoDistAlone = [sum(x) for x in zip(distAlone, self.whoDistAlone)]
        
        if len(self.whoTimeAlone) == 0:
            self.whoTimeAlone += timeAlone
        else:
            self.whoTimeAlone = [sum(x) for x in zip(timeAlone, self.whoTimeAlone)]