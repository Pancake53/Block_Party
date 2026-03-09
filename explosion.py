import pygame
import pygame.time

class Explosion():
    '''
    explosion class
    
    handels blitting of explosion rect
    '''

    def __init__(self, explosion_img, x_pos=-72, y_pos=-72):
        '''
        init attributes
        
        x & y: coordinates
        explosion_img: asset img for explosion
        '''

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = explosion_img

        # rect
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

        # for flash and fade
        self.start_time = 0
        self.duration = 1000 # ms
        self.start_alpha = 255
        self.active = False

    def update(self):
        '''
        updates images alpha if active
        and duration hasn't elapsed
        '''
        if not self.active:
            return
        
        elapsed = pygame.time.get_ticks() - self.start_time
        
        if elapsed >= self.duration:
            self.remove()
            return
        
        ratio_of_duration_left = (self.duration - elapsed) / self.duration
        alpha = max(0, int(self.start_alpha * ratio_of_duration_left))
        self.image.set_alpha(alpha)

    def render(self, surface):
        '''
        renders if active

        surface: surface to draw on
        '''
        if self.active:
            surface.blit(self.image, self.rect)

    def activate(self, x_pos, y_pos):
        '''
        activate explosion
        sets attributes and active state to true

        x & y: center coordinates for explosion
        '''
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
        self.start_time = pygame.time.get_ticks()
        self.active = True
        self.image.set_alpha(self.start_alpha)

    def remove(self):
        '''
        sets activity state to false
        and moves the explosion to a quiet corner
        '''
        self.active = False
        self.rect.x = -72
        self.rect.y = -72

