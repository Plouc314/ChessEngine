from base import E, scale, screen, Button, C, inter
from board import Board
from menu import PromMenu
from move import AttCoord, PossibleMove
from pieces import Pawn, Bishop, King, Queen, Rock, Knight
import pygame
from math import floor

DIMC = E(200)
POS_PMENU = scale((1600, 800))

class LivePlay:
    '''
    Control object for Game control
    
    Work with interface: screen, inter...
    
    Methods for control:
        play_turn()
        promote(piece)
    '''
    Game = None
    def __init__(self, color):
        self.color = color
        # get player obj from Game
        self.player = self.Game.players[color]
        self.pmenu = PromMenu(self.player,POS_PMENU)
        self.case_selected = None
        self.select = False

    def play_turn(self):
        '''Play turn'''
        turn_state = self.Game.turn
        
        while turn_state == self.Game.turn and inter.running:
            pressed, events = inter.run(fill=False)
            self.react_events(events, pressed)
            Board.display()
            self.Game.display()
        
        # reset state
        self.select = False
        self.case_selected.deselect()
    
    def handeln_case(self, coord):
        '''deselect previous case and select new one'''

        case = Board.get_case(coord)
        case.select()
        if not self.case_selected:
            self.case_selected = case
        elif self.case_selected and not case is self.case_selected:
            self.case_selected.deselect()
            self.case_selected = case

    def check_select_piece(self, coord, player):
        '''Select piece if possible: display possible moves'''
        selected_piece = player.get_piece(coord)
        # check if piece found
        if selected_piece:
            self.piece_selected = selected_piece
            self.select = True
            
            # update selected case
            self.handeln_case(coord)

            # display possible moves
            poss_moves = self.Game.get_possibles_moves(selected_piece)

            if selected_piece.name == 'king':
                # add castle moves
                can_long, can_short = PossibleMove.get_castle(player.color)

                self.handeln_castle_case(player.color, can_long, can_short)

            for coord in poss_moves:
                case = Board.get_case(coord)
                case.possible_move = True
    
    def handeln_castle_case(self, color, can_long, can_short):
        line = PossibleMove.get_line(color)
        
        if can_long:
            case = Board.get_case((2,line))
            case.possible_move = True
        if can_short:
            case = Board.get_case((6,line))
            case.possible_move = True

    def promote(self, piece):
        done = False
        # freeze normal execution (in main), wait for player to decide which piece take
        while not done:
            pressed, events = inter.run(fill=False) # keep all displayed thing
            self.pmenu.display()
            self.pmenu.react_events(events, pressed)
            if self.pmenu.state == 'done':
                done = True
                piece_name = self.pmenu.piece_name
                self.pmenu.state = 'wait'
        
        # create new piece
        if piece_name == 'queen':
            new_piece = Queen(piece.coord, piece.color)
        elif piece_name == 'bishop':
            new_piece = Bishop(piece.coord, piece.color)
        elif piece_name == 'rock':
            new_piece = Rock(piece.coord, piece.color)
        elif piece_name == 'knight':
            new_piece = Knight(piece.coord, piece.color)
        
        # remove pawn
        self.player.pieces.remove(piece)
        # add new piece
        self.player.pieces.append(new_piece)

    def react_events(self, events, pressed):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                # check for selected pieces
                mouse_pos = pygame.mouse.get_pos()
                x = floor(mouse_pos[0]/DIMC)
                y = floor(mouse_pos[1]/DIMC)
                # if nothing selected -> select
                if not self.select:
                    self.check_select_piece((x,y), self.player)
                else:
                    done = self.Game.handeln_movement(self.piece_selected, (x,y))
                    if not done:
                        # reset state
                        self.select = False
                        self.case_selected.deselect()