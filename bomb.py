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
        
        x & y: bombs coordinates
        image: asset of the bomb_image
        '''
        super().__init__(x_pos, y_pos, game_world)
        self.image = image
        self.rect = image.get_rect()
        self.WIDTH = self.rect.width
        self.HEIGHT = self.rect.height

    def update(self, dt, actions, tiles):
        '''
        Updates obj position, if obj is moving
        Handels inputs

        dt: delta time 
        actions: user inputs dictionary
        tiles: game levels collision tiles
        '''
        if self.state['locked']:
            # only update if bomb is flying
            
            # check if out of bounds on x axis
            if self.x_pos < - self.WIDTH / 2:
                self.out_of_bounds("left")
            elif self.x_pos > self.game_world.game.GAME_W - self.WIDTH / 2:
                self.out_of_bounds("right")
            # check if out of bounds on y axis
            elif self.y_pos > self.game_world.game.GAME_H:
                self.out_of_bounds("bottom")
            else:
                # moving and not out of bounds
                self.state['moving'] = True
                self.update_pos(dt, tiles)
                
            


        if not self.state['locked']:    
            self.handle_actions(actions)
    

    def render(self, surface):
        '''
        Rendering bomb onto game canvas
        
        surface: surface to render object on
        '''

        if self.state['selected']:
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

    def out_of_bounds(self, side):
        # levels that wrap around on sides
        if self.game_world.wrap_around:
            self.wrap_around(side)
        else:
            self.reset_state()
            self.reset_pos()

    def wrap_around(self, side):
        '''
        wrap around logic
        '''
        match side:
            # moving left -> move to right side of screen
            case "left":
                self.x_pos = self.game_world.game.GAME_W - self.WIDTH / 2
            # moving right -> move to left side side of screen
            case "right":
                self.x_pos = - self.WIDTH / 2
            # fell off the map
            case "bottom":
                self.reset_state()
                self.reset_pos()

            case _:
                pass    
                

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
        # print(f'Game World State: {self.game_world.state}')

    def fix_spawn(self, tiles): # TODO
        '''
        handels moving bombs spawn when it spawns
        too close to a wall

        tiles: Rect, collision tiles that collide with da bomb
        '''
        # only left and right side of bomb can not be colliding with a wall
        # so only need to look at x coordinates
        

        for tile in tiles:

            bomb_L = self.x_pos
            bomb_R = bomb_L + self.WIDTH

            tile_L = tile.x
            tile_R = tile_L + tile.width

            # right side of tile / left side of bomb
            if (self.rect.centerx > tile.centerx and
                tile_R > bomb_L):
                # print("left side of bomb colliding")
                # update calculations
                self.x_pos += tile_R - bomb_L
                # update actual position
                self.rect.x = self.x_pos
                continue

            # left side of tile / right side of bomb
            if (self.rect.centerx < tile.centerx and
                tile_L < bomb_R):
                # print("right side of bomb colliding")
                # update calculations
                self.x_pos -= bomb_R - tile_L 
                # update actual position
                self.rect.x = self.x_pos


    
                
            
