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

        # state dictionary
        self.state = {"selected": False, "choosing": False, "jump": False, "drag": False,
                       "throw": False, 'moving': False, "locked": False, "eliminated": False}


        

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

        self.reset_pos()


    def clicking(self, actions):
        '''
        handels hovered mouse clicks for Obj

        doesn't change choosing state

        actions: user inputs dictionary
        '''

        # Selecting
        if not (self.state["jump"] or self.state["throw"]):
        # print("select condition met") 

            # print("collision")
            self.state["selected"] = not self.state["selected"]
            # print(f"state: {self.state}")

        # Jumping / entering into drag
        # requere new click
        if self.state["jump"] and not self.state["drag"]:
            if actions["mouse_click"]:
                self.mouse_pos_list = [actions["mouse_pos"]]
                self.state["drag"] = True
