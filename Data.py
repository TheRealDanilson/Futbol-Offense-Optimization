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
    whereIntercepts
    whereRecieves
    whohadBall      Last PLAYER that had the ball -- Excludes None
    pastBall        Last possessor of the ball -- Includes None
    """
    
    def __init__(self,game):
        
        # Initial Initials
        self.game = game
        self.offenders = self.game.players[:len(self.game.players)//2]
        self.defenders = self.game.players[len(self.game.players)//2:]
        
        # Ball kinematics
        self.ballDist = 0
        self.ballDistAlone = 0
        self.ballDistHeld = 0
        self.ballTimeAlone = 0
        self.ballTimeHeld = 0 
        
        # Player Kinematics
        self.whoDist = {}
        self.whoDistAlone = {}
        self.whoDistHeld = {}
        self.whoTimeAlone = {}
        self.whoTimeHeld = {}
        
        # Wins and Losses
        self.Wins = 0
        self.Losses = 0
        
        # Player-Ball Interactions
        self.whoRecieves = {}
        self.whereRecieves = {}
        self.whoIntercepts = {}
        self.whereIntercepts = {}
        self.Passes = 0
        
        # For-loops to initialize dictionaries
        for i in self.game.players:
            self.whoDist[i] = 0
        for i in self.offenders:
            self.whoDistAlone[i] = 0
            self.whoDistHeld[i] = 0
            self.whoTimeAlone[i] = 0
            self.whoTimeHeld[i] = 0
            self.whoRecieves[i] = 0
            self.whereRecieves[i] = []
        for i in self.defenders:
            self.whoIntercepts = 0
            self.whereIntercepts = []

        # Past Time-Step Helper Attributes
        self.whohadBall = self.game.players[1]
        self.pastBall = self.game.players[1]


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
        return self.whoDist.copy()
    def get_whoDistAlone(self):
        """
        List of distances traveled by offenders without the ball.
        """
        return self.whoDistAlone.copy()
    def get_whoDistHeld(self):
        """
        List of distances traveled by offenders with the ball.
        """
        return self.whoDistHeld.copy()
    def get_whoTimeAlone(self):
        """
        List of each offender's time without the ball.
        """
        return self.whoTimeAlone.copy()
    def get_whoTimeHeld(self):
        """
        List of each offender's time with the ball.
        """
        return self.whoTimeHeld.copy()
    def get_WinLoss(self):
        """
        List of ints, wins to losses.
        """
        wl = [self.Wins, self.Losses]
        return wl.copy()
    def get_Winrate(self):
        """
        Float, percent wins.
        
        Winrate is not an attribute.
        """
        try:
            return (self.Wins/self.Losses)*100
        except ZeroDivisionError:
            return 100
    def get_whoIntercepts(self):
        """
        List of each Defender's number of intercepts.
        """
        return self.whoIntercepts.copy()
    def get_Passes(self):
        """
        Int, number of passes overall.
        """
        return self.Passes


    #-----------
    # While-Loop Methods
    #-----------
    
    
    def ball_DistTime(self):
        """
        Adds on time and distance traveled by the ball while being possessed by
        a player or not. Also adds on total distance traveled by ball.
        """
        
        x_moved = abs(self.game.ball.getPosition()[0] - self.game.ball.getOldPosition()[0])
        y_moved = abs(self.game.ball.getPosition()[1] - self.game.ball.getOldPosition()[1])
        hyp = (x_moved**2 + y_moved**2)**(1/2)
        
        self.ballDist += hyp
        
        if (self.game.ball.getPossession() == None) or (self.pastBall == None): # Alone ---> Player , Player ---> Alone , and Alone ---> Alone all count as Alone Time/Dist.
            self.ballDistAlone += hyp
            self.ballTimeAlone += 1
        elif (self.game.ball.getPossession() != None) and (self.pastBall != None): # Player ---> Player
            self.ballDistHeld += hyp
            self.ballTimeHeld += 1
    
    
    def player_Dist(self):
        """
        Adds on distance traveled for *each* player.
        
        -- Assumed that getOldPosition for Players has been implemented.
        
        Parameter game: Game object
        """
        for i in self.game.players:
            x_moved = abs(i.getPosition()[0] - i.getOldPosition()[0])
            y_moved = abs(i.getPosition()[1] - i.getOldPosition()[1])
            hyp = (x_moved**2 + y_moved**2)**(1/2)
            self.whoDist[i] += hyp
    
    
    def offender_DistTime(self):
        """
        Adds on time and distance traveled for *each* offender either with
        or without the ball.
        
        -- This is all assuming game.players list follows an offender-first
        format with half offender and half defender; ex. in [a,b,c,d,e,f]: a,
        b, and c are offenders, d, e, and f are defenders.
        
        Parameter game: Game object
        """
        for i in self.offenders:
            x_moved = abs(i.getPosition()[0] - i.getOldPosition()[0])
            y_moved = abs(i.getPosition()[1] - i.getOldPosition()[1])
            hyp = (x_moved**2 + y_moved**2)**(1/2)
            
            if i.hasBall():
                self.whoTimeHeld[i] += 1
            else:
                self.whoTimeAlone[i] += 1
                
            if i.hasBall() and (self.pastBall == i):
                self.whoDistHeld[i] += hyp
            else:
                self.whoDistAlone[i] += hyp


    def handle_WinLoss(self):
        """
        Records a win or a loss for the offending team. Only intercepts count
        as losses. This function handles interceptions as well.
        
        Parameter game: Game object
        """
        for i in self.defenders:
            if i.hasBall() and not self.whohadBall.hasBall():
                self.Losses += 1
                self.whoIntercepts[i] += 1
                self.whereIntercepts[i] += [tuple(i.getPosition())]
        
        if self.game.ball.isGoal(): # Unrelated to above. This is for wins.
            self.Wins += 1
        elif self.game.ball.isOutBounds():
            self.Losses += 1


    def handle_Passes(self):
        """
        Handles data regarding passing interactions.
        """
        for i in self.offenders:
            if i.hasBall() and (i != self.pastBall):
                self.Passes += 1
                self.whoRecieves[i] += 1
                self.whereRecieves[i] += [tuple(i.getPosition())]
    
    
    def handle_Past(self):
        """
        Handles remembering stuff from the past timestep, that I need.
        
        This is the only thing that needs to be 'in order' in the while loop, last. (I think it needs to).
        
        whohadBall: Last PLAYER that had the ball. (Basically does not include None, keeps the last Player)
        pastBall: ball.getPossession --- Includes None
        """
        for i in self.game.players:
            if i.hasBall():
                self.whohadBall = i
        
        if self.game.ball.getPossession() is None:
            self.pastBall = None
        else:
            self.pastBall = self.whohadBall