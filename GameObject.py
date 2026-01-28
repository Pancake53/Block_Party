import pygame

class GameObject():
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 0.5
        self.air_resistance = 0.99
        self.selected = False
        self.rect = pygame.Rect(x_pos, y_pos, 16, 32)

    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)

    def update(self, dt, actions, tiles):
        
        if (self.x_speed > 0) or (self.y_speed > 0):
            self.update_pos(tiles)

    def collision_test(self, tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions
    
    def update_pos(self, tiles):
        # self.y_pos += self.y_speed\
        # self.rect.y = self.y_pos
        # collision_test
        # self.x_pos += self.x_speed
        # self.rect.x = self.x_pos
        # collision_test
        pass

    def add_momentum(self, x_speed, y_speed):
        self.x_speed = x_speed
        self.y_speed = y_speed

