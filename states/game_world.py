import pygame, json, os
from states.state import State
from character import Character
from bomb import Bomb
from button import Button



class Game_World(State):
    def __init__(self, game):
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

        self.characters = [Character(self, 0, 1, 240, 170)]
        self.bombs = []
        self.button_choices = []
        self.button = Button(100, 100, 30, 30)

        self.load_level("ship.tmj")

    def update(self, delta_time, actions):
        for char in self.characters:
            char.update(delta_time, actions, self.tiles)
        

    def render(self, surface):

        surface.fill((self.BG_COL))
        self.game.draw_text(surface, "Gameplay",
                             self.game.BLACK, self.game.GAME_W / 2,
                               self.game.GAME_H / 8)
        for tile in self.tiles:
            pygame.draw.rect(surface, self.BROWN, tile)
        

        for char in self.characters:
            char.render(surface)
            if char.state["choosing"]:
                if self.button.action_on_button(100, 100, surface, self.game.actions):
                    char.state["jump"] = True
                    char.state["choosing"] = False
                
        for bomb in self.bombs:
            bomb.render(surface)

        
        
        
        
    def load_level(self, level_name):
        path = os.path.join(self.game.tilemap_dir, level_name)

        with open(path, "r", encoding="utf-8") as f:
            level_data = json.load(f)

        for layer in level_data["layers"]:
            if layer["type"] == "objectgroup":
                for obj in layer["objects"]:
                    self.tiles.append(pygame.Rect(obj["x"], obj["y"], obj["width"], obj["height"]))



    def spawn_bomb(self, x_pos, y_pos):
        self.bombs.append(Bomb(x_pos, y_pos, self.game.assets["bomb"]))

    def render_selections(self, x, y):
        for count, button in enumerate(self.button_choices):
            pass