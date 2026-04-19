import pygame

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


        self.left_clicked = False
        self.right_clicked = False

        # changes with regard to which rect has been last clicked
        self.selected_part = 0 # TO-DO


        


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
        
        self.handle_col_change()
        

        if self.selected:
            self.change_state()

    def handle_col_change(self):
        '''
        handels colour change
        '''
        self.change_col_left()

        self.change_col_right()


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

            self.main_colour = self.game.team_colours[self.colour_id]
            while self.main_colour in self.taken_colours:
                if self.colour_id == 0:
                    self.colour_id = len(self.game.team_colours) - 1
                else:
                    self.colour_id -= 1
                self.main_colour = self.game.team_colours[self.colour_id]

            self.character_parts[self.selected_part]['colour'] = self.main_colour


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

            self.main_colour = self.game.team_colours[self.colour_id]
            while self.main_colour in self.taken_colours:
                if self.colour_id == len(self.game.team_colours) - 1:
                    self.colour_id = 0
                else:
                    self.colour_id += 1
                self.main_colour = self.game.team_colours[self.colour_id]
            self.character_parts[self.selected_part]['colour'] = self.main_colour


    def handle_actions(self, actions):
        '''
        handels actions based on user input
        '''

        if actions["esc"]:
            self.exit_state()

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
        self.render_character(surface)
        if self.player_id > 0:
            self.render_created_characters(surface)

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

        self.game.draw_text(surface,
            'Done', self.game.TILE_COL,
            self.done_text_x,
            self.done_text_y,
            size='Medium'
        ) 
        
    def render_character(self, surface):
        '''
        renders the rects of character
        '''
        for part in self.character_parts:

            pygame.draw.rect(surface, part['colour'], part['rect'])

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
        '''
        # new dict for created characters
        new_dict = {}
        main_colour = next(
            part['colour']
            for part in self.character_parts 
            if part['main']
        )

        # create new surface and 
        char_surface = pygame.Surface(
            (self.char_surface_W, self.char_surface_H),
            pygame.SRCALPHA) # transparent

        # render each part onto character surface
        for part in self.character_parts:
            self.scale_part(part, char_surface)

        # update and return new dict
        new_dict['main_colour'] = main_colour
        new_dict['char_surface'] = char_surface
        return new_dict
    
    # BUG TEST THIS
    def scale_part(self, part, char_surface):
        '''
        rescales a single part and draws it on surface
        '''
        colour = part['colour']
        rect = part['rect']

        # coordinates
        # BUG TEST THIS SHIT
        x = ( rect.x + rect.width / 2 - self.bg_char_creating.x ) / self.scalar
        y = ( rect.y + rect.height / 2 - self.bg_char_creating.y ) / self.scalar

        # dimensions
        rect.width /= self.scalar
        rect.height /= self.scalar

        # reposition
        rect.x = x - rect.width / 2
        rect.y = y - rect.height / 2

        pygame.draw.rect(char_surface, colour, rect)
            
    def load(self):
        '''
        init needed classes and coordination calculations
        '''
        # background, area to create char in 
        W = self.game.GAME_W / 4
        H = W * 16 / 9
        self.bg_char_creating = pygame.Rect(W / 1.5, 
                                    self.game.GAME_H / 2 - H / 2,
                                    W, H)


        self.load_buttons()
        
        self.load_hitbox()
        
        self.load_created_characters()

    def load_buttons(self):
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

        self.done_text_x = self.done_button_x + self.done_button.width / 2
        self.done_text_y = self.done_button_y + self.done_button.height / 2

    def load_hitbox(self):
        '''
        loads initial box into view
        '''
        # surface / character size
        self.surface_multip = 5
        self.char_surface_H = 16 * self.surface_multip
        self.char_surface_W = 9 * self.surface_multip

        # scale of big view char to the real char in game
        self.scalar = self.bg_char_creating.height / self.char_surface_H
        # starting colour, position and dimensions, hitbox
        width = self.game.CHARACTER_SIZE * self.scalar
        height = width * 2
        print(f'Scalar: {self.scalar}, width: {width}')
        x = self.bg_char_creating.x + self.bg_char_creating.width / 2 - width / 2
        y = self.bg_char_creating.y + self.bg_char_creating.height - height
        rect = pygame.Rect(x, y, width, height)
        self.character_parts = [{'main': True, 'colour': self.main_colour, 'rect': rect}]

        # second rect for testing !!!
        self.add_hat(x, y, width, height)
        
    def add_hat(self, x, y, width, height):
        # hat :D
        # bottom part
        width *= 1.5
        height *= 0.2
        y -= height 
        x -= width / 1.5 * 0.25
        print(f'x: {x}, y: {y}')
        colour = (209, 31, 4)
        self.character_parts.append({
            'main': False,
            'colour': colour,
            'rect': pygame.Rect(x, y, width, height)
        })
        # top part
        width *= 0.5
        y -= height 
        x += width * 0.5
        print(f'x: {x}, y: {y}')
        colour = (209, 31, 4)
        self.character_parts.append({
            'main': False,
            'colour': colour,
            'rect': pygame.Rect(x, y, width, height)
        })

        # eyes and smile
        # left eye
        y += height * 3
        width = 6
        height = width
        colour = self.game.BLACK
        self.character_parts.append({
            'main': False,
            'colour': colour,
            'rect': pygame.Rect(x, y, width, height)
        })
        # right eye
        x += width * 3
        self.character_parts.append({
            'main': False,
            'colour': colour,
            'rect': pygame.Rect(x, y, width, height)
        })
        # smile
        x -= width * 3
        y += width * 3
        width *= 5
        self.character_parts.append({
            'main': False,
            'colour': colour,
            'rect': pygame.Rect(x, y, width, height)
        })

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
            x = self.char_surface_W

            for id, dict in self.created_chars.items():
                y = self.char_surface_H * 1.5 * (1 + id)
                self.created_characters_for_render.append(
                    {'x': x,
                    'y': y,
                    'char_surface' : dict['char_surface'],
                    'rect': pygame.Rect(x, y, 
                    dict['char_surface'].width,
                    dict['char_surface'].height)
                    }
                )     
                        


