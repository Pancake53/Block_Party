import pygame

from game_objects.tile import Tile

from dataclasses import dataclass

@dataclass
class Background(Tile):
    x: int
    y: int
    index: str
    game_world: object

    image: object =None
    width: int=None
    height: int=None
    colour: str =None
    speed: int =None
    surface: pygame.surface.Surface =None

    def __post_init__(self):
        
        self.x_origin = self.x
        self.y_origin = self.y
        
        if self.colour:
            print(f'{self.colour}')
            a = int(self.colour[1:3], 16)
            r = int(self.colour[3:5], 16)
            g = int(self.colour[5:7], 16)
            b = int(self.colour[7:9], 16)
            
            self.colour = (r, g, b, a)

        if self.game_world.wrap_around:
            self.update = self.update_wrap_around
            # if tile is entirely on the screen, 
            # then it has no dublicate 
            self.dublicated = not (
                0 <= self.x <= self.game_world.game.GAME_W
                  - self.rect.width)
        else:
            self.update = self.update_normal  

        if self.image:
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            self.render = self.render_image

        else:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.max_offset = 200

    def render_image(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dt):
        self.x += self.speed * dt


        if self.x <= - self.max_offset:
            self.x = self.game_world.game.GAME_W + self.max_offset
        self.rect.x = self.x


            