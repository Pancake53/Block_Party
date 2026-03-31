
class Camera():
    def __init__(self, game_world):
        self.game_world = game_world

        # Camera
        self.camera_speed = 100
        self.camera_buffer = 30 # px
        self.right_edge = self.game_world.game.GAME_W - self.camera_buffer
        self.bottom_edge = self.game_world.game.GAME_H - self.camera_buffer
        self.total_offset_x = 0
        self.total_offset_y = 0
        self.max_offset = 100

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
        offset = False
        x_offset = 0
        y_offset = 0

        offset, y_offset = self.update_y(y, delta_time)
        offset, x_offset = self.update_x(x, delta_time)

        # move movables if new offset was applied
        if offset:
            # collision tiles
            for tile in self.game_world.tiles:
                tile.update(x_offset, y_offset)
            # characters
            for team in self.game_world.teams_not_eliminated.values():
                for char in team:
                    char.on_camera_move(x_offset, y_offset)

    def update_y(self, y, delta_time): 
        '''
        updates y offset

        y: screen y mouse pos
        delta_time: time since last frame

        Returns: 
        True if new offset
        New offset
        '''

        # bottom of the screen --> objects go up
        if (y > self.bottom_edge and
            self.total_offset_y > - self.max_offset):
            # negative so things float up
            y_offset = - self.camera_speed * delta_time
            self.total_offset_y += y_offset # negative
            # cap to exactly max, because total negative
            max(self.total_offset_y, - self.max_offset)
            return True, y_offset

        # top of the screen --> objects go down
        if (y < self.camera_buffer and
            self.total_offset_y < self.max_offset):
            # positive so things going down
            y_offset = self.camera_speed * delta_time
            self.total_offset_y += y_offset
            # cap to exactly min, because total positive
            min(self.total_offset_y, self.max_offset)
            return True, y_offset
        
        return False, 0
    
    def update_x(self, x, delta_time): 
        '''
        updates x offset

        x: screen x mouse pos
        delta_time: time since last frame

        Returns: 
        True if new offset
        New offset
        '''

        # right edge of the screen --> offset negative --> objects to left
        if (x > self.bottom_edge and
            self.total_offset_x > - self.max_offset):
            # negative so obj move left
            x_offset = - self.camera_speed * delta_time
            self.total_offset_y += x_offset # negative
            # cap to exactly max, because total negative
            max(self.total_offset_x, - self.max_offset)
            return True, x_offset

        # left edge of the screen --> offset positive --> objects go right
        if (x < self.camera_buffer and
            self.total_offset_x < self.max_offset):
            # positive so obj move right
            x_offset = self.camera_speed * delta_time
            self.total_offset_y += x_offset
            # cap to exactly min, because total positive
            min(self.total_offset_x, self.max_offset)
            return True, x_offset
        
        return False, 0
        