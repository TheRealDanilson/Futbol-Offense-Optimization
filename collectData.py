#!/usr/bin/env python3
from Game import Game
from Data import Data
#from graphics import Graphics
from os import walk
import csv
from Player import *

def update(data):
    data.ball_DistTime()
    data.player_Dist()
    data.offender_DistTime()
    data.handle_Passes()
    data.handle_WinLoss()
    data.handle_Past()
    

def dataWrite(DataList, dataWriter):
    BallDist = ['Distance Ball Traveled']
    BallDistAlone = ['Distance Ball Traveled Alone']
    BallDistHeld = ['Distance Ball was held']
    BallTimeAlone = ['Time steps the ball was alone']
    BallTimeHeld = ['Time steps the ball was held']
    names = DataList[0].get_Names()
    playerDistances = {}
    playerDistancesAlone = {}
    playerDistancesHeld = {}
    playerTimeAlone = {}
    playerTimeHeld = {}
    playerInterceptions = {}
    InterceptLocations = {}
    playerReceives = {}
    playerKeeps = {}
    playerGoals = {}
    playerGoalLocations = {}
    playerPasses = {}
    playerAttempts = {}
    playerAttemptLocations = {}
    playerBlocks = {}
    for player in names.keys():
        if isinstance(player, Offender):
            team = 'Offender'
        else:
            team = 'Defender'
        title = team + ' ' + names[player]
        playerDistances[title] = [title + ' distance traveled']
        if isinstance(player, Offender):
            playerDistancesAlone[title] = [title + ' distance traveled without ball']
            playerDistancesHeld[title] = [title + ' distance traveled with ball']
            playerTimeAlone[title] = [title + ' time steps without ball']
            playerTimeHeld[title] = [title + ' time steps with ball']
            playerReceives[title] = [title + ' receive locations']
            playerKeeps[title] = [title + ' number of keeps']
            playerGoals[title] = [title + ' number of goals']
            playerGoalLocations[title] = [title + ' location of goal shots']
            playerPasses[title] = [title + ' number of passes']
            playerAttempts[title] = [title + ' number of goal attempts']
            playerAttemptLocations[title] = [title + ' locations of goal attempts']
        else:
            playerInterceptions[title] = [title + ' interceptions']
            InterceptLocations[title] = [title + ' interception locations']
            playerBlocks[title] = [title + ' number of blocks']
        
        
    for data in DataList:
        names = data.get_Names()
        BallDist += [data.get_ballDist()]
        BallDistAlone += [data.get_ballDistAlone()]
        BallDistHeld += [data.get_ballDistHeld()]
        BallTimeAlone += [data.get_ballTimeAlone()]
        BallTimeHeld += [data.get_ballTimeHeld()]
        distances = data.get_whoDist()
        distancesAlone = data.get_whoDistAlone()
        distancesHeld = data.get_whoDistHeld()
        timeAlone = data.get_whoTimeAlone()
        timeHeld = data.get_whoTimeHeld()
        interceptions = data.get_whoIntercepts()
        interceptLocations = data.get_whereIntercepts()
        receiveLocations = data.get_whereReceives()
        keeps = data.get_Keeps()
        goals = data.get_whoGoals()
        goalLocations = data.get_whereGoals()
        passes = data.get_whoPasses()
        attempts = data.get_whoAttempts()
        attemptLocations = data.get_whereAttempts()
        blocks = data.get_whoBlocks()
        for player in distances.keys():
            if isinstance(player, Offender):
                team = 'Offender'
            else:
                team = 'Defender'
            title = team + ' ' + names[player]
            playerDistances[title] += [distances[player]]
            
        for player in distancesAlone.keys():
            title = 'Offender' + ' ' + names[player]
            playerDistances[title] += [distances[player]]
            playerDistancesAlone[title] += [distancesAlone[player]]
            playerDistancesHeld[title] += [distancesHeld[player]]
            playerTimeAlone[title] += [timeAlone[player]]
            playerTimeHeld[title] += [timeHeld[player]]
            playerReceives[title] += [receiveLocations[player]]
            playerKeeps[title] += [keeps[player]]
            playerGoals[title] += [goals[player]]
            playerGoalLocations[title] += [goalLocations[player]]
            playerPasses[title] += [passes[player]]
            playerAttempts[title] += [attempts[player]]
            playerAttemptLocations[title] += [attemptLocations[player]]
            
            
        for player in interceptions.keys():
            title = 'Defender' + ' ' + names[player]
            playerInterceptions[title] += [interceptions[player]]
            InterceptLocations[title] += [interceptLocations[player]]
            playerBlocks[title] += [blocks[player]]
            
    dataWriter.writerow(BallDist)
    dataWriter.writerow(BallDistAlone)
    dataWriter.writerow(BallDistHeld)       
    dataWriter.writerow(BallTimeAlone)
    dataWriter.writerow(BallTimeHeld)
    for player in playerDistancesAlone.keys():
        dataWriter.writerow(playerDistances[player])
        dataWriter.writerow(playerDistancesAlone[player])
        dataWriter.writerow(playerDistancesHeld[player])                
        dataWriter.writerow(playerTimeAlone[player])
        dataWriter.writerow(playerTimeHeld[player])
        dataWriter.writerow(playerReceives[player])
        dataWriter.writerow(playerKeeps[player])
        dataWriter.writerow(playerGoals[player])
        dataWriter.writerow(playerGoalLocations[player])
        dataWriter.writerow(playerPasses[player])
        dataWriter.writerow(playerAttempts[player])
        dataWriter.writerow(playerAttemptLocations[player])
        
    for player in playerInterceptions.keys():
        dataWriter.writerow(playerDistances[player])
        dataWriter.writerow(playerInterceptions[player])
        dataWriter.writerow(InterceptLocations[player])
        dataWriter.writerow(playerBlocks[player])
        
    
def dump(DataList, offenderFormation, defenderFormation):
    name = ('DATA ' + offenderFormation + ' ' + defenderFormation + '.csv').replace('.txt', '')
    file = open(name, 'w')
    dataWriter = csv.writer(file, delimiter = ';')
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
            for k in range(500):
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
    print(offenderFormation, defenderFormation)
    game = Game(offenderFormation, defenderFormation)
    #movingPictures = Graphics(game)
    data = Data(game)
    DataList += [data]
    
    reachedTermination = False
    
    Winloss = data.get_WinLoss()
    while not reachedTermination:
        game.update()
        #game.printFieldNested()
        #movingPictures.update()
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
            if file.startswith('Off') and file.endswith('txt'):
                offenderFormations += [file]
            elif file.startswith('Def') and file.endswith('txt'):
                defenderFormations += [file]
    return (offenderFormations, defenderFormations)

runSimulations()     
infoDump(data)
