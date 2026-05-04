import pygame
from dataclasses import dataclass

@dataclass
class FloatingFade(pygame.sprite.Sprite):
    '''
    x&y center values
    '''
    x: float
    y: float
    float_speed: float
    text: str
    text_font: pygame.font.Font
    colour: tuple
    text2: str = None
    text_font2: pygame.font.Font = None
    colour2: tuple = None

    def __post_init__(self):
        '''
        init
        '''
        # sprites init
        super().__init__()
        # default values
        self.start_time = 0
        self.fade_start = 4000
        self.duration = 5000
        self.start_alpha = 255

        self.start_time = pygame.time.get_ticks()

        # text surface
        self.image = self.text_font.render(
            self.text, True, self.colour)
        # rect for moving, center
        self.rect = self.image.get_rect(
            center=(self.x, self.y))


        # if second text
        if (self.text2 and 
            self.text_font2 and 
            self.colour2):

            self.image2 = self.text_font.render(
                self.text, True, self.colour2)
            self.rect2 = self.image2.get_rect(
            center=(self.x, self.y))
        

    def update(self, delta_time):
        '''
        updates images alpha if active
        and duration hasn't elapsed
        '''
        # time since start
        elapsed = pygame.time.get_ticks() - self.start_time

        # 
        if elapsed >= self.duration:
            self.remove()
            return
        
        self.update_pos(delta_time)
        
        if elapsed >= self.fade_start:

            ratio_of_duration_left = (self.duration - elapsed
                    ) / (self.duration - self.fade_start)
            alpha = max(0, int(self.start_alpha * ratio_of_duration_left))
            self.image.set_alpha(alpha)
            

    def update_pos(self, delta_time):
        '''
        float up
        '''
        self.y -= self.float_speed * delta_time
        self.rect = round(self.y)


    def remove(self):
        '''
        sets activity state to false
        '''
        self.kill()