import pygame

from states.overlay import Overlay

from UI.button_stationary import ButtonStationary

from dataclasses import dataclass


@dataclass
class SaveMenu(Overlay):
    pass

    def __post_init__(self):
        self.title = 'Enter name'
        self.padding = 20
        self.name_box_col = (245, 225, 174)
        self.name = 'test'
        self.max_name_len = 10
        self.max_len = False
        self.min_name_len = 2
        self.min_len_rached = False

        self.inactive_btn_col = (139, 139, 139)
        self.active_btn_col = (0, 153, 136)
        super().__post_init__()
    
    def child_spesific_update(self, dt, actions):
        for button in self.buttons:
            button.update(actions)

    def child_spesific_render(self, surface):

        
        pygame.draw.rect(surface, self.name_box_col, self.name_box)
        pygame.draw.rect(surface, self.game.BG_COL, self.name_box, width=5)

        self.game.draw_text(surface, self.name, self.game.TEXT_COL, 
                            self.name_text_x, self.name_text_y, size='Medium')
        
        for button in self.buttons:
            button.render(surface)

        for text in self.texts:
            self.game.draw_text(surface, text['str'], self.game.TEXT_COL, 
                            text['x'], text['y'], text['size'])

    def handle_clicks(self, name):
        '''
        button callback

        name = name given to button
        '''
        if len(name) == 1:
            self.add_letter(name)
        else:
            match name:
                case 'backspace':
                    if len(self.name) > 0:
                        self.name = self.name[:-1]
                        if len(self.name) == 0:
                            self.update_button_col('empty')
                        elif len(self.name) <= self.min_name_len:
                            self.min_len_rached = False
                            self.update_button_col('under_min_len')
                        elif self.max_len:
                            self.max_len = False
                            self.update_button_col('not_max')
              
                        
                case 'space':
                    self.add_letter(' ')
                case 'enter':
                    if len(self.name) >= self.min_name_len:
                        self.game.state_m.exit_state(['save', self.name])
                case _:
                    print('something in the orange')

    def add_letter(self, letter):
        self.update_button_col('not_empty')

        if len(self.name) < self.max_name_len:
            self.name += letter

            if len(self.name) > self.min_name_len:
                self.min_len_rached = True
                self.update_button_col('over_min_len')

            if len(self.name) == self.max_name_len:
                self.max_len = True
            self.update_button_col('max_len')

        else:
            self.max_len = True
            self.update_button_col('max_len')

        


    def load_buttons(self):
        '''
        load all the letter buttons
        '''
        self.buttons = []
        self.texts = []

        letters = [['a', 'b', 'c', 'd', 'e', 'f', 'g','h', 'i',], 
                   ['j','k', 'l', 'm', 'n','o', 'p', 'q', 'r'], 
                   ['s', 't', 'u', 'v', 'w', 'x', 'y', 'z']]

        y = self.title_y + self.padding * 3 + 50
        

        w, h = 30, 32
        self.letter_padding = w / 3
        y_spacing_mlt = 1.7

        for i, row in enumerate(letters):
            # reset x at the beginning of each row
            x = self.rect_window.x + self.padding - w - self.letter_padding
            if i > 0:
                y += h + self.letter_padding * y_spacing_mlt

            for letter in row:
                x += w + self.letter_padding
                button = ButtonStationary(letter,
                                          x, y,
                                          on_click=self.handle_clicks,
                                          width=w, height=h)
                self.buttons.append(button)

                self.game.add_text(letter, 
                                   x + w / 2 + 2, 
                                   y + h / 2, 
                                   'Small', self.texts)

        # backspace
        name = 'backspace'
        x = self.rect_window.x + self.padding + (w + self.letter_padding) * len(letters[0])     
        y = self.title_y + self.padding * 3 + 50

        button = ButtonStationary(name,
                                  x, y,
                                  on_click=self.handle_clicks,
                                  image=self.game.assets['backspace_img'])
        
        self.buttons.append(button)

        # space
        name = 'space'     
        y += h + self.letter_padding * y_spacing_mlt

        button = ButtonStationary(name,
                                  x, y,
                                  on_click=self.handle_clicks,
                                  image=self.game.assets['space_img'])
        
        self.buttons.append(button)

        # enter
        name = 'enter'
        x -= w + self.letter_padding  
        y += h + self.letter_padding * y_spacing_mlt

        button = ButtonStationary(name,
                                  x, y,
                                  on_click=self.handle_clicks,
                                  image=self.game.assets['enter_img'])
        
        self.buttons.append(button)




    def load_else(self):
        '''
        loads the rect for name 
        '''

        w = self.width - self.padding * 2
        h = 50

        x = self.rect_window.x + self.padding
        y = self.title_y + self.padding * 2

        

        self.name_box = pygame.Rect(x, y, w, h)

        self.name_text_x = self.title_x
        self.name_text_y = y + h / 2 - 2
        
    def update_button_col(self, action):
        '''
        updates button active colour based on input
        '''

        match action:
            case 'max_len':
                for button in self.buttons[:-3]:
                    button.button_colour = self.inactive_btn_col

            case 'not_max':
                for button in self.buttons[:-3]:
                    button.button_colour = self.active_btn_col

            case 'empty':
                self.buttons[-3].button_colour = self.inactive_btn_col

            case 'not_empty':
                self.buttons[-3].button_colour = self.active_btn_col

            case 'under_min_len':
                self.buttons[-1].button_colour = self.inactive_btn_col

            case 'over_min_len':
                self.buttons[-1].button_colour = self.active_btn_col
