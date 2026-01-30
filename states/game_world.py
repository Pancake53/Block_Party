import pygame, json, os
from states.state import State
from character import Character
from bomb import Bomb



class Game_World(State):
    def __init__(self, game):
        super().__init__(game)
        self.BG_COLOUR = (56, 175, 218)
        self.BROWN = (245, 147, 49)
        self.tiles = []
        self.load_level("ship..tmj")
        self.characters = [Character(self, 0, 1, 240, 170)]
        self.bombs = []

    def update(self, delta_time, actions):
        for char in self.characters:
            char.update(delta_time, actions, self.tiles)

    def render(self, surface):
        surface.fill((self.BG_COLOUR))
        self.game.draw_text(surface, "Gameplay",
                             self.game.BLACK, self.game.GAME_W / 2,
                               self.game.GAME_H / 8)
        for tile in self.tiles:
            pygame.draw.rect(surface, self.BROWN, tile)

        for char in self.characters:
            char.render(surface)
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