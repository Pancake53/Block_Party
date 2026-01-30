import pygame
from GameObject import GameObject

class Bomb(GameObject):
    def __init__(self, x_pos, y_pos, image):
        super().__init__(x_pos, y_pos)
        self.image = image
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = x_pos, y_pos
        self.state = {"selected": True, "jump": True, "throw": False}
        

    def render(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, dt, actions, tiles):
        
        if (self.x_speed != 0) or (self.y_speed != 0):
            self.update_pos(dt, tiles)
        self.handle_actions(dt, actions, tiles)