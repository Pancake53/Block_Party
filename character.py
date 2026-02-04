import pygame
from GameObject import GameObject


class Character(GameObject):
    def __init__(self, game_world, team_id, width, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.team_id = team_id
        self.game_world = game_world
        self.width = width

        self.colour = [(184, 43, 43), (95, 184, 43)][team_id]
        self.y_stop = 20
        self.x_stop = 1
        self.retention = 0.25 # * width

        self.rect = pygame.Rect(x_pos, y_pos, self.CHARACTER_SIZE * width, self.CHARACTER_SIZE * 2)

        self.state = {"selected": False, "jump": False, "throw": False}
        self.selections = ["jump", "throw", "surrender"]

    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)
        if self.state["selected"]:
            self.render_selections(surface)

    def update(self, dt, actions, tiles):
        
        if (self.x_speed != 0) or (self.y_speed != 0):
            self.update_pos(dt, tiles)
        self.handle_actions(dt, actions, tiles)

    def collision_test(self, tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile): # returns a boolean
                collisions.append(tile)
        return collisions
    
    def update_pos(self, dt, tiles): # only active if we have speed

        self.update_pos_y(dt, tiles)
        self.update_pos_x(dt, tiles)

    def update_pos_x(self, dt, tiles):
        # x movement
        self.x_pos += self.x_speed * dt # for calculations
        self.rect.x = round(self.x_pos) # update rect position for collision_test
        collisions = self.collision_test(tiles)

        if not collisions:
            if abs(self.x_speed) < self.x_stop:
                self.x_speed = 0
            # else:
                # self.x_speed *= self.air_resistance
        else: # collision on x axis
            
            # self.x_speed = - self.x_speed * self.retention
            # DOING THIS BEFORE THE IF CHECK !!! BIG NO NO NO
            for tile in collisions:
                if self.x_speed > 0:
                    # print("colliding w left wall")
                    self.rect.right = tile.left # colliderect => False
                    self.x_pos = self.rect.x
                elif self.x_speed < 0:
                    # print("colliding w right wall")
                    self.rect.left = tile.right # colliderect => False
                    self.x_pos = self.rect.x

            self.x_speed = - self.x_speed * self.retention
            self.y_speed *= self.retention # also reduce y speed, MAY NEED TWEAKING

    def update_pos_y(self, dt, tiles):
        # y movement
        self.y_pos += self.y_speed * dt # for calculations
        self.rect.y = round(self.y_pos) # update rect w calculated pos
        collisions = self.collision_test(tiles)
        # print(f"y: {round(self.y_speed,3)}")
        if not collisions:
            self.y_speed += self.gravity * dt
        else: # collision on y axis
            tile = collisions[0]
            self.x_speed *= self.retention # also reduce x speed, MAY NEED TWEAKING

            if self.y_speed > self.y_stop: 
                # top
                # print(f"colliding w top of tile, y: {round(self.y_speed,3)}, x: {round(self.x_speed,3)}")
                self.rect.bottom = tile.top
                self.y_pos = self.rect.y
                self.y_speed = self.y_speed * -1 * self.retention
            elif -self.y_speed > 0: 
                # bottom
                # print("colliding w bottom of tile")
                self.rect.top = tile.bottom
                self.y_pos = self.rect.y
                self.y_speed = self.y_speed * -1 * self.retention / 2
            else:
                # top little momentum so momentum to 0
                # print("y_speed 0")
                self.rect.bottom = tile.top
                self.y_pos = self.rect.y
                self.y_speed = 0
    
    def handle_actions(self, dt, actions, tiles):

        if actions["left"]:
            self.add_momentum(-50, -50)
        if actions["right"]:
            self.add_momentum(50, -50)
        if actions["action1"]:
            self.x_pos = self.origin[0]
            self.y_pos = self.origin[1]
            self.x_speed = 0
            self.y_speed = 0.01


        # Handle mouse clicks for selecting character
        if (actions["mouse_click"]):
            actions["mouse_click"] = False # prevent double clicking
            print("Mouse Click")
            if not (self.state["jump"] or self.state["throw"]):
                # print("select condition met") 
                mouse_pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse_pos): # mouse on character
                    # print("collision")
                    self.state["selected"] = not self.state["selected"]
                    # print(f"state: {self.state}")

        # Jump
        # Dragging
        elif actions["mouse_pressed"] and self.state["selected"]: # and self.state["jump"]:
            print("Mouse Pressed")

            mouse_pos = pygame.mouse.get_pos()
            while len(self.mouse_pos_list) > 2:
                self.mouse_pos_list.pop()
            self.mouse_pos_list.append(mouse_pos)
            # render line or arrow function

        # Releasing
        elif (actions["mouse_pressed"] == False) and (len(self.mouse_pos_list) >= 2):
            print("time to throw!")
            x_speed = (self.mouse_pos_list[0][0] -self.mouse_pos_list[-1][0]) * self.throw_multiplier
            y_speed = (self.mouse_pos_list[0][1] -self.mouse_pos_list[-1][1]) * self.throw_multiplier
            self.add_momentum(x_speed, y_speed)

            self.mouse_pos_list = []
            self.reset_state()

        
        if actions["space"]: # bomb placeholder
            self.game_world.spawn_bomb(self.rect.x, self.rect.y)


    def render_selections(self, surface):
        pass