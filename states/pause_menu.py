import pygame

from states.overlay import Overlay
from states.settings_menu import SettingsMenu

from UI.button_stationary import ButtonStationary


from dataclasses import dataclass


@dataclass
class PauseMenu(Overlay):
    pass

    def __post_init__(self):
        self.title = 'pause menu'
        return super().__post_init__()
        
    
    def child_spesific_update(self, dt, actions):
        for button in self.buttons:
            button.update(actions)

    def handle_clicks(self, name):

        match name:
            case 'continue':
                self.exit_state()
            case 'settings':
                new_state = SettingsMenu(self.game, bg_surface=self.shaded_bg)
                new_state.enter_state()
            case _:
                print(f'Invalid case in handle clicks: {name}')

    def child_spesific_render(self, surface):

        for button in self.buttons:
            button.render(surface)

        for text in self.texts:
            self.game.draw_text(surface,
                                text['str'], self.game.TILE_COL,
                                text['x'], text['y'],
                                self.text_size)
            
        


    def load_buttons(self):

        # padding between edges of the box
        button_w, button_h = 300, 50
        padding = 25
        self.text_size = 'Medium'
        self.texts = []
        self.buttons = []

        # default x values
        text_x = self.title_x
        button_x = text_x - button_w / 2

        # continue

        button_y = self.title_y + padding * 2
        text_y = button_y + button_h / 2

        button_name = 'continue'

        button = ButtonStationary(
            button_name,
            button_x, button_y,  
            width=button_w, height=button_h,
            on_click=self.handle_clicks
        )
        self.buttons.append(button)
        self.add_text(button_name, text_x, text_y)

        # settings

        button_y += button_h + padding
        text_y = button_y + button_h / 2

        button_name = 'settings'

        button = ButtonStationary(
            button_name,
            button_x, button_y,  
            width=button_w, height=button_h,
            on_click=self.handle_clicks
        )
        self.buttons.append(button)
        self.add_text(button_name, text_x, text_y)

        # level select 

        button_y += button_h + padding
        text_y = button_y + button_h / 2

        button_name = 'level select'

        button = ButtonStationary(
            button_name,
            button_x, button_y,  
            width=button_w, height=button_h,
            on_click=self.handle_clicks
        )
        self.buttons.append(button)
        self.add_text(button_name, text_x, text_y)



