from interface import Form, Interface, C, Form, Button, TextBox, Cadre, Font
from pieces import Piece, Pawn, Bishop, King, Queen, Rock, Knight
import pygame

DIM_CASE = (200,200)
DIM_PM = (60,60)
MARGE_PM = 70

C1 = (173,216,230)
C2 = (153,196,210)
CS = C.RED

class Case(Form):
    poss_mov_form = Form(DIM_PM, (0,0), C.PURPLE)
    def __init__(self, dim, pos, color):
        super().__init__(dim, pos, color)
        self.possible_move = False
        self.coord = (int(pos[0]/200), int(pos[1]/200))
    
    def select(self):
        self.surf['main'].fill(CS)
    
    def deselect(self):
        self.surf['main'].fill(self.COLOR)
    
    def display(self):
        super().display()

        if self.possible_move:
            x = self.pos[0] + Interface.dim.E(MARGE_PM)
            y = self.pos[1] + Interface.dim.E(MARGE_PM)
            self.poss_mov_form.set_pos((x,y))
            self.poss_mov_form.display()

DIM_BOARD = (1600,1600)

class Board:

    @classmethod
    def create_cases(cls):
        cls.cases = []
        alter = True
        for x in range(8):
            alter = not alter
            for y in range(8):
                alter = not alter
                pos = (200*x, 200*y)
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

DIM_PIECE = (160,160)

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

# funcs that will be implemented as Piece.display, Piece.on_rezise
def display(self):
    marge = Interface.dim.E((DIMC - DIM_PIECE[0])/2)
    x = self.coord[0] * Interface.dim.E(DIMC) + marge
    y = self.coord[1] * Interface.dim.E(DIMC) + marge
    Interface.screen.blit(self.img, (x,y))

def on_resize(self, factor):
    self.img = pygame.transform.scale(self.original_img, [round(factor*DIM_PIECE[0]), round(factor*DIM_PIECE[1])])

def setup_pieces():
    '''
    Implement display methods in Piece,
    set imgs
    '''
    Piece.display = display
    Piece.on_resize = on_resize

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

POS_MENU = (1600, 0)

class Menu:
    default_text_turn = "Turn white"
    default_text_poss_moves = "Possible moves: 20"
    def __init__(self, ChessGame):
        self.ChessGame = ChessGame
        self.cadre = Cadre((600, 1600), POS_MENU)
        self.text_turn = TextBox((400, 80), (POS_MENU[0]+50,POS_MENU[1]+50),text="Turn white",font=Font.f(50), centered=False)
        self.text_poss_moves = TextBox((600, 60), (POS_MENU[0]+50,POS_MENU[1]+210),text="Possible moves: 20",font=Font.f(50), centered=False)
        self.text_end = TextBox((450, 120), (POS_MENU[0]+50,POS_MENU[1]+360),font=Font.f(50))
        self.button_start = Button((450, 100), (POS_MENU[0]+50,POS_MENU[1]+590), C.LIGHT_GREEN,text="Start new  game",font=Font.f(50))
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
                # re-add pieces
                Interface.add_resizable_objs(self.ChessGame.players['white'].pieces)
                Interface.add_resizable_objs(self.ChessGame.players['black'].pieces)
    
    def __call__(self, turn, poss_moves):
        '''Call in ChessGame.check_end_game'''
        self.text_turn.set_text(f'Turn: {turn}')
        self.text_poss_moves.set_text(f'Possible moves: {poss_moves}')

    def end_game(self, winner):
        self.text_end.set_text(f'Winner {winner}')
        self.text_turn.set_text(self.default_text_turn)
        self.text_poss_moves.set_text(self.default_text_poss_moves)
        self.state = 'start'

DIM_PBUTTON = (200,200)
DIMC = 200


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

        self.button_queen = Button(DIM_PBUTTON, (pos[0]+50,pos[1]),surface=queen_img, surf_font_color=C.LIGHT_GREY)
        self.button_bishop = Button(DIM_PBUTTON, (pos[0]+300,pos[1]),surface=bishop_img, surf_font_color=C.LIGHT_GREY)
        self.button_rock = Button(DIM_PBUTTON, (pos[0]+50,pos[1]+250),surface=rock_img, surf_font_color=C.LIGHT_GREY)
        self.button_knight = Button(DIM_PBUTTON, (pos[0]+300,pos[1]+250),surface=knight_img, surf_font_color=C.LIGHT_GREY)
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