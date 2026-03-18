import pygame
from gameObject import GameObject

class Bomb(GameObject):
    '''Player thrown object.

    Handels rendering, updating position, explosion
    
    Attributes:
        x, y: top left position x and y
        image: image of bomb selected
    '''
    def __init__(self, x_pos, y_pos, game_world, image):
        '''Initialize attributes, rectangle, state manager
        
        x & y: bombs center coordinates
        image: asset of the bomb_image
        '''
        super().__init__(x_pos, y_pos, game_world)
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = (x_pos, y_pos)


    def render(self, surface):
        '''
        Rendering bomb onto game canvas
        
        surface: surface to render object on
        '''

        if self.state['selected'] or self.state['moving']:
            surface.blit(self.image, self.rect) 


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
        x_pos = self.rect.centerx
        y_pos = self.rect.centery
        self.game_world.activate_explosion(x_pos, y_pos)

        self.reset_state()
        self.reset_pos()


    def clicking(self, actions):
        '''
        handels hovered mouse clicks for Obj

        for bomb no selecting,
        only switching to drag state

        actions: user inputs dictionary
        '''

        # Jumping / entering into drag
        # requere new click
        if self.state["jump"] and not self.state["drag"]:
            if actions["mouse_click"]:
                self.mouse_pos_list = [actions["mouse_pos"]]
                self.state["drag"] = True

    def releasing(self):
        '''
        handels giving Obj velocity after mousedrag
        '''
        x_speed = (self.mouse_pos_list[0][0] -self.mouse_pos_list[-1][0]) * self.throw_multiplier
        y_speed = (self.mouse_pos_list[0][1] -self.mouse_pos_list[-1][1]) * self.throw_multiplier
        self.add_momentum(x_speed, y_speed)

        self.mouse_pos_list = []
        self.state['locked'] = True
        self.game_world.state['turn'] += 1
        print(f'Game World State: {self.game_world.state}')