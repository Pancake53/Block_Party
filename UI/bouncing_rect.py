import pygame
import random

class BouncingRect:
    def __init__(self, x, y, WIDTH, HEIGHT, x_speed, y_speed, game_W, game_H, cols):
        self.x = x
        self.y = y
        self.W = WIDTH
        self.H = HEIGHT
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.game_W = game_W
        self.game_H = game_H
        self.colours = cols

        self.colour = random.choice(self.colours)

        self.rect = pygame.Rect(self.x, self.y, self.W, self.H)

    def update(self):
        '''
        updates pos based on speed
        and handels collisions
        '''
        # update pos
        self.x += self.x_speed
        self.y += self.y_speed
        # variables for corner hit
        x_hit, y_hit = False, False

        # collisions
        # x
        # right side
        if self.x + self.W > self.game_W:
            self.x = self.game_W - self.W
            self.x_speed *= -1
            self.change_col()
            x_hit = True

        # left side
        elif self.x < 0:
            self.x = 0
            self.x_speed *= -1
            self.change_col()
            x_hit = True


        # y
        # bottom
        if self.y + self.H > self.game_H:
            self.y = self.game_H - self.H
            self.y_speed *= -1
            self.change_col()
            y_hit = True

        # top
        elif self.y < 0:
            self.y = 0
            self.y_speed *= -1
            self.change_col()
            y_hit = True

        self.rect.x = self.x
        self.rect.y = self.y

        if x_hit and y_hit:
            self.corner_hit()

    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)

    def change_col(self):
        '''
        changes the colour of the bouncing rectangle
        '''
        new_col = random.choice(self.colours)
        while self.colour == new_col:
            new_col = random.choice(self.colours)

        self.colour = new_col

    def corner_hit(self):
        '''
        react to hitting the corner WOAHH
        '''
        self.W *= 2
        self.H *= 2
        self.x_speed *= 2
        self.y_speed *= 2
        self.x = self.game_W / 2 - self.W / 2
        self.y = self.game_H / 2 - self.H / 2
        self.rect = pygame.Rect(self.x, self.y, self.W, self.H)