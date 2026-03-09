from pygame import Vector2 


    # def add_momentum(self, x_speed, y_speed): 
    #     ''' 
    #     give gameObject clamped x and y momentum

    #     x_speed: given speed on x axis
    #     y_speed: given speed on y axis
    #     '''

    #     speed_vec = Vector2(x_speed, y_speed)
    #     total_speed = speed_vec.length()

    #     if total_speed > self.max_velocity:
    #         normalized = speed_vec.normalize()
    #         speed_vec = self.max_velocity * normalized

    #     self.x_speed = speed_vec[0]
    #     self.y_speed = speed_vec[1]


def test_add_momentum():
    x, y = 2, 2
    speed_vec = Vector2(x, y)
    total_speed = speed_vec.length()
    
    assert x + y == 4