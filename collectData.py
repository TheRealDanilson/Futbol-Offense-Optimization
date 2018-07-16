#!/usr/bin/env python3
from Game import Game
from Data import Data
from graphics import Graphics

def update(data):
    data.ball_DistTime()
    data.player_Dist()
    data.offender_DistTime()
    data.handle_WinLoss()
    data.handle_Passes()

def infoDump(data):
    print('Distance ball traveled: ' + str(data.get_ballDist()))
    print('Distance ball traveled while being passed/shot: ' + str(data.get_ballDistAlone()))
    print('Distance ball traveled while being held: ' + str(data.get_ballDistHeld()))
    print('Number of time steps ball was being passed/shot: ' + str(data.get_ballTimeAlone()))
    print('Number of time steps ball was held: ' + str(data.get_ballTimeHeld()))
    print('List of distances travelled by each offender: ' + str(data.get_whoDist()))
    print('List of distances travelled by each offender when they didn\'t have the ball: ' + \
          str(data.get_whoDistAlone()))
    print('List of distances travelled by each offender when they had: ' + \
          str(data.get_whoDistHeld()))
    print('List of the number of time steps that each offender was without the ball: ' + \
          str(data.get_whoTimeAlone()))
    print('List of the number of time steps that each offender was without the ball: ' + \
          str(data.get_whoTimeHeld()))
    print('List of Wins, Losses: ' + str(Winloss))
    print('Winrate for offenders: ' + str(data.get_Winrate()))
    print('List of interceptions for each defender: ' + str(data.get_whoIntercepts()))
    print('Number of passes: ' + str(data.get_Passes()))

game = Game('Off testing.txt', 'Def testing.txt')
movingPictures = Graphics(game)
data = Data(game)

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
        
infoDump(data)
    