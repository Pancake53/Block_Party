from button import Button
from dataclasses import dataclass
from typing import Callable


@dataclass
class ImageButton(Button):
    x: int
    y: int
    image: object
    hover_img: object = None


    def __post_init__(self):
        if self.image:
            self.rect = self.image.get_rect()
            self.width = self.rect.width
            self.height = self.rect.height