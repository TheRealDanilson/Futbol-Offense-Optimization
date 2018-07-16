# passes complete (by each player/all), shot from where, time posession
# (each player/all), which defender intercepted the most, number of decisions
# to keep (player), no. goals, no. shots, distance moved by offenders, distance
# moved by defenders.

class Data:
    """
    I made everything in this file assuming that all data collected 
    
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
    Wins            Number of wins for the offending team.
    Losses          Number of losses for the offending team.
    Passes          Number of passes made by the offending team.
    whoIntercepts   List of each defender's intercepts.
    whoRecieves     Dictionary of each Offender's number of recieves.
    """
    
    def __init__(self,game):
        
        self.game = game
        self.offenders = self.game.players[:len(self.game.players)//2]
        self.defenders = self.game.players[len(self.game.players)//2:]
        
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
        
        self.Wins = 0
        self.Losses = 0
        
        self.whoRecieves = {}
        for i in self.offenders:
            self.whoRecieves[i] = 0
        self.whereRecieves = {}
        for i in self.offenders:
            self.whereRecieves[i] = []
        self.whoIntercepts = {}
        for i in self.defenders:
            self.whoIntercepts[i] = []
        self.whereIntercepts = {}
        for i in self.defenders:
            self.whereIntercepts[i] = []
        self.Passes = 0
        
        # Past time-step helper
        self.whohadBall = self.game.players[1]


    #-----------
    # Getter methods
    #-----------
    
    
    def get_ballDist(self):
        """
        Float, total ball distance traveled.
        """
        return self.ballDist
    def get_ballDistAlone(self):
        """
        Float, total ball distance traveled without a possessor.
        """
        return self.ballDistAlone
    def get_ballDistHeld(self):
        """
        Float, total ball distance traveled with a possessor.
        """
        return self.ballDistHeld
    def get_ballTimeAlone(self):
        """
        Int, total ball time without a possessor.
        """
        return self.ballTimeAlone
    def get_ballTimeHeld(self):
        """
        Int, total ball time with a possessor.
        """
        return self.ballTimeHeld
    def get_whoDist(self):
        """
        List of distances traveled, in order of players.
        """
        return self.whoDist
    def get_whoDistAlone(self):
        """
        List of distances traveled by offenders without the ball.
        """
        return self.whoDistAlone
    def get_whoDistHeld(self):
        """
        List of distances traveled by offenders with the ball.
        """
        return self.whoDistHeld
    def get_whoTimeAlone(self):
        """
        List of each offender's time without the ball.
        """
        return self.whoTimeAlone
    def get_whoTimeHeld(self):
        """
        List of each offender's time with the ball.
        """
        return self.whoTimeHeld
    def get_WinLoss(self):
        """
        List of ints, wins to losses.
        """
        wl = [self.Wins, self.Losses]
        return wl
    def get_Winrate(self):
        """
        Float, percent wins.
        """
        try:
            return (self.Wins/self.Losses)*100
        except ZeroDivisionError:
            return 100
    def get_whoIntercepts(self):
        """
        List of each Defender's number of intercepts.
        """
        return self.whoIntercepts
    def get_Passes(self):
        """
        Int, number of passes overall.
        """
        return self.Passes
    def get_avgPassLength(self):
        """
        Float, average pass length.
        """
        return self.get_ballDistAlone()/self.get_Passes()


    #-----------
    # While-Loop Methods
    #-----------
    
    
    def ball_DistTime(self):
        """
        Adds on time and distance traveled by the ball while being possessed by
        a player or not. Also adds on total distance traveled by ball.
        
        Parameter game: Game object
        """
        
        x_moved = abs(self.game.ball.getPosition()[0] - self.game.ball.getOldPosition()[0])
        y_moved = abs(self.game.ball.getPosition()[1] - self.game.ball.getOldPosition()[1])
        hyp = (x_moved**2 + y_moved**2)**(1/2)
        
        self.ballDist += hyp
        
        if self.game.ball.getPossession() == None:
            self.ballDistAlone += hyp
            self.ballTimeAlone += 1
        else:
            self.ballDistHeld += hyp
            self.ballTimeHeld += 1
    
    
    def player_Dist(self):
        """
        Adds on distance traveled for *each* player.
        
        -- Assumed that getOldPosition for Players has been implemented.
        
        Parameter game: Game object
        """
        dist = []
        
        for i in self.game.players:
            x_moved = abs(i.getPosition()[0] - i.getOldPosition()[0])
            y_moved = abs(i.getPosition()[1] - i.getOldPosition()[1])
            dist.append((x_moved**2 + y_moved**2)**(1/2))
        
        if len(self.whoDist) == 0:
            self.whoDist += dist # Make dist the whoDist if whoDist is empty
        else:
            self.whoDist = [sum(x) for x in zip(dist, self.whoDist)] # Element-wise sum
    
    
    def offender_DistTime(self):
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
        
        for i in self.offenders:
            x_moved = abs(i.getPosition()[0] - i.getOldPosition()[0])
            y_moved = abs(i.getPosition()[1] - i.getOldPosition()[1])
            hyp = (x_moved**2 + y_moved**2)**(1/2)
            
            if i.hasBall() == True:
                #If the Offender 'i' is not the one holding the ball, his distance for holding the ball is 0 and his dist. w/o the ball is the formula/
                distHeld.append(hyp)
                timeHeld.append(1)
                distAlone.append(0)
                timeAlone.append(0)
            else:
                distHeld.append(0)
                timeHeld.append(0)
                distAlone.append(hyp)
                timeAlone.append(1)
        
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


    def handle_WinLoss(self):
        """
        Records a win or a loss for the offending team. Only intercepts count
        as losses. This function handles interceptions as well.
        
        Parameter game: Game object
        """
        intercepts = []
        
        for i in self.defenders:
            if i.hasBall() and not self.whohadBall.hasBall():
                self.Losses += 1
                self.whoIntercepts[i] += 1
                self.whereIntercepts[i] += [tuple(i.getPosition())]
                self.whohadBall = i
        
        if self.game.ball.isGoal(): # Unrelated to above. This is for wins.
            self.Wins += 1 


    def handle_Passes(self):
        """
        Handles data regarding passing interactions.
        """
        
        for i in self.offenders:
            if i.hasBall() and not self.whohadBall.hasBall():
                self.Passes += 1
                self.whoRecieves[i] += 1
                self.whereRecieves[i] += [tuple(i.getPosition())]
                self.whohadBall = i
    