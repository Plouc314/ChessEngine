from interface import Interface

Interface.setup((2200, 1600), 'Chess', scale_factor=0.7)

from graphics import Board, Menu
from game import ChessGame
from live_play import LivePlay
from tests import Tests
import bruteforce


menu = Menu(ChessGame)

ChessGame.menu = menu

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

ChessGame.set_players()

LivePlay.ChessGame = ChessGame

#agent_white = bruteforce.Agent('white', ChessGame)
#agent_black = bruteforce.Agent('black', ChessGame)


ChessGame.set_control_methods(LivePlay('white'), LivePlay('black'))

Tests.run(ChessGame)

while Interface.running:
    pressed, events = Interface.run()
    Board.display()
    menu.react_events(events, pressed)
    menu.display()
    ChessGame.display()
    if menu.state == 'run':
        ChessGame.play_turn()
        if ChessGame.ended:
            menu.end_game(ChessGame.winner)