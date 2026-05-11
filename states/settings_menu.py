import pygame

from states.overlay import Overlay

from UI.button_stationary import ButtonStationary
from UI.slider import Slider

from dataclasses import dataclass


@dataclass
class SettingsMenu(Overlay):
    pass

    def __post_init__(self):
        return super().__post_init__()
    
    def child_spesific_update(self, delta_time, actions):
        for button in self.buttons:
            button.update(actions)

        for slider in self.sliders:
            slider.update(actions)

    def handle_clicks(self, name):

        match name:
            case 'toggle fullscreen':
                self.game.toggle_fullscreen()
            case 'toggle music':
                self.game.toggle_music()
            case _:
                print(f'Invalid case in handle clicks: {name}')

    def child_spesific_render(self, surface):

        for text in self.texts:
            self.game.draw_text_topleft(surface,
                                text['str'], self.game.TILE_COL,
                                text['x'], text['y'],
                                self.text_size)
            
        for button in self.buttons:
            button.render(surface)

        for slider in self.sliders:
            slider.render(surface)

        for number in self.slider_numbers.values():
            self.game.draw_text_topleft(surface,
                                number['str'], self.game.TILE_COL,
                                number['x'], number['y'],
                                self.text_size)
            
    def update_settings(self, name, value):
        '''
        fires on slider movement
        '''
        # update settings class value
        setattr(self.game.settings, name, value / 100)
        # update number on screen
        if name in self.slider_numbers.keys():
            self.slider_numbers[name]['str'] = str(value)

        # apply volume change to playing music
        if name in ['master_volume', 'music_volume']:
            self.game.change_volume('music', self.game.track_volume)

        print(self.game.settings.master_volume)

    def load_buttons(self):


        # padding between edges of the box
        button_w, button_h = 50, 30
        padding = 25
        self.text_size = 'Small'
        self.texts = []
        self.buttons = []

        # columns
        self.text_x = self.rect_window.x + padding
        button_x = self.rect_window.x + self.width - button_w - padding

        # rows
        self.y_1 =  self.title_y + padding * 2

        button_name = 'toggle fullscreen'

        btn_toggle_fullscreen = ButtonStationary(
            button_name,
            button_x, self.y_1 - 4,  
            width=button_w, height=button_h,
            on_click=self.handle_clicks
        )
        self.buttons.append(btn_toggle_fullscreen)
        self.add_text(button_name, self.text_x, self.y_1)

        # rows
        self.y_2 =  self.y_1 + padding * 2

        button_name = 'toggle music'

        btn_toggle_fullscreen = ButtonStationary(
            button_name,
            button_x, self.y_2 - 4,  
            width=button_w, height=button_h,
            on_click=self.handle_clicks
        )
        self.buttons.append(btn_toggle_fullscreen)
        self.add_text(button_name, self.text_x, self.y_2)
        


    def load_sliders(self):

        self.sliders = []
        self.slider_numbers = {}
        padding = 25
        self.y_3 = self.y_2 + padding * 2
        
        self.slider_lenght = 100
        self.slider_x = self.rect_window.x + self.width - padding - self.slider_lenght

        master_volume_slider = Slider('master_volume', 
                                      self.slider_x, self.y_3 + 8,
                                      self.slider_lenght, 
                                      0, 100, 
                                      self.game.settings.master_volume * 100,
                                      on_change=self.update_settings)
        
        self.add_text('master volume', self.text_x, self.y_3)
        self.add_slider_number(
            'master_volume', int(self.game.settings.master_volume * 100), 
            self.slider_x - padding * 2,
            self.y_3)
        self.sliders.append(master_volume_slider)

        self.y_4 = self.y_3 + padding * 2
        music_volume_slider = Slider('music_volume', 
                                      self.slider_x, self.y_4 + 8,
                                      self.slider_lenght, 
                                      0, 100, 
                                      self.game.settings.music_volume * 100,
                                      on_change=self.update_settings)
        
        self.add_text('music volume', self.text_x, self.y_4)
        self.add_slider_number(
            'music_volume', int(self.game.settings.music_volume * 100), 
            self.slider_x - padding * 2,
            self.y_4)
        self.sliders.append(music_volume_slider)

        self.y_5 = self.y_4 + padding * 2
        sfx_volume_slider = Slider('sfx_volume', 
                                      self.slider_x, self.y_5 + 8,
                                      self.slider_lenght, 
                                      0, 100, 
                                      self.game.settings.sfx_volume * 100,
                                      on_change=self.update_settings)
        
        self.add_text('sfx volume', self.text_x, self.y_5)
        self.add_slider_number(
            'sfx_volume', int(self.game.settings.sfx_volume * 100), 
            self.slider_x - padding * 2,
            self.y_5)
        self.sliders.append(sfx_volume_slider)


    def load_else(self):
        pass

    # HELPERS

    def add_text(self, str, x, y):
        '''
        helper function for adding text to a list
        '''
        self.texts.append({'str': str, 'x': x, 'y': y}) 

    def add_slider_number(self, name, number, x, y):
        self.slider_numbers[name] = {'str': str(number), 'x': x, 'y': y}