import os, pygame, time

from states.title import Title

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False

        self.FONT_SIZE = 20
        self.GAME_W, self.GAME_H = 480, 270
        self.WINDOW_W, self.WINDOW_H = 480, 270
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.window = pygame.display.set_mode((self.WINDOW_W, self.WINDOW_H))

        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

        self.actions = {"left": False, "right": False, "up": False,
                        "down": False, "mouse1": False, "action1": False,
                        "action2": False, "start": False}
        
        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.load_assets()
        self.load_states()
        

    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.check_events()
            self.update()
            self.render()


    def check_events(self):
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

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)

    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.window.blit(pygame.transform.scale(self.game_canvas,
                                                 (self.WINDOW_W, self.WINDOW_H)),
                                                   (0, 0))
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, colour, x, y):
        text_surface = self.font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def load_assets(self):
        # Pointers for assets
        self.assets_dir = os.path.join("assets")
        self.font_dir = os.path.join(self.assets_dir, "font")
        # Assets themselves
        self.font = pygame.font.Font(os.path.join(self.font_dir, '8-BIT WONDER.TTF'), self.FONT_SIZE)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)


