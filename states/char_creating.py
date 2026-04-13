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
        # value is list of character parts, which 
        # contain a dict for colour and rect obj
        
        # selecting players id
        if created_chars:
            self.created_chars = created_chars
            self.player_id = len(self.created_chars)
            self.taken_colours = [part['colour']
                                for character_parts in created_chars.values()
                                for part in character_parts 
                                if part['main']
                                ]
        else:
            self.player_id = 0
            self.created_chars = {}
            self.taken_colours = []

        self.selected = False

        # set startoff colour
        self.colour_id = 0
        self.main_colour = self.game.team_colours[self.colour_id]
        while self.main_colour in self.taken_colours:
            self.colour_id += 1
            self.main_colour = self.game.team_colours[self.colour_id]

        self.load_classes() # Buttons / UI elements 

        self.left_clicked = False
        self.right_clicked = False

        # changes with regard to which rect has been last clicked
        self.selected_part = 0 # TO-DO

        


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
            self.game.reset_keys()


    def change_state(self):
        '''
        handels what happens after next is selected

        changes state either to next chars creation
        or 
        to select selection screen
        '''
        self.created_chars[self.player_id] = self.character_parts

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

        pygame.draw.rect(surface, self.game.BG_COL, self.level_bg)

        self.game.draw_text(surface, "Create your character",
                             self.game.WHITE, self.game.GAME_W / 2,
                               self.game.GAME_H / 8)
        
        self.game.draw_text(surface, f"Player {self.player_id + 1}",
                             self.game.WHITE, self.game.GAME_W * 0.25,
                               self.game.GAME_H * 0.25)
        
        
        
        self.render_buttons(surface)
        self.render_character(surface)

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
        
        
    def render_character(self, surface):
        '''
        renders the rects of character
        '''
        for part in self.character_parts:
            pygame.draw.rect(surface, part['colour'], part['rect'])

    def load_classes(self):
        '''
        init needed classes and coordination calculations
        '''
        self.level_bg = pygame.Rect(self.game.GAME_W / 4, self.game.GAME_H / 4,
                                                  self.game.GAME_W / 2, self.game.GAME_H / 2)

        self.left_arrow = Button(0, 0, button_colour=(139, 139, 139),
                                  hover_colour=(50, 50, 50), image = 
                                 self.game.assets["arrowleft_img"])
        self.right_arrow = Button(0, 0, button_colour=(139, 139, 139),
                                  hover_colour=(50, 50, 50), image =
                                  self.game.assets["arrowright_img"])
        
        self.done_button = Button(0, 0, width=100, height=50)
        
        # starting colour, position and dimensions
        width = 50
        height = width * 2
        x = self.game.GAME_W / 2 - width / 2
        y = self.game.GAME_H / 2 - height / 2
        rect = pygame.Rect(x, y, width, height)
        self.character_parts = [{'main': True, 'colour': self.main_colour, 'rect': rect}]
        
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

        self.done_text_x = self.game.GAME_W - self.done_button.rect.width - 10
        self.done_text_y = self.game.GAME_H - self.done_button.rect.width - 10
