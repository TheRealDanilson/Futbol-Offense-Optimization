#!/usr/bin/env python3
from Game import Game
from Data import Data
from graphics import Graphics
from os import walk
import csv

def update(data):
    data.ball_DistTime()
    data.player_Dist()
    data.offender_DistTime()
    data.handle_WinLoss()
    data.handle_Passes()
    

def dataWrite(DataList, dataWriter):
    pass
    
def dump(DataList, offenderFormation, defenderFomration):
    name = (offenderFormation + ' ' + defenderFormation + '.csv').replace('.txt', '')
    file = open(name, 'w')
    dataWriter = csv.writer(file)
    dataWrite(DataList, dataWriter)
    file.close()
    

def infoDump(data):
    print('Distance ball traveled: ' + str(data.get_ballDist()))
    print('Distance ball traveled while being passed/shot: ' + str(data.get_ballDistAlone()))
    print('Distance ball traveled while being held: ' + str(data.get_ballDistHeld()))
    print('Number of time steps ball was being passed/shot: ' + str(data.get_ballTimeAlone()))
    print('Number of time steps ball was held: ' + str(data.get_ballTimeHeld()))
    print('List of distances travelled by each offender: ' + str(data.get_whoDist()))
    print('List of distances travelled by each offender when they didn\'t have the ball: ' + \
          str(data.get_whoDistAlone()))
    print('List of distances travelled by each offender when they held: ' + \
          str(data.get_whoDistHeld()))
    print('List of the number of time steps that each offender was without the ball: ' + \
          str(data.get_whoTimeAlone()))
    print('List of the number of time steps that each offender was with the ball: ' + \
          str(data.get_whoTimeHeld()))
    print('List of Wins, Losses: ' + str(Winloss))
    print('Winrate for offenders: ' + str(data.get_Winrate()))
    print('List of interceptions for each defender: ' + str(data.get_whoIntercepts()))
    print('Number of passes: ' + str(data.get_Passes()))

#game = Game('Off testing.txt', 'Def testing.txt')
# movingPictures = Graphics(game)
# data = Data(game)
# 
# reachedTermination = False
# 
# Winloss = data.get_WinLoss()
# while not reachedTermination:
#     game.update()
#     #game.printFieldNested()
#     movingPictures.update()
#     update(data)
#     curWinLoss = data.get_WinLoss()
#     reachedTermination = Winloss != curWinLoss
#     if reachedTermination:
#         Winloss = curWinLoss

"""
Daniel Son, the idea here was that runSimulations() would set up all the
formation combos, then formationCombo() would run 1000 matches, and match()
would create the actual game.

EDIT: I actually commented out formationCombo() because it seemed pretty useless.
From what I understood with out talk before you wanted it, but again, it didn't
seem like it was doing much.  Anyway, I just put three for loops in
runSimulations().  Of course, change it as needed.  I wasn't sure what the directory
in getFormations() should be, so I leave it to you.  Hope this helped.
"""


def runSimulations():
    """
    This method pairs up all the different formations and runs 1000 simulations
    of each matchup
    """
    allFormations = getFormations()
    offenderFormations = allFormations[0]
    defenderFormations = allFormations[1]
    
    for i in offenderFormations:
        for j in defenderFormations:
            DataList = []
            #self.formationCombo(i,j)
            for k in range(1000):
                match(i,j, DataList)
            dump(DataList, i, j)
        

# def formationCombo(self,offenderFormation,defenderFormation):
#     for i in range(1000):
#         self.match(offenderFormation,defenderFormation)


def match(offenderFormation, defenderFormation, DataList):
    """
    offenderFormation - textfile with formation details
    defenderFormation - textfile with formation details
    This method is what actually runs each simulation, terminates each
    simulation, and collects data
    """
    game = Game(offenderFormation, defenderFormation)
    movingPictures = Graphics(game)
    data = Data(game)
    DataList += [data]
    
    reachedTermination = False
    
    Winloss = data.get_WinLoss()
    while not reachedTermination:
        game.update()
        #game.printFieldNested()
        movingPictures.update()
        update(data)
        curWinLoss = data.get_WinLoss()
        reachedTermination = Winloss != curWinLoss
        if reachedTermination:
            Winloss = curWinLoss
    
def getFormations():
    """
    Goes into current directory and searches for the formation files,  adding
    each one to it's respective list (offenderFormations or defenderFormations)
    """
    offenderFormations = []
    defenderFormations = []
    for root, dirs, files in walk("./"):
        for file in files:
            if file.startswith('Off'):
                offenderFormations += [file]
            elif file.startswith('Def'):
                defenderFormations += [file]
    return (offenderFormations, defenderFormations)

runSimulations()     
infoDump(data)
