import pygame
from GameObject import GameObject


class Character(GameObject):
    def __init__(self, team_id, width, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.team_id = team_id
        self.colour = [(184, 43, 43), (95, 184, 43)][team_id]
        self.width = width
        self.y_stop = 20
        self.x_stop = 1
        self.retention = 0.25 # * width

        self.rect = pygame.Rect(x_pos, y_pos, 12 * width, 25)

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
                    print("colliding w left wall")
                    self.rect.right = tile.left # colliderect => False
                    self.x_pos = self.rect.x
                elif self.x_speed < 0:
                    print("colliding w right wall")
                    self.rect.left = tile.right # colliderect => False
                    self.x_pos = self.rect.x

            self.x_speed = - self.x_speed * self.retention
            self.y_speed *= self.retention # also reduce y speed, MAY NEED TWEAKING

    def update_pos_y(self, dt, tiles):
        # y movement
        self.y_pos += self.y_speed * dt # for calculations
        self.rect.y = round(self.y_pos) # update rect w calculated pos
        collisions = self.collision_test(tiles)
        print(f"y: {round(self.y_speed,3)}")
        if not collisions:
            self.y_speed += self.gravity * dt
        else: # collision on y axis
            tile = collisions[0]
            self.x_speed *= self.retention # also reduce x speed, MAY NEED TWEAKING

            if self.y_speed > self.y_stop: 
                # top
                print(f"colliding w top of tile, y: {round(self.y_speed,3)}, x: {round(self.x_speed,3)}")
                self.rect.bottom = tile.top
                self.y_pos = self.rect.y
                self.y_speed = self.y_speed * -1 * self.retention
            elif -self.y_speed > 0: 
                # bottom
                print("colliding w bottom of tile")
                self.rect.top = tile.bottom
                self.y_pos = self.rect.y
                self.y_speed = self.y_speed * -1 * self.retention / 2
            else:
                # top little momentum so momentum to 0
                print("y_speed 0")
                self.rect.bottom = tile.top
                self.y_pos = self.rect.y
                self.y_speed = 0
    
