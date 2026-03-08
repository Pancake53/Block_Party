from states.state import State
from states.game_world import Game_World

class Title(State):
    '''
    title screen
    '''
    def __init__(self, game):
        super().__init__(game)

    def update(self, delta_time, actions):
        '''
        updates state

        on start: creates and enters game world 
        (or level select menu in future)

        delta_time: dt
        actions: user inputs dictionary
        '''
        if actions["start"]:
            new_state = Game_World(self.game, "ship.tmj")
            new_state.enter_state()
        self.game.reset_keys()

    def render(self, surface):
        '''
        renders background and title on the screen
        
        surface: surface to render on
        '''
        surface.fill((self.game.BLACK))
        self.game.draw_text(surface, "Mutiny Downmaster",
                             self.game.WHITE, self.game.GAME_W / 2,
                               self.game.GAME_H / 2)