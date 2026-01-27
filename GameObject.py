import pygame

class GameObject():
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = 0
        self.y_speed = 0
        self.rect = pygame.Rect(x_pos, y_pos, 16, 32)

    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.charRect)

    def update(self, dt, actions):
        pass

    def collision_test(self, tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions
    
    def move(self, movement, force, tiles):
        pass
