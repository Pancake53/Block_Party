import pygame
from gameObject import GameObject


class Character(GameObject):
    '''
    In game character which players have many at the beginning of a round

    Handels rendering, updating pos, collision testing,
      action such as selecting, jumping, spawning in bomb
    
    '''
    def __init__(self, game_world, team_id, width, x_pos, y_pos):
        '''Initialize attributes

        game_world: level the character loads into
        team_id: team number
        characters width
        x & y position
        
        '''
        super().__init__(x_pos, y_pos)
        self.team_id = team_id
        self.game_world = game_world
        self.width = width
        # Character colour based on team id
        self.colour = self.game_world.team_colours[team_id]
        # Physics
        # y bounce, lower value -> more small bounces
        self.y_stop = 20 
        # x speed stopper, if x_speed < x_stop -> x_speed = 0
        self.x_stop = 1 
        # speed loss multiplier on collision
        self.retention = 0.25 

        self.rect = pygame.Rect(x_pos, y_pos, self.CHARACTER_SIZE * width, self.CHARACTER_SIZE * 2)
        # State management
        self.state = {"selected": False, "choosing": False, "jump": False, "drag": False, "throw": False}
        
      

    def render(self, surface):
        '''
        Render char on given surface
        If char is choosing, then render options
        '''
        pygame.draw.rect(surface, self.colour, self.rect)
        if self.state["choosing"]:
            self.game_world.render_selections(self.rect.x, self.rect.y)



    def collision_x_axis(self, collisions):
        '''
        reaction to collision on x axis
        
        collisions: list of overlapping tiles
        '''
        for tile in collisions:
            if self.x_speed > 0:
                # print("colliding w left wall")
                self.rect.right = tile.left # colliderect => False
                self.x_pos = self.rect.x
            elif self.x_speed < 0:
                # print("colliding w right wall")
                self.rect.left = tile.right # colliderect => False
                self.x_pos = self.rect.x

        self.x_speed = - self.x_speed * self.retention
        self.y_speed *= self.retention # also reduce y speed, MAY NEED TWEAKING


    def collision_y_axis(self, collisions):
        '''
        reaction to collision on y axis
        
        collisions: list of overlapping tiles
        '''
        tile = collisions[0]
        self.x_speed *= self.retention # also reduce x speed, MAY NEED TWEAKING

        if self.y_speed > self.y_stop: 
            # top
            # print(f"colliding w top of tile, y: {round(self.y_speed,3)}, x: {round(self.x_speed,3)}")
            self.rect.bottom = tile.top
            self.y_pos = self.rect.y
            self.y_speed = self.y_speed * -1 * self.retention
        elif -self.y_speed > 0: 
            # bottom
            # print("colliding w bottom of tile")
            self.rect.top = tile.bottom
            self.y_pos = self.rect.y
            self.y_speed = self.y_speed * -1 * self.retention / 2
        else:
            # top little momentum so momentum to 0
            # print("y_speed 0")
            self.rect.bottom = tile.top
            self.y_pos = self.rect.y
            self.y_speed = 0


    def handle_actions(self, actions):
        '''handels actions for char
          based on actions dictionary'''
        if actions["left"]:
            self.add_momentum(-50, -50)
        if actions["right"]:
            self.add_momentum(50, -50)
        if actions["action1"]:
            self.x_pos = self.origin[0]
            self.y_pos = self.origin[1]
            self.x_speed = 0
            self.y_speed = 0.01

        # print(f"char state: {self.state}")
        
        # mouse on character
        hovered = self.rect.collidepoint(actions["mouse_pos"])

        # Handle mouse clicks for selecting character
        if hovered:
            if actions["mouse_click"]:
                if not (self.state["jump"] or self.state["throw"]):
                    # print("select condition met") 

                        # print("collision")
                        self.state["selected"] = not self.state["selected"]
                        self.state["choosing"] = not self.state["choosing"]
                        # print(f"state: {self.state}")

        # Jump
        # require new click to enter drag state
        if self.state["jump"] and not self.state["drag"]:
            if actions["mouse_click"]:
                self.mouse_pos_list = [actions["mouse_pos"]]
                self.state["drag"] = True

        # Dragging
        elif self.state["drag"]:
            if actions["mouse_pressed"]:
                while len(self.mouse_pos_list) > 2:
                    self.mouse_pos_list.pop()
                self.mouse_pos_list.append(actions["mouse_pos"])
                # render line or arrow function

        # Releasing
        if (not actions["mouse_pressed"]) and (len(self.mouse_pos_list) >= 2):
            print("time to throw!")
            x_speed = (self.mouse_pos_list[0][0] -self.mouse_pos_list[-1][0]) * self.throw_multiplier
            y_speed = (self.mouse_pos_list[0][1] -self.mouse_pos_list[-1][1]) * self.throw_multiplier
            self.add_momentum(x_speed, y_speed)

            self.mouse_pos_list = []
            self.reset_state()

        
        if actions["space"]: # bomb placeholder
            self.game_world.spawn_bomb(self.rect.x, self.rect.y)


