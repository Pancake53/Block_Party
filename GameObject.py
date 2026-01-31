import pygame

class GameObject():
    def __init__(self, x_pos, y_pos):
        self.origin = (x_pos, y_pos)
        self.x_pos = float(x_pos)
        self.y_pos = float(y_pos)
        self.x_speed = 0
        self.y_speed = 0.01
        self.gravity = 200
        self.air_resistance = 0.99
        self.state = {"selected": False, "jump": False}
        self.mouse_pos_list = []
        self.throw_multiplier = 1
        self.max_velocity = 600

        self.CHARACTER_SIZE = 24
        self.rect = pygame.Rect(x_pos, y_pos, self.CHARACTER_SIZE, self.CHARACTER_SIZE * 2)

    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)

    def update(self, dt, actions, tiles):
        
        if (self.x_speed != 0) or (self.y_speed != 0):
            self.update_pos(dt, tiles)
        self.handle_actions(dt, actions, tiles)


    def collision_test(self, tiles):
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
        self.x_speed = max(-self.max_velocity,
                        min(x_speed, self.max_velocity))
        self.y_speed = max(-self.max_velocity,
                        min(y_speed, self.max_velocity))

    def handle_actions(self, dt, actions, tiles):

        if actions["left"]:
            self.add_momentum(-100, -100)
        if actions["right"]:
            self.add_momentum(100, -100)
        if actions["action1"]:
            self.x_pos = self.origin[0]
            self.y_pos = self.origin[1]
            self.x_speed = 0
            self.y_speed = 0.01

        if actions["M1"] and not self.state["jump"] and not self.state["throw"]:
            mouse_pos = pygame.mouse.get_pos()


        elif actions["M1"] and self.state["jump"]:
            mouse_pos = pygame.mouse.get_pos()
            while len(self.mouse_pos_list) > 2:
                self.mouse_pos_list.pop()
            self.mouse_pos_list.append(mouse_pos)

        if (actions["M1"] == False) and (len(self.mouse_pos_list) >= 2):
            print("time to throw!")
            x_speed = (self.mouse_pos_list[0][0] -self.mouse_pos_list[-1][0]) * self.throw_multiplier
            y_speed = (self.mouse_pos_list[0][1] -self.mouse_pos_list[-1][1]) * self.throw_multiplier
            self.add_momentum(x_speed, y_speed)

            self.mouse_pos_list = []
            self.reset_state()


    def reset_state(self):
        for k in self.state:
            self.state[k] = False
