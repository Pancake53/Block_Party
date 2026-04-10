import pygame, json, os

from states.state import State
from states.game_world import Game_World
from UI.button import Button
from helpers import draw_shading_for_rect

class Level_Menu(State):
    '''
    level menu for choosing level
    '''
    def __init__(self, game, created_chars):
        super().__init__(game)

        self.player_count = len(created_chars)
        self.created_chars = created_chars

        self.BROWN = (181, 67, 0)

        self.current_level = 0
        self.levels = []
        self.filenames = []

        self.left_arrow = None
        self.right_arrow = None
        
        self.load_classes() # Buttons
        self.load_levels()

    def update(self, delta_time, actions):
        '''
        updates state

        on start: creates and enters game world 
        (or level select menu in future)

        delta_time: dt
        actions: user inputs dictionary
        '''

        self.handle_actions(actions)
        
        self.game.reset_keys()

        if self.left_clicked:
            # first level loop around to last
            if self.current_level == 0:
                self.current_level = self.level_count - 1
            # continue normally if not first
            else:
                self.current_level -= 1

        if self.right_clicked:
            # at last level, loop to first
            if self.current_level == self.level_count - 1:
                self.current_level = 0
            else:
                self.current_level += 1

    def handle_actions(self, actions):
        if actions["start"]:
            new_state = Game_World(self.game,
                                    self.filenames[self.current_level],
                                       self.created_chars)
            new_state.enter_state()

        if actions["esc"]:
            self.exit_state()

    def render(self, surface):
        '''
        renders background and levels to choose from
        
        surface: surface to render on
        '''
        surface.fill((self.game.BLACK))
        self.game.draw_text(surface, "Select Level",
                             self.game.WHITE, self.game.GAME_W / 2,
                               self.game.GAME_H / 8)
        
        pygame.draw.rect(surface, self.game.BG_COL, self.level_bg)
        
        self.render_selected_level(surface)
        draw_shading_for_rect(self.game.WHITE, self.level_bg, surface, shading_W=4)

        self.render_buttons(surface)
        
    def render_selected_level(self, surface):
        '''
        renders tile data on screen
        '''
        for tile in self.levels[self.current_level]:
            pygame.draw.rect(surface, self.BROWN, tile)
            
    def render_buttons(self, surface):

        self.left_clicked = self.left_arrow.action_on_button(
            self.left_arrow_x,
            self.left_arrow_y, surface, self.game.actions)
        
        self.right_clicked = self.right_arrow.action_on_button(
            self.right_arrow_x,
            self.right_arrow_y, surface, self.game.actions)

    def load_classes(self):
        '''
        init needed classes and coordination calculations
        '''
        self.level_bg = pygame.Rect(self.game.GAME_W / 4, self.game.GAME_H / 4,
                                                  self.game.GAME_W / 2, self.game.GAME_H / 2)

        self.left_arrow = Button(0, 0, button_colour=(139, 139, 139),
                                  hover_colour=(50, 50, 50), image = 
                                 self.game.assets["arrowleft_img"])
        self.right_arrow = Button(0, 0, button_colour=(139, 139, 139),
                                  hover_colour=(50, 50, 50), image =
                                  self.game.assets["arrowright_img"])
        
        # calculate locations for buttons
        self.left_arrow_x = self.game.GAME_W / 6 - self.left_arrow.rect.width / 2
        self.left_arrow_y = self.game.GAME_H / 2 - self.left_arrow.rect.height / 2

        self.right_arrow_x = self.game.GAME_W * 5 / 6 - self.right_arrow.rect.width / 2
        self.right_arrow_y = self.game.GAME_H / 2 - self.right_arrow.rect.height / 2
        

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

            

            for layer in level_data["layers"]:
                if layer["type"] == "objectgroup":
                    for obj in layer["objects"]:

                        # tiles
                        if obj['type'] == "collision_tile":
                            tile = self.transform_level_data(obj)
                            tiles.append(tile)
                                
            self.levels.append(tiles)
        # variable for level count    
        self.level_count = len(self.levels)

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
    

