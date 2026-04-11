


class Physics:
    # Game physics
    def __init__(self):
        # CONSTANTS

        # y bounce, lower value -> more small bounces
        self.Y_STOP = 50 
        # x speed stopper, if x_speed < x_stop -> x_speed = 0
        self.X_STOP = 1 
        self.MIN_JUMP = 15

        # VARIABLES

        # Gravity and throwing
        self.gravity = 250
        self.throw_multiplier = 2.5
        self.max_velocity = 330 # throw vector 
        # * throw multiplier lenght
        self.max_arrow_len = self.max_velocity / self.throw_multiplier

        # speed loss multiplier on collision
        self.retention = 0.25 

        # bomb damage multip (divided by distance)
        self.force_of_exp = 250
        

        


        