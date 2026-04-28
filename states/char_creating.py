import pygame

from part import Part
from states.state import State
from states.level_menu import Level_Menu
from UI.button import Button
from helpers import draw_shading_for_rect

class Char_Creating(State):
    def __init__(self, game, players_left, created_chars=None):
        self.game = game
        # how many players havent created their characters yet
        self.players_left = players_left - 1

        # About created_chars
        # all characters created by players so far
        # dictionary with player id as the first key
        # value is dict, which 
        # contain keys main_colour and char_surface
        
        # selecting players id
        if created_chars:
            self.created_characters_for_render = []
            self.created_chars = created_chars
            self.player_id = len(self.created_chars)
            self.taken_colours = [char['main_colour']
                                for char in self.created_chars.values()]
    
            print(f'{self.taken_colours}')
        else:
            self.player_id = 0
            self.created_chars = {}
            self.taken_colours = []

        # print(f'{self.created_chars}')

        self.selected = False

        # set startoff colour
        self.colour_id = 0
        self.main_colour = self.game.team_colours[self.colour_id]
        while self.main_colour in self.taken_colours:
            self.colour_id += 1
            self.main_colour = self.game.team_colours[self.colour_id]

        self.selected_colour = self.main_colour

        self.left_clicked = False
        self.right_clicked = False

        # changes with regard to which rect has been last clicked
        self.selected_part = None

        self.top_part = None
        self.top_part_pos = 0
        self.character_parts = []
        

        # cursor assets easier
        self.cursor = None
        self.cursor_half = 25
        self.move_cursor = self.game.assets['move_cursor']
        self.resize_width_cursor = self.game.assets['resize_width_cursor']
        self.resize_height_cursor = self.game.assets['resize_height_cursor']


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
        self.handle_buttons()

        self.update_parts(delta_time, actions)

        if self.selected:
            self.change_state()

    def handle_actions(self, actions):
        '''
        handels actions based on user input
        '''

        if actions["esc"]:
            self.exit_state()

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


    def handle_buttons(self):
        '''
        handels colour change
        '''
        self.change_col_left()

        self.change_col_right()

        if self.create_part:
            self.spawn_part()

    def change_col_left(self):
        '''
        handle left button colour change logic
        wrap around and assignment
        '''
        if self.left_clicked:
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

            self.selected_part.colour = self.selected_colour

    def change_col_right(self):
        '''
        handle right button colour change logic
        wrap around and assignment
        '''
        if self.right_clicked:
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

            self.selected_part.colour = self.selected_colour
                


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
        

        self.created_chars[self.player_id] = self.create_surface_from_created_char()

        if self.players_left > 0:
            # more characters to be created
            new_state = Char_Creating(self.game, self.players_left, self.created_chars)
            
        else:
            # all characters created, go to selecting level
            new_state = Level_Menu(self.game, self.created_chars)
            
        new_state.enter_state()
        # reset the selected state
        self.selected = False

    def render(self, surface):
        '''
        renders background and character customatization
        
        surface: surface to render on
        '''
        surface.fill((self.game.BLACK))

        pygame.draw.rect(surface, self.game.BG_COL, self.bg_char_creating)
        draw_shading_for_rect(self.game.TILE_COL,
            self.bg_char_creating, surface, shading_W=5)

        self.game.draw_text(surface, "Create palikka",
                             self.game.WHITE, self.game.GAME_W / 2,
                               self.game.GAME_H / 8)
        
        # self.game.draw_text(surface, f"Player {self.player_id + 1}",
        #                     self.game.WHITE, self.game.GAME_W * 0.25,
        #                       self.game.GAME_H * 0.25)
        
        
        
        self.render_buttons(surface)
        self.render_parts(surface)
        if self.player_id > 0:
            self.render_created_characters(surface)

        self.render_cursor(surface)

    def render_buttons(self, surface):
        '''
        renders buttons duh and controls what actions get 
        triggered by them
        '''
        # switch colours between presets
        self.left_clicked = self.left_arrow.action_on_button(
            self.left_arrow_x, self.left_arrow_y, 
            surface, self.game.actions)
        
        self.right_clicked = self.right_arrow.action_on_button(
            self.right_arrow_x, self.right_arrow_y,
            surface, self.game.actions)
        
        # done button
        self.selected = self.done_button.action_on_button(
            self.done_button_x, self.done_button_y,
            surface, self.game.actions
        )

        # new part
        self.create_part = self.new_piece_button.action_on_button(
            self.new_piece_button_x, self.new_piece_button_y,
            surface, self.game.actions
        )

        self.game.draw_text(surface,
            'Done', self.game.TILE_COL,
            self.done_text_x,
            self.done_text_y,
            size='Medium'
        ) 

        self.game.draw_text(surface,
            'New piece', self.game.TILE_COL,
            self.new_piece_text_x,
            self.new_piece_text_y,
            size='Medium'
        ) 
        
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

    def render_cursor(self, surface):
        '''
        render custom cursor based on mouse pos
        '''
        print(self.cursor)
        if self.cursor == 'move':
            pygame.mouse.set_visible(False)
            surface.blit(self.move_cursor, self.center_cursor())

        elif self.cursor == 'resize_width':
            pygame.mouse.set_visible(False)
            surface.blit(self.resize_width_cursor, self.center_cursor())


        elif self.cursor == 'resize_height':
            pygame.mouse.set_visible(False)
            surface.blit(self.resize_height_cursor, self.center_cursor())

        else:
            pygame.mouse.set_visible(True)

    def center_cursor(self):

        x, y =  self.game.actions['mouse_pos']
        return (x - self.cursor_half, y - self.cursor_half)    

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

    def load_ui(self):
        '''
        load needed buttons for the view
        '''


        self.left_arrow = Button(0, 0, button_colour=self.game.BG_COL,
                                  hover_colour=self.game.TILE_COL, image = 
                                 self.game.assets["arrowleft_img"])
        self.right_arrow = Button(0, 0, button_colour=self.game.BG_COL,
                                  hover_colour=self.game.TILE_COL, image =
                                  self.game.assets["arrowright_img"])
        
        self.done_button = Button(0, 0, width=100, height=50, button_colour=self.game.BG_COL)

        self.new_piece_button = Button(0, 0, button_colour=self.game.BG_COL,
                                        width=200, height=50)

        # calculate locations for buttons
        # 1 arrow
        self.left_arrow_x = self.game.GAME_W / 6 - self.left_arrow.rect.width / 2
        self.left_arrow_y = self.game.GAME_H / 2 - self.left_arrow.rect.height / 2
        # 2 arrow
        self.right_arrow_x = self.game.GAME_W * 5 / 6 - self.right_arrow.rect.width / 2
        self.right_arrow_y = self.game.GAME_H / 2 - self.right_arrow.rect.height / 2
        # Done
        self.done_button_x = self.game.GAME_W - self.done_button.rect.width - 10
        self.done_button_y = self.game.GAME_H - self.done_button.rect.height - 10

        
        padding = self.new_piece_button.rect.width * 0.5
        self.new_piece_button_x = (self.game.GAME_W - 
            self.new_piece_button.rect.width - padding)
        self.new_piece_button_y = (self.game.GAME_H * 2 / 3 -
            self.new_piece_button.rect.height / 2)
        

        # centered text
        self.done_text_x = self.done_button_x + self.done_button.width / 2
        self.done_text_y = self.done_button_y + self.done_button.height / 2

        self.new_piece_text_x = (self.new_piece_button_x 
            + self.new_piece_button.width / 2)
        self.new_piece_text_y = (self.new_piece_button_y 
            + self.new_piece_button.height / 2)

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
        print(f'x: {x}, y: {y}')
        colour = (209, 31, 4)
        self.spawn_part(x, y, width, height, colour)
        # top part
        width *= 0.5
        y -= height - 4
        x += width * 0.5
        print(f'x: {x}, y: {y}')
        colour = (209, 31, 4)
        self.spawn_part(x, y, width, height, colour)

        # eyes and smile
        # left eye
        y += height * 3
        width = 8
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
                        
    def spawn_part(self, x = None, y = None, W = None, H = None, colour = None, main = False):
        '''
        creates new Part obj and adds it character parts
        '''
        if x is None:
            x = self.new_piece_button_x
        
        if y is None:
            y = self.new_piece_button_y + self.new_piece_button.height * 1.5

        if W is None:   
            W = 50
        if H is None:
            H = 50

        if colour is None:
            colour = self.selected_colour

        

        layer = len(self.character_parts)
        new_part = Part(x, y, W, H, colour, layer, self, main)
        self.character_parts.append(new_part)



