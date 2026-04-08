import pygame

class Tile:
    def __init__(self, x, y, width, height, colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        self.x_pos = self.rect.x
        self.y_pos = self.rect.y
        self.x_origin = self.x_pos
        self.y_origin = self.y_pos
        

    def update(self, x_offset, y_offset):
        self.x_pos += x_offset
        self.y_pos += y_offset

        self.rect.x = self.x_pos
        self.rect.y = self.y_pos

    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)

    def reset(self):
        self.x_pos = self.x_origin
        self.y_pos = self.y_origin
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos