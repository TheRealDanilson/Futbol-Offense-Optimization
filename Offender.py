class Offender(Player):
    """ Subclass of Player
            
    """
    
    def __init__(self, position, game, bounds = FIELD_BOUNDS):
        super().__init__(position, game, bounds)
        
    def update(self):
        Vx = 0
        Vy = 0
        self.shootPassKeep()
        if self.receiving is not True:
            for objective in Objectives:
                weight = self.genWeight(objective)
                if objective is Objectives.GOAL:
                    vector = self.game.playerDistGoal(self)
                    Vx += weight * vector[0]
                    Vy += weight * vector[1]
                elif objective is Objectives.TEAMMATES:
                    team = self.game.playerTeam(self)
                    for teammate in team:
                        vector = self.game.playerDistPlayer(self, teammate)
                        Vx += weight * -vector[0]
                        Vy += weight * -vector[1]
                    
            speed = (Vx**2 + Vy**2)**(0.5)
            if speed > MAX_SPEED:
                Vx *= MAX_SPEED/speed
                Vy *= MAX_SPEED/speed
        self.velocity = [Vx, Vy]