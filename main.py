from base import inter, scale
from board import Board
from game import Game
from menu import Menu
import pygame

POS_MENU = scale((1600, 0))

menu = Menu(POS_MENU)

Board.create_cases()

Game.menu = menu
Game.set_players()

while inter.running:
    pressed, events = inter.run()
    Board.display()
    menu.react_events(events, pressed)
    menu.display()
    Game.display()
    if menu.state == 'run':
        Game.react_events(events, pressed)
        if Game.ended:
            menu.end_game(Game.winner)