import pygame
from gameObject import GameObject
from healthBar import HealthBar

class Character(GameObject):
    '''
    In game character which players have many at the beginning of a round

    Handels rendering, updating pos, collision testing,
      action such as selecting, jumping, spawning in bomb
    
    '''
    def __init__(self, team_id, x_pos, y_pos, game_world, width=1):
        '''Initialize attributes

        game_world: level the character loads into
        team_id: team number
        characters width
        x & y position
        
        '''
        super().__init__(x_pos, y_pos, game_world)
        self.team_id = team_id
        self.width = width
        # Character colour based on team id
        self.colour = self.game_world.team_colours[team_id]
        # Physics
        # y bounce, lower value -> more small bounces
        self.y_stop = 20 
        self.y_speed = 0.1
        # x speed stopper, if x_speed < x_stop -> x_speed = 0
        self.x_stop = 1 
        # speed loss multiplier on collision
        self.retention = 0.25 

        self.rect = pygame.Rect(x_pos, y_pos, self.CHARACTER_SIZE * width, self.CHARACTER_SIZE * 2)
       
        # Health points
        self.max_hp = 100
        self.current_hp = 100
        self.health_bar = HealthBar(self)
        
      

    def render(self, surface):
        '''
        Render char on given surface

        surface: game canvas
        '''
        if not self.state['eliminated']:
            pygame.draw.rect(surface, self.colour, self.rect)
            # if self.state["choosing"]:
            #     self.game_world.render_selections(self.rect.x, self.rect.y)

            self.health_bar.render(surface)

    def update(self, dt, actions, tiles):
        '''
        Updates obj position, if obj is moving
        Handels inputs

        dt: delta time 
        actions: user inputs dictionary
        tiles: game levels collision tiles
        '''
        if not self.state['eliminated']:
            # only update if character is moving and on the screen
            if (self.x_speed != 0) or (self.y_speed != 0):
                # check if out of bounds on x axis
                if (self.x_pos < - self.CHARACTER_SIZE) or (self.x_pos > self.game_world.game.GAME_W):
                    self.out_of_bounds()
                # check if out of bounds on y axis
                elif self.y_pos > self.game_world.game.GAME_H:
                    self.out_of_bounds()
                else:
                    # moving and not out of bounds
                    self.state['moving'] = True
                    self.update_pos(dt, tiles)
                
            else:
                self.state['moving'] = False


            if not self.state['locked']:    
                self.handle_actions(actions)

            self.health_bar.update()

        # bug fixing
        # if self.state['choosing']:
        #     print(f'char state: {self.state}')

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


    def clicking(self, actions):
        '''
        handels hovered mouse clicks for Obj
        '''
        print(f'"CLICK!! : " {self.state}')
        # Selecting
        if not (self.state["jump"] or self.state["throw"]):
        # print("select condition met") 
            
            # store current state
            selected_state = self.state["selected"]
            choosing_state = self.state["choosing"]

            # reset every characters selected state
            for char in self.game_world.characters:
                char.state["selected"] = False
                char.state["choosing"] = False
                char.state["jump"] = False

            # reverse current state
            self.state["selected"] = not selected_state
            self.state["choosing"] = not choosing_state

            
            # print(f"state: {self.state}")

        # Jumping / entering into drag
        # requere new click
        if self.state["jump"] and not self.state["drag"]:
            if actions["mouse_click"]:
                self.mouse_pos_list = [actions["mouse_pos"]]
                self.state["drag"] = True

    def dragging(self, actions):
        '''
        handels what happens during the mousedrag

        actions: user inputs dictionary
        '''

        if self.state["drag"]:
            if actions["mouse_pressed"]:
                while len(self.mouse_pos_list) > 2:
                    self.mouse_pos_list.pop()
                self.mouse_pos_list.append(actions["mouse_pos"])
                # render line or arrow function
        
    def throw_bomb(self):
        '''
        spawns in bomb at the characters coordinates
        resets characters state
        '''
        x_pos = self.rect.centerx
        y_pos = self.rect.centery
            
        self.game_world.spawn_bomb(x_pos, y_pos)
        self.reset_state()

    def reset_pos(self):
        '''
        reset position
        '''
        # calculated values to origin
        self.x_pos = self.origin[0]
        self.y_pos = self.origin[1]
        # move rect to calculated values
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        # remove velocity
        self.x_speed = 0
        self.y_speed = 0.01
        # max hp
        self.current_hp = self.max_hp

    def take_damage(self, damage):

        '''
        react to taking damage

        damage: force of bomb
        '''
        self.current_hp -= min(50, 
                                    max(int(damage * 1.8), 10))
        if self.current_hp <= 0:
            self.eliminated()

        self.health_bar.activate()

    def eliminated(self):
        self.state['eliminated'] = True
        self.x_speed = 0
        self.y_speed = 0
        self.state['moving'] = False

    def out_of_bounds(self):
        self.eliminated()