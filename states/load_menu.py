import pygame

from states.overlay import Overlay

from UI.button_stationary import ButtonStationary
from UI.saved_char import SavedChar



from dataclasses import dataclass
from dataclasses import field


@dataclass
class LoadMenu(Overlay):
    saved_chars_data: list = field(default_factory=list)
    char_surface_pos: tuple = field(default_factory=tuple)
    scalar: int = None

    def __post_init__(self):
        
        self.height = self.game.GAME_H * 2 / 3
        self.width = self.game.GAME_W * 3 / 4
        self.title = 'Choose Character'
        
        self.texts = []
        self.buttons = []
        self.images = []
        self.selection = None


        self.current_index = 0
        self.result = None
        self.reduce_chars_displayed_by = 0
        self.name_y_padding = 20

        self.size_multiplier = 2
        self.char_display_surface_W = self.game.char_surface_W * self.size_multiplier
        self.char_display_surface_H = self.game.char_surface_H * self.size_multiplier
        self.char_rect = pygame.Rect(500, 200, 
                                     self.game.char_surface_H, 
                                     self.game.char_surface_W)
        

        super().__post_init__()
        
        
    
        
        
    
    def child_spesific_update(self, dt, actions):
        for button in self.buttons:
            button.update(actions)

        for chars in self.saved_chars:
            chars.update(actions)

    def handle_clicks(self, name):

        try:
            name = int(name)
            # chars index number
            # print(f'name: {name} is an int')
            for char in self.saved_chars:
                char.selected = False
            self.selection = name
            print(f'selected index: {name}')
            


        except ValueError:
            # string
            match name:

                case 'left':
                    if self.current_index > 0:
                        self.current_index -= self.amount_of_chars_displayed
                        self.update_visible_chars()

            
                case 'right':
                    if self.current_index < len(self.saved_chars) - self.amount_of_chars_displayed:
                        self.current_index += self.amount_of_chars_displayed
                        self.update_visible_chars()


                case 'confirm':
                    self.result = self.selection
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
        for char in self.visible_chars:
            char.render(surface)
        


    def load_buttons(self):

        # padding between edges of the box
        padding = 25
        self.button_padding = 25
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
        self.arrow_w, self.arrow_h = button_w, button_h

        # default y values
        button_y = self.rect_window.y + self.height / 2 - button_h / 2
        self.arrow_y = button_y

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

        saved characters
        '''
        
        self.saved_chars = []

        # COORDINATES AND PADDING

        # default
        y = self.arrow_y + self.arrow_h / 2 - self.char_display_surface_H / 2
        self.name_y = y - self.name_y_padding
        space_for_chars = self.width - self.arrow_w * 2 - self.button_padding * 4

        # variables
        self.amount_of_chars_displayed = int(space_for_chars / 
                                        self.char_display_surface_W) - self.reduce_chars_displayed_by
        space_per_char = space_for_chars / self.amount_of_chars_displayed
        self.x_padding = ((space_per_char - self.char_display_surface_W) 
                        * 
                     (self.amount_of_chars_displayed / (self.amount_of_chars_displayed - 1)))
        
        print(self.x_padding)

        # end x 


        # start x value
        self.start_x = self.rect_window.x + self.button_padding * 2 + self.arrow_w
        x = self.start_x
        # DATA INTO CLASSES AND LIST
        for i, char_data in enumerate(self.saved_chars_data):
            if i > 0:
                x += self.char_display_surface_W + self.x_padding
            name = char_data['name']
            char_surface = pygame.Surface(
            (self.char_display_surface_W, self.char_display_surface_H),
            pygame.SRCALPHA)
            for part in char_data['parts']:
                self.scale_part(part, char_surface)

            new_saved_char = SavedChar(name, i, char_surface, x, y, 
                                       on_click=self.handle_clicks,
                                       draw_name=self.draw_name)

            self.saved_chars.append(new_saved_char)

        self.update_visible_chars()

        

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

        ''' x, y, w and h has been normalized 
            -> same as in creating char scale
            next apply size multiplier
        '''
        x = (x + w / 2) * self.size_multiplier
        y = (y + h / 2) * self.size_multiplier
        w *= self.size_multiplier
        h *= self.size_multiplier

        x -= w / 2
        y -= h / 2

        pygame.draw.rect(char_surface, colour,
                          pygame.Rect(x, y, w, h))

    def update_visible_chars(self):
        self.visible_chars = self.saved_chars[
            self.current_index: 
            self.current_index + self.amount_of_chars_displayed]
        
        # start x value
        x = self.start_x

        for i, char in enumerate(self.visible_chars):
            if i > 0:
                x += (self.char_display_surface_W + self.x_padding)
            char.x = x
            char.rect.x = char.x
            print(x)

    def draw_name(self, name, x, surface):
        self.game.draw_text(surface, name, 
                            self.game.TILE_COL, 
                            x + self.char_display_surface_W / 2, 
                            self.name_y, size='Small')
    





    