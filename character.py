import pygame
from GameObject import GameObject


class Character(GameObject):
    def __init__(self, team_id, width, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.team_id = team_id
        self.colour = [(184, 43, 43), (95, 184, 43)][team_id]
        self.width = width
        self.y_stop = 1
        self.x_stop = 1
        self.retention = 0.25 # * width

        self.rect = pygame.Rect(x_pos, y_pos, 16 * width, 32)

    def collision_test(self, tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile): # returns a boolean
                collisions.append(tile)
        return collisions
    
    def update_pos(self, tiles): # only active if we have speed
        self.update_pos_x(tiles)
        self.update_pos_y(tiles)

    def update_pos_x(self, tiles):
        # x movement
        self.x_pos += self.x_speed # for calculations
        self.rect.x = self.x_pos # update rect position for collision_test
        collisions = self.collision_test(tiles)

        if not collisions:
            if self.x_speed < self.x_stop:
                self.x_speed = 0
            else:
                self.x_speed *= self.air_resistance
        else: # collision on x axis
            tile = collisions[0]
            self.x_speed = - self.x_speed * self.retention

            if self.x_speed > 0:
                self.rect.right = tile.left # colliderect => False
            elif self.x_speed < 0:
                self.rect.left = tile.right # colliderect => False

    def update_pos_y(self, tiles):
                # y movement
        self.y_pos += self.y_speed # for calculations
        self.rect.y = self.y_pos # update rect w calculated pos
        collisions = self.collision_test(tiles)

        if not collisions:
            self.y_speed += self.gravity
        else: # collision on y axis
            tile = collisions[0]

            if self.y_speed > self.y_stop: # top
                self.rect.bottom = tile.top
                self.y_speed = self.y_speed * -1 * self.retention
            elif -self.y_speed > self.y_stop: # bottom
                self.rect.top = tile.bottom
                self.y_speed = self.y_speed * -1 * self.retention / 2
            else:
                self.y_speed = 0
    
