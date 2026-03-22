import pygame, json, os

from states.state import State
from states.game_world import Game_World


class Level_Menu(State):
    '''
    title screen
    '''
    def __init__(self, game):
        super().__init__(game)

        self.BROWN = (181, 67, 0)
        self.BG_COL = (0, 153, 136)

        self.current_level = 0
        self.levels = []
        self.filenames = []
        self.load_levels()

    def update(self, delta_time, actions):
        '''
        updates state

        on start: creates and enters game world 
        (or level select menu in future)

        delta_time: dt
        actions: user inputs dictionary
        '''
        if actions["start"]:
            new_state = Game_World(self.game, self.filenames[self.current_level])
            new_state.enter_state()
        self.game.reset_keys()

    def render(self, surface):
        '''
        renders background and levels to choose from
        
        surface: surface to render on
        '''
        surface.fill((self.game.BLACK))
        self.game.draw_text(surface, "Select Level",
                             self.game.WHITE, self.game.GAME_W / 2,
                               self.game.GAME_H / 8)
        
        self.render_selected_level(surface)
        
    def render_selected_level(self, surface):
        for i, tile in enumerate(self.levels[self.current_level]):
            if i == 0:
                pygame.draw.rect(surface, self.BG_COL, tile)
            else:
                pygame.draw.rect(surface, self.BROWN, tile)
            

    def load_levels(self):
        '''
        loads levels tile data for level selection
        '''

        print("Loading levels...")

        for file in os.listdir(self.game.level_dir):
            path = os.path.join(self.game.level_dir, file)

            self.filenames.append(file)

            with open(path, "r", encoding="utf-8") as f:
                level_data = json.load(f)

            tiles = []

            tiles.append(pygame.Rect(self.game.GAME_W / 4, self.game.GAME_H / 4, self.game.GAME_W / 2, self.game.GAME_H / 2))

            for layer in level_data["layers"]:
                if layer["type"] == "objectgroup":
                    for obj in layer["objects"]:

                        # tiles
                        if obj['type'] == "collision_tile":
                            tile = self.transform_level_data(obj)
                            tiles.append(tile)
                                
            self.levels.append(tiles)

    def transform_level_data(self, tile):
        '''
        transforms one tile coordinates and
        dimensions for level select display

        tile: data for one tile

        return Rect obj of tile
        '''
        x_center = tile['x'] + tile['width'] / 2
        y_center = tile['y'] + tile['height'] / 2

        x_distance_from_center = self.game.GAME_W / 2 - x_center 
        y_distance_from_center = self.game.GAME_H / 2 - y_center

        x_center += x_distance_from_center / 2
        y_center += y_distance_from_center / 2

        width = tile['width'] / 2
        height = tile['height'] / 2

        x = x_center - width / 2
        y = y_center - height / 2

        return pygame.Rect(x, y, width, height)