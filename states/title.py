import pygame
import random

from states.state import State
from states.player_menu import Player_Menu
from settings import Settings
from UI.bouncing_rect import BouncingRect

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
        self.max_rects = 12
        self.directions = [-3, 3]
        self.max_added = False
    
        self.rects = []

        

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

        if actions["m1"]:
            new_state = Player_Menu(self.game)
            new_state.enter_state()

        if actions["esc"]:
            self.game.playing = False
            self.game.running = False

    def load_rect(self):
        '''
        spawns a new rect on title screen
        '''
        # langerly randomized spawn location
        rect = (self.game.GAME_W / 2 + random.randint(  # x spawn
            round(-self.game.GAME_W / 4), round(self.game.GAME_W / 4)), 
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
        surface.fill((self.game.BLACK))
        for rect in self.rects:
            rect.render(surface)
        self.game.draw_text(surface, "Block Party",
                             self.game.WHITE, self.game.GAME_W / 2,
                               self.game.GAME_H / 2)
        
        