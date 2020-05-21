from game import Game
from base import TextBox, Cadre, Font, C, Button, dim, InputText, E, scale, Form, screen
import pygame

class Menu:
    default_text_turn = "Turn white"
    default_text_poss_moves = "Possible moves: 20"
    def __init__(self, pos):
        self.cadre = Cadre((E(600), E(1600)), C.WHITE, pos)
        self.text_turn = TextBox((E(400), E(80)), C.WHITE, (pos[0]+E(50),pos[1]+E(50)),"Turn white",font=Font.f50, centered=False)
        self.text_poss_moves = TextBox((E(600), E(60)), C.WHITE, (pos[0]+E(50),pos[1]+E(210)),"Possible moves: 20",font=Font.f50, centered=False)
        self.text_end = TextBox((E(450), E(120)), C.WHITE, (pos[0]+E(50),pos[1]+E(360)),"",font=Font.f50)
        self.button_start = Button((E(450), E(100)), C.LIGHT_GREEN, (pos[0]+E(50),pos[1]+E(590)),"Start new  game",font=Font.f50)
        self.state = 'start'

    def display(self):
        self.cadre.display()
        self.text_turn.display()
        self.text_poss_moves.display()
        if self.state == 'start':
            self.text_end.display()
            self.button_start.display()

    def react_events(self, events, pressed):
        if self.state == 'start':
            if self.button_start.pushed(events):
                self.state = 'run'
                Game.set_players()
    
    def set_game_info(self, turn, poss_moves):
        self.text_turn.set_text(f'Turn: {turn}')
        self.text_poss_moves.set_text(f'Possible moves: {poss_moves}')

    def end_game(self, winner):
        self.text_end.set_text(f'Winner {winner}')
        self.text_turn.set_text(self.default_text_turn)
        self.text_poss_moves.set_text(self.default_text_poss_moves)
        self.state = 'start'
