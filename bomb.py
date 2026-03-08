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

        # state dictionary
        self.state = {"selected": False, "jump": False, "drag": False, "throw": False}
        

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
        self.handle_actions(actions)
        print(self.state)

    def update_pos_x(self, dt, tiles):
        '''
        update position x wise and react to collisions
        
        dt: delta time 
        tiles: game levels collision tiles
        '''
        # x movement
        self.x_pos += self.x_speed * dt # x_pos is used for calculations
        self.rect.x = round(self.x_pos) # update rect position for collision_test
        collisions = self.collision_test(tiles)

        if collisions:
            #collision on x axis
            self.collision_x_axis(collisions)

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
        x_exp = self.rect.x
        y_exp = self.rect.y

        self.x_speed, self.y_speed = 0, 0
