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
        self.transparancy = 150
        colour = [i for i in random.choice(self.colours)]
        colour.append(self.transparancy)
        self.colour = tuple(colour)

        self.rect = pygame.Rect(0, 0, self.W, self.H)
        self.update_surface()

        self.left_wall = game_W * 2 / 3

        self.corners_hit = 0



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
        elif self.x < self.left_wall:
            self.x = self.left_wall
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

        if x_hit and y_hit:
            if self.corners_hit < 1:
                self.corner_hit()

    def render(self, surface):
        surface.blit(self.rect_surface, (self.x, self.y))

    def change_col(self):
        '''
        changes the colour of the bouncing rectangle
        '''
        new_col = random.choice(self.colours)
        while self.colour == new_col:
            new_col = random.choice(self.colours)

        colour = [i for i in new_col]
        colour.append(self.transparancy)
        self.colour = tuple(colour)
        self.update_surface()

    def corner_hit(self):
        '''
        react to hitting the corner WOAHH
        '''
        # print("corner hit")
        self.corners_hit += 1

        self.W *= 2
        self.H *= 2
        self.x_speed *= 2
        self.y_speed *= 2
        self.x = self.left_wall + 20
        self.y = self.game_H / 2 - self.H / 2
        self.rect = pygame.Rect(0, 0, self.W, self.H)
        self.update_surface()
        # print(f'new x: {self.x}, y: {self.y}, w: {self.W}, h: {self.H}')

    def update_surface(self):
        '''
        creates new surface and draws rect on it
        '''
        self.rect_surface = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        pygame.draw.rect(self.rect_surface, self.colour, self.rect)
