import pygame
from GameObject import GameObject


class Character(GameObject):
    def __init__(self, team_id, width, x_pos, y_pos):
        self.team_id = team_id
        self.colour = [(184, 43, 43), (95, 184, 43)][team_id]
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = 0
        self.y_speed = 0
        self.retention = 0.8 / width
        self.charRect = pygame.Rect(x_pos, y_pos, 16 * width, 32)

    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.charRect)

    def update(self, dt, ):
        pass

    def collision_test(self, tiles):
        collisions = []
        for tile in tiles:
            if self.charRect.colliderect(tile):
                collisions.append(tile)
        return collisions
    
    def move(self, movement, tiles):
        self.charRect
    
    
