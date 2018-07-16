#!/usr/bin/env python3
from Game import Game
from Data import Data

def update(data):
    data.ball_DistTime()
    data.player_Dist()
    data.offender_DistTime()
    data.handle_WinTime()
    data.handle_WinLoss()
    data.handle_Passes()



game = Game('Off testing.txt', 'Def testing.txt')
data = Data(game)

reachedTermination = False

Winloss = data.getWinLoss()
while not reachedTermination:
    game.update()
    update(data)
    curWinLoss = data.getWinLoss()
    reachedTermination = Winloss is not curWinLoss
    if reachedTermination:
        Winloss = curWinLoss
    