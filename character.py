import pygame
from GameObject import GameObject


class Character(GameObject):
    def __init__(self, team_id, width, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.team_id = team_id
        self.colour = [(184, 43, 43), (95, 184, 43)][team_id]
        self.width = width
        self.bounce_stop = 0.4
        self.retention = 0.8 / width
        self.rect = pygame.Rect(x_pos, y_pos, 16 * width, 32)

    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)


    def collision_test(self, tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions
    
    def move(self, tiles):
        collisions = self.collision_test(tiles)
        if not collisions:
            self.y_speed += self.gravity
        elif self.y_speed > self.bounce_stop:
            self.y_speed = self.y_speed * -1 * self.retention
        else:
            self.y_speed = 0
    
    
