import pygame

from states.state import State
from states.level_menu import Level_Menu
from UI.button import Button
from helpers import draw_shading_for_rect

class Char_Creating(State):
    def __init__(self, game, players_left, created_chars={}):
        self.game = game
        # how many players havent created their characters yet
        self.players_left = players_left - 1
        # all characters created by players so far
        self.created_chars = created_chars

        self.selected = False


    def update(self, delta_time, actions):
        '''
        updates state

        on click: creates and enters game world 
        (or level select menu in future)

        delta_time: dt
        actions: user inputs dictionary
        '''

        self.handle_actions(actions)
        

        if self.selected:
            self.change_state()

    def handle_actions(self, actions):
        '''
        handels actions based on user input
        '''

        if actions["esc"]:
            self.exit_state()
            self.game.reset_keys()

        if actions["mouse_click"]:
            self.selected = True

    def change_state(self):
        '''
        handels what happens after next is selected

        changes state either to next chars creation
        or 
        to select selection screen
        '''
        if self.players_left > 0:
            # more characters to be created
            new_state = Char_Creating(self.game, self.players_left, self.created_chars)
            new_state.enter_state()
            # reset the selected state
            self.selected = False
        else:
            # all characters created, go to selecting level
            self.created_chars = [1, 2, 3] # comment out later
            new_state = Level_Menu(self.game, len(self.created_chars))
            new_state.enter_state()
            # reset the selected state
            self.selected = False


    def render(self, surface):
        '''
        renders background and character customatization
        
        surface: surface to render on
        '''
        surface.fill((self.game.BLACK))
        self.game.draw_text(surface, "Create your character",
                             self.game.WHITE, self.game.GAME_W / 2,
                               self.game.GAME_H / 8)
        
        self.game.draw_text(surface, f"Player: {self.players_left}",
                             self.game.WHITE, self.game.GAME_W / 2,
                               self.game.GAME_H / 2)
        