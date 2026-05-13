

class State():
    '''
    blueprint/parent state for all states
    '''
    def __init__(self, game):
        '''
        Init 
        
        game: game class
        '''
        self.cursor = 'default'
        self.game = game
        self.prev_state = None
        result = None
        self.images = []

    def update(self, delta_time, actions):
        '''
        updates state
        '''
        pass

    def render(self, surface):
        pass



    def on_return(self, returned):
        '''
        handels overlay passing in information
        '''
        print(f'something returned: {returned} to state: {self}')