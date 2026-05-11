import pygame
from helpers import draw_shading_for_rect
from typing import Callable

# Button that can have optionally image or text
class Button():
    '''Class for UI buttons
    
    returns True when clicked

    handels rendering and actions on button
    '''
    def __init__(self, x, y, on_click: Callable[[str], None],
                 button_colour=(255, 255, 255),
                hover_colour=(139, 139, 139), width=0, height=0,
                image=None ):
        
        '''
        Docstring for __init__
        

         x & y: top left position of button
         
         button_colour: color as rgb (default white)
         hover_colour: color on mouseover as rgb (default gray)

         one of the following:
         width & height: dimensions 
         image: image rendered on top of button
        '''
        self.x = x 
        self.y = y

        self.button_col = button_colour
        self.hover_col = hover_colour

        self.width = width
        self.height = height

        self.on_click = on_click

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.click_col = self.BLACK
        self.image = image

        
        
        # print an error if we are missing the image or width and height
        if (not self.image) and (self.width == 0 or self.height == 0):
            print("ERROR: Button has no image and no dimensions!")

        # make Rect object
        if self.image:
            self.rect = self.image.get_rect()
            self.width = self.rect.width
            self.height = self.rect.height
        else:    
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        
        

    def update(self, actions):

        pressed = False
        # mouse position
        self.hovered = self.rect.collidepoint(actions["mouse_pos"])
        # check for mouseover
        if self.hovered:
            if actions["mouse_click"]:
                self.clicked = True
                pressed = True
            else:
                self.clicked = False
        
        return pressed
                

    def render(self, x, y, surface):
        '''
        Handels user actions, mouseover and click 
        and calls draw_button

        x & y coordinates
        surface: surface to render object on
        actions: user inputs dictionary

        Return True when button is clicked
        '''
        self.rect.x = x
        self.rect.y = y

        if self.clicked:
            self.draw_button(self.click_colour, surface)
        elif self.hovered:
            self.draw_button(self.hover_colour, surface)
        else:
            self.draw_button(self.button_colour, surface)
    
    def draw_button(self, col, surface):
        '''
        Draws button onto surface
    
        col: button col, default, hover or click
        surface: surface for rendering
        '''
        # draw rect

        if self.image:
            pygame.draw.rect(surface, col, self.rect)
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, col, self.rect)

        draw_shading_for_rect(self.WHITE, self.rect,
                               surface, right_color = self.BLACK)
        


        
