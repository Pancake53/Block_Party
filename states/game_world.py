import pygame, json, os, random
from states.state import State
from character import Character
from bomb import Bomb
from explosion import Explosion
from button import Button
from pygame.math import Vector2




class Game_World(State):
    def __init__(self, game, level_name, player_count=3):
        super().__init__(game)
        # Teal
        self.BG_COL = (0, 153, 136) # (56, 175, 218) light blue
        self.BROWN = (181, 67, 0)
        self.tiles = []
        

        self.team_colours = [
        
        (204, 121, 167), # Purple
        (34, 136, 51), # Forest green
        
        (68, 119, 170), # Dark blue
        (255, 242, 89), # Yellow
        (0, 0, 0), # Black
        (230, 159, 0), # Orange
        (213, 94, 0), # Dark orange
        (204, 51, 17) # Vibrant red
        ] 

        self.characters = []
        self.characters_not_eliminated = []
        self.winner_id = 0
        self.victory_messages = ['has won\nthe pissing contest', 
                            '\nate all the crayons', 
                            'wiped the\nfloor with his toes', 
                            'crushed\nall opposition', 
                            'left\nno survivors', 
                            'dominated\nopposing force',
                            'claimed\ntotal victory',
                            '\nended it in style', 
                            'proved\nunstoppable',
                            'brought\nthe paintrain',
                            'sealed\ntheir enemies fate',
                            '\nreigned supreme',
                            'delivered\nthe final blow(job)',
                            '\nis the lash',
                            'is\n very special']

        self.bomb = Bomb(-36, -36, self, self.game.assets["bomb_img"])
        self.explosion = Explosion(self.game.assets['explosion_img'])
        self.jump_button = Button(0, 0, image=self.game.assets['jump_img'])
        self.bomb_button = Button(0, 0, image=self.game.assets['bomb_img'])
        self.flag_button = Button(0, 0, image=self.game.assets['flag_img'])

        self.player_count = player_count
        self.players_alive = [i for i in range(player_count)]
        self.load_level(level_name)
        

        self.state = {'turn': 0, 'selecting_locked': False, 'game_over': False}

    def update(self, delta_time, actions):
        '''
        update state
        call game objects update functions
        locks selecting if objects are moving 

        delta_time: dt
        actions: user inputs dictionary
        '''
        
        characters_locked = self.check_for_character_lock()
        
        for char in self.characters:
            # Universal lock if char or bomb is moving
            #  or if bomb is being thrown
            char.state['locked'] = characters_locked
            if not characters_locked:
                char.state['locked'] = self.turn_based_lock(char)
            char.update(delta_time, actions, self.tiles)
            char.health_bar.update()
        
        self.bomb.update(delta_time, actions, self.tiles)

        self.explosion.update()
        self.handle_actions(actions)
        # print(self.game_state)

        if self.state['game_over']:
            self.update_winning()
        

    def render(self, surface):
        '''
        renders onto game canvas
        background, text, tiles, characters and bomb
        
        surface: surface to render on
        '''
        surface.fill((self.BG_COL))

        self.game.draw_text(surface, "Gameplay",
                             self.game.BLACK, self.game.GAME_W / 2,
                               self.game.GAME_H / 8)
        
        # collision tiles
        for tile in self.tiles:
            pygame.draw.rect(surface, self.BROWN, tile)

        # characters
        self.render_characters(surface)
        # bomb
        self.bomb.render(surface)
        # explosion
        self.explosion.render(surface)

        if self.state['game_over']:
            self.render_winning(surface)

    def render_characters(self, surface):
        '''
        renders characters and calls render_selections
        
        surface: surface to render on
        '''
        for char in self.characters:
            char.render(surface)
            if char.state["choosing"]:
                self.render_selections(char, surface)
                
    def render_selections(self, char, surface):
        '''
        renders selections
        handels state changes based on selection
        
        char: character that is choosing
        surface: surface to render on
        '''
        y = char.rect.y - self.jump_button.height - 10
        x_jump = char.rect.x - self.jump_button.width - 12

        if self.jump_button.action_on_button(x_jump, y, surface, self.game.actions):
            # jump button pressed
            # set state to jump and choosing to false
            char.state["jump"] = True
            char.state["choosing"] = False
            

        x_bomb = x_jump + self.jump_button.width + 6

        if self.bomb_button.action_on_button(x_bomb, y, surface, self.game.actions):
            char.state["throw"] = True
            

        x_flag = x_bomb + self.jump_button.width + 6

        if self.flag_button.action_on_button(x_flag, y, surface, self.game.actions):
            char.state["jump"] = True
            char.state["choosing"] = False
        
    def load_level(self, level_name):
        '''
        loads level data and stores it in tiles list as Rects
        creates needed instances:
        - characters
        - bomb

        level_name: filename with level data
        '''
        # level data
        path = os.path.join(self.game.tilemap_dir, level_name)

        with open(path, "r", encoding="utf-8") as f:
            level_data = json.load(f)

        for layer in level_data["layers"]:
            if layer["type"] == "objectgroup":
                for obj in layer["objects"]:

                    # tiles
                    if obj['type'] == "collision_tile":
                        self.tiles.append(
                            pygame.Rect(obj["x"], obj["y"],
                                obj["width"], obj["height"])
                        )
                        
                    # playable characters
                    if obj['type'] == "character":
                        self.load_character(obj)

    def load_character(self, obj):
        '''
        loads character object into the level

        obj: data of character class from file

        has testing section for only spawning one character
        '''
        # team id of character
        player_id = int(obj["name"]) - 1
        
        one_char_per_player = False
        # TESTING SECTION COMMENT OUT LATER
        for char in self.characters: 
            if char.team_id == player_id: 
                one_char_per_player = True

        if not one_char_per_player:
            self.characters.append(
                # create character instances
                Character(player_id, # id
                        obj["x"], # x position
                        obj['y'], # y position
                        self)
            )

    def spawn_bomb(self, x_pos, y_pos):
        '''
        create an illusion of creating bomb
        handels bombs state, coordinates

        x & y: center coordinates of bomb
        '''
        # state
        self.bomb.state["selected"] = True
        self.bomb.state["jump"] = True
        # rect x&y
        self.bomb.rect.centerx = x_pos 
        self.bomb.rect.centery = y_pos 
        # for calculations
        self.bomb.x_pos = self.bomb.rect.x 
        self.bomb.y_pos = self.bomb.rect.y 

    def activate_explosion(self, x_pos, y_pos):
        '''
        activates bombs explosion animation
        handels hit registration
        
        x & y: center coordinates of explosion
        '''
        self.explosion.activate(x_pos, y_pos)

        hit_characters = []
        for char in self.characters:
            if char.rect.colliderect(self.explosion):
                hit_characters.append(char)

        if hit_characters:
            self.explosion_calculations(x_pos, y_pos, hit_characters)

    def explosion_calculations(self, x_pos, y_pos, hit_characters):
        '''
        handels reacting to bomb explosion if it is near characters

        x & y: center coordinates of explosion
        hit_characters: list of hit characters
        '''
        explosion_pos = Vector2(x_pos, y_pos)

        for char in hit_characters:
            char_pos = Vector2(char.rect.centerx,
                                char.rect.centery)
            
            direction = char_pos - explosion_pos
            distance = max(direction.length(), 1)
            force = char.force_mp / distance
            print(f'force: {force}')
            char.x_speed = direction[0] * force
            char.y_speed = direction[1] * force

            char.take_damage(force)
            
    def handle_actions(self, actions):

         # reset position (for testing)
        if actions["action1"]:
            self.reset_level()

    def reset_level(self):
        # reset characters to their original position and states
        for char in self.characters:
                char.reset_pos()
                char.reset_state()

        self.state['turn'] = 0
        self.state['game_over'] = False
        self.players_alive = [i for i in range(self.player_count)]

    def check_for_character_lock(self):
        '''
        checks for ongoing events
        - movement
        - bomb selected

        return:
        boolean
        - True if there is an ongoing event
        - False if no actions
        '''
        for char in self.characters:
            if char.state['moving']:
                return True

        if self.bomb.state['selected']:
            return True
        
        if self.state['game_over']:
            return True
        
        return False
    
    def turn_based_lock(self, character):
        '''
        locks characters based on games turn state
        return True if it is not teams turn

        character: character which is being inspected
        '''
        turn = self.state['turn'] % self.player_count
        # eliminated players turn
        while turn not in self.players_alive:
            # change turn will we get a valid turn
            self.state['turn'] += 1
            turn = self.state['turn'] % self.player_count

        return turn != character.team_id
            
    def check_for_player_eliminated(self, player_id):
        '''
        checks if one players all characters are eliminated

        player_id: player id

        if player eliminated then change turn logic and check for win
        '''
        print("checking for player elimination")
        # update list of characters that are not eliminated
        self.characters_not_eliminated = [char for char in self.characters if not char.state['eliminated']]
        # eliminated characters team
        teams_chars_alive = [char for char in self.characters_not_eliminated if char.team_id == player_id]

        # if list not empty quit check
        if teams_chars_alive:
            return
        
        # list empty, player eliminated
        self.players_alive.remove(player_id)
        print(f'Player eliminated, alive ids: {self.players_alive}')
        self.check_for_win()
    
    def check_for_win(self):
        '''
        checks remaining characters are all from one team

        only runs on character elimination
        '''
        
        print('checking win conditions')
        # check for winning conditions
        if len(self.characters_not_eliminated) > 0: # eliminated list is not empty
            # all characters team id is the same as first ones 
            if all(char.team_id == self.characters_not_eliminated[0].team_id 
                    for char in self.characters_not_eliminated):
                self.state['game_over'] = True
                self.winner_id = self.characters_not_eliminated[0].team_id + 1
                # select at random one of the victory messages
                self.displayed_message = self.victory_messages[random.randint(0, len(self.victory_messages) - 1)]
                
        else:
            print('DRAW') # logically impossible

    def update_winning(self):
        '''
        characters jumping from joy after winning
        '''
        for char in self.characters_not_eliminated:
            # if not moving then jump
            if not char.state['moving']:
                char.y_speed -= random.randint(50, 150)

    def render_winning(self, surface):
        '''
        difines what happens when someone wins        
        '''

        text = f'Player {self.winner_id} {self.displayed_message}'
        self.game.draw_text(surface, text, self.game.BLACK, self.game.GAME_W / 2, self.game.GAME_H / 2)


        