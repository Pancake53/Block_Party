import pygame, json


from part import Part
from states.state import State
from states.level_menu import Level_Menu
from UI.button_stationary import ButtonStationary
from UI.slider import Slider
from helpers import draw_shading_for_rect

class Char_Creating(State):
    def __init__(self, game, players_left=1, created_chars=None):
        super().__init__(game)
        # how many players havent created their characters yet
        self.players_left = players_left - 1

        # About created_chars
        # all characters created by players so far
        # dictionary with player id as the first key
        # value is dict, which 
        # contain keys main_colour and char_surface
        print(created_chars)

        # selecting players id
        if created_chars:
            self.created_characters_for_render = []
            self.created_chars = created_chars
            self.player_id = len(self.created_chars)
            self.taken_colours = [char['main_colour']
                                for char in self.created_chars.values()]
    
            # print(f'{self.taken_colours}')
        else:
            self.player_id = 0
            self.created_chars = {}
            self.taken_colours = []

        # print(f'{self.created_chars}')

        # set startoff colour
        self.colour_id = 0
        self.main_colour = self.game.team_colours[self.colour_id]
        while self.main_colour in self.taken_colours:
            self.colour_id += 1
            self.main_colour = self.game.team_colours[self.colour_id]

        self.selected_colour = self.main_colour
        self.red, self.green, self.blue = self.selected_colour

        # button pressed states 
        self.lock_colour = False


        # changes with regard to which rect has been last clicked
        self.selected_part = None

        self.top_part = None
        self.top_part_pos = 0
        self.character_parts = []


        # sliders
        self.sliders = []
        self.lines = []

        self.load() # Buttons / UI elements / coordinates

    def update(self, delta_time, actions):
        '''
        updates state

        on click: creates and enters game world 
        (or level select menu in future)

        delta_time: dt
        actions: user inputs dictionary
        '''
        
        # print(self.created_chars)
        self.handle_actions(actions)
        for button in self.buttons:
            button.update(actions)

        for slider in self.sliders:
            slider.update(actions)
        self.update_helpers()

        self.update_parts(delta_time, actions)
        self.game.cursor = self.cursor


    def handle_clicks(self, name):

        match name:
            case 'left_arrow':
                self.change_col_left()
            case 'right_arrow':
                self.change_col_right()

            case 'bucket':
                self.lock_colour = not self.lock_colour

            case 'new_piece':
                self.spawn_part()

            case 'duplicate':
                if self.selected_part:
                    self.spawn_part(self.selected_part.x + 12, 
                                self.selected_part.y - 12, 
                                self.selected_part.W,
                                self.selected_part.H,
                                self.selected_part.colour,
                                selected=True)

            case 'reset':
                self.reset_parts()

            case 'save':
                self.save()

            case 'load':
                self.load_from_save()

            case 'done':
                self.change_state()

    def handle_actions(self, actions):
        '''
        handels actions based on user input
        '''

        if actions["esc"]:
            self.game.state_m.exit_state()

        self.mouse_actions(actions)

    def mouse_actions(self, actions):
        '''
        mouse over the parts 
        and checking which part is the top one
        '''
        mouse_pos = actions['mouse_pos']

        self.update_selection(actions)
        
    def update_selection(self, actions):
        '''
        update which part is selected
        '''
        # reset
        self.top_part = None
        self.top_part_pos = 0

        for part in self.character_parts:
            # mouse over part
            if part.hovered:
                # if first part
                if not self.top_part:
                    self.top_part = part
                    self.top_part_layer = part.layer
                # part is on top of another
                elif part.layer > self.top_part_layer:
                    self.top_part = part
                    self.top_part_layer = part.layer

        for part in self.character_parts:
            if part == self.top_part:
                part.state['top'] = True
            else:
                part.state['top'] = False    




    def change_col_left(self):
        '''
        handle left button colour change logic
        wrap around and assignment
        '''
        
        if self.colour_id == 0:
            self.colour_id = len(self.game.team_colours) - 1
        else:
            self.colour_id -= 1

        self.selected_colour = self.game.team_colours[self.colour_id]

        if self.selected_part is None:
            self.selected_part = self.character_parts[0]

        if self.selected_part.main:
            while self.selected_colour in self.taken_colours:
                if self.colour_id == 0:
                    self.colour_id = len(self.game.team_colours) - 1
                else:
                    self.colour_id -= 1
                self.selected_colour = self.game.team_colours[self.colour_id]

        self.handle_colour_change()


    def change_col_right(self):
        '''
        handle right button colour change logic
        wrap around and assignment
        '''
        
        if self.colour_id == len(self.game.team_colours) - 1:
            self.colour_id = 0
        else:
            self.colour_id += 1

        self.selected_colour = self.game.team_colours[self.colour_id]

        if self.selected_part is None:
            self.selected_part = self.character_parts[0]

        if self.selected_part.main:
            while self.selected_colour in self.taken_colours:
                if self.colour_id == len(self.game.team_colours) - 1:
                    self.colour_id = 0
                else:
                    self.colour_id += 1
                self.selected_colour = self.game.team_colours[self.colour_id]

        self.handle_colour_change()          
            
    def handle_colour_change(self):
            self.selected_part.colour = self.selected_colour
            self.red, self.green, self.blue = self.selected_colour
            self.update_sliders()   
            self.update_buttons()

    def update_helpers(self):
        '''
        updates helper rect for choosing colour
        '''    
        for helper in self.helpers:
            colour = [i for i in self.selected_colour]
            if helper['side'] == -1: # left side
                extreme_value = 0
            elif helper['side'] == 1: # right side
                extreme_value = 255
            colour[helper['colour_id']] = extreme_value
            helper['rgb'] = tuple(colour)

    def update_parts(self, dt, actions):
        for part in self.character_parts:
            part.update(dt, actions)

    def change_state(self):
        '''
        handels what happens after next is selected

        changes state either to next chars creation
        or 
        to select selection screen
        '''
        # reset the selected state
        self.selected = False

        self.created_chars[self.player_id] = self.create_surface_from_created_char()

        if self.players_left > 0:
            # more characters to be created
            self.game.state_m.enter_state('char_creating', 
                                          player_count = self.players_left,
                                          created_chars = self.created_chars 
                                          )
            
        else:
            # all characters created, go to selecting level
            self.game.state_m.enter_state('level_menu', 
                                   created_chars = self.created_chars)            

    def render(self, surface):
        '''
        renders background and character customatization
        
        surface: surface to render on
        '''
        surface.fill((self.game.UI_BG_COL))

        pygame.draw.rect(surface, self.game.BG_COL, self.bg_char_creating)
        draw_shading_for_rect(self.game.TILE_COL,
            self.bg_char_creating, surface, shading_W=5)
        
        for line in self.lines:
            pygame.draw.line(surface, 
                            self.game.LIGHT_GREY, 
                            line[0], line[1], 
                            width=7)
        
        self.render_buttons(surface)
        self.render_slicers(surface)
        self.render_helpers(surface)
        
        if self.player_id > 0:
            self.render_created_characters(surface)

        self.render_parts(surface)    

    def render_buttons(self, surface):
        '''
        renders buttons duh and controls what actions get 
        triggered by them
        '''
        # switch colours between presets
        for button in self.buttons:
            button.render(surface)


        # Text for buttons

        for text in self.texts:
            self.game.draw_text(
                surface,
                text['str'],
                self.game.TILE_COL,
                text['x'], text['y'],
                size=text['size']
            )

        # images
        for image in self.images:
            surface.blit(image['img'], image['rect'])  

        # to show that is selected
        if self.lock_colour:
            pygame.draw.rect(surface, self.game.BLACK, self.btn_lock_colour.rect, width=3) 
        
    def render_slicers(self, surface):

        for slider in self.sliders:
            slider.render(surface)

    def render_helpers(self, surface):
        '''
        render rects that help w colour choosing
        '''
        for helper in self.helpers:
            pygame.draw.rect(surface, helper['rgb'], helper['rect'])
            draw_shading_for_rect(self.game.BLACK, helper['rect'],
                                surface, shading_W=2)

    def render_parts(self, surface):
        '''
        calls each parts render function
        '''
        for part in self.character_parts:
            part.render(surface)

    def render_created_characters(self, surface):
        # About created_characters_for_render
        # all characters created by players so far
        # list with dicts, which 
        # contain keys char_surface, x, y
        for char_dict in self.created_characters_for_render:
            
            surface.blit(char_dict['char_surface'],
                (char_dict['x'], char_dict['y']))

            draw_shading_for_rect(self.game.TILE_COL,
                char_dict['rect'], surface)


    def create_surface_from_created_char(self):
        '''
        create a surface from created character

        returns:
        a dict with keys main_colour and char_surface
        '''
        new_dict = {}
        main_colour = next(
            part.colour
            for part in self.character_parts 
            if part.main
        )

        # create new surface and 
        char_surface = pygame.Surface(
            (self.game.char_surface_W, self.game.char_surface_H),
            pygame.SRCALPHA) # transparent

        # render each part onto character surface
        for part in self.character_parts:
            self.scale_part(part, char_surface)

        # update and return new dict
        new_dict['main_colour'] = main_colour
        new_dict['char_surface'] = char_surface
        return new_dict
    
    
    def scale_part(self, part, char_surface):
        '''
        rescales a single part and draws it on surface
        '''
        colour = part.colour
        rect = part.rect

        # coordinates
        
        x = ( rect.x + rect.width / 2 - self.bg_char_creating.x ) / self.scalar
        y = ( rect.y + rect.height / 2 - self.bg_char_creating.y ) / self.scalar

        # dimensions
        w = rect.width / self.scalar
        h = rect.height / self.scalar

        # reposition
        x -= w / 2
        y -= h / 2

        pygame.draw.rect(char_surface, colour,
                          pygame.Rect(x, y, w, h))
            
    def load(self):
        '''
        calls other load functions
        '''

        self.load_ui()
        
        self.load_hitbox()
        
        self.load_created_characters()

        self.load_saved_chars_data()

    def load_ui(self):
        '''
        load needed buttons for the view
        '''



        self.buttons = []
        self.texts = []
        self.images = []
        
        
        self.load_images()

        self.load_buttons()
        self.load_sliders()

        self.title_x = self.red_slider.x + self.red_slider.width / 2 - 10
        self.title_y = self.game.GAME_H / 8 - 10
        self.add_text('create your character', self.title_x, self.title_y, size='H1')

        self.load_helpers()
        self.load_lines()
        
    def load_images(self):
        # bucket
        self.bucket_img = self.game.assets['bucket_img']
        self.bucket_rect = self.bucket_img.get_rect()
        self.add_image(self.bucket_img, self.bucket_rect)
        # add
        self.add_img = self.game.assets['add_img']
        self.add_rect = self.add_img.get_rect()
        self.add_image(self.add_img, self.add_rect)
        # copy
        self.duplicate_img = self.game.assets['copy_img']
        self.duplicate_rect = self.duplicate_img.get_rect()
        self.add_image(self.duplicate_img, self.duplicate_rect)
        # save
        self.save_img = self.game.assets['save_img']
        self.save_rect = self.save_img.get_rect()
        self.add_image(self.save_img, self.save_rect)

        # load
        self.load_img = self.game.assets['load_img']
        self.load_rect = self.load_img.get_rect()
        self.add_image(self.load_img, self.load_rect)
        # trash_closed
        self.trash_closed_img = self.game.assets['trash_closed_img']
        self.trash_rect = self.trash_closed_img.get_rect()
        self.add_image(self.trash_closed_img, self.trash_rect)
        # trash_open
        self.trash_open_img = self.game.assets['trash_open_img']

    def load_buttons(self):
        
        padding = 15
        
        # 1 arrow
        name = 'left_arrow'
        self.left_arrow_x = self.game.GAME_W / 2 
        self.left_arrow_y = self.game.GAME_H / 4
        self.arrow_W, self.arrow_H = self.game.assets["arrowleft_img"].get_size()

        button = ButtonStationary(
            name,
            self.left_arrow_x, self.left_arrow_y, 
            image = self.game.assets["arrowleft_img"],
            on_click=self.handle_clicks
        )
        self.buttons.append(button)

        # 2 arrow
        name = 'right_arrow'    
        self.right_arrow_x = self.game.GAME_W - self.arrow_W - padding
        self.right_arrow_y = self.left_arrow_y

        button = ButtonStationary(
            name,
            self.right_arrow_x, self.right_arrow_y, 
            image = self.game.assets["arrowright_img"],
            on_click=self.handle_clicks
        )
        self.buttons.append(button)

        
        
        # New piece
        name = 'new_piece'

        w = 200
        h = 50

        # new piece
        x = (self.game.GAME_W / 2 - 10)
        y = (self.game.GAME_H * 2 / 3 -
            h / 2)

        button = ButtonStationary(
            name,
            x, y, 
            width=w, height=h, 
            button_colour=self.game.BG_COL,
            on_click=self.handle_clicks
        )

        self.buttons.append(button)

        text_x = x + w / 3 + 12
        text_y = y + h / 2

        self.add_text('new piece', text_x, text_y)

        self.add_rect.x = x + w - self.add_rect.width - 3
        self.add_rect.y = y + 2



        # duplicate
        name = 'duplicate'

        x += padding + w

        button = ButtonStationary(
            name,
            x, y, 
            width=w, height=h, 
            button_colour=self.game.BG_COL,
            on_click=self.handle_clicks
        )

        self.buttons.append(button)

        text_x = x + w / 3 + 12
        text_y = y + h / 2

        self.add_text(name, text_x, text_y)

        self.duplicate_rect.x = x + w - self.duplicate_rect.width - 3
        self.duplicate_rect.y = y + 2

        # reset
        name = 'reset'
 
        x += padding + w 

        
        button = ButtonStationary(
            name,
            x, y,  
            button_colour=self.game.BG_COL,
            image=self.game.assets["reset_img"],
            on_click=self.handle_clicks
        )

        self.buttons.append(button)



        # lock colour
        name = 'bucket'

        h = 100
        w = 70

        x = self.left_arrow_x
        y = self.left_arrow_y + self.arrow_H + padding

        self.btn_lock_colour = ButtonStationary(
            name,
            x, y, 
            width=w, height=h, 
            button_colour=self.selected_colour,
            hover_colour=self.selected_colour,
            on_click=self.handle_clicks
        )

        self.buttons.append(self.btn_lock_colour)

        self.bucket_rect.x = x + 12
        self.bucket_rect.y = y + 12

        # BOTTOM ROW

        # Done
        name = 'done'

        w = 100
        h = 50

        x = self.game.GAME_W - w - 10
        y = self.game.GAME_H - h - 10
        self.y_bottom = y

        button = ButtonStationary(
            name,
            x, y, 
            width=w, height=h, 
            button_colour=self.game.BG_COL,
            on_click=self.handle_clicks)
        
        self.buttons.append(button)

        text_x = x + w / 2
        text_y = y + h / 2
        self.add_text(name, text_x, text_y)
        
        # load
        name = 'load'

        w = 150
        x -= w + padding
        
        button = ButtonStationary(
            name,
            x, y, 
            width=w, height=h, 
            button_colour=self.game.BG_COL,
            on_click=self.handle_clicks
        )

        self.buttons.append(button)

        text_x = x + w / 3 + 4
        text_y = y + h / 2
        self.add_text(name, text_x, text_y)

        self.load_rect.x = x + w - self.load_rect.width - 3
        self.load_rect.y = y

        # save
        name = 'save'

        x -= w + padding

        button = ButtonStationary(
            name,
            x, y, 
            width=w, height=h, 
            button_colour=self.game.BG_COL,
            on_click=self.handle_clicks
        )

        self.buttons.append(button)

        text_x = x + w / 3 + 4
        text_y = y + h / 2
        self.add_text(name, text_x, text_y)

        self.save_rect.x = x + w - self.save_rect.width - 3
        self.save_rect.y = y

    def load_sliders(self):
        '''
        loads slider objects
        '''
        w = 255
        h = 20
        x = (self.left_arrow_x + self.arrow_W + self.right_arrow_x) / 2 - w / 2
        y = self.left_arrow_y + self.arrow_H / 2 - h * 2
        self.red_slider = Slider("red",
                            x, y, w,
                            0, 255, self.red,
                            height = h, 
                            on_change=self.update_colour, colour=(255, 0, 0))

        y += h * 2
        self.green_slider = Slider("green",
                            x, y, w,  
                            0, 255, 
                            self.green, 
                            height = h, 
                            on_change=self.update_colour, colour=(0, 255, 0))

        y += h * 2
        self.blue_slider = Slider("blue", 
                            x, y, w,
                            0, 255, 
                            self.blue, 
                            height = h, 
                            on_change=self.update_colour, colour=(0, 0, 255))

        self.sliders.extend([self.red_slider, self.green_slider, self.blue_slider])    

    def load_helpers(self):
        '''
        loads rects that help w colour choosing
        '''
        w = 16
        h = 24
        left_value = 0
        right_value = 255
        padding = 10
        self.helpers = []

        # red
        x_left = self.red_slider.x - padding - w
        y_red = self.red_slider.y - h / 2
        left_red = pygame.Rect(x_left, y_red, w, h)
        self.helpers.append({
            'side' : -1, 'colour_id': 0,
            'rgb' : (255, 120, 120),
            'rect': left_red})

        x_right = self.red_slider.x + self.red_slider.width + padding
        right_red = pygame.Rect(x_right, y_red, w, h)
        self.helpers.append({
            'side' : 1, 'colour_id': 0,
            'rgb' : (255, 120, 120),
            'rect': right_red})

        # green
        y_green = self.green_slider.y - h / 2
        left_green = pygame.Rect(x_left, y_green, w, h)
        self.helpers.append({
            'side' : -1, 'colour_id': 1,
            'rgb' : (255, 120, 120),
            'rect': left_green})

        right_green = pygame.Rect(x_right, y_green, w, h)
        self.helpers.append({
            'side' : 1, 'colour_id': 1,
            'rgb' : (255, 120, 120),
            'rect': right_green})

        # blue
        y_blue = self.blue_slider.y - h / 2
        left_blue = pygame.Rect(x_left, y_blue, w, h)
        self.helpers.append({
            'side' : -1, 'colour_id': 2,
            'rgb' : (255, 120, 120),
            'rect': left_blue})

        right_blue = pygame.Rect(x_right, y_blue, w, h)
        self.helpers.append({
            'side' : 1, 'colour_id': 2,
            'rgb' : (255, 120, 120),
            'rect': right_blue})      

    def load_lines(self):
        # LINES / DIVIDERS

        # title
        y = self.title_y + 40
        x_left = self.left_arrow_x - 5
        line_start = (x_left, y)

        x_right = self.game.GAME_W - 5
        line_end = (x_right, y)
        self.lines.append([line_start, line_end])

        y = self.y_bottom - 20
        line_start = (x_left, y)
        line_end = (x_right, y)
        self.lines.append([line_start, line_end])  

    def load_hitbox(self):
        '''
        loads initial box into view
        '''
        # background, area to create char in 
        W = self.game.GAME_W / 4
        H = W * self.game.char_surface_H / self.game.char_surface_W
        x = W * 0.75 # from left side 
        y = self.game.GAME_H / 2 - H / 2 # center

        self.bg_char_creating = pygame.Rect(x, y, W, H) 

        # scale of big view char to the real char in game
        # scalar = 3
        self.scalar = self.bg_char_creating.height / self.game.char_surface_H

        # starting colour, position and dimensions, hitbox
        height = self.game.CHARACTER_SIZE * 2 * self.scalar
        width = height / 2
        print(f'Scalar: {self.scalar}, width: {width}')

        x = self.bg_char_creating.x + self.bg_char_creating.width / 2 - width / 2
        y = self.bg_char_creating.y + self.bg_char_creating.height - height

        self.spawn_part(x, y, width, height, self.main_colour, main= True)

        # second rect for testing !!!
        self.default_outfit(x, y, width, height)
        
    def default_outfit(self, x, y, width, height):
        # hat :D
        # bottom part
        width *= 1.5
        height *= 0.2
        y -= height - 4
        x -= width / 1.5 * 0.25
        # print(f'x: {x}, y: {y}')
        colour = (209, 31, 4)
        self.spawn_part(x, y, width, height, colour)
        # top part
        width *= 0.5
        y -= height - 4
        x += width * 0.5
        # print(f'x: {x}, y: {y}')
        colour = (209, 31, 4)
        self.spawn_part(x, y, width, height, colour)

        # eyes and smile
        # left eye
        y += height * 3
        width = 12
        height = width
        colour = self.game.BLACK
        
        self.spawn_part(x, y, width, height, colour)
    
        # right eye
        x += width * 3
        self.spawn_part(x, y, width, height, colour)
        # smile
        x -= width * 3
        y += width * 3
        width *= 4
        self.spawn_part(x, y, width, height, colour)

    def load_created_characters(self):
        '''
        showcase created characters
        '''
        # Created chatacters

        # About created_chars
        # all characters created by players so far
        # dictionary with player id as the first key
        # value is dict, which 
        # contain keys main_colour and char_surface

        if self.created_chars:
            x = self.game.char_surface_W

            for id, dict in self.created_chars.items():
                y = self.game.char_surface_H * 1.5 * (1 + id)
                self.created_characters_for_render.append(
                    {'x': x,
                    'y': y,
                    'char_surface' : dict['char_surface'],
                    'rect': pygame.Rect(x, y, 
                    dict['char_surface'].width,
                    dict['char_surface'].height)
                    }
                )     
                        
    def spawn_part(self, x = None, y = None, W = None, H = None, colour = None, main = False, selected = False):
        '''
        creates new Part obj and adds it character parts
        '''
        if x is None:
            x = self.left_arrow_x
        
        if y is None:
            y = self.y_bottom - 70

        if W is None:   
            W = 50
        if H is None:
            H = 50

        if colour is None:
            colour = self.selected_colour

        

        layer = len(self.character_parts)
        new_part = Part(x, y, W, H, colour, layer, self, main)
        self.character_parts.append(new_part)
        if selected:
            self.selected_part = new_part
            new_part.state['selected'] = True

    def reset_parts(self):
        '''
        resets back to default
        '''
        self.character_parts.clear()
        self.load_hitbox()

    def update_colour(self, colour, value):
        setattr(self, colour, value)
        self.selected_colour = (self.red, self.green, self.blue)

        if self.selected_part is None:
            self.selected_part = self.character_parts[0]
        self.selected_part.colour = self.selected_colour
        self.update_buttons()

    def update_sliders(self):
        self.red, self.green, self.blue = self.selected_colour
        self.red_slider.current_value_float = self.red
        self.green_slider.current_value_float = self.green
        self.blue_slider.current_value_float = self.blue
        for slider in self.sliders:
            slider.update_pos()

    def update_buttons(self):
        self.btn_lock_colour.button_col = self.selected_colour
        self.btn_lock_colour.hover_col = self.selected_colour

    def set_selection(self, part):
        self.selected_part = part

        if not self.lock_colour:
            self.selected_colour = part.colour

            # set colour id to match parts colour
            if self.selected_colour in self.game.team_colours:
                for i, colour in enumerate(self.game.team_colours):
                    if colour == self.selected_colour:
                        self.colour_id = i
                        print(f'Colour id: {self.colour_id}')

            # update ui
            self.update_sliders()   
            self.update_buttons()
        
        # colour lock button has been pressed
        else: 
            self.selected_part.colour = self.selected_colour
    
    # save & load

    def save(self):

        name = 'test4'
        parts = []
        for part in self.character_parts:
            part_data = {
                'x': part.rect.x,
                'y': part.rect.y,
                'w': part.rect.width,
                'h': part.rect.height,
                'colour': part.colour,
                'layer': part.layer,
                'main': part.main
            }
            parts.append(part_data)
        
        new_char = {
            'name': name,
            'main_colour': self.main_colour,
            'parts': parts
        }

        self.saved_chars_data.append(new_char)

        with open('data/saved_characters.json', 'w') as file:
            json.dump(self.saved_chars_data, file, indent=4)

    def load_saved_chars_data(self):
        '''
        loads saved chars data for saving and displaying
        '''
        # load data from file
        try:
            with open('data/saved_characters.json', 'r') as file:
                self.saved_chars_data = json.load(file)

        except FileNotFoundError:
            print('File not found')
            self.saved_chars_data = []

        except json.JSONDecodeError:
            print('decoder error')
            self.saved_chars_data = []

    def load_from_save(self):
        self.game.state_m.enter_state('load_menu', data = self.saved_chars_data, 
                                      char_surface_pos = self.bg_char_creating.topleft)

    # helpers

    def add_text(self, str, x, y, size='Small'):
        self.texts.append({'str': str, 'x': x, 'y': y, 'size': size})

    def add_image(self, asset, rect):
        self.images.append({'img': asset, 'rect': rect})