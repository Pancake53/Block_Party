import pygame
from pygame.math import Vector2
from physics import Physics

class GameObject():
    '''Interactive movable object in game world
    
    Handels rendering, updating pos, collision testing, actions

    Important constants for game physics
    '''
    def __init__(self, x_pos, y_pos, game_world):
        '''
        Initialize attributes
        
        x & y: coordinates on canvas
        '''
        # x & y
        self.origin = (x_pos, y_pos)
        # position on screen 
        # takes offset into account
        self.x_screen = float(x_pos)
        self.y_screen = float(y_pos)
        # position in the entire level
        # useful in out_of_bounds
        self.x_level = self.x_screen
        self.y_level = self.y_screen
        self.x_speed = 0
        self.y_speed = 0

        self.game_world = game_world

        # Game physics
        self.gravity = 250
        self.throw_multiplier = 2.5
        self.max_velocity = 330
        self.min_jump = 10
        self.force_mp = 250
        # self.air_resistance = 0.99 # not in use

        # state dictionary
        self.state = {"selected": False, "choosing": False, "jump": False, "drag": False,
                       "throw": False, 'moving': False, "locked": False, "eliminated": False}

        # for jumping, throwing
        self.throwing_list = []
  
        # rect
        self.CHARACTER_SIZE = 24

        # how many pixels can in map to be considered 
        # to not be out of bounds
        # Buffer for levels with wrapping left/right
        self.out_of_bounds_buffer = 5 # only Char uses

        # for camera, if no wrap around let objects fall out of screen
        # despite the offset by camera
        self.edge_buffer = (
            self.game_world.camera.max_offset 
            if not self.game_world.wrap_around
            else 0)

        # default Rect
        self.rect = pygame.Rect(6, 7, 6, 7)
        self.WIDTH = self.rect.width
        self.HEIGHT = self.rect.height
      

    def render(self, surface):
        '''
        Render obj on given surface

        surface: game canvas
        '''
        pygame.draw.rect(surface, self.colour, self.rect)



    def update(self, dt, actions, tiles):
        '''
        Updates obj position, if obj is moving
        Handels inputs

        dt: delta time 
        actions: user inputs dictionary
        tiles: game levels collision tiles
        '''
        if not self.state['eliminated']:
            
            # only update if obj is moving and on the screen
            if (self.x_speed != 0) or (self.y_speed != 0):

                # update level position
                self.x_level = self.x_screen - self.game_world.camera.total_offset_x
                self.y_level = self.y_screen - self.game_world.camera.total_offset_y

                #  check if out of bounds on x axis
                if self.x_level < - self.WIDTH / 2 - self.edge_buffer:
                    self.out_of_bounds("left")
                elif self.x_level > (self.game_world.game.GAME_W
                                      - self.WIDTH / 2 + self.edge_buffer):
                    self.out_of_bounds("right")
                # check if out of bounds on y axis
                elif self.y_level > self.game_world.game.GAME_H + self.edge_buffer:
                    self.out_of_bounds("bottom")
                else:
                    # moving and not out of bounds
                    self.state['moving'] = True
                    self.update_pos(dt, tiles)
                
            else:
                self.state['moving'] = False


            if not self.state['locked']:    
                self.handle_actions(actions)

            if self.throwing_list:
                self.game_world.update_arrow(
                Vector2(*self.throwing_list[0]),
                Vector2(*self.throwing_list[1])
                )

    def collision_test(self, tiles):
        '''
        tests if gameObject has overlapping with collision tiles

        tiles: game levels collision tiles

        Returns:
        collisions: list of overlapping tiles
        '''
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                collisions.append(tile.rect)
        return collisions
    
    def update_pos(self, dt, tiles): # only active if we have speed
        '''
        Updates object position

        dt: delta time 
        tiles: game levels collision tiles
        '''
        self.update_pos_y(dt, tiles)
        self.update_pos_x(dt, tiles)



    def update_pos_y(self, dt, tiles):
        '''
        update position y wise and react to collisions
        
        dt: delta time 
        tiles: game levels collision tiles
        '''
        self.y_screen += self.y_speed * dt # for calculations
        self.rect.y = round(self.y_screen) # update rect w calculated pos
        collisions = self.collision_test(tiles)
        # print(f"y: {round(self.y_speed,3)}")
        if not collisions:
            self.y_speed += self.gravity * dt
        else: # collision on y axis
            self.collision_y_axis(collisions)

    def collision_y_axis(self, collisions):
        '''
        reaction to collision on y axis
        
        collisions: list of overlapping tiles
        '''
        pass

    def update_pos_x(self, dt, tiles):
        '''
        update position x wise and react to collisions
        
        dt: delta time 
        tiles: game levels collision tiles
        '''
        # x movement
        self.x_screen += self.x_speed * dt # x_pos is used for calculations
        self.rect.x = round(self.x_screen) # update rect position for collision_test
        collisions = self.collision_test(tiles)

        if not collisions: # no collision
            if abs(self.x_speed) < self.x_stop: # low speed limit
                self.x_speed = 0
            # else:
                # self.x_speed *= self.air_resistance
        else: # collision on x axis
            
            self.collision_x_axis(collisions)

    def collision_x_axis(self, collisions):
        '''
        reaction to collision on x axis
        
        collisions: list of overlapping tiles
        '''
        pass

    def add_momentum(self, x_speed, y_speed): 
        ''' 
        give gameObject clamped x and y momentum

        x_speed: given velocity on x axis
        y_speed: given velocity on y axis
        '''
        # # logic: speed can be positive or negative
        # self.x_speed = max(-self.max_velocity, # caps max negative
        #                 min(x_speed, self.max_velocity)) # caps max positive
        # self.y_speed = max(-self.max_velocity,
        #                 min(y_speed, self.max_velocity))

        speed_vec = Vector2(x_speed, y_speed)
        total_speed = speed_vec.length()

        if total_speed > self.max_velocity:
            normalized = speed_vec.normalize()
            speed_vec = self.max_velocity * normalized

        self.x_speed = speed_vec[0]
        self.y_speed = speed_vec[1]



    def handle_actions(self, actions):
        '''
        handels actions for gameObject
        based on actions dictionary from Game

        actions: user inputs dictionary

        '''
       
            

        # Handle mouse clicks for selecting obj
        

        # mouse on Obj
        hovered = self.rect.collidepoint(actions["mouse_pos"])

        if hovered:
            if actions["mouse_click"]:
                self.clicking(actions)

        if self.state['selected']:
            # Dragging
            if self.state["drag"]:
                self.dragging(actions)


            # Releasing
            if (not actions["mouse_pressed"]) and (len(self.throwing_list) == 2):
                self.releasing()

            if self.state["throw"]: # bomb placeholder
                self.throw_bomb()

    def clicking(self, actions):
        '''
        handels hovered mouse clicks for Obj
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
                self.throwing_list = []
                self.state["drag"] = True

    def dragging(self, actions):
        '''
        handels what happens during the mousedrag

        actions: user inputs dictionary
        '''

        if self.state["drag"]:
            if actions["mouse_pressed"]:
                self.throwing_list = [(self.rect.centerx, self.rect.centery),
                                      actions['mouse_pos'] ]
                # render line or arrow function

    def releasing(self):
        '''
        handels giving Obj velocity after mousedrag

        actions: user inputs dictionary
        '''
        x_vector = (self.throwing_list[0][0] -self.throwing_list[-1][0]) * self.throw_multiplier
        y_vector = (self.throwing_list[0][1] -self.throwing_list[-1][1]) * self.throw_multiplier
        self.add_momentum(x_vector, y_vector)

        self.throwing_list = []
        self.reset_state()
        self.game_world.next_turn()


    def throw_bomb(self):
        pass

    def reset_pos(self):
        '''
        reset position
        '''
        # calculated values to origin
        self.x_screen = self.origin[0]
        self.y_screen = self.origin[1]
        # move rect to calculated values
        self.rect.x = self.x_screen
        self.rect.y = self.y_screen
        # remove velocity
        self.x_speed = 0
        self.y_speed = 0

    def reset_state(self):
        '''
        False all states in obj state dictionary
        '''
        for state in self.state:
            self.state[state] = False

    def out_of_bounds(self):
        pass

    def on_camera_move(self, x_offset, y_offset):
        '''
        update char screen position based on camera movement

        x_offset: offset x axis
        y_offset: offset y axis 
        '''
        # update screen x & y
        self.x_screen += x_offset
        self.y_screen += y_offset

        # update rect
        self.rect.x = self.x_screen
        self.rect.y = self.y_screen