from base import Form, screen, scale, C, E
import pygame

DIM_CASE = scale((200,200))
DIM_PM = scale((80,80))
MARGE_PM = E(60)

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
        self.coord = (int(pos[0]/200), int(pos[1]/200))
    
    def select(self):
        self.surf.fill(CS)
    
    def deselect(self):
        self.surf.fill(self.color)
    
    def display(self):
        screen.blit(self.surf, self.pos)

        if self.possible_move:
            x = self.pos[0] + MARGE_PM
            y = self.pos[1] + MARGE_PM
            screen.blit(self.poss_mov_surf,(x,y))

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