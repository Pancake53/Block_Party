import json, os, pygame
from pygame import Vector2

from settings import Settings
from audio_manager import AudioManager
from state_manager import StateManager


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
        self.SCREEN_W, self.SCREEN_H = self.WINDOW_W, self.WINDOW_H # updates on fullscreen toggle

        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.window = pygame.display.set_mode((self.WINDOW_W, self.WINDOW_H))
        self.is_fullscreen = False

        # scaling
        self.scale_multiplier_x = self.GAME_W / self.WINDOW_W
        self.scale_multiplier_y = self.GAME_H / self.WINDOW_H

        # colours
        self.UI_BG_COL = (41, 186, 162) # brighter
        self.BG_COL = (0, 153, 136)
        self.TILE_COL = (181, 67, 0)
        self.BLACK, self.WHITE, self.GREY = (0, 0, 0), (255, 255, 255), (139, 139, 139)
        self.LIGHT_GREY = (200, 200, 200)
        self.RED = (255, 0, 0)
        # fonts
        self.TEXT_COL = (181, 67, 0)
        self.FONT_TITLE = 40
        self.FONT_H1 = 32
        self.FONT_MEDIUM = 24
        self.FONT_SMALL = 16
        self.FONT_TINY = 8

        # surface / character size
        self.CHARACTER_SIZE = 24                
        self.surface_multip = 5
        self.char_surface_H = 16 * self.surface_multip
        self.char_surface_W = 8 * self.surface_multip

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
                        "down": False, "m1": False, "m3": False,
                        "mouse_click": False, "mouse_pos": (0, 0), 
                        "action1": False, "action2": False,
                        "space": False, "start": False, 
                        'esc': False}
        

        # set clock and tickrate
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000



        # load assets
        self.assets = {}
        self.load_assets()

        
        self.load_controller()

        self.audio = AudioManager(self.settings, self.audio_dir, self.sound_fx_dir)


        # cursors
        self.cursor_half = 25
        self.cursor = None
        self.cursor_pos = list(pygame.mouse.get_pos())
        self.last_input = 'mouse'

        # SHARED DATA BETWEEN CLASSES

        self.players = None
        self.chars_created = None

        # state management
        self.state_stack = []
        self.load_states()

        print('\n\n ---- NEW GAME ---- \n\n')




        
        

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
        self.actions['m3_click'] = False
        
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
                # Toggle audio
                if event.key == pygame.K_m:
                    self.audio.toggle_mute()

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

            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print("mousebuttonDOWN")
                self.last_input = 'mouse'
                if event.button == 1:
                    self.actions["mouse_click"] = True 
                    self.actions["m1"] = True
                if event.button == 3:
                    self.actions['m3_click'] = True
                    self.actions["m3"] = True

            if event.type == pygame.MOUSEBUTTONUP:
                # print("mousebuttonUP")
                if event.button == 1:
                    self.actions["m1"] = False
                if event.button == 3:
                    self.actions["m3"] = False

            if event.type == pygame.MOUSEMOTION:
                # if actual mouse input, catch controller logic
                if self.last_input == 'mouse':
                    self.cursor_pos = list(event.pos)
                    # print(f"Updating with MUUSE: {self.cursor_pos}")

        # CONTROLLER  

            if event.type == pygame.JOYDEVICEADDED:
                self.load_controller()

            if self.joysticks:
                self.check_controller_events(event)
       
        # OUTSIDE OF EVENT LOOP   
        # UPDATE MOUSE POS BASED ON ANALOG INPUT
        if self.last_input == 'controller':
            self.update_mouse_pos(self.dt) 
        self.actions["mouse_pos"] = (self.cursor_pos[0] * self.scale_multiplier_x,
                                      self.cursor_pos[1] * self.scale_multiplier_y)
    
        
    def check_controller_events(self, event):
        '''
        handels controller input

        event: pygame event object
        '''
        # BUTTONS

        if event.type == pygame.JOYBUTTONDOWN:
            print(f'event button: {event.button}')
            self.last_input = 'controller'

            if event.button == self.button_keys['a']:
                self.actions['mouse_click'] = True
                self.actions['m1'] = True
            if event.button == self.button_keys['RB']:
                self.actions['m3_click'] = True
                self.actions['m3'] = True

            if event.button == self.button_keys['options']:
                self.actions['esc'] = True

        if event.type == pygame.JOYBUTTONUP:
            print(f'event button up: {event.button}')  

            if event.button == self.button_keys['a']:
                self.actions['m1'] = False
            if event.button == self.button_keys['RB']:
                self.actions['m3'] = False

            if event.button == self.button_keys['options']:
                self.actions['esc'] = False

        # ANALOG INPUTS

        if event.type == pygame.JOYAXISMOTION:
            self.last_input = 'controller'
            self.analog_keys[event.axis] = event.value


    def update(self):
        '''
        calls the update function from the top of the stack
        '''
        self.cursor = None

        self.state_stack[-1].update(self.dt, self.actions)

        if self.actions['mouse_click']:
            self.audio.play_sfx('menu_click')

        if self.cursor is None:
            if self.actions['mouse_click']:
                self.cursor = 'click'


    def render(self):
        '''
        calls the render function from the top of the stack
        supports scaling (not in use rn)
        draws the canvas on users screen
        '''
        self.state_stack[-1].render(self.game_canvas)
        # render cursor
        if self.cursor:
            self.render_cursor(self.game_canvas, cursor_input=self.cursor)
        else:
            self.render_cursor(self.game_canvas)

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


    def load_assets(self):
        '''
        loads games assets
        '''

        
        # Pointers for assets
        self.assets_dir = os.path.join("assets")
        self.image_dir = os.path.join(self.assets_dir, "images")
        self.font_dir = os.path.join(self.assets_dir, "font")
        self.audio_dir = os.path.join(self.assets_dir, "audio")
        self.sound_fx_dir = os.path.join(self.audio_dir, "sound_fx")
        self.level_dir = os.path.join("levels")
        self.cursor_dir = os.path.join(self.image_dir, "cursors")
        # self.tilemap_dir = os.path.join("tilemap") NOT IN USE
        # Assets themselves
        # fonts
        self.font_title = pygame.font.Font(os.path.join(self.font_dir, '8-BIT WONDER.TTF'), self.FONT_TITLE)
        self.font_h1 = pygame.font.Font(os.path.join(self.font_dir, '8-BIT WONDER.TTF'), self.FONT_H1)
        self.font_medium = pygame.font.Font(os.path.join(self.font_dir, '8-BIT WONDER.TTF'), self.FONT_MEDIUM)
        self.font_small = pygame.font.Font(os.path.join(self.font_dir, '8-BIT WONDER.TTF'), self.FONT_SMALL)
        self.font_tiny = pygame.font.Font(os.path.join(self.font_dir, '8-BIT WONDER.TTF'), self.FONT_TINY)
        # in game graphics
        self.assets["explosion_img"] = pygame.image.load(os.path.join(self.image_dir, "explosion.png")).convert_alpha()
        self.assets["wave_img"] = pygame.image.load(os.path.join(self.image_dir, "wave.png")).convert_alpha()
        self.assets["wave_small_img"] = pygame.image.load(os.path.join(self.image_dir, "wave_small.png")).convert_alpha()
        # level ui
        self.assets["bomb_img"] = pygame.image.load(os.path.join(self.image_dir, "bomb.png")).convert_alpha()
        self.assets["jump_img"] = pygame.image.load(os.path.join(self.image_dir, "jump.png")).convert_alpha()
        self.assets["flag_img"] = pygame.image.load(os.path.join(self.image_dir, "white_flag.png")).convert_alpha()
        
        # buttons
        self.assets["arrowleft_img"] = pygame.image.load(os.path.join(self.image_dir, "arrowleft.png")).convert_alpha()
        self.assets["arrowright_img"] = pygame.image.load(os.path.join(self.image_dir, "arrowright.png")).convert_alpha()
        self.assets['reset_img'] = pygame.image.load(os.path.join(self.image_dir, "reset.png")).convert_alpha()
        self.assets['bucket_img'] = pygame.image.load(os.path.join(self.image_dir, "bucket.png")).convert_alpha()
        self.assets['credits_img'] = pygame.image.load(os.path.join(self.image_dir, "credits.png")).convert_alpha()
        self.assets['add_img'] = pygame.image.load(os.path.join(self.image_dir, "add.png")).convert_alpha()
        self.assets['copy_img'] = pygame.image.load(os.path.join(self.image_dir, "copy.png")).convert_alpha()
        self.assets['save_img'] = pygame.image.load(os.path.join(self.image_dir, "save.png")).convert_alpha()
        self.assets['load_img'] = pygame.image.load(os.path.join(self.image_dir, "load.png")).convert_alpha()
        self.assets['trash_open_img'] = pygame.image.load(os.path.join(self.image_dir, "trash_opened2.png")).convert_alpha()
        self.assets['trash_closed_img'] = pygame.image.load(os.path.join(self.image_dir, "trash_closed2.png")).convert_alpha()
        self.assets['pause_img'] = pygame.image.load(os.path.join(self.image_dir, "pause.png")).convert_alpha()
        self.assets['sound_img'] = pygame.image.load(os.path.join(self.image_dir, "sound.png")).convert_alpha()
        self.assets['mute_img'] = pygame.image.load(os.path.join(self.image_dir, "mute.png")).convert_alpha()
        self.assets['settings_img'] = pygame.image.load(os.path.join(self.image_dir, "settings2.png")).convert_alpha()
        self.assets['continue_img'] = pygame.image.load(os.path.join(self.image_dir, "continue.png")).convert_alpha()
        self.assets['random_img'] = pygame.image.load(os.path.join(self.image_dir, "random.png")).convert_alpha()
        self.assets['confirm_img'] = pygame.image.load(os.path.join(self.image_dir, "confirm.png")).convert_alpha()
        self.assets['delete_img'] = pygame.image.load(os.path.join(self.image_dir, "delete.png")).convert_alpha()
        self.assets['backspace_img'] = pygame.image.load(os.path.join(self.image_dir, "backspace2.png")).convert_alpha()
        self.assets['enter_img'] = pygame.image.load(os.path.join(self.image_dir, "enter2.png")).convert_alpha()
        self.assets['space_img'] = pygame.image.load(os.path.join(self.image_dir, "space.png")).convert_alpha()
        self.assets['forward1_img'] = pygame.image.load(os.path.join(self.image_dir, "forward1.png")).convert_alpha()
        self.assets['back1_img'] = pygame.image.load(os.path.join(self.image_dir, "back1.png")).convert_alpha()
        self.assets['top_img'] = pygame.image.load(os.path.join(self.image_dir, "top.png")).convert_alpha()
        self.assets['bottom_img'] = pygame.image.load(os.path.join(self.image_dir, "bottom.png")).convert_alpha()

        self.load_cursors()
        # cursors


    def load_cursors(self):
        self.assets['move_cursor'] = pygame.image.load(os.path.join(self.cursor_dir, "move4.png")).convert_alpha() 
        self.assets['resize_width_cursor'] = pygame.image.load(os.path.join(self.cursor_dir, "resize_width.png")).convert_alpha()
        self.assets['resize_height_cursor'] = pygame.image.load(os.path.join(self.cursor_dir, "resize_height.png")).convert_alpha()
        self.assets['default_cursor'] = pygame.image.load(os.path.join(self.cursor_dir, "default5.png")).convert_alpha()
        self.assets['click_cursor'] = pygame.image.load(os.path.join(self.cursor_dir, "click5.png")).convert_alpha()
        self.assets['drag_cursor'] = pygame.image.load(os.path.join(self.cursor_dir, "drag.png")).convert_alpha()

        self.assets['x1_cursor'] = pygame.image.load(os.path.join(self.cursor_dir, "1x.png")).convert_alpha()
        x1_cursor = {
            0: self.assets['x1_cursor'],
            90: pygame.transform.rotate(self.assets['x1_cursor'], 90),
            180: pygame.transform.rotate(self.assets['x1_cursor'], 180),
            270: pygame.transform.rotate(self.assets['x1_cursor'], 270),
        }
        self.assets['x2_cursor'] = pygame.image.load(os.path.join(self.cursor_dir, "2x.png")).convert_alpha()
        x2_cursor = {
            0: self.assets['x2_cursor'],
            90: pygame.transform.rotate(self.assets['x2_cursor'], 90),
            180: pygame.transform.rotate(self.assets['x2_cursor'], 180),
            270: pygame.transform.rotate(self.assets['x2_cursor'], 270),
        }

        self.rotated_cursors = {'x1_cursor' : x1_cursor,
                                'x2_cursor' : x2_cursor}



    def load_states(self):
        '''
        creates an instance of first state and appends it to state stack
        '''
        self.state_m = StateManager(self)
        self.state_m.enter_state('title')

    def load_controller(self):
        '''
        loads controllers
        '''
        self.joysticks = []
        self.controller_moved = False
        

        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))

        for joystick in self.joysticks:
            joystick.init()
            print(joystick.get_name())

        with open(os.path.join('ps4_keys.json'), 'r+') as file:
            self.button_keys = json.load(file)

        self.analog_keys = {0: 0, # left_x
                            1: 0, # left_y
                            2: 0, # right_x
                            3: 0, # right_y
                            4: -1, # left_trigger
                            5: -1} # right_trigger

    def toggle_fullscreen(self):
    
        '''
        need I explain this
        updates fullscreen values, scaling values
        '''
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.SCREEN_H = self.window.get_height()   
            self.SCREEN_W = self.window.get_width()
            # scaling for new H and W
            self.scale_multiplier_x = self.GAME_W / self.SCREEN_W
            self.scale_multiplier_y = self.GAME_H / self.SCREEN_H
            # print(f'x scaler: {self.scale_multiplier_x}, y scaler: {self.scale_multiplier_y}, fullscreen')

        else:
            self.window = pygame.display.set_mode((self.WINDOW_W, self.WINDOW_H))
            self.SCREEN_W, self.SCREEN_H = self.WINDOW_W, self.WINDOW_H
            # scaling for new H and W
            self.scale_multiplier_x = self.GAME_W / self.WINDOW_W
            self.scale_multiplier_y = self.GAME_H / self.WINDOW_H
            # print(f'x scaler: {self.scale_multiplier_x}, y scaler: {self.scale_multiplier_y}')



    def render_cursor(self, surface, cursor_input='default'):
        '''
        render custom cursor based on mouse pos

        cursor_input: either tuple or a string
        if tuple then second value indicates the rotation
        '''
        if isinstance(cursor_input, tuple):
            cursor, rotation = cursor_input
        else:
            cursor = cursor_input
            rotation = 0

        cursor += "_cursor"
        # print(self.cursor)
        if cursor in self.assets.keys():
            if rotation == 0:
                pygame.mouse.set_visible(False)
                surface.blit(self.assets[cursor],
                            self.center_cursor())

            else:
                image = self.rotated_cursors[cursor][rotation]
                pygame.mouse.set_visible(False)
                surface.blit(image,
                            self.center_cursor())
        else:
            pygame.mouse.set_visible(True)

    def center_cursor(self):

        x, y =  self.actions['mouse_pos']
        return (x - self.cursor_half, y - self.cursor_half)    

    def update_mouse_pos(self, dt):
        '''
        updates the mouse pos based on controllers stick movement

        dt: delta time
        '''
        # print(f'x: {self.analog_keys[0]}, y: {self.analog_keys[1]}')        
        self.controller_moved = False

        # some movement
        if abs(self.analog_keys[0]) > self.settings.deadzone:
            # print(f'cursor x before: {self.cursor_pos[0]}')
            # print(f'analog x: {self.analog_keys[0]}, dt: {dt}, speed: {self.settings.stick_speed}')
            movement = self.analog_keys[0] * dt * self.settings.stick_speed / self.scale_multiplier_x
            if abs(self.analog_keys[0]) > self.settings.high_speed_deadzone:
                movement *= 2
            elif abs(self.analog_keys[0]) < self.settings.low_speed_deadzone:
                movement /= 2
            # print(f'cursor x after: {self.cursor_pos[0]}')
            self.cursor_pos[0] = max(min(self.cursor_pos[0] + movement, self.SCREEN_W), 0)
            # print(f'cursor x after CAPING: {self.cursor_pos[0]}\n')
            # print(f'stick x value {self.analog_keys[0]}') 
            
            self.controller_moved = True
            

        if abs(self.analog_keys[1]) > self.settings.deadzone:
            movement = self.analog_keys[1] * dt * self.settings.stick_speed / self.scale_multiplier_y
            if abs(self.analog_keys[1]) > self.settings.high_speed_deadzone:
                movement *= 2
            elif abs(self.analog_keys[0]) < self.settings.low_speed_deadzone:
                movement /= 2
            self.cursor_pos[1] = max(min(self.cursor_pos[1] + movement, self.SCREEN_H), 0)
            # print(f'stick y value {self.analog_keys[1]}') 
            # print(f'cursor y: {self.cursor_pos[1]}\n')
            self.controller_moved = True
            
        
        if self.controller_moved:
            # print(f"Updating with Controller: {self.cursor_pos}\n")
            pygame.mouse.set_pos((round(self.cursor_pos[0]), round(self.cursor_pos[1])))

    def reset_keys(self):
        '''
        helper function for resetting actions dictionary
        '''
        for action in self.actions:
            if action != "mouse_pos":
                self.actions[action] = False

    # HELPERS

    def draw_text(self, surface, text, colour, x, y, size="Title"):
        '''
        helper function for drawing text

        surface: game canvas
        text: written message
        colour: colour of text
        x & y: center coordinates of text rect
        size: Title, H1, Medium or Small
        '''
        match size:
            case "Title":
                text_surface = self.font_title.render(text,
                                                True, colour)
            case "H1":
                text_surface = self.font_h1.render(text,
                                                True, colour)
            case "Medium":
                text_surface = self.font_medium.render(text,
                                                True, colour)
            case "Small":
                text_surface = self.font_small.render(text,
                                                True, colour)
            case "xs":
                text_surface = self.font_tiny.render(text,
                                                True, colour)
            
            case _:
                text_surface = self.font_medium.render(text,
                                                True, colour)
                print(f"Draw text input error, size: {size} is not in Title, Medium, Small")
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def draw_text_topleft(self, surface, text, colour, x, y, size="Title"):
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
            case "H1":
                text_surface = self.font_h1.render(text,
                                                True, colour)
            case "Medium":
                text_surface = self.font_medium.render(text,
                                                True, colour)
            case "Small":
                text_surface = self.font_small.render(text,
                                                True, colour)
            case "xs":
                text_surface = self.font_tiny.render(text,
                                                True, colour)
            case _:
                text_surface = self.font_medium.render(text,
                                                True, colour)
                print(f"Draw text input error, size: {size} is not in Title, Medium, Small")
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

    def add_image(self, image_asset_name, x, y, list):

        rect = self.assets[image_asset_name].get_rect()
        rect.topleft = (x, y)
        list.append({'img': self.assets[image_asset_name],
                            'rect': rect})
        
    def add_text(self, str, x, y, size, list, colour = None):
        if colour is None:
            colour = self.TEXT_COL
        list.append({'str': str, 
                     'x': x,
                     'y': y,
                     'size': size,
                     'colour': colour})


