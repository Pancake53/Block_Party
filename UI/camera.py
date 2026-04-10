
class Camera():
    def __init__(self, game_world):
        self.game_world = game_world

        # Camera
        self.camera_speed = 60
        
    
        # 1x speed
        self.edge_buffer_1x = 25 # px
        self.right_edge_1x = self.game_world.game.GAME_W - self.edge_buffer_1x
        self.bottom_edge_1x = self.game_world.game.GAME_H - self.edge_buffer_1x

        # 2x speed
        self.edge_buffer_2x = 5 # px # double speed if closer to edge
        self.right_edge_2x = self.game_world.game.GAME_W - self.edge_buffer_2x
        self.bottom_edge_2x = self.game_world.game.GAME_H - self.edge_buffer_2x
        self.total_offset_x = 0
        self.total_offset_y = 0
        self.max_offset = 100

        if self.game_world.wrap_around:
            self.update_x = self.update_x_wrap_around
            self.update_y = self.update_y_normal
        else:
            self.update_x = self.update_x_normal
            self.update_y = self.update_y_normal


    def update(self, delta_time, actions):
        '''
        moves 'camera' by moving every object on screen

        delta_time: dt
        actions: user inputs dictionary
        '''
        # level pos is the effective pos of mouse
        # after the camera has moved

        # offset is the total offset so far, starts at 0
        x = actions['mouse_pos'][0]
        y = actions['mouse_pos'][1]
        # start off with false offset
        x_offset = 0
        y_offset = 0

        y_offset = self.update_y(y, delta_time)
        x_offset = self.update_x(x, delta_time)

        # move movables if new offset was applied
        if y_offset or x_offset:
            # print(f'Offset, y: {y_offset}, x: {x_offset}')
            self.update_positions(x_offset, y_offset)

    def update_x(self, delta_time, actions):
        self.update_x(delta_time, actions)

    def update_y(self, delta_time, actions):
        self.update_y(delta_time, actions)

    def update_y_normal(self, y, delta_time): 
        '''
        updates y offset

        y: screen y mouse pos
        delta_time: time since last frame

        Returns: 
        True if new offset
        New offset
        '''

        # bottom of the screen --> objects go up
        if (y > self.bottom_edge_1x and
            self.total_offset_y > - self.max_offset):
            
            # negative so things float up
            y_offset = - self.camera_speed * delta_time

            if y > self.bottom_edge_2x:
                y_offset *= 2

            y_offset = round(y_offset)
            self.total_offset_y += y_offset # negative
            
            return y_offset

        # top of the screen --> objects go down
        if (y < self.edge_buffer_1x and
            self.total_offset_y < self.max_offset):

            # positive so things going down
            y_offset = self.camera_speed * delta_time

            if y < self.edge_buffer_2x:
                y_offset *= 2

            y_offset = round(y_offset)
            self.total_offset_y += y_offset
            
            return y_offset
        
        return 0
    
    def update_x_normal(self, x, delta_time): 
        '''
        updates x offset

        x: screen x mouse pos
        delta_time: time since last frame

        Returns: 
        True if new offset
        New offset
        '''

        # right edge of the screen --> offset negative --> objects to left
        if (x > self.right_edge_1x and
            self.total_offset_x > - self.max_offset):

            # negative so obj move left
            x_offset = - self.camera_speed * delta_time

            if x > self.right_edge_2x:
                x_offset *= 2

            x_offset = round(x_offset)
            self.total_offset_x += x_offset # negative
            
            return x_offset

        # left edge of the screen --> offset positive --> objects go right
        if (x < self.edge_buffer_1x and
            self.total_offset_x < self.max_offset):

            # positive so obj move right
            x_offset = self.camera_speed * delta_time

            if x < self.edge_buffer_2x:
                x_offset *= 2

            x_offset = round(x_offset)

            self.total_offset_x += x_offset
            
            return x_offset
        
        return 0

    def update_x_wrap_around(self, x, delta_time): 
        '''
        updates x offset

        x: screen x mouse pos
        delta_time: time since last frame

        Returns: 
        True if new offset
        New offset
        '''

        # right edge of the screen --> offset negative --> objects to left
        if (x > self.right_edge_1x):

            # negative so obj move left
            x_offset = - self.camera_speed * delta_time

            if x > self.right_edge_2x:
                x_offset *= 2

            x_offset = round(x_offset)
            self.total_offset_x += x_offset # negative

            
            return x_offset

        # left edge of the screen --> offset positive --> objects go right
        if (x < self.edge_buffer_1x):

            # positive so obj move right
            x_offset = self.camera_speed * delta_time

            if x < self.edge_buffer_2x:
                x_offset *= 2

            x_offset = round(x_offset)

            self.total_offset_x += x_offset

            
            return x_offset
        
        return 0


    def update_positions(self, x_offset, y_offset):
        '''
        updates positions in game_world

        x_offset: x-axis offset
        y_offset: y-axis offset
        '''
        # var
        self.game_world.camera_moved = True
        # collision tiles
        # self.game_world.temp_tiles = self.game_world.tiles.copy()
        for tile in self.game_world.tiles:
            tile.update(x_offset, y_offset)
        self.game_world.tiles = self.game_world.temp_tiles.copy()
        # characters
        for team in self.game_world.teams_not_eliminated.values():
            for char in team:
                char.on_camera_move(x_offset, y_offset)
        # bomb
        self.game_world.bomb.on_camera_move(x_offset, y_offset)
        # explosion
        self.game_world.explosion.on_camera_move(x_offset, y_offset)
    