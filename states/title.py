import pygame
import random

from states.state import State
from states.credits import Credits
from states.player_menu import Player_Menu
from states.settings_menu import SettingsMenu
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
        self.show_credits = False

        self.load()
        self.load_rect()

        

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

        if self.show_credits:
            new_state = Credits(self.game, 500, 300, 'credits')
            new_state.enter_state()


        if actions["esc"] or self.quit:
            self.game.playing = False
            self.game.running = False

        if actions['start']:
            new_state = SettingsMenu(self.game, 500, 300, 'settings')
            new_state.enter_state()

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
        pygame.draw.rect(surface, self.game.LIGHT_GREY, self.bouncing_bg)
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
        self.render_images(surface)
        
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

        self.show_credits = self.btn_credits.action_on_button(
            self.btn_credits.x, self.btn_credits.y,
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

        self.game.draw_text(surface, "Credits",
            self.game.TILE_COL, self.credits_text_x,
            self.credits_text_y, size="Medium"
        )       
       
    def render_images(self, surface):

        surface.blit(self.credit_img, self.credit_rect)
        surface.blit(self.flag_img, self.flag_rect)
        surface.blit(self.bomb_img, self.bomb_rect)
        surface.blit(self.bomb_img, self.bomb_rect2)
        surface.blit(self.bomb_img, self.bomb_rect3)


    def load(self):
        '''
        loads buttons and inits rects at init
        '''
        self.load_bg()

        self.load_buttons()

        self.load_images()

    def load_bg(self):

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
        h = self.game.GAME_H / 6 + 15
        x = - 2
        y = self.game.GAME_H / 4 - 5
        self.title_rect = pygame.Rect(x, y, w, h)


    def load_buttons(self):
        '''
        loads buttons
        '''
        # play btn
        w = 400
        h = 60

        x = 25
        y = self.game.GAME_H / 2

        self.btn_play = Button(x, y,
            button_colour=self.game.BG_COL, width=w, height=h)
        # text
        self.play_text_x = self.btn_play.x + self.btn_play.width / 4 - 30
        self.play_text_y = self.btn_play.y + self.btn_play.height / 2

        # quit
        y += h * 1.5
        self.btn_quit = Button(x, y,
            button_colour=self.game.BG_COL, width=w, height=h)
        # text
        self.quit_text_x = self.btn_quit.x + self.btn_quit.width / 4 - 36
        self.quit_text_y = self.btn_quit.y + self.btn_quit.height / 2

        # credits
        y += h * 1.5
        self.btn_credits = Button(x, y,
            button_colour=self.game.BG_COL, width=w, height=h)
        # text
        self.credits_text_x = self.btn_credits.x + self.btn_credits.width / 3 - 34
        self.credits_text_y = self.btn_credits.y + self.btn_credits.height / 2

    def load_images(self):
        '''
        images and their coordinates
        '''
        x_offset = 180
        y_offset = self.btn_play.height * -1
        scale_factor = 2

        # play
        img = self.game.assets['bomb_img']
        w, h = img.get_size()
        self.bomb_img = pygame.transform.scale(img,
                (w * scale_factor, h * scale_factor))

        self.bomb_rect = self.bomb_img.get_rect()

        self.bomb_rect.x = self.play_text_x + x_offset
        self.bomb_rect.y = self.play_text_y + y_offset

        self.bomb_rect2 = self.bomb_rect.copy()
        self.bomb_rect2.x -= self.bomb_rect2.width / 3 + 10
        self.bomb_rect2.y += self.bomb_rect2.height / 3 

        self.bomb_rect3 = self.bomb_rect.copy()
        self.bomb_rect3.x += self.bomb_rect2.width / 2
        self.bomb_rect3.y += self.bomb_rect2.height / 3 + 5



        # quit
        scale_factor = 3
        img = self.game.assets["flag_img"]
        w, h = img.get_size()
        self.flag_img = pygame.transform.scale(img,
                (w * scale_factor, h * scale_factor))
        
        self.flag_rect = self.flag_img.get_rect()

        self.flag_rect.x = self.quit_text_x + x_offset
        self.flag_rect.y = self.quit_text_y + y_offset

        # credits
        self.credit_img = self.game.assets['credits_img']
        self.credit_rect = self.credit_img.get_rect()

        self.credit_rect.x = self.credits_text_x + x_offset
        self.credit_rect.y = self.credits_text_y + y_offset