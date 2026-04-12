import pygame
from pygame.math import Vector2


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

        

        # state dictionary
        self.state = {"selected": False, "choosing": False, "jump": False, "drag": False,
                       "throw": False, 'moving': False, "locked": False, "eliminated": False}

        # for jumping, throwing
        self.throwing_list = []
        self.diff_vector = None
  
        # rect
        self.CHARACTER_SIZE = 24

        # for camera, if no wrap around let objects fall out of screen
        # despite the offset by camera
        self.edge_buffer = self.game_world.camera.max_offset 

        # update function -> check if out of bounds
        # func is different if level wraps around
        if self.game_world.wrap_around:
            self.update_chosen = self.update_wrap_around
        else:
            self.update_chosen = self.update_normal
        
        


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
        calls the appropriate update function for gamemode
        '''
        if not self.state['eliminated']:
            self.update_chosen(dt, actions, tiles)
            print("updating gameObj")

            

    def update_normal(self, dt, actions, tiles):
        '''
        Updates obj position, if obj is moving
        Handels inputs

        dt: delta time 
        actions: user inputs dictionary
        tiles: game levels collision tiles
        '''
        
            
        # only update if obj is moving and on the screen
        if (self.x_speed != 0) or (self.y_speed != 0):
            if not self.check_out_of_bounds_normal():
                # moving and not out of bounds
                self.state['moving'] = True
                self.update_pos(dt, tiles)
        else:
            self.state['moving'] = False


        if not self.state['locked']:    
            self.handle_actions(actions)

        # when dragging 
        self.handle_drag()
 
    def check_out_of_bounds_normal(self):
        '''
        out of bounds check logic for normal levels

        return True if out of bounds
        '''
        # update level position
        self.x_level = self.x_screen - self.game_world.camera.total_offset_x
        self.y_level = self.y_screen - self.game_world.camera.total_offset_y

        #  check if out of bounds on x axis
        if self.x_level < - self.WIDTH / 2 - self.edge_buffer:
            self.out_of_bounds("left")
            return True
        elif self.x_level > (self.game_world.game.GAME_W
                                - self.WIDTH / 2 + self.edge_buffer):
            self.out_of_bounds("right")
            return True
        # check if out of bounds on y axis
        elif self.y_level > self.game_world.game.GAME_H + self.edge_buffer:
            self.out_of_bounds("bottom")
            return True
        # not out of bounds
        return False

    def update_wrap_around(self, dt, actions, tiles):
        '''
        Updates obj position, if obj is moving
        Handels inputs

        dt: delta time 
        actions: user inputs dictionary
        tiles: game levels collision tiles
        '''
        
            
        # only update if obj is moving or cam moved:
        if ((self.x_speed != 0) or 
            (self.y_speed != 0)):
            if not self.check_out_of_bounds_wrap():
                # not out of bounds / no need to wrap
                self.state['moving'] = True
                self.update_pos(dt, tiles)
        else:
            self.state['moving'] = False


        if not self.state['locked']:    
            self.handle_actions(actions)


        # when dragging 
        self.handle_drag()  

    def check_out_of_bounds_wrap(self):
        '''
        out of bounds check logic for wrapping levels

        returns True if out of bounds and need to wrap
        '''

        #  check if out of bounds on x axis
        if self.x_screen < - self.WIDTH / 2:
            self.out_of_bounds("left")
            return True
        elif self.x_screen > (self.game_world.game.GAME_W
                                - self.WIDTH / 2):
            self.out_of_bounds("right")
            return True
        # check if out of bounds on y axis
        elif self.y_screen > self.game_world.game.GAME_H + self.edge_buffer:
            self.out_of_bounds("bottom")
            return True
        
        return False


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
        self.rect.y = int(self.y_screen) # update rect w calculated pos
        collisions = self.collision_test(tiles)
        # print(f"y: {round(self.y_speed,3)}")
        if not collisions:
            self.y_speed += self.game_world.physics.gravity * dt
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
        self.rect.x = int(self.x_screen) # update rect position for collision_test
        collisions = self.collision_test(tiles)

        if not collisions: # no collision
            if abs(self.x_speed) < self.game_world.physics.X_STOP: # low speed limit
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

    def add_momentum(self, direction_vec): 
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

        # multiply to get more momentum
        direction_vec *= self.game_world.physics.throw_multiplier
        # if total momentum overspill normalize
        if direction_vec.length() > self.game_world.physics.max_velocity:
            normalized = direction_vec.normalize()
            direction_vec = self.game_world.physics.max_velocity * normalized

        # add momentum to object
        self.x_speed = direction_vec[0] 
        self.y_speed = direction_vec[1] 



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

            # resetting actions
            if actions["m3"]:
                self.throwing_list = []
                self.reset_state()
                if self.__class__.__name__ == 'Bomb':
                    self.reset_pos()


            # Releasing
            if (not actions["m1"]) and (len(self.throwing_list) == 2):
                self.releasing()

            if self.state["throw"]: # bomb placeholder
                self.throw_bomb()

        

    def clicking(self, actions):
        '''
        handels hovered mouse clicks for Obj
        '''

        # Selecting
        if not (self.state["jump"] or self.state["throw"]):
            self.state["selected"] = not self.state["selected"]
            

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
            if actions["m1"]:
                self.throwing_list = [(self.rect.centerx, self.rect.centery),
                                      actions['mouse_pos'] ]
            
    def handle_drag(self):
        '''
        handels what happens to dragging data
        '''
        if self.throwing_list:
            self.diff_vector = Vector2(self.throwing_list[0]) - Vector2(self.throwing_list[1])
            if self.diff_vector.length() > self.game_world.physics.MIN_JUMP:
                self.game_world.update_arrow(
                    self.throwing_list[0], 
                    self.throwing_list[1], self.diff_vector)
        
                

    def releasing(self):
        '''
        handels giving Obj velocity after mousedrag

        actions: user inputs dictionary
        '''
        # if over minimum jump, then jump
        if self.diff_vector.length() > self.game_world.physics.MIN_JUMP:
            self.add_momentum(self.diff_vector)
            self.game_world.next_turn()
            self.throwing_list = []
            if self.__class__.__name__ == 'Bomb':
                self.state['locked'] = True
            else:
                self.reset_state()

        # else reset
        else:
            self.throwing_list = []
            self.reset_state()
            if self.__class__.__name__ == 'Bomb':
                self.reset_pos()

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

    def out_of_bounds(self, side):
        '''
        handels logic for going outside of map
        '''
        # levels that wrap around on sides
        if self.game_world.wrap_around:
            self.wrap_around(side)
        # normal levels
        else:
            self.eliminated()

    def wrap_around(self, side):
        '''
        wrap around logic

        side: of map
        '''
        match side:
            # moving left -> move to right side of the screen
            case 'left':
                self.x_screen += self.game_world.game.GAME_W
                self.rect.x = self.x_screen
            # moving right -> move to left side
            case 'right':
                self.x_screen -= self.game_world.game.GAME_W
                self.rect.x = self.x_screen
            # fell through the floor
            case 'bottom':
                self.eliminated()

    def on_camera_move(self, x_offset, y_offset):
        '''
        update char screen position based on camera movement

        x_offset: offset x axis
        y_offset: offset y axis 
        '''
        # update screen x & y
        self.x_screen += x_offset
        self.y_screen += y_offset

        if self.game_world.wrap_around:
            if self.check_out_of_bounds_wrap():
                return

        # update rect
        self.rect.x = self.x_screen
        self.rect.y = self.y_screen
