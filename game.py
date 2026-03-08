import os, pygame, time

from states.title import Title

class Game():
    def __init__(self):
        pygame.init()
        '''
        initialize attributes for game
        '''
        # booleans that handle closing
        self.running, self.playing = True, False

        # window and game canvas
        self.GAME_W, self.GAME_H = 960, 540
        self.WINDOW_W, self.WINDOW_H = 960, 540
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.window = pygame.display.set_mode((self.WINDOW_W, self.WINDOW_H))

        # default
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.FONT_SIZE = 40
        
        # actions dictionary for user input
        self.actions = {"left": False, "right": False, "up": False,
                        "down": False, "mouse_pressed": False, "mouse_click": False, "mouse_pos": (0, 0), "action1": False,
                        "action2": False, "space": False, "start": False}
        

        # set clock and tickrate
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000

        # load assets
        self.assets = {}
        self.load_assets()

        # state management
        self.state_stack = []
        self.load_states()
        
        

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
                    self.running, self.playing = False, False
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

            if event.type == pygame.KEYUP:
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
        
        self.actions["mouse_pos"] = pygame.mouse.get_pos()
        
        

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
        self.window.blit(pygame.transform.scale(self.game_canvas,
                                                 (self.WINDOW_W, self.WINDOW_H)),
                                                   (0, 0))
        pygame.display.flip()

    def get_dt(self):
        '''
        update dt
        '''
        self.dt = self.clock.tick(60) / 1000

    def draw_text(self, surface, text, colour, x, y):
        '''
        helper function for drawing text

        surface: game canvas
        text: written message
        colour: colour of text
        x & y: center coordinates of text rect
        '''
        text_surface = self.font.render(text, True, colour)
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
        self.level_dir = os.path.join("levels")
        self.tilemap_dir = os.path.join("tilemap")
        # Assets themselves
        self.font = pygame.font.Font(os.path.join(self.font_dir, '8-BIT WONDER.TTF'), self.FONT_SIZE)
        self.assets["bomb_img"] = pygame.image.load(os.path.join(self.image_dir, "bomb.png")).convert_alpha()
        self.assets["jump_img"] = pygame.image.load(os.path.join(self.image_dir, "jump.png")).convert_alpha()
        self.assets["flag_img"] = pygame.image.load(os.path.join(self.image_dir, "white_flag.png")).convert_alpha()

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


