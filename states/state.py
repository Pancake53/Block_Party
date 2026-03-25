

class State():
    '''
    blueprint/parent state for all states
    '''
    def __init__(self, game):
        '''
        Init 
        
        game: game class
        '''
        self.game = game
        self.prev_state = None

    def update(self, delta_time, actions):
        '''
        updates state
        '''
        pass

    def render(self, surface):
        pass

    def enter_state(self):
        '''
        appends self to state stack
        '''
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)
        self.game.reset_keys()

    def exit_state(self):
        '''
        removes top state
        '''
        self.game.state_stack.pop()
        self.game.reset_keys()