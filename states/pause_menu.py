import pygame

from states.overlay import Overlay

from UI.button_stationary import ButtonStationary



from dataclasses import dataclass


@dataclass
class PauseMenu(Overlay):
    pass

    def __post_init__(self):
        
        self.height = self.game.GAME_H * 2 / 3
        self.title = 'pause menu'
        self.texts = []
        self.buttons = []
        self.images = []
        self.prev_state = self.game.state_stack[-1]
        # for greying out level select if not in game world
        self.level_select_active = (
            self.prev_state.__class__.__name__ == "Game_World"
        )

        super().__post_init__()
        
        
    
        
        
    
    def child_spesific_update(self, dt, actions):
        for button in self.buttons:
            button.update(actions)

    def handle_clicks(self, name):

        match name:
            case 'continue':
                self.game.state_m.exit_state()

            case 'settings':
                self.game.state_m.enter_state('settings', bg_surface = self.shaded_bg)

            case 'level select':
                if self.level_select_active:
                    self.game.state_m.exit_state()
                    self.game.state_m.exit_state()


            case _:
                print(f'Invalid case in handle clicks: {name}')

    def child_spesific_render(self, surface):

        for button in self.buttons:
            button.render(surface)

        for text in self.texts:
            self.game.draw_text_topleft(surface,
                                text['str'], self.game.TILE_COL,
                                text['x'], text['y'],
                                self.text_size)
            
        for image in self.images:
            surface.blit(image['img'], image['rect'])
            
        


    def load_buttons(self):

        # padding between edges of the box
        button_w, button_h = self.width * 2 / 3, 60
        padding = 25
        text_padding = 18
        image_padding = 5
        self.text_size = 'Medium'


        # default x values
        button_x = self.title_x - button_w / 2
        text_x = button_x + text_padding
        img_x = button_x + button_w - 50 - image_padding

        # continue

        button_y = self.title_y + padding * 2
        text_y = button_y + text_padding
        img_y = button_y + image_padding - 2

        button_name = 'continue'

        button = ButtonStationary(
            button_name,
            button_x, button_y,  
            width=button_w, height=button_h,
            on_click=self.handle_clicks
        )
        self.buttons.append(button)
        self.add_text(button_name, text_x, text_y)

        self.game.add_image('continue_img', img_x, img_y, self.images)
        self.game.add_image('continue_img', img_x - 15, img_y + 5, self.images)

        # settings

        button_y += button_h + padding
        text_y = button_y + text_padding
        img_y = button_y + image_padding - 2

        button_name = 'settings'

        button = ButtonStationary(
            button_name,
            button_x, button_y,  
            width=button_w, height=button_h,
            on_click=self.handle_clicks
        )
        self.buttons.append(button)
        self.add_text(button_name, text_x, text_y)

        self.game.add_image('settings_img', img_x, img_y, self.images)
        self.game.add_image('settings_img', img_x - 15, img_y + 5, self.images)
        

        # level select 

        button_y += button_h + padding
        text_y = button_y + text_padding

        button_name = 'level select'

        if self.level_select_active:

            button = ButtonStationary(
                button_name,
                button_x, button_y,  
                width=button_w, height=button_h,
                on_click=self.handle_clicks
            )

        else:
            button = ButtonStationary(
                button_name,
                button_x, button_y,  
                width=button_w, height=button_h,
                button_colour=self.game.GREY,
                hover_colour=self.game.GREY,
                on_click=self.handle_clicks
            )

        self.buttons.append(button)
        self.add_text(button_name, text_x, text_y)



    