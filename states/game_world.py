import pygame, json, os
from states.state import State
from character import Character



class Game_World(State):
    def __init__(self, game):
        super().__init__(game)
        self.BG_COLOUR = (56, 175, 218)
        self.BROWN = (245, 147, 49)
        self.tiles = []
        self.load_level("ship.json")
        self.character = Character(0, 1, 240, 150)

    def update(self, delta_time, actions):
        pass

    def render(self, surface):
        surface.fill((self.BG_COLOUR))
        self.game.draw_text(surface, "Gameplay",
                             self.game.BLACK, self.game.GAME_W / 2,
                               self.game.GAME_H / 4)
        for tile in self.tiles:
            pygame.draw.rect(surface, self.BROWN, tile)

        self.character.render(surface)
        
        
        
    def load_level(self, level_name):
        path = os.path.join(self.game.level_dir, level_name)

        with open(path, "r", encoding="utf-8") as f:
            level_data = json.load(f)

        for tile in level_data["tiles"]:
            self.tiles.append(pygame.Rect(tile[0], tile[1], tile[2], tile[3]))