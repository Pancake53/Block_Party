from states.state import State

class Game_World(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, delta_time, actions):
        pass

    def render(self, surface):
        surface.fill((self.game.BLACK))
        self.game.draw_text(surface, "Gameplay",
                             self.game.WHITE, self.game.WINDOW_W / 2,
                               self.game.WINDOW_H / 2)