#!/usr/bin/env python3
from Game import Game
from time import sleep

step = 0
game = Game()
while True:
    print('')
    game.update()
    sleep(0.3)
    step += 1
