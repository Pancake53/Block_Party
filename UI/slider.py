import pygame
from dataclasses import dataclass
from typing import Callable

@dataclass
class Slider:
    '''
    class for sliders that control some value
    '''
    # position of left center of the slicer
    name: str
    x: int
    y: int
    width: int # total width of line
    height: int # height of indicator
    min_value: int
    max_value: int
    current_value: int
    on_change: Callable[[str, int], None]
    colour: tuple = (0, 0, 0)

    def __post_init__(self):
        '''
        function that runs on init
        '''
        self.load()

    

    def update(self, actions):
        '''
        react to mouse and player actions
        '''
        hovered = self.pointer.collidepoint(actions['mouse_pos'])

        # on top of pointer and clicked, enter drag
        if hovered:
            if actions['mouse_click']:
                self.drag = True

        # in drag and released m1 -> exit drag
        if self.drag:
            if actions['m1'] == False:
                self.drag = False
                self.old_mouse_pos = None
            else:
                self.handle_drag(actions)


    def handle_drag(self, actions):
        '''
        handle what happens during drag state
        '''
        # no old pos, get one and return
        if self.old_mouse_pos is None:
            self.old_mouse_pos = actions['mouse_pos']
            return

        x_move = actions['mouse_pos'][0] - self.old_mouse_pos[0]
        self.current_value += x_move
        # cap
        if self.current_value < 0:
            self.current_value = 0
            self.update_pos()
        elif self.current_value > self.max_value:
            self.current_value = self.max_value
            self.update_pos()
        else:
            self.pointer.x += x_move
        # update old pos
        self.old_mouse_pos = actions['mouse_pos']
        # callback
        self.on_change(self.name, self.current_value)
        

    def render(self, surface):
        '''
        render slider onto screen
        '''
        # left
        pygame.draw.line(surface, self.slider_colour, self.left_top, self.left_bottom, self.W)
        # slider
        pygame.draw.line(surface, self.slider_colour, self.left, self.right, self.W)
        # right
        pygame.draw.line(surface, self.slider_colour, self.right_top, self.right_bottom, self.W)

        # circle
        pygame.draw.rect(surface, self.colour,
                            self.pointer)
        

    def load(self):
        '''
        handels coordinates and objects creating
        '''
        # init attributes
        self.W = 7
        self.side_lenght = self.height
        self.slider_colour = (255, 255, 255)
        pointer_H = self.height * 1.5
        pointer_W = 10

        self.drag = False
        self.old_mouse_pos = None

        # left side line
        self.left_top = (self.x, self.y - self.side_lenght / 2)
        self.left_bottom = (self.x, self.y + self.side_lenght / 2)

        # slider line
        self.left = (self.x, self.y)
        self.right = (self.x + self.width, self.y)

        # right side line
        self.right_top = (self.right[0], self.right[1] - self.side_lenght / 2)
        self.right_bottom = (self.right[0], self.right[1] + self.side_lenght / 2)

        # pointer
        
        self.pointer_x = self.x + self.current_value - pointer_W / 2 
        self.pointer_y = self.y - pointer_H / 2
        self.pointer = pygame.Rect(self.pointer_x, self.pointer_y,
                               pointer_W, pointer_H)
        
    def update_pos(self):
        # updating sliders
        self.pointer_x = self.x + self.current_value - self.pointer.width / 2
        self.pointer.x = self.pointer_x