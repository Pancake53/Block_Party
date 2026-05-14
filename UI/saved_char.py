import pygame

from dataclasses import dataclass
from typing import Callable

@dataclass
class SavedChar():
    name: str
    i: int
    surface: pygame.surface.Surface
    x: int
    y: int
    on_click: Callable[[int], None]
    draw_name: Callable[[str, int, pygame.surface.Surface], None]

    def __post_init__(self):
        self.selected = False
        self.load()





    def update(self, actions):
        hovered = self.rect.collidepoint(actions['mouse_pos'])

        if hovered:
            if actions['mouse_click']:
                self.selected = not self.selected
                if self.selected:
                    self.on_click(self.i)

    def render(self, surface):
        surface.blit(self.surface, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, width=3)
        self.draw_name(self.name, self.rect.x, surface)

    def load(self):
        self.rect = pygame.Rect(self.x, self.y, 
                                self.surface.get_width(), self.surface.get_height())
        
        # text

