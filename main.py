from base import inter, scale
from board import Board
from game import Game
from menu import Menu
from live_play import LivePlay
from tests import Tests
import pygame

POS_MENU = scale((1600, 0))

menu = Menu(POS_MENU, Game)

Board.create_cases()

Game.menu = menu

white_conf = [
    {'name':'king','coord':(2,7),'c':'white'},
    {'name':'pawn','coord':(0,6),'c':'white'},
    {'name':'pawn','coord':(1,6),'c':'white'},
    {'name':'pawn','coord':(2,6),'c':'white'},
    {'name':'pawn','coord':(5,6),'c':'white'},
    {'name':'queen','coord':(4,7),'c':'white'},
]

black_conf = [
    {'name':'king','coord':(5,3),'c':'black'},
    {'name':'pawn','coord':(5,4),'c':'black'},
    {'name':'rock','coord':(6,0),'c':'black'},
    {'name':'rock','coord':(7,0),'c':'black'},
]

Game.set_players()
Game.set_control_methods(LivePlay('white'), LivePlay('black'))

Tests.run(Game)

while inter.running:
    pressed, events = inter.run()
    Board.display()
    menu.react_events(events, pressed)
    menu.display()
    Game.display()
    if menu.state == 'run':
        Game.play_turn()
        if Game.ended:
            menu.end_game(Game.winner)