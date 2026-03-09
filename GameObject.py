import pygame

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
        self.x_pos = float(x_pos)
        self.y_pos = float(y_pos)
        self.x_speed = 0
        self.y_speed = 0

        self.game_world = game_world

        # Game physics
        self.gravity = 250
        self.throw_multiplier = 2.5
        self.max_velocity = 300
        self.min_jump = 10
        # self.air_resistance = 0.99 # not in use

        # state dictionary
        self.state = {"selected": False, "choosing": False, "jump": False, "drag": False,
                       "throw": False, 'moving': False, "locked": False, "eliminated": False}

        # for jumping, throwing
        self.mouse_pos_list = []
  
        # rect
        self.CHARACTER_SIZE = 24
        self.rect = pygame.Rect(x_pos, y_pos, self.CHARACTER_SIZE, self.CHARACTER_SIZE * 2)

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
        if (self.x_speed != 0) or (self.y_speed != 0):
            self.update_pos(dt, tiles)
            self.state['moving'] = True
        
        else:
            self.state['moving'] = False

        if not self.state['locked']:    
            self.handle_actions(actions)


    def collision_test(self, tiles):
        '''
        tests if gameObject has overlapping with collision tiles

        tiles: game levels collision tiles

        Returns:
        collisions: list of overlapping tiles
        '''
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
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
        self.y_pos += self.y_speed * dt # for calculations
        self.rect.y = round(self.y_pos) # update rect w calculated pos
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
        self.x_pos += self.x_speed * dt # x_pos is used for calculations
        self.rect.x = round(self.x_pos) # update rect position for collision_test
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
        # logic: speed can be positive or negative
        self.x_speed = max(-self.max_velocity, # caps max negative
                        min(x_speed, self.max_velocity)) # caps max positive
        self.y_speed = max(-self.max_velocity,
                        min(y_speed, self.max_velocity))

    def handle_actions(self, actions):
        '''
        handels actions for gameObject
        based on actions dictionary from Game

        actions: user inputs dictionary

        '''
        # reset position (for testing)
        if actions["action1"]:
            self.reset_pos()
            

        # mouse on Obj
        hovered = self.rect.collidepoint(actions["mouse_pos"])

        # Handle mouse clicks for selecting obj
        if hovered and not self.state['locked']:
            if actions["mouse_click"]:
                self.clicking(actions)

        if self.state['selected']:
            # Dragging
            if self.state["drag"]:
                self.dragging(actions)


            # Releasing
            if (not actions["mouse_pressed"]) and (len(self.mouse_pos_list) >= 2):
                self.releasing(actions)

            if self.state["throw"]: # bomb placeholder
                self.throw_bomb(actions)

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
                self.mouse_pos_list = [actions["mouse_pos"]]
                self.state["drag"] = True

    def dragging(self, actions):
        '''
        handels what happens during the mousedrag

        actions: user inputs dictionary
        '''

        if self.state["drag"]:
            if actions["mouse_pressed"]:
                while len(self.mouse_pos_list) > 2:
                    self.mouse_pos_list.pop()
                self.mouse_pos_list.append(actions["mouse_pos"])
                # render line or arrow function

    def releasing(self):
        '''
        handels giving Obj velocity after mousedrag

        actions: user inputs dictionary
        '''
        x_speed = (self.mouse_pos_list[0][0] -self.mouse_pos_list[-1][0]) * self.throw_multiplier
        y_speed = (self.mouse_pos_list[0][1] -self.mouse_pos_list[-1][1]) * self.throw_multiplier
        self.add_momentum(x_speed, y_speed)

        self.mouse_pos_list = []
        self.reset_state()

    def throw_bomb(self):
        pass

    def reset_pos(self):
        '''
        reset position
        '''
        # calculated values to origin
        self.x_pos = self.origin[0]
        self.y_pos = self.origin[1]
        # move rect to calculated values
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        # remove velocity
        self.x_speed = 0
        self.y_speed = 0

    def reset_state(self):
        '''
        False all states in obj state dictionary
        '''
        for k in self.state:
            self.state[k] = False
