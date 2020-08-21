
class Piece:
    def __init__(self, coord, color):
        self.coord = list(coord)
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
        '''Only implemented if graphics
        
        Allow to not import pygame and base in this file
        '''
        pass
    
    def on_resize(self, dim_object):
        '''Only implemented if graphics
        
        Allow to not import pygame and base in this file
        '''
        pass


class Pawn(Piece):
    name = 'pawn'
    black_img = None
    white_img = None
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if self.black_img:
            if color == 'black':
                self.img = self.black_img
            else:
                self.img = self.white_img
            self.original_img = self.img.copy()

class Bishop(Piece):
    name = 'bishop'
    black_img = None
    white_img = None
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if self.black_img:
            if color == 'black':
                self.img = self.black_img
            else:
                self.img = self.white_img
            self.original_img = self.img.copy()
        
class Rock(Piece):
    name = 'rock'
    black_img = None
    white_img = None
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if self.black_img:
            if color == 'black':
                self.img = self.black_img
            else:
                self.img = self.white_img
            self.original_img = self.img.copy()

class Queen(Piece):
    name = 'queen'
    black_img = None
    white_img = None
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if self.black_img:
            if color == 'black':
                self.img = self.black_img
            else:
                self.img = self.white_img
            self.original_img = self.img.copy()

class King(Piece):
    name = 'king'
    black_img = None
    white_img = None
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if self.black_img:
            if color == 'black':
                self.img = self.black_img
            else:
                self.img = self.white_img
            self.original_img = self.img.copy()

class Knight(Piece):
    name = 'knight'
    black_img = None
    white_img = None
    def __init__(self, coord, color):
        super().__init__(coord, color)
        if self.black_img:
            if color == 'black':
                self.img = self.black_img
            else:
                self.img = self.white_img
            self.original_img = self.img.copy()



