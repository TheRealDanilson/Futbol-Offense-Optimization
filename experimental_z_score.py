from Game import playerDistPlayer, playerTeam

    def calcPassChoose(self):
        """
        This function calculates *who* this player will pass to, if he is about to pass.
        It uses a Z-score from the distances and positions of other players, with respect
        to this player.
        
        Note: This chooses who to pass to if and only if this player has chosen to pass at all.
        """
        
        # 'Constants'
        x1 = self.position[0] # *This* player's x
        y1 = self.position[1] # *This* player's y
        a = ((x1)**2)/150 + ((y1)**2)/300 # 'a' value 
        
        
        # Player List
        playerList = playerTeam # List of players
        for finder in playerList: 
            if finder is self:
                you = finder # Finds which position in playerList *this* player is.
            else:
                pass
        
        
        # Distances and positions
        deltas = [] # List of tuples of distances (dx,dy) between this guy and each of his teammates 
        positions = [] # List of tuples of positions (x,y) for each of this guy's teammates (this list is in order with distances)
        for teammate in playerList:
            if teammate is not self:
                deltas.append(playerDistPlayer(self,you,teammate)) # Appends distance between this guy and his teammates
                positions.append(teammate.getPosition()) # Appends position of teammate
            else:
                pass
            
        d = [] # Will contain true distances (distance equation)
        for dxdy in deltas:
            d.append(((dxdy[0]-x1)**2)+((dxdy[1]-y1)**2)**(1/2))
            
        
        # Calculations
        b = [] # List of 'b' values for each teammate (Essentially other players' 'a' values)
        for tup in positions:
            b.append( ((tup[0]**2)/150) + ((tup[1]**2)/300) ) # Appends a 'b' value to list b. In order w/ distance and position lists.
        
        Z = [] # List of Z scores for each team
        for index in range(0,(len(playerList)-1)): # All lists are ordered playerwise so a general index is used.
        # Minus one to account for *this* player being included in the list
            Z.append( ((a-b[index] + 16)/16) + (abs(d[index]-15)/15) )
            
        return max(Z) # Not sure about this ask Thomas
            
            
            
        
