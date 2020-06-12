from interface import Form, Interface, scale, C, E, Form, Button, TextBox, Cadre, Font
from pieces import Piece, Pawn, Bishop, King, Queen, Rock, Knight
import pygame

DIM_CASE = scale((200,200))
DIM_PM = scale((60,60))
MARGE_PM = E(70)

C1 = (173,216,230)
C2 = (153,196,210)
CS = C.RED

class Case:
    poss_mov_surf = pygame.Surface(DIM_PM)
    poss_mov_surf.fill(C.PURPLE)
    def __init__(self, dim, pos, color):
        self.surf = pygame.Surface(dim)
        self.color = color
        self.surf.fill(color)
        self.pos = pos
        self.possible_move = False
        self.coord = (int(pos[0]/E(200)), int(pos[1]/E(200)))
    
    def select(self):
        self.surf.fill(CS)
    
    def deselect(self):
        self.surf.fill(self.color)
    
    def display(self):
        Interface.screen.blit(self.surf, self.pos)

        if self.possible_move:
            x = self.pos[0] + MARGE_PM
            y = self.pos[1] + MARGE_PM
            Interface.screen.blit(self.poss_mov_surf,(x,y))

DIM_BOARD = scale((1600,1600))

class Board:

    @classmethod
    def create_cases(cls):
        cls.cases = []
        alter = True
        for x in range(8):
            alter = not alter
            for y in range(8):
                alter = not alter
                pos = (E(200)*x, E(200)*y)
                if alter:
                    color = C1
                else:
                    color = C2
                case = Case(DIM_CASE, pos, color)
                cls.cases.append(case)

    @classmethod
    def get_case(cls, coord):
        '''Return the case with the given coord'''
        for case in cls.cases:
            if case.coord == coord:
                return case

    @classmethod
    def display(cls):
        for case in cls.cases:
            case.display()

# auto create cases
Board.create_cases()

DIM_PIECE = scale((160,160))

# load imgs
white_pawn = pygame.image.load('imgs/pawn2.png')
white_pawn = pygame.transform.scale(white_pawn,DIM_PIECE)
white_bishop = pygame.image.load('imgs/bishop2.png')
white_bishop = pygame.transform.scale(white_bishop,DIM_PIECE)
white_rock = pygame.image.load('imgs/rock2.png')
white_rock = pygame.transform.scale(white_rock,DIM_PIECE)
white_queen = pygame.image.load('imgs/queen2.png')
white_queen = pygame.transform.scale(white_queen,DIM_PIECE)
white_king = pygame.image.load('imgs/king2.png')
white_king = pygame.transform.scale(white_king,DIM_PIECE)
white_knight = pygame.image.load('imgs/knight2.png')
white_knight = pygame.transform.scale(white_knight,DIM_PIECE)
black_pawn = pygame.image.load('imgs/pawn.png')
black_pawn = pygame.transform.scale(black_pawn,DIM_PIECE)
black_bishop = pygame.image.load('imgs/bishop.png')
black_bishop = pygame.transform.scale(black_bishop,DIM_PIECE)
black_rock = pygame.image.load('imgs/rock.png')
black_rock = pygame.transform.scale(black_rock,DIM_PIECE)
black_queen = pygame.image.load('imgs/queen.png')
black_queen = pygame.transform.scale(black_queen,DIM_PIECE)
black_king = pygame.image.load('imgs/king.png')
black_king = pygame.transform.scale(black_king,DIM_PIECE)
black_knight = pygame.image.load('imgs/knight.png')
black_knight = pygame.transform.scale(black_knight,DIM_PIECE)

# func that will be implemented as Piece.display
def display(self):
    marge = int((DIMC - DIM_PIECE[0])/2)
    x = self.coord[0] * DIMC + marge
    y = self.coord[1] * DIMC + marge
    Interface.screen.blit(self.img, (x,y))

def setup_pieces():
    '''
    Implement display method in Piece,
    set imgs
    '''
    Piece.display = display

    Pawn.black_img = black_pawn
    Pawn.white_img = white_pawn

    Knight.black_img = black_knight
    Knight.white_img = white_knight

    Bishop.black_img = black_bishop
    Bishop.white_img = white_bishop

    Rock.black_img = black_rock
    Rock.white_img = white_rock

    Queen.black_img = black_queen
    Queen.white_img = white_queen

    King.black_img = black_king
    King.white_img = white_king

# when import: auto setup pieces
setup_pieces()

POS_MENU = scale((1600, 0))

class Menu:
    default_text_turn = "Turn white"
    default_text_poss_moves = "Possible moves: 20"
    def __init__(self, ChessGame):
        self.ChessGame = ChessGame
        self.cadre = Cadre((E(600), E(1600)), C.WHITE, POS_MENU)
        self.text_turn = TextBox((E(400), E(80)), C.WHITE, (POS_MENU[0]+E(50),POS_MENU[1]+E(50)),"Turn white",font=Font.f50, centered=False)
        self.text_poss_moves = TextBox((E(600), E(60)), C.WHITE, (POS_MENU[0]+E(50),POS_MENU[1]+E(210)),"Possible moves: 20",font=Font.f50, centered=False)
        self.text_end = TextBox((E(450), E(120)), C.WHITE, (POS_MENU[0]+E(50),POS_MENU[1]+E(360)),"",font=Font.f50)
        self.button_start = Button((E(450), E(100)), C.LIGHT_GREEN, (POS_MENU[0]+E(50),POS_MENU[1]+E(590)),"Start new  game",font=Font.f50)
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
                self.ChessGame.set_players()
    
    def __call__(self, turn, poss_moves):
        '''Call in ChessGame.check_end_game'''
        self.text_turn.set_text(f'Turn: {turn}')
        self.text_poss_moves.set_text(f'Possible moves: {poss_moves}')

    def end_game(self, winner):
        self.text_end.set_text(f'Winner {winner}')
        self.text_turn.set_text(self.default_text_turn)
        self.text_poss_moves.set_text(self.default_text_poss_moves)
        self.state = 'start'

DIM_PBUTTON = scale((200,200))
DIMC = E(200)


class PromMenu:
    def __init__(self, player, pos):
        
        if player.color == 'white':
            queen_img = white_queen
            bishop_img = white_bishop
            rock_img = white_rock
            knight_img = white_knight
        else:
            queen_img = black_queen
            bishop_img = black_bishop
            rock_img = black_rock
            knight_img = black_knight

        self.button_queen = Button(DIM_PBUTTON, C.LIGHT_GREY, (pos[0]+E(50),pos[1]),image=queen_img)
        self.button_bishop = Button(DIM_PBUTTON, C.LIGHT_GREY, (pos[0]+E(300),pos[1]),image=bishop_img)
        self.button_rock = Button(DIM_PBUTTON, C.LIGHT_GREY, (pos[0]+E(50),pos[1]+E(250)),image=rock_img)
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