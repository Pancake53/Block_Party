import pygame, json, os, random
from states.state import State
from character import Character
from bomb import Bomb
from explosion import Explosion
from button import Button
from pygame.math import Vector2




class Game_World(State):
    def __init__(self, game, level_name, player_count=4):
        super().__init__(game)
        # Teal
        self.BG_COL = (0, 153, 136) # (56, 175, 218) light blue
        self.BROWN = (181, 67, 0)
        self.tiles = []
        

        self.player_count = player_count
        self.players_alive = [i for i in range(player_count)]

        # stores player character data as team_id: [characters]
        self.teams = {i: [] for i in range(self.player_count)}
        self.teams_not_eliminated = {}

        self.winner_id = None
        self.victory_messages = ['has won\nthe pissing contest', 
                            '\nate all the crayons', 
                            'wiped the\nfloor with his toes', 
                            'eats\ntheir nails', 
                            'is\nthe biggest nerd', 
                            'is\ngoofy as heck',
                            'claimed\nvictory royale',
                            '\nended it in style', 
                            'proved\nunstoppable',
                            'brought\nthe paintrain',
                            'sealed\ntheir enemies fate',
                            '\nreigned supreme',
                            'delivered\nthe final blow(job)',
                            '\nis the lash',
                            'is\nvery special']

        # Init needed classes
        self.load_entities()

        self.wrap_around = None
        self.load_level(level_name)

        # Game State
        self.state = {'turn': 0, 'selecting_locked': False, 'game_over': False}
        self.current_turn = 0
        self.round = int(self.state['turn'] 
                                    / self.player_count) + 1

    # update functions

    def update(self, delta_time, actions):
        '''
        update state
        call game objects update functions
        locks selecting if objects are moving 

        delta_time: dt
        actions: user inputs dictionary
        '''
        
        self.update_characters(delta_time, actions)
            
        self.bomb.update(delta_time, actions, self.tiles)

        self.explosion.update()
        self.handle_actions(actions)
        # print(self.game_state)

        if self.state['game_over']:
            self.update_winning()    

    def update_characters(self, delta_time, actions):
        '''
        calls characters update function
        locks character selection logic

        delta_time: dt
        actions: user inputs dictionary
        '''
        # Universal lock if char or bomb is moving
        #  or if bomb is being thrown
        characters_locked = self.check_for_character_lock()
        # update self.turn

        for id, team in self.teams_not_eliminated.items():
            turn_lock = (id != self.current_turn) # for each team
            for char in team:
                if characters_locked:
                    char.state['locked'] = characters_locked
                else: 
                    char.state['locked'] = turn_lock
                        
                char.update(delta_time, actions, self.tiles)
                char.health_bar.update()

    # render functions

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

        self.render_turn(surface)

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
        choosing_char = None
        for id, team in self.teams_not_eliminated.items():
            for char in team:
                char.render(surface)
                if char.state["choosing"]:
                    choosing_char = char
        if choosing_char:
            self.render_selections(choosing_char, surface)            
                    
    def render_selections(self, char, surface):
        '''
        renders selections
        handels state changes based on selection
        if char is near edges then alter the selection position
        
        char: character that is choosing
        surface: surface to render on
        '''
        padding = 6
        button_W = self.jump_button.width
        button_H = self.jump_button.height
        # char is next to left edge, render right
        if char.x_pos < button_W + padding * 4:
            # y
            y_jump = char.rect.centery - button_H - padding * 4
            y_bomb = y_jump + button_H + padding
            y_flag = y_bomb + button_H + padding
            # x
            x = char.rect.x + char.WIDTH + padding * 2
            x_jump = x_bomb = x_flag = x

        # char next to right edge, render left
        elif char.x_pos > self.game.GAME_W - (button_W + padding * 4):
            # y
            y_jump = char.rect.centery - button_H - padding * 4
            y_bomb = y_jump + button_H + padding
            y_flag = y_bomb + button_H + padding
            # x
            x = char.rect.x - button_W - padding * 2
            x_jump = x_bomb = x_flag = x


        # char next to top, render below
        elif char.y_pos < button_H * 2:
            # y
            y = char.rect.y + char.rect.height + padding * 2
            y_jump = y_bomb = y_flag = y
            # x
            x_jump = char.rect.x - button_W - padding * 2
            x_bomb = x_jump + button_W + padding
            x_flag = x_bomb + button_W + padding

        # render above, normal behavior
        else:
            # y
            y = char.rect.y - button_H - padding * 2
            y_jump = y_bomb = y_flag = y
            # x
            x_jump = char.rect.x - button_W - padding * 2
            x_bomb = x_jump + button_W + padding
            x_flag = x_bomb + button_W + padding

        if self.jump_button.action_on_button(x_jump, y_jump, surface, self.game.actions):
            # jump button pressed
            # set state to jump and choosing to false
            char.state["jump"] = True
            char.state["choosing"] = False
            

        if self.bomb_button.action_on_button(x_bomb, y_bomb, surface, self.game.actions):
            char.state["choosing"] = False
            char.state["throw"] = True
            

        if self.flag_button.action_on_button(x_flag, y_flag, surface, self.game.actions):
            char.state["choosing"] = False
            self.surrender(char.team_id)

    def render_turn(self, surface):
        '''
        render whose turn it is
        bottom left of screen
        '''
        colour = self.game.team_colours[self.current_turn]
        pygame.draw.rect(surface, colour, self.turn_rect)
        self.game.draw_text(surface,
                "turn", self.game.BLACK, 55, self.game.GAME_H - 32, "Medium")

    # load functions

    def load_entities(self):
        '''
        loads classes and pygame obj at the init of level
        '''
        self.bomb = Bomb(-36, -36, self, self.game.assets["bomb_img"])
        self.explosion = Explosion(self.game.assets['explosion_img'])
        self.jump_button = Button(0, 0, image=self.game.assets['jump_img'])
        self.bomb_button = Button(0, 0, image=self.game.assets['bomb_img'])
        self.flag_button = Button(0, 0, image=self.game.assets['flag_img'])    

        self.turn_rect = pygame.Rect(15, self.game.GAME_H - 45, 80, 30)

    def load_level(self, level_name):
        '''
        loads level data and stores it in tiles list as Rects
        creates needed instances:
        - characters
        - bomb

        level_name: filename with level data
        '''
        # level data
        path = os.path.join(self.game.level_dir, level_name)

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

        self.teams_not_eliminated = self.teams.copy()

        if level_name.split('.')[0] in ['tree of life', 'swords']:
            self.wrap_around = True
        # print(f'Level Loaded \nLevel Data:\n{self.teams}')

    def load_character(self, obj):
        '''
        loads character object into the level

        obj: data of character class from file

        has testing section for only spawning one character
        '''
        # team id of character
        player_id = int(obj["name"]) - 1
        if player_id not in self.players_alive:
            return

        one_char_per_player = False
        # TESTING SECTION COMMENT OUT LATER
        # if self.teams[player_id]: 
        #     one_char_per_player = True

        if not one_char_per_player:
            self.teams[player_id].append(
                # create character instances
                Character(player_id, # id
                        obj["x"], # x position
                        obj['y'], # y position
                        self)
            )

    # bomb / explosion

    def spawn_bomb(self, x_pos, y_pos):
        '''
        create an illusion of creating bomb
        handels bombs state, coordinates

        x & y: center coordinates of bomb
        '''
        # print(f'Spawning bomb')
        # state
        self.bomb.state["selected"] = True
        self.bomb.state["jump"] = True
        # rect x&y
        self.bomb.rect.centerx = x_pos 
        self.bomb.rect.centery = y_pos 

        # for calculations
        self.bomb.x_pos = self.bomb.rect.x 
        self.bomb.y_pos = self.bomb.rect.y 

        # check if bomb has spawned already colliding with a wall
        collisions = self.bomb.collision_test(self.tiles)
        if collisions:
            # print(f"Bomb collides w wall on spawn, fixing, collisions: {collisions}")
            self.bomb.fix_spawn(collisions)

        # bomb spawned normally

    def activate_explosion(self, x_pos, y_pos):
        '''
        activates bombs explosion animation
        handels hit registration
        
        x & y: center coordinates of explosion
        '''
        self.explosion.activate(x_pos, y_pos)

        hit_characters = []
        for id, team in self.teams_not_eliminated.items():
            for char in team:
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

            char.take_damage(force)
            # if still alive after taking damage
            if not char.state['eliminated']:
            
                char.x_speed = direction[0] * force
                char.y_speed = direction[1] * force     

    # actions

    def handle_actions(self, actions):

         # reset position (for testing)
        if actions["action1"]:
            self.reset_level()
        
        if actions["esc"]:
            self.exit_state()
            self.game.reset_keys()

    def reset_level(self):
        # reset characters to their original position and states
        for id, team in self.teams.items():
            for char in team:
                char.reset_pos()
                char.reset_state()

        self.state['turn'] = 0
        self.round = 0
        self.state['game_over'] = False
        self.players_alive = [i for i in range(self.player_count)]

        self.teams_not_eliminated = self.teams.copy()

    # locks & turn

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
        for id, team in self.teams_not_eliminated.items():
            for char in team:
                if char.state['moving']:
                    return True

        if self.bomb.state['selected']:
            return True
        
        if self.state['game_over']:
            return True
        
        return False
    
    def turn_based_lock(self):
        '''
        locks characters based on games turn state

        character: character which is being inspected
        '''
        self.current_turn = self.state['turn'] % self.player_count
        # reverse order on second round
        if self.round == 2:
            # select from the end of player count, so last player first then second to last
            self.current_turn = self.player_count - self.current_turn - 1
            # eliminated players turn
            while self.current_turn not in self.players_alive:
                # change turn will we get a valid turn
                self.next_turn()
                self.current_turn = self.player_count - self.state['turn'] % self.player_count

            return
        
        # normal order
        
        # eliminated players turn
        while self.current_turn not in self.players_alive:
            # change turn will we get a valid turn
            self.state['turn'] += 1
            self.current_turn = self.state['turn'] % self.player_count

        return 
            
    def next_turn(self):
        '''
        update turn and round after an action
        '''
        self.state['turn'] += 1
        self.round = int(self.state['turn'] 
                                    / self.player_count) + 1
        
        self.turn_based_lock()

    # checks

    def check_for_player_eliminated(self, char_eliminated):
        '''
        checks if one players all characters are eliminated

        char_eliminated: character that was eliminated

        if player eliminated then change turn logic and check for win
        '''
        print("checking for player elimination")

        # eliminated characters team
        player_id = char_eliminated.team_id

        teams_chars_alive = False

        for char in self.teams_not_eliminated[player_id]:
            if not char.state['eliminated']:
                teams_chars_alive = True

        # if list not empty, update characters_not_eliminated and quit check
        if teams_chars_alive:
            # update teams & chars that are not eliminated
            self.teams_not_eliminated[player_id].remove(char_eliminated)
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
        match len(self.players_alive): # eliminated list is not empty
            # len of teams alive is one, only one team left
            case 1:
                self.state['game_over'] = True
                self.winner_id = self.players_alive[0] + 1
                # select at random one of the victory messages
                self.displayed_message = self.victory_messages[random.randint(0, len(self.victory_messages) - 1)]
                
            case 0:
                self.state['game_over'] = True
                print('DRAW') # logically impossible

    # winning

    def update_winning(self):
        '''
        characters jumping from joy after winning
        '''
        for id, team in self.teams_not_eliminated.items():
            for char in team:
                # if not moving then jump
                if not char.state['moving']:
                    char.y_speed -= random.randint(50, 150)

    def render_winning(self, surface):
        '''
        difines what happens when someone wins        
        '''

        text = f'Player {self.winner_id} {self.displayed_message}'
        self.game.draw_text(surface, text, self.game.BLACK, self.game.GAME_W / 2, self.game.GAME_H / 2)

    def surrender(self, player_id):
        '''
        handels logic for surrendering

        player_id: id of player who pressed the surrender button
        '''
        # change character states
        for char in self.teams[player_id]:
            char.state['eliminated'] = True
            char.x_speed = 0
            char.y_speed = 0
            char.state['moving'] = False
        # remove from alive
        self.players_alive.remove(player_id)
        # check for win
        self.check_for_win()
        self.next_turn()