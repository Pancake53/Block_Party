import pygame, json


from part import Part
from states.state import State
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

        if isinstance(name, tuple):
           
            self.selected_colour = name
            self.handle_colour_change()
            return

        match name:
            case 'left_arrow':
                self.change_col_left()
            case 'right_arrow':
                self.change_col_right()

            case 'bucket':
                self.lock_colour = not self.lock_colour

            case 'new_piece':
                self.spawn_part(selected=True)

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

            case 'trash':
                if self.selected_part:
                    if self.selected_part.main == False:
                        self.character_parts.remove(self.selected_part)
                        self.selected_part = None

            case 'forward1':
                if self.selected_part:
                    self.update_layers(self.selected_part, name)
                else:
                    print('no selection!')

            case 'back1':
                if self.selected_part:
                    self.update_layers(self.selected_part, name)
                else:
                    print('no selection!')

            case 'top':
                if self.selected_part:
                    self.update_layers(self.selected_part, name)
                else:
                    print('no selection!')

            case 'bottom':
                if self.selected_part:
                    self.update_layers(self.selected_part, name)
                else:
                    print('no selection!')

            case 'save':
                self.save()

            case 'load':
                self.load_from_save()

            case 'done':
                self.change_state()

            case _:
                print(f'Char creating handle cliks invalid name: {name}!')

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
            if self.selected_part is None:
                self.selected_part = self.character_parts[0]

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

        for line in self.grid_lines:
            pygame.draw.line(surface, self.game.TEXT_COL, 
                             line['start'], line['end'], width=1)

        pygame.draw.rect(surface, self.game.TILE_COL, self.hitbox, width=3, border_radius=5)
        self.game.draw_text(surface, 'hitbox', 
                            self.game.TEXT_COL, 
                            self.hitbox_text_x, self.hitbox_text_y, 
                            'Small')
        
        draw_shading_for_rect(self.game.TILE_COL,
            self.bg_char_creating, surface, shading_W=5)
        
        for line in self.lines:
            pygame.draw.line(surface, 
                            self.game.LIGHT_GREY, 
                            line[0], line[1], 
                            width=5)
        
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
            pygame.draw.rect(surface, self.game.TEXT_COL, self.btn_lock_colour.rect, width=5) 
        
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
        
        self.load_editbox()
        
        self.load_created_characters()

        self.load_saved_chars_data()

    def load_ui(self):
        '''
        load needed buttons for the view
        '''

        self.padding = 15
        self.line_padding = 10


        self.left_x = self.game.GAME_W / 2 - 10
        self.left_arrow_y = self.game.GAME_H / 4
        self.arrow_W, self.arrow_H = self.game.assets["arrowleft_img"].get_size()
        self.right_arrow_x = self.game.GAME_W - self.arrow_W - self.padding
        self.right_arrow_y = self.left_arrow_y


        self.buttons = []
        self.texts = []
        self.images = []
        
        
        self.load_images()
        self.load_sliders()
        self.load_buttons()
        

        self.title_x = self.red_slider.x + self.red_slider.width / 2 - 10
        self.title_y = self.game.GAME_H / 8 - 10
        self.add_text('create your character', self.title_x, self.title_y, size='Medium')

        self.load_helpers()
        self.load_lines()
        


    def load_images(self):
        
        
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
        

    def load_buttons(self):
        
        # grid
        
        
        # 1 arrow
        name = 'left_arrow'


        # button = ButtonStationary(
        #     name,
        #     self.left_arrow_x, self.left_arrow_y, 
        #     image = self.game.assets["arrowleft_img"],
        #     on_click=self.handle_clicks
        # )
        # self.buttons.append(button)

        # 2 arrow
        name = 'right_arrow'    


        # button = ButtonStationary(
        #     name,
        #     self.right_arrow_x, self.right_arrow_y, 
        #     image = self.game.assets["arrowright_img"],
        #     on_click=self.handle_clicks
        # )
        # self.buttons.append(button)

                # lock colour
        name = 'bucket'

        x = self.left_x
        y_bucket = self.blue_slider.y + self.blue_slider.height + self.padding
        bucket_h = self.game.assets['bucket_img'].get_height()
        bucket_w = self.game.assets['bucket_img'].get_width()

        self.btn_lock_colour = ButtonStationary(
            name,
            x, y_bucket, 
            button_colour=self.selected_colour,
            hover_colour=self.selected_colour,
            image=self.game.assets['bucket_img'],
            on_click=self.handle_clicks
        )

        self.buttons.append(self.btn_lock_colour)

        # small colour buttons :)
        w = 35
        h = 35
        x_grid = [(x+bucket_w + self.padding) + i * (w + self.line_padding) for i in range(8)]
        y_grid = [y_bucket, y_bucket + h + self.padding]

        colours = [
            (0, 0, 0),
            (115, 115, 115),
            (255, 255, 255),
            (235, 117, 117),
            (224, 25, 25),
            (222, 105, 22), 
            (222, 125, 22),
            (232, 221, 63),
            (149, 227, 32),
            (5, 179, 43),
            (44, 209, 198),
            (44, 110, 209),
            (113, 44, 209),
            (209, 44, 209),
            (209, 44, 110),
            (209, 44, 44)
            # (130, 0, 0)
        ]

        i = 0
        for y in y_grid:
            for x in x_grid:
                colour = colours[i]

                button = ButtonStationary(
                    colour,
                    x, y,
                    width=w, height=h,
                    on_click=self.handle_clicks,
                    hover_colour=colour,
                    button_colour=colour
                )

                self.buttons.append(button)

                i += 1


        # --- PIECE CONTROL ---

        # New piece
        name = 'new_piece'

        w = 150
        h = 50

        # new piece
        x = self.left_x
        new_piece_y = y_bucket + bucket_h + self.line_padding * 2
        y = new_piece_y

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

        self.add_text('new', text_x, text_y)

        self.add_rect.x = x + w - self.add_rect.width - 3
        self.add_rect.y = y + 2



        # duplicate
        name = 'duplicate'

        x += self.padding + w

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

        self.add_text('copy', text_x, text_y)

        self.duplicate_rect.x = x + w - self.duplicate_rect.width - 3
        self.duplicate_rect.y = y + 2

        # trah
        name = 'trash'

        x += self.padding + w

        button = ButtonStationary(
            name,
            x, y,  
            image=self.game.assets['trash_open_img'],
            hovered_image=self.game.assets['trash_closed_img'],
            background = False,
            change_col = False,
            on_click=self.handle_clicks
        )

        self.buttons.append(button)

        


        # --- FORWARD / BACKWARD / LAYERS CONTROL ---

        
        name = 'forward1'

        w = 50
        h = 50

        x = self.left_x
        y = new_piece_y + h + self.padding
        

        button = ButtonStationary(
            name,
            x, y, 
            width=w, height=h, 
            button_colour=self.game.BG_COL,
            image=self.game.assets['forward1_img'],
            on_click=self.handle_clicks)
        
        self.buttons.append(button)

        name = 'back1'

        x += self.padding + w

        button = ButtonStationary(
            name,
            x, y, 
            width=w, height=h, 
            button_colour=self.game.BG_COL,
            image=self.game.assets['back1_img'],
            on_click=self.handle_clicks)
        
        self.buttons.append(button)

        name = 'top'

        x += self.padding + w

        button = ButtonStationary(
            name,
            x, y, 
            width=w, height=h, 
            button_colour=self.game.BG_COL,
            image=self.game.assets['top_img'],
            on_click=self.handle_clicks)
        
        self.buttons.append(button)

        name = 'bottom'

        x += self.padding + w

        button = ButtonStationary(
            name,
            x, y, 
            width=w, height=h, 
            button_colour=self.game.BG_COL,
            image=self.game.assets['bottom_img'],
            on_click=self.handle_clicks)
        
        self.buttons.append(button)

        # reset
        name = 'reset'
 
        x += self.padding + w  + 5

        
        button = ButtonStationary(
            name,
            x, y,  
            button_colour=self.game.BG_COL,
            image=self.game.assets["reset_img"],
            on_click=self.handle_clicks
        )

        self.buttons.append(button)


        # --- BOTTOM ROW ---
        # save
        name = 'save'

        w = 150
        h = 50

        x = self.left_x
        y += h + self.line_padding * 2
        self.y_bottom = y


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

        # load
        name = 'load'


        x += w + self.padding
        
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



        # Done
        name = 'done'


        x += w + self.padding
        w = 100


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
        

    def load_sliders(self):
        '''
        loads slider objects
        '''
        w = 255
        h = 20
        x = (self.left_x + self.arrow_W + self.right_arrow_x) / 2 - w / 2
        y = self.left_arrow_y + self.arrow_H / 2 - h * 2 - 6
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
        w = 24
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
        x_left = self.left_x - self.padding
        line_start = (x_left, y)

        x_right = self.game.GAME_W - 5
        line_end = (x_right, y)
        self.lines.append([line_start, line_end])

        y = (self.btn_lock_colour.y 
             + self.btn_lock_colour.height + self.line_padding)
        line_start = (x_left, y)
        line_end = (x_right, y)
        self.lines.append([line_start, line_end]) 

        y = self.y_bottom - 10
        line_start = (x_left, y)
        line_end = (x_right, y)
        self.lines.append([line_start, line_end])

        
        



    def load_editbox(self):
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
        # scalar = 6
        self.scalar = self.bg_char_creating.height / self.game.char_surface_H
        # print(self.scalar)

        # load grid
        self.grid_lines = []
        for y_temp in range(int(y), int(y + H), int(self.scalar * 4)):
            self.grid_lines.append({'start': (x, y_temp), 'end': (x + W, y_temp)})
        for x_temp in range(int(x), int(x + W), int(self.scalar * 4)):
            self.grid_lines.append({'start': (x_temp, y), 'end': (x_temp, y + H)})

        

        # starting colour, position and dimensions, hitbox
        height = self.game.CHARACTER_SIZE * 2 * self.scalar
        width = height / 2
        # print(f'Scalar: {self.scalar}, width: {width}')

        x = self.bg_char_creating.x + self.bg_char_creating.width / 2 - width / 2
        y = self.bg_char_creating.y + self.bg_char_creating.height - height
        self.hitbox = pygame.Rect(x, y, width, height)
        self.hitbox_text_x = x + width / 2
        self.hitbox_text_y = y + 25

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
            x = self.left_x
        
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
        self.load_editbox()

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
        # print('button should update')
        self.btn_lock_colour.button_colour = self.selected_colour
        self.btn_lock_colour.hover_colour = self.selected_colour

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
    
    # layer

    def update_layers(self, part, action):
        '''
        changes parts order in character_parts
        '''

        match action:
            case 'forward1':
                
                index = self.character_parts.index(part)

                if index < len(self.character_parts) - 1:
                    self.character_parts.remove(part)
                    index += 1
                    self.character_parts.insert(index, part)

            case 'back1':
                
                index = self.character_parts.index(part)
                if index > 0:
                    self.character_parts.remove(part)
                    index += -1
                    self.character_parts.insert(index, part)

            case 'top':
                
                self.character_parts.remove(part)
            
                self.character_parts.append(part)

            case 'bottom':
    
                self.character_parts.remove(part)
                index = 0
                self.character_parts.insert(index, part)

    # save & load

    def save(self):
        self.game.state_m.enter_state('save_menu')
        

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
                                      char_surface_pos = self.bg_char_creating.topleft,
                                      scalar = self.scalar)

    def on_return(self, returned):
        '''
        handels 
        a) returned index out of load overlay
        b) returned name string out of save overlay

        returned 
        '''

        action = returned[0]
        print(returned)
        match action:
            case 'load':
                
                index = int(returned[1])
        
                #  => loading from save
                # print(f'handling returned in char creating, returned: {returned}')
                self.character_parts.clear()
                # print(f'parts list after clear: {self.character_parts}')

                new_char_data = self.saved_chars_data[index]

                for part in new_char_data['parts']:
                    
                    new_part = Part(part['x'], part['y'], 
                                    part['w'], part['h'], 
                                    part['colour'], part['layer'], 
                                    self, part['main'])
                    
                    self.character_parts.append(new_part)

                with open('data/saved_characters.json', 'w') as file:
                    json.dump(self.saved_chars_data, file, indent=4) 
            
                # print(f'parts list after adding: {self.character_parts}')

            case 'delete':
                # only deleting in load menu
                with open('data/saved_characters.json', 'w') as file:
                    json.dump(self.saved_chars_data, file, indent=4) 

            case 'save':
                # => name for saved character
                name = returned[1]
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

            case _:
                print(f'On return in char creating failed, action: {action}')


    # helpers

    def add_text(self, str, x, y, size='Small'):
        self.texts.append({'str': str, 'x': x, 'y': y, 'size': size})

    def add_image(self, asset, rect):
        self.images.append({'img': asset, 'rect': rect})