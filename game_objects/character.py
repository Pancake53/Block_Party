import pygame
from game_objects.gameObject import GameObject
from UI.healthBar import HealthBar
from pygame.math import Vector2

class Character(GameObject):
    '''
    In game character which players have many at the beginning of a round

    Handels rendering, updating pos, collision testing,
      action such as selecting, jumping, spawning in bomb
    
    '''
    def __init__(self, team_id, x_pos, y_pos, game_world):
        '''Initialize attributes

        game_world: level the character loads into
        team_id: team number
        characters width
        x & y position
        
        '''
        super().__init__(x_pos, y_pos, game_world)
        self.team_id = team_id
        

        # Character colour based on team id
        self.colour = self.game_world.created_chars[team_id]['main_colour']
        
        # make fall down from spawn location
        self.y_speed = 0.01
        
        self.WIDTH = self.CHARACTER_SIZE
        self.HEIGHT = self.CHARACTER_SIZE * 2
        self.rect = pygame.Rect(x_pos, y_pos, self.WIDTH, self.HEIGHT)
       
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
            self.update_chosen(dt, actions, tiles)
            self.health_bar.update()

        
    def collision_x_axis(self, collisions):
        '''
        reaction to collision on x axis
        
        collisions: list of overlapping tiles
        '''
        for tile in collisions:
            if self.x_speed > 0:
                # print("colliding w left wall")
                self.rect.right = tile.left # colliderect => False
                self.x_screen = self.rect.x
            elif self.x_speed < 0:
                # print("colliding w right wall")
                self.rect.left = tile.right # colliderect => False
                self.x_screen = self.rect.x

        self.x_speed = - self.x_speed * self.game_world.physics.retention
        self.y_speed *= self.game_world.physics.retention # also reduce y speed, MAY NEED TWEAKING

    def collision_y_axis(self, collisions):
        '''
        reaction to collision on y axis
        
        collisions: list of overlapping tiles
        '''
        tile = collisions[0]
        # print(f'collision on y-axis, char pos: {self.x_screen, self.y_screen}, tile pos: {tile.x, tile.y}')
        self.x_speed *= self.game_world.physics.retention # also reduce x speed, MAY NEED TWEAKING

        if self.y_speed > self.game_world.physics.Y_STOP: 
            # top
            # print(f"colliding w top of tile, y: {round(self.y_speed,3)}, x: {round(self.x_speed,3)}")
            self.rect.bottom = tile.top
            self.y_screen = self.rect.y
            self.y_speed = self.y_speed * -1 * self.game_world.physics.retention
        elif -self.y_speed > 0: 
            # bottom
            # print("colliding w bottom of tile")
            self.rect.top = tile.bottom
            self.y_screen = self.rect.y
            self.y_speed = self.y_speed * -1 * self.game_world.physics.retention / 2
        else:
            # top little momentum so momentum to 0
            # print("y_speed 0")
            self.rect.bottom = tile.top
            self.y_screen = self.rect.y
            self.y_speed = 0

    def clicking(self, actions):
        '''
        handels hovered mouse clicks for Obj

        own function because reverses
            all own players characters states on click
        '''
        
        # Selecting
        if not (self.state["jump"] or self.state["throw"]):
        # print("select condition met") 
            
            # store current state
            selected_state = self.state["selected"]
            choosing_state = self.state["choosing"]

            # reset every characters selected state
            for char in self.game_world.teams_not_eliminated[self.team_id]:
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
                self.throwing_list = []
                self.state["drag"] = True


        
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
        reset position for restarting round
        full hp
        '''
        # calculated values to origin
        self.x_screen = self.origin[0]
        self.y_screen = self.origin[1]
        # move rect to calculated values
        self.rect.x = self.x_screen
        self.rect.y = self.y_screen
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
        damage = min(50, # max
            max(int(damage * 1.8), # scale
            10)) # min
        
        if self.game_world.round >= 3:
            if damage == 50:
                self.game_world.grant_another_turn()

        self.current_hp -= damage
        if self.current_hp <= 0:
            self.eliminated()

        self.health_bar.activate()

    def eliminated(self):
        self.state['eliminated'] = True
        self.x_speed = 0
        self.y_speed = 0
        self.state['moving'] = False

        # checks if all players characters are eliminated
        self.game_world.check_for_player_eliminated(self)

