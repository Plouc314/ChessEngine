from base import TextBox, Cadre, Font, C, Button, dim, InputText, E, scale, Form, screen
import pygame

class Menu:
    default_text_turn = "Turn white"
    default_text_poss_moves = "Possible moves: 20"
    def __init__(self, pos, Game):
        self.Game = Game
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
                self.Game.set_players()
    
    def set_game_info(self, turn, poss_moves):
        self.text_turn.set_text(f'Turn: {turn}')
        self.text_poss_moves.set_text(f'Possible moves: {poss_moves}')

    def end_game(self, winner):
        self.text_end.set_text(f'Winner {winner}')
        self.text_turn.set_text(self.default_text_turn)
        self.text_poss_moves.set_text(self.default_text_poss_moves)
        self.state = 'start'

DIM_PBUTTON = scale((200,200))
DIM_PIECE = scale((160,160))
DIMC = E(200)

# load imgs
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