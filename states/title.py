import pygame
import random

from states.state import State
from states.player_menu import Player_Menu
from settings import Settings
from UI.bouncing_rect import BouncingRect
from UI.button import Button
from helpers import draw_shading_for_rect

class Title(State):
    '''
    title screen
    '''
    def __init__(self, game):
        super().__init__(game)

        # for animations
        self.start_time = pygame.time.get_ticks()
        self.interval = 3000
        self.last_add = self.start_time
        self.max_rects = 15
        self.directions = [-2, 2]
        self.max_added = False
    
        self.rects = []
        self.play = False
        self.quit = False

        self.load()

        

    def update(self, delta_time, actions):
        '''
        updates state

        on start: creates and enters game world 
        (or level select menu in future)

        delta_time: dt
        actions: user inputs dictionary
        '''

        self.add_rects()

        for rect in self.rects:
            rect.update()

        if self.play:
            new_state = Player_Menu(self.game)
            new_state.enter_state()

        if actions["esc"] or self.quit:
            self.game.playing = False
            self.game.running = False

    def load_rect(self):
        '''
        spawns a new rect on title screen
        '''
        # langerly randomized spawn location
        rect = (self.game.GAME_W * 5 / 6 + random.randint(  # x spawn
            round(-self.game.GAME_W / 6), round(self.game.GAME_W / 6)), 
        self.game.GAME_H / 2 + random.randint(  # y spawn
            round(-self.game.GAME_H / 4), round(self.game.GAME_H / 4)), 
        48, 92, # width and height
        random.choice(self.directions), # x momentum
        random.choice(self.directions),  # y momentum
        self.game.GAME_W,
        self.game.GAME_H,
        self.game.team_colours
        )

        rect = BouncingRect(*rect)
        self.rects.append(rect)

    def add_rects(self):
        '''
        add animations based on time passed
        '''
        elapsed = pygame.time.get_ticks() - self.start_time
        since_last_add = elapsed - self.last_add

        # add rects
        if not self.max_added:
            if since_last_add > self.interval:
                self.load_rect()
                self.last_add = elapsed
                # print(f"rect added, time since last rect: {since_last_add}")
                if len(self.rects) == self.max_rects:
                    self.max_added = True


    def render(self, surface):
        '''
        renders background and title on the screen
        
        surface: surface to render on
        '''
        surface.fill((self.game.WHITE))
        pygame.draw.rect(surface, self.game.UI_BG_COL, self.menu_bg)
        # pygame.draw.rect(surface, self.game.GREY, self.div_rect)
        draw_shading_for_rect(self.game.BLACK, self.bouncing_bg, surface, shading_W=7)
        pygame.draw.rect(surface, self.game.GREY, self.div_rect)

        
        for rect in self.rects:
            rect.render(surface)

        # title
        pygame.draw.rect(surface, self.game.BG_COL, self.title_rect)
        draw_shading_for_rect(self.game.WHITE, self.title_rect,
                            surface, right_color=self.game.BLACK)
        
        
        self.render_buttons(surface)
        self.render_text(surface)
        
    def render_buttons(self, surface):
        '''
        renders buttons
        '''
        self.play = self.btn_play.action_on_button(
            self.btn_play.x, self.btn_play.y,
            surface, self.game.actions
        )

        self.quit = self.btn_quit.action_on_button(
            self.btn_quit.x, self.btn_quit.y,
            surface, self.game.actions
        )



    def render_text(self, surface):
        self.game.draw_text(surface, "Perkeleen\npalikka peli",
            self.game.TILE_COL, self.title_x,
            self.title_y
        )
        
        self.game.draw_text(surface, "Play",
            self.game.TILE_COL, self.play_text_x,
            self.play_text_y, size="Medium"            
        )
        
        self.game.draw_text(surface, "Quit",
            self.game.TILE_COL, self.quit_text_x,
            self.quit_text_y, size="Medium"
        )       



    def load(self):
        '''
        loads buttons and inits rects at init
        '''
        # titles center coordinates
        self.title_x = self.game.GAME_W * 4 / 16
        self.title_y = self.game.GAME_H / 3
        self.lines = []

        # lighter bg

        w = self.game.GAME_W * 2 / 3 - self.game.GAME_W / 32
        h = self.game.GAME_H
        x = 0
        y = 0
        self.menu_bg = pygame.Rect(x, y, w, h)

        # divider bg
        
        x = w
        w = self.game.GAME_W / 32
        
        
        self.div_rect = pygame.Rect(x, y, w, h)
        
        # bouncing bg
        x = self.div_rect.x + self.div_rect.width
        w = self.game.GAME_W - self.div_rect.width - self.menu_bg.width
        y = 0
        h = self.game.GAME_H
        self.bouncing_bg = pygame.Rect(x, y, w, h)

        
        # title bg

        w = self.game.GAME_W * 2 / 3 - self.game.GAME_W / 16
        h = self.game.GAME_H / 6 + 10
        x = - 2
        y = self.game.GAME_H / 4
        self.title_rect = pygame.Rect(x, y, w, h)

       



        # buttons

        self.load_buttons()

    def load_buttons(self):
        '''
        loads buttons
        '''
        # play btn
        w = 120
        h = w/2

        x = 25
        y = self.game.GAME_H / 2

        self.btn_play = Button(x, y,
            button_colour=self.game.BG_COL, width=w, height=h)
        # text
        self.play_text_x = self.btn_play.x + self.btn_play.width / 2
        self.play_text_y = self.btn_play.y + self.btn_play.height / 2

        # quit
        y += h * 1.5
        self.btn_quit = Button(x, y,
            button_colour=self.game.BG_COL, width=w, height=h)
        # text
        self.quit_text_x = self.btn_quit.x + self.btn_quit.width / 2
        self.quit_text_y = self.btn_quit.y + self.btn_quit.height / 2
