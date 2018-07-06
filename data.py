from Ball import getPossession, getPosition, getOldPosition

# passes complete (by each player/all), shot from where, time posession (each player/all), which defender intercepted the most, number of decisions to keep (player)
# no. goals, no. shots, distance moved by offenders, distance moved by defenders.


def __init__(self):
    """
    Totals
    """
    self.balldistance = 0
    self.possessiontime = 0 
    
def distStep(self):
    """
        Returns units traveled by the ball, including whenever it's held by a player.
        
        Note: Calculates the distance traveled by the ball in the timestep that just
        passed.
    """
    x_moved = abs(getPosition[0] - getOldPosition[0])
    y_moved = abs(getPosition[1] - getOldPosition[1])
    
    hyp = (x_moved**2 + y_moved**2)**(1/2)
    
    return hyp

def timePossessed(self):
    """
        Returns either 0 or 1 (step) depending on if the offending team is holding
        the ball.
    """
    if 
