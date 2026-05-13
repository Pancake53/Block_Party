import pygame

from states.overlay import Overlay

from dataclasses import dataclass


@dataclass
class Credits(Overlay):
    pass

    def __post_init__(self):
        self.title = 'credits'
        super().__post_init__()
    
    def child_spesific_update(self, dt, actions):
        pass

    def child_spesific_render(self, surface):
        self.game.draw_text(surface,
                            self.description, self.game.TILE_COL,
                            self.description_x, self.description_y,
                            size="Medium")


    def load_else(self):
        self.description = 'Made by\nme\nmyself\nand I' \
    

        self.description_x = self.title_x
        self.description_y = self.rect_window.centery