from interface import Interface, TextBox, InputText, Button, Font, C, E, Cadre, Dimension, set_screen, Form, scale
import pygame

dim = Dimension(scale((2200,1600)))

screen = pygame.display.set_mode(dim.window)
screen.fill(C.WHITE)
pygame.display.set_caption('Chess')

inter = Interface()
inter.FPS = 30

set_screen(screen)