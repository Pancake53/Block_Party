import pygame

class GameObject():
    '''Interactive movable object in game world
    
    Handels rendering, updating pos, collision testing, actions

    Important constants for game physics
    '''
    def __init__(self, x_pos, y_pos):
        '''Initialize attributes
        
        '''
        # x & y
        self.origin = (x_pos, y_pos)
        self.x_pos = float(x_pos)
        self.y_pos = float(y_pos)
        self.x_speed = 0
        self.y_speed = 0.01

        # Game physics
        self.gravity = 200
        self.throw_multiplier = 2.5
        self.max_velocity = 300
        self.min_jump = 10
        # self.air_resistance = 0.99 # not in use 

        # state dictionary
        self.state = {"selected": False, "jump": False}

        # for jumping, throwing
        self.mouse_pos_list = []
  
        # rect
        self.CHARACTER_SIZE = 24
        self.rect = pygame.Rect(x_pos, y_pos, self.CHARACTER_SIZE, self.CHARACTER_SIZE * 2)

    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)

    def update(self, dt, actions, tiles):
        # if in place no momentum no need to update position
        if (self.x_speed != 0) or (self.y_speed != 0):
            self.update_pos(dt, tiles)
        self.handle_actions(actions)


    def collision_test(self, tiles):
        '''tests if gameObject has overlapping with collision tiles
        then return list of overlapping tiles
        '''
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions
    
    def update_pos(self, dt, tiles):
        # self.y_pos += self.y_speed\
        # self.rect.y = self.y_pos
        # collision_test
        # self.x_pos += self.x_speed
        # self.rect.x = self.x_pos
        # collision_test
        pass

    def add_momentum(self, x_speed, y_speed): 
        ''' give gameObject clamped x and y momentum
        '''
        # logic: speed can be positive or negative
        self.x_speed = max(-self.max_velocity, # caps max negative
                        min(x_speed, self.max_velocity)) # caps max positive
        self.y_speed = max(-self.max_velocity,
                        min(y_speed, self.max_velocity))

    def handle_actions(self, actions):
        '''handels actions for gameObject
          based on actions dictionary from Game'''

        if actions["left"]:
            self.add_momentum(-100, -100)
        if actions["right"]:
            self.add_momentum(100, -100)
        if actions["action1"]:
            # reset position
            self.x_pos = self.origin[0]
            self.y_pos = self.origin[1]
            self.x_speed = 0
            self.y_speed = 0.01

        if actions["mouse_pressed"] and not self.state["jump"] and not self.state["throw"]:
            mouse_pos = pygame.mouse.get_pos()


        elif actions["mouse_pressed"] and self.state["jump"]:
            mouse_pos = pygame.mouse.get_pos()
            while len(self.mouse_pos_list) > 2:
                self.mouse_pos_list.pop()
            self.mouse_pos_list.append(mouse_pos)

        if (actions["mouse_pressed"] == False) and (len(self.mouse_pos_list) >= 2):
            print("time to throw!")
            x_speed = (self.mouse_pos_list[0][0] -self.mouse_pos_list[-1][0]) * self.throw_multiplier
            y_speed = (self.mouse_pos_list[0][1] -self.mouse_pos_list[-1][1]) * self.throw_multiplier
            self.add_momentum(x_speed, y_speed)

            self.mouse_pos_list = []
            self.reset_state()


    def reset_state(self):
        for k in self.state:
            self.state[k] = False
