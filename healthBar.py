import pygame
import pygame.time

class HealthBar():
    '''
    HealthBar class
    
    handels blitting of char hp on screen
    each character has own health bar
    '''

    def __init__(self, character, offset_x=-25, offset_y=-20):
        '''
        init attributes
        character: character who owns the healthBar
        x & y: offset from character center
        '''

        self.character = character          
        self.offset_x = offset_x            
        self.offset_y = offset_y

        self.x_pos = -72
        self.y_pos = -72

        # colours
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        # dimensions
        self.MAX_WIDTH = 50
        self.HEIGHT = 10
        
        # surfaces
        self.red_bar = pygame.Surface((self.MAX_WIDTH, self.HEIGHT)).convert_alpha()
        self.red_bar.fill(self.RED)
        self.green_bar = pygame.Surface((self.MAX_WIDTH, self.HEIGHT)).convert_alpha()

        # for flash and fade
        self.start_time = 0
        self.fade_start = 2000
        self.duration = 3000 # ms
        self.start_alpha = 255
        self.active = False

    def update(self):
        '''
        updates images alpha if active
        and duration hasn't elapsed

        '''
        if not self.active:
            return
        
        # get position from character
        self.x_pos = self.character.rect.centerx + self.offset_x
        self.y_pos = self.character.rect.top + self.offset_y

        elapsed = pygame.time.get_ticks() - self.start_time
        

        if elapsed >= self.duration:
            self.remove()
            return
        

        if elapsed >= self.fade_start:

            ratio_of_duration_left = (self.duration - elapsed) / (self.duration - self.fade_start)
            alpha = max(0, int(self.start_alpha * ratio_of_duration_left))
            self.red_bar.set_alpha(alpha)
            self.green_bar.set_alpha(alpha)

    def render(self, surface):
        '''
        renders if active

        surface: surface to draw on
        '''
        if self.active:
            surface.blit(self.red_bar, (self.x_pos, self.y_pos))
            surface.blit(self.green_bar, (self.x_pos, self.y_pos))

    def set_width(self):
        '''
        modidier green bars width when hp changes
        '''
        current_hp = max(0, self.character.current_hp)
        green_width = int(current_hp / self.character.max_hp * self.MAX_WIDTH)

        self.green_bar = pygame.Surface((green_width, self.HEIGHT)).convert_alpha()
        self.green_bar.fill(self.GREEN)

    def activate(self):
        '''
        activate health_bar when hp changes
        sets attributes and active state to true

        current_hp = characters current hp
        x & y: topleft coordinates for health bar
        '''
        self.set_width()
        self.start_time = pygame.time.get_ticks()
        self.active = True
        self.red_bar.set_alpha(self.start_alpha)
        self.green_bar.set_alpha(self.start_alpha)

    def remove(self):
        '''
        sets activity state to false
        '''
        self.active = False


        