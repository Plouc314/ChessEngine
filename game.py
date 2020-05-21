from base import E, scale, screen, Button, C, inter
from pieces import Pawn, Bishop, King, Queen, Rock, Knight
from board import Board
from move import Movement, AttCoord, PossibleMove
import pygame
from math import floor
from copy import deepcopy

DIMC = E(200)


white_config = [
    {'name':'pawn','coord':(0,6),'c':'white'},
    {'name':'pawn','coord':(1,6),'c':'white'},
    {'name':'pawn','coord':(2,6),'c':'white'},
    {'name':'pawn','coord':(3,6),'c':'white'},
    {'name':'pawn','coord':(4,6),'c':'white'},
    {'name':'pawn','coord':(5,6),'c':'white'},
    {'name':'pawn','coord':(6,6),'c':'white'},
    {'name':'pawn','coord':(7,6),'c':'white'},
    {'name':'king','coord':(4,7),'c':'white'},
    {'name':'bishop','coord':(2,7),'c':'white'},
    {'name':'bishop','coord':(5,7),'c':'white'},
    {'name':'knight','coord':(1,7),'c':'white'},
    {'name':'knight','coord':(6,7),'c':'white'},
    {'name':'rock','coord':(0,7),'c':'white'},
    {'name':'rock','coord':(7,7),'c':'white'},
    {'name':'queen','coord':(3,7),'c':'white'},
]

black_config = [
    {'name':'pawn','coord':(0,1),'c':'black'},
    {'name':'pawn','coord':(1,1),'c':'black'},
    {'name':'pawn','coord':(2,1),'c':'black'},
    {'name':'pawn','coord':(3,1),'c':'black'},
    {'name':'pawn','coord':(4,1),'c':'black'},
    {'name':'pawn','coord':(5,1),'c':'black'},
    {'name':'pawn','coord':(6,1),'c':'black'},
    {'name':'pawn','coord':(7,1),'c':'black'},
    {'name':'king','coord':(4,0),'c':'black'},
    {'name':'bishop','coord':(2,0),'c':'black'},
    {'name':'bishop','coord':(5,0),'c':'black'},
    {'name':'knight','coord':(1,0),'c':'black'},
    {'name':'knight','coord':(6,0),'c':'black'},
    {'name':'rock','coord':(0,0),'c':'black'},
    {'name':'rock','coord':(7,0),'c':'black'},
    {'name':'queen','coord':(3,0),'c':'black'},
]

class Player:
    in_check = False
    def __init__(self, config):
        self.create_pieces(config)

    def create_pieces(self, config):
        self.pieces = []
        self.king = None
        for pdict in config:
            if pdict['name'] == 'pawn':
                pawn = Pawn(pdict['coord'], pdict['c'])
                self.pieces.append(pawn)
            elif pdict['name'] == 'bishop':
                bishop = Bishop(pdict['coord'], pdict['c'])
                self.pieces.append(bishop)
            elif pdict['name'] == 'queen':
                queen = Queen(pdict['coord'], pdict['c'])
                self.pieces.append(queen)
            elif pdict['name'] == 'rock':
                rock = Rock(pdict['coord'], pdict['c'])
                self.pieces.append(rock)
            elif pdict['name'] == 'knight':
                knight = Knight(pdict['coord'], pdict['c'])
                self.pieces.append(knight)
            elif pdict['name'] == 'king':
                king = King(pdict['coord'], pdict['c'])
                self.pieces.append(king)
                self.king = king
        
        # get player's color
        self.color = self.king.color

    def get_piece(self, coord):
        for piece in self.pieces:
            if piece.coord == coord:
                return piece    

    def get_piece_by_name(self, name):
        for piece in self.pieces:
            if piece.name == name:
                return piece

    def display(self):
        for piece in self.pieces:
            piece.display()

def inv_c(color):
    if color == 'white':
        return 'black'
    else:
        return 'white'

DIM_PBUTTON = scale((200,200))
POS_PMENU = scale((1600, 800))

class PromMenu:
    def __init__(self, player, pos):
        queen_img = player.get_piece_by_name('queen').img
        self.button_queen = Button(DIM_PBUTTON, C.LIGHT_GREY, (pos[0]+E(50),pos[1]),image=queen_img)
        bishop_img = player.get_piece_by_name('bishop').img
        self.button_bishop = Button(DIM_PBUTTON, C.LIGHT_GREY, (pos[0]+E(300),pos[1]),image=bishop_img)
        rock_img = player.get_piece_by_name('rock').img
        self.button_rock = Button(DIM_PBUTTON, C.LIGHT_GREY, (pos[0]+E(50),pos[1]+E(250)),image=rock_img)
        knight_img = player.get_piece_by_name('knight').img
        self.button_knight = Button(DIM_PBUTTON, C.LIGHT_GREY, (pos[0]+E(300),pos[1]+E(250)),image=knight_img)
        self.state = 'wait'
    
    def react_events(self, events, pressed):
        if self.button_knight.pushed(events):
            self.state = 'done'
            self.piece_name = 'knight'
        if self.button_queen.pushed(events):
            self.state = 'done'
            self.piece_name = 'queen'
        if self.button_rock.pushed(events):
            self.state = 'done'
            self.piece_name = 'rock'
        if self.button_bishop.pushed(events):
            self.state = 'done'
            self.piece_name = 'bishop'

    def display(self):
        self.button_queen.display()
        self.button_bishop.display()
        self.button_rock.display()
        self.button_knight.display()

class Game:
    menu = None
    case_selected = None
    piece_selected = None
    
    @classmethod
    def init(cls, players):
        cls.select = False
        cls.turn = True
        cls.winner = None
        cls.ended = False
        cls.players = players
        pmenu_white = PromMenu(players['white'],POS_PMENU)
        pmenu_black = PromMenu(players['black'],POS_PMENU)
        cls.pmenus = {'white':pmenu_white, 'black':pmenu_black}
        Movement.players = players
        AttCoord.Game = cls
        PossibleMove.players = players

    @classmethod
    def set_players(cls):
        '''Classic set up. For custom: use Config and init method'''
        white_player = Player(white_config)
        black_player = Player(black_config)

        cls.init({'white':white_player, 'black':black_player})

    @classmethod
    def check_for_check(cls, color, kingcheck=True):
        if color == 'white':
            king_coord = cls.players['white'].king.coord
            # check if king coord is attack by an opponent piece
            for piece in cls.players['black'].pieces:
                if king_coord in AttCoord.get(piece, kingcheck=kingcheck):
                    return True
        else:
            king_coord = cls.players['black'].king.coord
            # check if king coord is attack by an opponent piece
            for piece in cls.players['white'].pieces:
                if king_coord in AttCoord.get(piece, kingcheck=kingcheck):
                    return True

    @classmethod
    def handeln_case(cls, coord):
        # get case
        case = Board.get_case(coord)
        case.select()
        if not cls.case_selected:
            cls.case_selected = case
        elif cls.case_selected and not case is cls.case_selected:
            cls.case_selected.deselect()
            cls.case_selected = case

    @classmethod
    def handeln_castle_case(cls, color, can_long, can_short):
        line = PossibleMove.get_line(color)
        
        if can_long:
            case = Board.get_case((2,line))
            case.possible_move = True
        if can_short:
            case = Board.get_case((6,line))
            case.possible_move = True

    @classmethod
    def check_select_piece(cls, coord, player):
        selected_piece = player.get_piece(coord)
        # check if piece found
        if selected_piece:
            cls.piece_selected = selected_piece
            cls.select = True
            
            # update selected case
            cls.handeln_case(coord)

            # display possible moves
            poss_moves = cls.get_possibles_moves(selected_piece)

            if selected_piece.name == 'king':
                # add castle moves
                can_long, can_short = PossibleMove.get_castle(player.color)

                cls.handeln_castle_case(player.color, can_long, can_short)

            for coord in poss_moves:
                case = Board.get_case(coord)
                case.possible_move = True

    @classmethod
    def handeln_movement(cls, piece, coord):
        '''Handeln pieces movement'''
        attack = False
        # first check if other pieces on coord
        if cls.players[inv_c(piece.color)].get_piece(coord):
            attack = True

        cls.move(piece, coord, attack)
    
    @classmethod
    def move(cls, piece, coord, attack):
        if attack:
            if coord in AttCoord.get(piece):
                attacked_piece = cls.get_piece(coord)
                cls.players[attacked_piece.color].pieces.remove(attacked_piece)
                piece.move(coord)
                # pass a turn
                cls.end_turn(piece.color)
        else:
            if coord in PossibleMove.get(piece):
                piece.move(coord)
                if piece.name == 'pawn':
                    cls.check_pawn_promotion(piece)
                # pass a turn
                cls.end_turn(piece.color)
            elif piece.name == 'king':
                cls.check_castle_moves(piece)

        cls.deselect()

    @classmethod
    def check_castle_moves(cls, king):
        line = PossibleMove.get_line(king.color)
        
        can_long, can_short = PossibleMove.get_castle(king.color)

        if can_long:
            rock = cls.players[king.color].get_piece((0, line))
            # execute long castle
            king.move((2,line))
            rock.move((3, line))
            # pass a turn
            cls.end_turn(king.color)
        
        if can_short:
            rock = cls.players[king.color].get_piece((7, line))
            # execute short castle
            king.move((6,line))
            rock.move((5, line))
            # pass a turn
            cls.end_turn(king.color)

    @classmethod
    def check_pawn_promotion(cls, piece):
        # line of promotion
        line = PossibleMove.get_line(inv_c(piece.color))

        if piece.y == line:
            # promote
            cls.run_prom_menu(piece)

    @classmethod
    def run_prom_menu(cls, piece):
        done = False
        # freeze normal execution (in main), wait for player to decide which piece take
        while not done:
            pressed, events = inter.run(fill=False) # keep all displayed thing
            cls.pmenus[piece.color].display()
            cls.pmenus[piece.color].react_events(events, pressed)
            if cls.pmenus[piece.color].state == 'done':
                done = True
                piece_name = cls.pmenus[piece.color].piece_name
        
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
        cls.players[piece.color].pieces.remove(piece)
        # add new one
        cls.players[piece.color].pieces.append(new_piece)

    @classmethod
    def get_possibles_moves(cls, piece):
        movements = PossibleMove.get(piece)
        alls = AttCoord.get(piece)
        for coord in alls:
            if cls.players[inv_c(piece.color)].get_piece(coord):
                movements.append(coord)
        return movements
                
    @classmethod
    def get_piece(cls, coord):
        '''Return piece corresponding coord (of both color)'''
        piece = cls.players['white'].get_piece(coord)
        if piece:
            return piece
        piece = cls.players['black'].get_piece(coord)
        if piece:
            return piece

    @classmethod
    def deselect(cls):
        for case in Board.cases:
            case.possible_move = False
        cls.case_selected.deselect()
        cls.select = False

    @classmethod
    def end_turn(cls, color):
        cls.turn = not cls.turn
        # check if the game is over
        cls.check_end_game(inv_c(color))

    @classmethod
    def check_end_game(cls, color):
        poss_moves = []
        # get every possible moves for the player
        for piece in cls.players[color].pieces:
            pmoves = cls.get_possibles_moves(piece)
            poss_moves.extend(pmoves)
        
        # send turn infos to menu
        cls.menu.set_game_info(color, len(poss_moves))

        if not poss_moves: # player can't move
            if cls.check_for_check(color): # if player in check and can't move -> checkmate
                cls.winner = inv_c(color)
            else: # player can't move but not in check -> stalemate
                pass
            cls.ended = True

    @classmethod
    def react_events(cls, events, pressed):
        # select current player 
        if cls.turn:
            player = cls.players['white']
        else:
            player = cls.players['black']

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                # check for selected pieces
                mouse_pos = pygame.mouse.get_pos()
                x = floor(mouse_pos[0]/DIMC)
                y = floor(mouse_pos[1]/DIMC)
                # if nothing selected -> select
                if not cls.select:
                    cls.check_select_piece((x,y), player)
                else:
                    cls.handeln_movement(cls.piece_selected, (x,y))

    @classmethod
    def display(cls):
        cls.players['white'].display()
        cls.players['black'].display()