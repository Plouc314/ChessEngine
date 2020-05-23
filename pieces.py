from base import screen, Form, C, E, scale
import pygame

DIM_PIECE = scale((160,160))
DIMC = E(200)

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

class Piece:
    def __init__(self, coord, color):
        self.coord = coord
        self.color = color
        self.moved = False
    
    @property
    def x(self):
        return self.coord[0]

    @x.setter
    def x(self, value):
        self.coord[0] = value

    @property
    def y(self):
        return self.coord[1]

    @y.setter
    def y(self, value):
        self.coord[1] = value

    def __str__(self):
        return f'{self.color} {self.name}: ({self.x},{self.y})'

    def move(self, coord):
        self.coord = coord
        self.moved = True
        print('[MOVE]', self)

    def display(self):
        marge = int((DIMC - DIM_PIECE[0])/2)
        x = self.coord[0] * DIMC + marge
        y = self.coord[1] * DIMC + marge
        screen.blit(self.img, (x,y))

class Pawn(Piece):
    name = 'pawn'
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if color == 'black':
            self.img = black_pawn
        else:
            self.img = white_pawn

class Bishop(Piece):
    name = 'bishop'
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if color == 'black':
            self.img = black_bishop
        else:
            self.img = white_bishop
        
class Rock(Piece):
    name = 'rock'
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if color == 'black':
            self.img = black_rock
        else:
            self.img = white_rock

class Queen(Piece):
    name = 'queen'
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if color == 'black':
            self.img = black_queen
        else:
            self.img = white_queen

class King(Piece):
    name = 'king'
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if color == 'black':
            self.img = black_king
        else:
            self.img = white_king

class Knight(Piece):
    name = 'knight'
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if color == 'black':
            self.img = black_knight
        else:
            self.img = white_knight



