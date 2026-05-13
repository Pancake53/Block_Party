import pygame

from states.state import State

from dataclasses import dataclass


@dataclass
class Overlay(State):
    game: object
    width: int = 500
    height: int = 300
    title: str = None
    '''
    overlay class, previous state renders in the background
    '''

    def __post_init__(self):
        '''
        set variables
        '''

        self.cursor = 'default'
        self.prev_state = self.game.state_stack[-1]
        self.exit = False

        # variables
        self.ALPHA = 100

        self.load()




    def update(self, delta_time, actions):
        '''
        updates state
        '''
        self.handle_actions(actions)
        self.child_spesific_update(delta_time, actions)

        if self.exit:
            self.game.state_m.exit_state()

        


    def render(self, surface):

        surface.fill((self.game.GREY))
        surface.blit(self.shaded_bg, self.rect_bg)

        pygame.draw.rect(surface, self.game.UI_BG_COL, self.rect_window)
        pygame.draw.rect(surface, self.game.BG_COL, self.rect_window, width=7)
        if self.title:
            self.game.draw_text(surface, self.title, 
                                self.game.TILE_COL, 
                                self.title_x, self.title_y, 
                                size='H1')
            
        self.child_spesific_render(surface)

    def child_spesific_update(self, dt, actions):
        pass

    def child_spesific_render(self, surface):
        pass


    def handle_actions(self, actions):

        if actions['esc']:
            self.exit = True

        hovered = self.rect_window.collidepoint(actions['mouse_pos'])

        if not hovered:
            if actions['mouse_click']:
                self.exit = True

        self.child_spesific_actions(actions)

    def child_spesific_actions(self, actions):
        pass

    # LOAD

    def load(self):
        '''
        loads coordinates, buttons and sliders
        '''

        self.load_bg()
        self.load_rect()
        if self.title:
            self.load_title()
        self.load_buttons()
        self.load_sliders()
        self.load_else()
    
    def load_bg(self):
        self.shaded_bg = pygame.Surface((self.game.GAME_W, self.game.GAME_H))
        self.prev_state.render(self.shaded_bg)
        self.shaded_bg.set_alpha(self.ALPHA)

        self.rect_bg = pygame.Rect(0, 0, self.game.GAME_W, self.game.GAME_H)


    def load_rect(self):
        '''
        bg rect object
        '''
        rect_x = self.game.GAME_W / 2 - self.width / 2
        rect_y = self.game.GAME_H / 2 - self.height / 2
        self.rect_window = pygame.Rect(rect_x, rect_y, self.width, self.height)

    def load_title(self):
        self.title_x = self.game.GAME_W / 2
        self.title_y = self.rect_window.y + 35

    def load_buttons(self):
        pass

    def load_sliders(self):
        pass

    def load_else(self):
        pass


    # HELPERS

    def add_text(self, str, x, y):
        '''
        helper function for adding text to a list
        '''
        self.texts.append({'str': str, 'x': x, 'y': y}) 