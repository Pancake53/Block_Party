import pygame

class Tile:
    def __init__(self, x, y, width, height, colour, index, game_world):
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour
        self.x = self.rect.x
        self.y = self.rect.y
        self.x_origin = self.x
        self.y_origin = self.y
        self.index = index
        self.game_world = game_world

        if self.game_world.wrap_around:
            self.update = self.update_wrap_around
            # if tile is entirely on the screen, 
            # then it has no dublicate 
            self.dublicated = not (
                0 <= self.x <= self.game_world.game.GAME_W
                  - self.rect.width)
        else:
            self.update = self.update_normal
        
    def update(self, x_offset, y_offset):
        self.update(x_offset, y_offset)

    def update_normal(self, x_offset, y_offset):
        self.camera_move(x_offset, y_offset)

    def update_wrap_around(self, x_offset, y_offset):

        self.camera_move(x_offset, y_offset)
        

        self.duplicating()
        self.deleting()

    def camera_move(self, x_offset, y_offset):
        self.x += x_offset
        self.y += y_offset

        self.rect.x = self.x
        self.rect.y = self.y

    def duplicating(self):
        # if hasn't created a dublicate on the other side
        # or if the dublicate has been removed
        if not self.dublicated:
            # left side
            if self.x < 0:
                self.game_world.wrap_tiles(self, "left")
                self.dublicated = True
            # right side
            elif self.x > self.game_world.game.GAME_W - self.rect.width:
                
                self.game_world.wrap_tiles(self, "right")
                self.dublicated = True

        else:
            # comes back to being fully in view / no duplicates
            if (0 <= self.x <= self.game_world.game.GAME_W - self.rect.width):
                self.dublicated = False

    def deleting(self):
        # left side
        if self.x < -self.rect.width:
            self.game_world.delete_tile(self)
        # right side
        elif self.x > self.game_world.game.GAME_W:
            self.game_world.delete_tile(self)

    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)

    def reset(self):
        self.x = self.x_origin
        self.y = self.y_origin
        self.rect.x = self.x
        self.rect.y = self.y