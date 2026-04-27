import pygame

from helpers import draw_shading_for_rect

class Part():
    def __init__(self, x, y, width, height, colour, layer, char_creating, main=False):
        '''
        pass in atributes
        '''
        self.x = x
        self.y = y
        self.W = width
        self.H = height
        self.colour = colour


        # height from bottom, 
        # eg 0 is covered by other parts
        self.layer = layer

        # list of all parts
        # for checking if object is on top 
        # and for knowing how many total parts 
        # there are for bringing objects to the top 
        self.char_creating = char_creating

        # if main = True, then part
        # determines characters main colour
        self.main = main

        # state managment for part
        self.hovered = False
        self.state = {'top': False, 'selected': False, 'move': False, 
                      
                    'resize_left': False, 'resize_right': False,
                    'resize_top': False, 'resize_bottom': False}
        
        self.old_mouse_pos = None

        # create rect obj
        self.rect = pygame.Rect(self.x, self.y, self.W, self.H)

        # variables
        # how many pixels part moves at a time when resizing
        self.move_buffer = self.char_creating.scalar

        # determines what is considered an edge and what is center
        # larger value => less space for center/moving, more for resizing 
        self.min_size = 8
        self.min_edge = 3
        self.edge_buffer_W = max(self.min_edge, self.W / 12)
        self.edge_buffer_H = max(self.min_edge / 2, self.H / 12)



    def render(self, surface):
        '''
        render part, outline, mouse
        '''
        pygame.draw.rect(surface, self.colour, self.rect)

        # draw outline for selected part
        if self.state['selected']:
            draw_shading_for_rect((0, 0, 0), self.rect, surface, 3)


    def update(self, dt, actions):
        '''
        make part react to mouse actions
        '''
        self.mouse_actions(dt, actions)

    def mouse_actions(self, dt, actions):

        self.hovered = self.rect.collidepoint(actions["mouse_pos"])

        # 'top' is based on position of mouse and 
        # layers of part that exist in the same position
        if actions['mouse_click']:
            # print('mouse clicked now this shit should reset right')
            if self.state['top']:
                
                if not self.state['selected']:
                    self.state['selected'] = True
                    self.char_creating.selected_part = self
            else:
                # print('it should reset')
                self.reset_state()

        # after the part is selected
        if self.state['selected']:
            print(f'States: {self.state}')
            if self.state['move']:
                self.move(actions)
                print('moving')
            elif self.state['resize_left']:
                self.resize_left(actions)
            elif self.state['resize_right']:
                self.resize_right(actions)
            elif self.state['resize_top']:
                self.resize_top(actions)
            elif self.state['resize_bottom']:
                self.resize_bottom(actions)
            elif actions['m1']:
                # print('m1')
                self.m1_actions(actions)

    def m1_actions(self, actions):
        '''
        reacts to m1 actions
        '''
        x, y = actions['mouse_pos']

        # move zone
        # width
        if (self.x + self.edge_buffer_W < 
            x < self.x + self.rect.width - self.edge_buffer_W and 
        # height    
        self.y + self.edge_buffer_H < 
        y < self.y + self.rect.height - self.edge_buffer_H):
            self.state['move'] = True
            return

        # resize part
        # right
        right_edge = self.x + self.rect.width
        if (right_edge - self.edge_buffer_W < 
              x < right_edge + self.edge_buffer_W 
                and  
        self.y < y < self.y + self.rect.height):
            self.state['resize_right'] = True
            return
        
        # left
        left_edge = self.x
        if (left_edge - self.edge_buffer_W < 
              x < left_edge + self.edge_buffer_W 
                and  
        self.y < y < self.y + self.rect.height):
            self.state['resize_left'] = True
            return
        
        # top
        top_edge = self.y
        if (self.x < x < self.x + self.rect.width
                and  
        top_edge - self.edge_buffer_H < y < top_edge + self.edge_buffer_H):
            self.state['resize_top'] = True
            return
        
        # bottom
        bottom_edge = self.y + self.rect.height
        if (self.x < x < self.x + self.rect.width
                and  
        bottom_edge - self.edge_buffer_H < y < bottom_edge + self.edge_buffer_H):
            self.state['resize_bottom'] = True
            return

    def move(self, actions):
        '''
        moves the piece w mouse
        '''
        # dragging stopped
        if not actions['m1']:
            self.old_mouse_pos = None
            self.state['move'] = False
            return

        # if no history of mouse pos then get some and return
        if self.old_mouse_pos is None:
            self.old_mouse_pos = actions['mouse_pos']
            return
        
        x_movement = actions['mouse_pos'][0] - self.old_mouse_pos[0]
        y_movement = actions['mouse_pos'][1] - self.old_mouse_pos[1]
        
        self.x += x_movement
        self.y += y_movement

        self.rect.x = self.x
        self.rect.y = self.y

        # store current value into old value
        self.old_mouse_pos = actions['mouse_pos']

        

    # Resize

    def resize_left(self, actions):
        '''
        resize width left
        '''
        # dragging stopped
        if not actions['m1']:
            self.old_mouse_pos = None
            self.state['resize_left'] = False
            return

        # if no history of mouse pos then get some and return
        if self.old_mouse_pos is None:
            self.old_mouse_pos = actions['mouse_pos']
            return
        
        width_change =  self.old_mouse_pos[0] - actions['mouse_pos'][0]
        
        self.W += width_change
        self.W = max(self.min_size, self.W)
        self.rect.width = self.W

        self.x -= width_change
        self.rect.x = self.x

        # store current value into old value
        self.old_mouse_pos = actions['mouse_pos']

        self.edge_buffer_W = max(self.min_edge, self.W / 12)
        

    def resize_right(self, actions):
        '''
        resize width left
        '''
        # dragging stopped
        if not actions['m1']:
            self.old_mouse_pos = None
            self.state['resize_right'] = False
            return

        # if no history of mouse pos then get some and return
        if self.old_mouse_pos is None:
            self.old_mouse_pos = actions['mouse_pos']
            return
        
        width_change = actions['mouse_pos'][0] - self.old_mouse_pos[0]
        
        self.W += width_change
        self.W = max(self.min_size, self.W)
        self.rect.width = self.W

        # store current value into old value
        self.old_mouse_pos = actions['mouse_pos']

        # update edge buffer
        self.edge_buffer_W = max(self.min_edge, self.W / 12)
        


    def resize_top(self, actions):
        '''
        resize height top
        '''
        # dragging stopped
        if not actions['m1']:
            self.old_mouse_pos = None
            self.state['resize_top'] = False
            return

        # if no history of mouse pos then get some and return
        if self.old_mouse_pos is None:
            self.old_mouse_pos = actions['mouse_pos']
            return
        
        height_change = self.old_mouse_pos[1] - actions['mouse_pos'][1] 
        
        self.H += height_change
        self.H = max(self.min_size, self.H)
        self.rect.height = self.H

        self.y -= height_change
        self.rect.y = self.y

        # store current value into old value
        self.old_mouse_pos = actions['mouse_pos']

        # update edge buffer
        self.edge_buffer_H = max(self.min_edge, self.W / 12)

    def resize_bottom(self, actions):
        '''
        resize height bottom
        '''
        # dragging stopped
        if not actions['m1']:
            self.old_mouse_pos = None
            self.state['resize_bottom'] = False
            return

        # if no history of mouse pos then get some and return
        if self.old_mouse_pos is None:
            self.old_mouse_pos = actions['mouse_pos']
            return
        
        height_change = actions['mouse_pos'][1] - self.old_mouse_pos[1]
        
        self.H += height_change
        self.H = max(self.min_size, self.H)
        self.rect.height = self.H


        # store current value into old value
        self.old_mouse_pos = actions['mouse_pos']

        # update edge buffer
        self.edge_buffer_H = max(self.min_edge, self.W / 12)

    # Colour
      
    def change_colour(self, new_colour):
        if self.state['selected']:
            self.colour = new_colour

    def reset_state(self):
        for key in self.state.keys():
            self.state[key] = False

    


    


