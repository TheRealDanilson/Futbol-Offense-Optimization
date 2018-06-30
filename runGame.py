#!/usr/bin/env python3
from Game import Game
from time import sleep

game = Game()
while True:
    print('')
    game.update()
    sleep(0.3)

