from button import Button
from dataclasses import dataclass
from typing import Callable


@dataclass
class ImageButton(Button):
    x: int
    y: int
    default_img: object
    hover_img: object = None
    on_click: Callable[[None], None]


    def __post_init__(self):
        '''
        runs after init
        '''
        if self.image:
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.width = self.rect.width
            self.height = self.rect.height

    def action_on_button(self, x, y, surface, actions):
        '''
        Handels user actions, mouseover and click 
        and calls draw_button

        x & y coordinates
        surface: surface to render object on
        actions: user inputs dictionary

        Return True when button is clicked
        '''
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

        # mouse position
        hovered = self.rect.collidepoint(actions["mouse_pos"])

        # check for mouseover
        if hovered:
            # hover button
            self.draw_button(self.hover_img, surface)
            # click button
            if actions["mouse_click"]:
                self.draw_button(self.hover_img, surface)
                # pressed button
                
        else:
            # default button
            self.draw_button(self.default_img, surface)
        