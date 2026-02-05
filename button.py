import pygame

# Button that can have optionally image or text
class Button():
    def __init__(self, x, y, width, height, button_colour=(255, 255, 255),
                  hover_colour=(139, 139, 139), image=None, text=None, font=None):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.button_col = button_colour
        self.hover_col = hover_colour

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.click_col = self.black
        self.image = image
        self.text = text
        self.font = font


        # make Rect object
        if self.image:
            self.rect = self.image.get_rect()
        else:    
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        

    def action_on_button(self, x, y, surface, actions):

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
            if pygame.mouse.get_just_pressed()[0]:
                self.draw_button(self.click_col, surface)
                # pressed button
                pressed = True
                actions["mouse_click"] = False
        else:
            # default button
            self.draw_button(self.button_col, surface)
        return pressed
    
    def draw_button(self, col, surface):
        # draw rect
        pygame.draw.rect(surface, col, self.rect)

        # Draw shading
        # top
        pygame.draw.line(surface, self.white, (self.x, self.y), (self.x + self.width, self.y), 2)
        # left
        pygame.draw.line(surface, self.white, (self.x, self.y), (self.x, self.y + self.height), 2)
        # right
        pygame.draw.line(surface, self.black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)
        # bottom
        pygame.draw.line(surface, self.black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        

        if self.image:
            pass
        if self.text:
            pass