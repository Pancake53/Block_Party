import pygame
from helpers import draw_shading_for_rect

# Button that can have optionally image or text
class Button():
    '''Class for UI buttons
    
    returns True when clicked

    handels rendering and actions on button
    '''
    def __init__(self, x, y, button_colour=(255, 255, 255),
                  hover_colour=(139, 139, 139), width=0, height=0, image=None):
        
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

        
        

    def action_on_button(self, x, y, surface, actions) -> bool:
        '''
        Handels user actions, mouseover and click 
        and calls draw_button

        x & y coordinates
        surface: surface to render object on
        actions: user inputs dictionary

        Return True when button is clicked
        '''
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

        pressed = False
        # mouse position
        hovered = self.rect.collidepoint(actions["mouse_pos"])

        # check for mouseover
        if hovered:
            # hover button
            self.draw_button(self.hover_col, surface)
            # click button
            if actions["mouse_click"]:
                self.draw_button(self.click_col, surface)
                # pressed button
                pressed = True
        else:
            # default button
            self.draw_button(self.button_col, surface)
        return pressed
    
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
        
