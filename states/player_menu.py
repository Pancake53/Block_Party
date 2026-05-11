import pygame

from states.state import State
from states.char_creating import Char_Creating
from UI.button_stationary import ButtonStationary
from helpers import draw_shading_for_rect

class Player_Menu(State):
    '''
    level menu for player amount
    '''
    def __init__(self, game):
        super().__init__(game)



        # count (int)
        self.player_count = None

        # boolean to seperate button rendering and updates
        self.selected = False

        # list of lists
        # 0: colour, 1: Rect
        self.characters = []
        
        # loads Button classes and rects
        self.load_menu()


    def update(self, delta_time, actions):
        '''
        updates state

        on click: creates and enters game world 
        (or level select menu in future)

        delta_time: dt
        actions: user inputs dictionary
        '''
        for button in self.buttons:
            button.update(actions)

        self.handle_actions(actions)

        if self.selected:
            new_state = Char_Creating(self.game, self.player_count)
            new_state.enter_state()
            # reset the selected state
            self.selected = False

    def handle_actions(self, actions):

        if actions["esc"]:
            self.exit_state()

    def handle_clicks(self, name):

        try:
            name = int(name)
            self.player_count = int(name)
            self.selected = True

        except ValueError:
            match name:
                case _:
                    print('Invalid input')
            

    def render(self, surface):
        '''
        renders background and character amount to choose from
        
        surface: surface to render on
        '''
        surface.fill((self.game.UI_BG_COL))
        self.game.draw_text(surface, "Select Player Count",
                             self.game.TILE_COL, self.game.GAME_W / 2,
                               self.game.GAME_H / 8)
        
        self.render_buttons(surface)
        self.render_characters(surface)
        self.render_text(surface)

    def render_buttons(self, surface):
        '''
        renders buttons and reacts to mouse input
        
        surface: surface to render on
        '''
        for button in self.buttons:
            button.render(surface)


    def render_characters(self, surface):
        '''
        renders "characters"
        
        surface: surface to render on
        '''
        for list in self.characters:
            # list[0] = colour, list[1] = Rect Obj
            pygame.draw.rect(surface, list[0], list[1])

    def render_text(self, surface):
        '''
        renders text "2 players" 
        
        surface: surface to render on
        '''
        pass

    def load_menu(self):
        '''
        loads Buttons and rects for menu
        '''

        # variables for buttons
        
        self.button_W = self.game.GAME_W / 4
        self.button_H = self.game.GAME_H / 2
        self.padding = 20 # px

        # calculations for positions of buttons
        self.y = self.game.GAME_H / 2 - self.button_H / 2
        # if more buttons add to button_W multiplier
        self.x_two = self.game.GAME_W / 2 - self.button_W * 1.5 - self.padding
        self.x_three = self.x_two + self.button_W + self.padding
        self.x_four = self.x_three + self.button_W + self.padding
        # Buttons
        self.buttons = []
        button = ButtonStationary(
                '2',
                self.x_two, self.y,
                button_colour=self.game.BG_COL,
                hover_colour=self.game.GREY,
                width=self.button_W, height=self.button_H,
                on_click=self.handle_clicks)
        
        self.buttons.append(button)
        
        button = ButtonStationary(
                '3',
                self.x_three, self.y,
                button_colour=self.game.BG_COL,
                hover_colour=self.game.GREY,
                width=self.button_W, height=self.button_H,
                on_click=self.handle_clicks)
        
        self.buttons.append(button)


        button = ButtonStationary(
                '4',
                self.x_four, self.y,
                button_colour=self.game.BG_COL,
                hover_colour=self.game.GREY,
                width=self.button_W, height=self.button_H,
                on_click=self.handle_clicks)
        
        self.buttons.append(button)

        # Rects
        colours = self.game.team_colours
        
        # two players
        width = 90
        height = 2 * width
        self.characters.append(
            [colours[0],
              pygame.Rect(self.x_two + 50, self.y + 25, width, height)]
        )
        self.characters.append(
            [colours[1],
              pygame.Rect(self.x_two + 100, self.y + 75, width, height)]
        )

        # three players
        width = 75
        height = 2 * width
        self.characters.append(
            [colours[2],
              pygame.Rect(self.x_three + 30, self.y + 25, width, height)]
        )
        self.characters.append(
            [colours[1],
              pygame.Rect(self.x_three + 80, self.y + 100, width, height)]
        )
        self.characters.append(
            [colours[0],
              pygame.Rect(self.x_three + 130, self.y + 50, width, height)]
        )

        # four players
        width = 69
        height = 2 * width
        self.characters.append(
            [colours[2],
              pygame.Rect(self.x_four + 35, self.y + 110, width, height)]
        )
        self.characters.append(
            [colours[1],
              pygame.Rect(self.x_four + 65, self.y + 50, width, height)]
        )
        self.characters.append(
            [colours[0],
              pygame.Rect(self.x_four + 115, self.y + 100, width, height)]
        )
        self.characters.append(
            [colours[3],
              pygame.Rect(self.x_four + 145, self.y + 25, width, height)]
        )