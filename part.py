import pygame
from helpers import draw_shading_for_rect

class Part():
    def __init__(self, x, y, width, height, colour, layer, char_creating, main=False):
        '''
        pass in atributes
        '''
        self.x = x
        self.y = y
        self.W = width
        self.H = height
        self.colour = colour


        # height from bottom, 
        # eg 0 is covered by other parts
        self.layer = layer

        # list of all parts
        # for checking if object is on top 
        # and for knowing how many total parts 
        # there are for bringing objects to the top 
        self.char_creating = char_creating

        # if main = True, then part
        # determines characters main colour
        self.main = main

        # state managment for part
        self.hovered = False
        self.state = {'selected': False, 'moving': False, 'resize': False}

        # create rect obj
        self.rect = pygame.Rect(self.x, self.y, self.W, self.H)

        # variables
        # how many pixels part moves at a time when resizing
        self.move_buffer = self.char_creating.scalar



    def render(self, surface):
        '''
        render part, outline, mouse
        '''
        pygame.draw.rect(surface, self.colour, self.rect)

        # draw outline for selected part
        if self.state['selected']:
            draw_shading_for_rect((0, 0, 0), self.rect, surface, 3)


    def update(self, dt, actions):
        '''
        make part react to mouse actions
        '''
        self.mouse_actions(dt, actions)

    def mouse_actions(self, dt, actions):

        self.hovered = self.rect.collidepoint(actions["mouse_pos"])

        if self.hovered:
            if actions['mouse_click']:
                self.state['selected'] = not self.state['selected']

            if actions['m1']:
                self.m1_actions(actions)

    def m1_actions(self, actions):
        '''
        reacts to m1 actions
        '''
        pass

    # Resize
    def resize(self, actions):
        pass

    # Colour
      
    def change_colour(self, new_colour):
        if self.state['selected']:
            self.colour = new_colour

        

    


    


