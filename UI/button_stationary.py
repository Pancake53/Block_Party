import pygame
from helpers import draw_shading_for_rect
from dataclasses import dataclass
from typing import Callable

@dataclass
# Button that can have optionally image or text
class ButtonStationary():
    '''Class for UI buttons
    
    returns True when clicked

    handels rendering and actions on button
    '''
    name: str
    x: int
    y: int
    on_click: Callable[[str], None] 
    button_colour: tuple =(0, 153, 136)
    hover_colour: tuple =(139, 139, 139)
    width: int =0
    height: int =0
    image: object =None # asset
    


    def __post_init__(self):

        

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.click_colour = self.BLACK
        
        # print an error if we are missing the image or width and height
        if (not self.image) and (self.width == 0 or self.height == 0):
            print("ERROR: Button has no image and no dimensions!")

        # make Rect object
        if self.image:
            self.rect = self.image.get_rect()
            self.width = self.rect.width
            self.height = self.rect.height

            self.rect.x = self.x
            self.rect.y = self.y

        else:    
            self.rect = pygame.Rect(self.x, self.y, 
                                    self.width, self.height)
            
        self.hovered, self.clicked = False, False

        
    def update(self, actions, position = None):
        if position:
            self.rect.topleft = position

        # mouse position
        self.hovered = self.rect.collidepoint(actions["mouse_pos"])
        # check for mouseover
        if self.hovered:
            if actions["mouse_click"]:
                self.clicked = True
                self.on_click(self.name)
            else:
                self.clicked = False
        else:
            self.clicked = False
                

    def render(self, surface):
        '''
        Handels user actions, mouseover and click 
        and calls draw_button

        x & y coordinates
        surface: surface to render object on
        actions: user inputs dictionary

        Return True when button is clicked
        '''

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
        # draw rec

        if self.image:
            pygame.draw.rect(surface, col, self.rect)
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, col, self.rect)

        draw_shading_for_rect(self.WHITE, self.rect,
                               surface, right_color = self.BLACK)
        


        
