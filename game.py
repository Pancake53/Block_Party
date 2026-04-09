import os, pygame

from states.title import Title
from settings import Settings

class Game():
    def __init__(self):
        pygame.init()
        '''
        initialize attributes for game
        '''
        # booleans that handle closing
        self.running, self.playing = True, False

        # create needed classes
        self.settings = Settings()

        # window and game canvas
        self.GAME_W, self.GAME_H = 960, 540
        self.WINDOW_W, self.WINDOW_H = 960, 540
        self.SCREEN_H, self.SCREEN_W = 0, 0 # updates on fullscreen toggle

        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.window = pygame.display.set_mode((self.WINDOW_W, self.WINDOW_H))
        self.is_fullscreen = False

        # scaling
        self.scale_multiplier_x = self.GAME_W / self.WINDOW_W
        self.scale_multiplier_y = self.GAME_H / self.WINDOW_H

        # default
        self.BG_COL = (0, 153, 136)
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.FONT_TITLE = 40
        self.FONT_MEDIUM = 15
        self.FONT_SMALL = 8

        self.team_colours = [
        
            (204, 121, 167), # Purple
            (34, 136, 51), # Forest green
            (68, 119, 170), # Dark blue
            (255, 242, 89), # Yellow
            (0, 0, 61), # Gray
            (230, 159, 0), # Orange
            (213, 94, 0), # Dark orange
            (204, 51, 17) # Vibrant red
        ] 
        
        # actions dictionary for user input
        self.actions = {"left": False, "right": False, "up": False,
                        "down": False, "mouse_pressed": False, 
                        "mouse_click": False, "mouse_pos": (0, 0), 
                        "action1": False, "action2": False,
                        "space": False, "start": False, 
                        'esc': False}
        

        # set clock and tickrate
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000

        # music 
        pygame.mixer.init()
        self.audio = {}

        # load assets
        self.assets = {}
        self.load_assets()

        # state management
        self.state_stack = []
        self.load_states()

        self.play_music('main_theme')
        self.change_volume()
        
        

    def game_loop(self):
        '''
        main game loop
        '''
        while self.playing:
            self.get_dt() # update dt
            self.check_events() # update actions dictionart
            self.update() # update calculated values
            self.render() # draw on canvas


    def check_events(self):
        '''
        update actions dictionary based on user input
        '''
        # reset
        self.actions["mouse_click"] = False
        
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.actions['esc'] = True
                if event.key == pygame.K_a:
                    self.actions["left"] = True
                if event.key == pygame.K_d:
                    self.actions["right"] = True
                if event.key == pygame.K_w:
                    self.actions["up"] = True
                if event.key == pygame.K_s:
                    self.actions["down"] = True
                if event.key == pygame.K_1:
                    self.actions["action1"] = True
                if event.key == pygame.K_RETURN:
                    self.actions["start"] = True
                if event.key == pygame.K_2:
                    self.actions["action2"] = True
                if event.key == pygame.K_SPACE:
                    self.actions["space"] = True
                # Fullscreen
                if event.key == pygame.K_f:
                    self.toggle_fullscreen()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.actions['esc'] = False
                if event.key == pygame.K_a:
                    self.actions["left"] = False
                if event.key == pygame.K_d:
                    self.actions["right"] = False
                if event.key == pygame.K_w:
                    self.actions["up"] = False
                if event.key == pygame.K_s:
                    self.actions["down"] = True
                if event.key == pygame.K_1:
                    self.actions["action1"] = False
                if event.key == pygame.K_RETURN:
                    self.actions["start"] = False
                if event.key == pygame.K_2:
                    self.actions["action2"] = False
                if event.key == pygame.K_SPACE:
                    self.actions["space"] = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print("mousebuttonDOWN")
                self.actions["mouse_pressed"] = True
                # print(f"mouse_click: {self.actions["mouse_click"]}")

            # else: # if we have no (down or up) mouse action then click = false 
            #     self.actions["mouse_click"] = False    
            #     print("NOT mousebuttondown")
            #     print(f"mouse_click: {self.actions["mouse_click"]}")

            if event.type == pygame.MOUSEBUTTONUP:
                # print("mousebuttonUP")
                self.actions["mouse_pressed"] = False
                
        # print(f"mouse_click: {self.actions["mouse_click"]}") 

        if pygame.mouse.get_just_pressed()[0]:
            # for clicking only interaction
            self.actions["mouse_click"] = True   
        
        unscaled_mouse_pos = pygame.mouse.get_pos()
        self.actions["mouse_pos"] = (unscaled_mouse_pos[0] * self.scale_multiplier_x,
                                      unscaled_mouse_pos[1] * self.scale_multiplier_y)
        

    def update(self):
        '''
        calls the update function from the top of the stack
        '''
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        '''
        calls the render function from the top of the stack
        supports scaling (not in use rn)
        draws the canvas on users screen
        '''
        self.state_stack[-1].render(self.game_canvas)
        if self.is_fullscreen:
            self.window.blit(pygame.transform.scale(self.game_canvas,
                                                 (self.SCREEN_W, self.SCREEN_H)),
                                                   (0, 0))
        else:
            self.window.blit(pygame.transform.scale(self.game_canvas,
                                                 (self.WINDOW_W, self.WINDOW_H)),
                                                   (0, 0))
        pygame.display.flip()

    def get_dt(self):
        '''
        update dt
        '''
        self.dt = self.clock.tick(60) / 1000

    def draw_text(self, surface, text, colour, x, y, size="Title"):
        '''
        helper function for drawing text

        surface: game canvas
        text: written message
        colour: colour of text
        x & y: center coordinates of text rect
        size: Title, Medium or Small
        '''
        match size:
            case "Title":
                text_surface = self.font_title.render(text,
                                                True, colour)
            case "Medium":
                text_surface = self.font_medium.render(text,
                                                True, colour)
            case "Small":
                text_surface = self.font_small.render(text,
                                                True, colour)
            case _:
                text_surface = self.font_medium.render(text,
                                                True, colour)
                print(f"Draw text input error, size: {size} is not in Title, Medium, Small")
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def load_assets(self):
        '''
        loads games assets
        '''
        # Pointers for assets
        self.assets_dir = os.path.join("assets")
        self.image_dir = os.path.join(self.assets_dir, "images")
        self.font_dir = os.path.join(self.assets_dir, "font")
        self.audio_dir = os.path.join(self.assets_dir, "audio")
        self.level_dir = os.path.join("levels")
        # self.tilemap_dir = os.path.join("tilemap") NOT IN USE
        # Assets themselves
        # fonts
        self.font_title = pygame.font.Font(os.path.join(self.font_dir, '8-BIT WONDER.TTF'), self.FONT_TITLE)
        self.font_medium = pygame.font.Font(os.path.join(self.font_dir, '8-BIT WONDER.TTF'), self.FONT_MEDIUM)
        self.font_small = pygame.font.Font(os.path.join(self.font_dir, '8-BIT WONDER.TTF'), self.FONT_SMALL)
        # assets
        self.assets["explosion_img"] = pygame.image.load(os.path.join(self.image_dir, "explosion.png")).convert_alpha()
        # ui
        self.assets["bomb_img"] = pygame.image.load(os.path.join(self.image_dir, "bomb.png")).convert_alpha()
        self.assets["jump_img"] = pygame.image.load(os.path.join(self.image_dir, "jump.png")).convert_alpha()
        self.assets["flag_img"] = pygame.image.load(os.path.join(self.image_dir, "white_flag.png")).convert_alpha()
        
        self.assets["arrowleft_img"] = pygame.image.load(os.path.join(self.image_dir, "arrowleft.png")).convert_alpha()
        self.assets["arrowright_img"] = pygame.image.load(os.path.join(self.image_dir, "arrowright.png")).convert_alpha()

        # audio
        self.audio['main_theme'] = os.path.join(self.audio_dir, 'main_music.ogg')

    def reset_keys(self):
        '''
        helper function for resetting actions dictionary
        '''
        for action in self.actions:
            if action != "mouse_pos":
                self.actions[action] = False

    def load_states(self):
        '''
        creates an instance of first state and appends it to state stack
        '''
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def toggle_fullscreen(self):
    
        '''
        need I explain this
        updates fullscreen values
        '''
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.SCREEN_H = self.window.get_height()   
            self.SCREEN_W = self.window.get_width()
            # scaling for new H and W
            self.scale_multiplier_x = self.GAME_W / self.SCREEN_W
            self.scale_multiplier_y = self.GAME_H / self.SCREEN_H

        else:
            self.window = pygame.display.set_mode((self.WINDOW_W, self.WINDOW_H))
            # scaling for new H and W
            self.scale_multiplier_x = self.GAME_W / self.WINDOW_W
            self.scale_multiplier_y = self.GAME_H / self.WINDOW_H


    def play_music(self, audio_name, loops=-1):
        '''
        plays audio if audio exists in files

        audio_name: filename of played audio
        loops: looping mechanism (-1 = forever, 0 = once)
        '''
        if audio_name in self.audio:
            pygame.mixer.music.load(self.audio[audio_name])
            pygame.mixer.music.play(loops)

    def change_volume(self):
        '''
        volume of audio
        '''
        pygame.mixer.music.set_volume(self.settings.music_vol * self.settings.master_volume)

