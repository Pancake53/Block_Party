import pygame

from states.overlay import Overlay

from UI.button_stationary import ButtonStationary



from dataclasses import dataclass
from dataclasses import field


@dataclass
class LoadMenu(Overlay):
    saved_chars_data: list = field(default_factory=list)
    char_surface_pos: tuple = field(default_factory=tuple)

    def __post_init__(self):
        
        self.height = self.game.GAME_H * 2 / 3
        self.width = self.game.GAME_W * 3 / 4
        self.title = 'Choose Character'
        
        self.texts = []
        self.buttons = []
        self.images = []
        self.selection = None

        self.result = None

        self.scalar = 3
        self.char_rect = pygame.Rect(500, 200, 
                                     self.game.char_surface_H, 
                                     self.game.char_surface_W)
        

        super().__post_init__()
        
        
    
        
        
    
    def child_spesific_update(self, dt, actions):
        for button in self.buttons:
            button.update(actions)

    def handle_clicks(self, name):

        match name:

            case 'left':
                print(f'WORK IN PROGRESS: {name}')
        
            case 'right':
                print(f'WORK IN PROGRESS: {name}')


            case 'confirm':
                self.result = 'test1'
                self.game.state_m.exit_state(result = self.result)

            case 'delete':
                print(f'WORK IN PROGRESS: {name}')

            case 'random':
                print(f'WORK IN PROGRESS: {name}')

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

        self.render_chars(surface)
            
    def render_chars(self, surface):
        for char_surface in self.char_surfaces:
            surface.blit(char_surface, self.char_rect)


    def load_buttons(self):

        # padding between edges of the box
        padding = 25
        button_w, button_h = (self.width - 4 * padding) / 3, 40
        
        text_padding = 12
        image_padding = 5
        self.text_size = 'Small'


        # default y values
        button_y = self.rect_window.y + self.height - button_h - padding
        text_y = button_y + text_padding
        img_y = button_y + image_padding

        # delete
        button_x = self.rect_window.x + padding
        text_x = button_x + text_padding
        img_x = button_x + button_w - 50 - image_padding

        button_name = 'delete'

        button = ButtonStationary(
            button_name,
            button_x, button_y,  
            width=button_w, height=button_h,
            on_click=self.handle_clicks
        )
        self.buttons.append(button)
        self.add_text(button_name, text_x, text_y)

        self.game.add_image('delete_img', img_x, img_y, self.images)

        # random
        button_x += button_w + padding
        text_x = button_x + text_padding
        img_x = button_x + button_w - 50 - image_padding

        button_name = 'random'

        button = ButtonStationary(
            button_name,
            button_x, button_y,  
            width=button_w, height=button_h,
            on_click=self.handle_clicks
        )
        self.buttons.append(button)
        self.add_text(button_name, text_x, text_y)

        self.game.add_image('random_img', img_x, img_y, self.images)

        # confirm
        button_x += button_w + padding
        text_x = button_x + text_padding
        img_x = button_x + button_w - 50 - image_padding

        button_name = 'confirm'

        button = ButtonStationary(
            button_name,
            button_x, button_y,  
            width=button_w, height=button_h,
            on_click=self.handle_clicks
        )
        self.buttons.append(button)
        self.add_text(button_name, text_x, text_y)

        self.game.add_image('confirm_img', img_x, img_y, self.images)

        # LEFT AND RIGHT ARROWS

        button_w, button_h = self.game.assets['arrowleft_img'].get_size()

        # default y values
        button_y = self.rect_window.y + self.height / 2 - button_h / 2

        # left
        button_name = 'left'
        button_x = self.rect_window.x + padding

        button = ButtonStationary(
            button_name,
            button_x, button_y,  
            image=self.game.assets['arrowleft_img'],
            on_click=self.handle_clicks
        )
        self.buttons.append(button)

        # right
        button_name = 'right'
        button_x = self.rect_window.x + self.width - button_w - padding

        button = ButtonStationary(
            button_name,
            button_x, button_y,  
            image=self.game.assets['arrowright_img'],
            on_click=self.handle_clicks
        )
        self.buttons.append(button)


    def load_else(self):
        '''
        loads the middle component
        '''
        self.char_names = []
        self.char_surfaces = []

        # defaults
        y = self.rect_window.y + self.height / 3
        for char_data in self.saved_chars_data:
            self.char_names.append(char_data['name'])
            char_surface = pygame.Surface(
            (self.game.char_surface_W, self.game.char_surface_H),
            pygame.SRCALPHA)
            for part in char_data['parts']:
                self.scale_part(part, char_surface)

            self.char_surfaces.append(char_surface)

    def scale_part(self, part, char_surface):
        '''
        rescales a single part and draws it on surface
        '''
        colour = part['colour']
        
        # coordinates
        
        x = ( part['x'] + part['w'] / 2 - self.char_surface_pos[0] ) / self.scalar
        y = ( part['y'] + part['h'] / 2 - self.char_surface_pos[1] ) / self.scalar

        # dimensions
        w = part['w'] / self.scalar
        h = part['h'] / self.scalar

        # reposition
        x -= w / 2
        y -= h / 2

        pygame.draw.rect(char_surface, colour,
                          pygame.Rect(x, y, w, h))

        

    





    