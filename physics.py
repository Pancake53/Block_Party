


class Physics:
    # Game physics
    def __init__(self):
        # Gravity and throwing
        self.gravity = 250
        self.throw_multiplier = 2.5
        self.max_velocity = 330
        self.min_jump = 10

        # y bounce, lower value -> more small bounces
        self.y_stop = 20 
        self.y_speed = 0.1
        # x speed stopper, if x_speed < x_stop -> x_speed = 0
        self.x_stop = 1 
        # speed loss multiplier on collision
        self.retention = 0.25 

        # bomb damage
        self.force_mp = 250
        

        


        