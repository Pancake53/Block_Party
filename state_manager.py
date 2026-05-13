import pygame
from dataclasses import dataclass

from states.title import Title
from states.player_menu import Player_Menu
from states.char_creating import Char_Creating
from states.level_menu import Level_Menu
from states.game_world import Game_World
from states.pause_menu import PauseMenu
from states.settings_menu import SettingsMenu
from states.credits import Credits
from states.load_menu import LoadMenu

# from states. import



@dataclass
class StateManager():
    game: object

    def __post_init__(self):

        self.load_state_manager()


    def load_state_manager(self):
        self.state_stack = []

        self.state_lambdas = {

            'title': lambda: Title(self.game),
            'player_menu': lambda: Player_Menu(self.game),

            'char_creating': lambda 
            player_count = None, created_chars = None: 
            Char_Creating(self.game, player_count, created_chars),

            'level_menu': lambda 
            created_chars = None: Level_Menu(self.game, created_chars),

            'game_world': lambda 
            created_chars = None, level_name = None: 
            Game_World(self.game, level_name, created_chars),

            # overlays

            'pause_menu': lambda: PauseMenu(self.game),
            'settings': lambda bg_surface=None: 
            SettingsMenu(self.game, bg_surface=bg_surface),

            'load_menu': lambda data=None, char_surface_pos=None: 
            LoadMenu(self.game, saved_chars_data=data, 
                    char_surface_pos= char_surface_pos),

            'credits': lambda: Credits(self.game)
        }

    def enter_state(self, next_state, **kwargs):

        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        new_state = self.state_lambdas[next_state](**kwargs)
        self.game.state_stack.append(new_state)
        self.game.reset_keys()



    def exit_state(self, result=None):
        '''
        removes top state

        passes on result of top removed state to the now top state
        '''
        self.prev_state = self.game.state_stack.pop()
        
        if result:
            self.game.state_stack[-1].on_return(result)

        self.game.reset_keys()


