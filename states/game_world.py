import pygame, json, os
from states.state import State
from character import Character
from bomb import Bomb
from button import Button



class Game_World(State):
    def __init__(self, game, level_name):
        super().__init__(game)
        # Teal
        self.BG_COL = (0, 153, 136) # (56, 175, 218) light blue
        self.BROWN = (181, 67, 0)
        self.tiles = []
        

        self.team_colours = [
        
        (204, 121, 167), # Purple
        (34, 136, 51), # Forest green
        (204, 51, 17), # Vibrant red
        (68, 119, 170), # Dark blue
        (255, 242, 89), # Yellow
        (0, 0, 0), # Black
        (230, 159, 0), # Orange
        (213, 94, 0) # Dark orange
        ] 

        self.characters = []
        self.bombs = []
        self.jump_button = Button(0, 0, image=self.game.assets['jump_img'])
        self.bomb_button = Button(0, 0, image=self.game.assets['bomb_img'])
        self.flag_button = Button(0, 0, image=self.game.assets['flag_img'])

        self.load_level(level_name)

    def update(self, delta_time, actions):
        '''
        update state
        call game objects update functions

        delta_time: dt
        actions: user inputs dictionary
        '''
        for char in self.characters:
            char.update(delta_time, actions, self.tiles)
        

    def render(self, surface):
        '''
        renders onto game canvas
        background, text, tiles, characters and bombs
        
        surface: surface to render on
        '''
        surface.fill((self.BG_COL))

        self.game.draw_text(surface, "Gameplay",
                             self.game.BLACK, self.game.GAME_W / 2,
                               self.game.GAME_H / 8)
        
        for tile in self.tiles:
            pygame.draw.rect(surface, self.BROWN, tile)
        
        self.render_characters(surface)

                
        for bomb in self.bombs:
            bomb.render(surface)

    def render_characters(self, surface):
        for char in self.characters:
            char.render(surface)
            if char.state["choosing"]:
                
                y = char.rect.y - self.jump_button.height - 10
                x_jump = char.rect.x - self.jump_button.width - 12

                if self.jump_button.action_on_button(x_jump, y, surface, self.game.actions):
                    char.state["jump"] = True
                    char.state["choosing"] = False

                x_bomb = x_jump + self.jump_button.width + 6
        
                if self.bomb_button.action_on_button(x_bomb, y, surface, self.game.actions):
                    char.state["jump"] = True
                    char.state["choosing"] = False

                x_flag = x_bomb + self.jump_button.width + 6
        
                if self.flag_button.action_on_button(x_flag, y, surface, self.game.actions):
                    char.state["jump"] = True
                    char.state["choosing"] = False
        
    def load_level(self, level_name):
        '''
        loads level data and stores it in tiles list as Rects
        creates needed instances:
        - characters

        level_name: filename with level data
        '''
        # level data
        path = os.path.join(self.game.tilemap_dir, level_name)

        with open(path, "r", encoding="utf-8") as f:
            level_data = json.load(f)

        for layer in level_data["layers"]:
            if layer["type"] == "objectgroup":
                for obj in layer["objects"]:
                    self.tiles.append(pygame.Rect(obj["x"], obj["y"], obj["width"], obj["height"]))

        # characters
        self.characters.append(Character(self, 0, 1, 240, 170))


    def spawn_bomb(self, x_pos, y_pos):
        '''
        creates an instance of Bomb and adds it to bombs list

        x & y: center coordinates of bomb
        '''
        self.bombs.append(Bomb(x_pos, y_pos, self.game.assets["bomb_img"]))

