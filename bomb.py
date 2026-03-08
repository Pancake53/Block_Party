import pygame
from gameObject import GameObject

class Bomb(GameObject):
    '''Player thrown object.

    Handels rendering, updating position, explosion
    
    Attributes:
        x, y: top left position x and y
        image: image of bomb selected
    '''
    def __init__(self, x_pos, y_pos, image):
        '''Initialize attributes, rectangle, state manager
        
        x & y: bombs center coordinates
        image: asset of the bomb_image
        '''
        super().__init__(x_pos, y_pos)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.state = {"selected": True, "jump": True, "throw": False}
        

    def render(self, surface):
        '''
        Rendering bomb onto game canvas
        
        surface: surface to render object on
        '''
        surface.blit(self.image, self.rect)

    def update(self, dt, actions, tiles):
        '''
        Updating bombs position in game        

        dt: delta time
        actions: user inputs dictionary
        tiles: game worlds collision tiles
        '''
        
        if (self.x_speed != 0) or (self.y_speed != 0):
            self.update_pos(dt, tiles)
        self.handle_actions(dt, actions, tiles)

    def collision_y_axis(self, collisions):
        '''
        reaction to collision on y axis
        
        collisions: list of overlapping tiles
        '''
        self.explosion()

    def collision_x_axis(self, collisions):
        '''
        reaction to collision on x axis
        
        collisions: list of overlapping tiles
        '''
        self.explosion()

    def explosion(self):
        pass