

class Settings():
    def __init__(self):

        # Audio
        self.master_volume = 0.5
        self.music_volume = 0.5
        self.sfx_volume = 0.6
        self.dialogue_volume = 0.8

        self.mute = False
        self.skip_dialogue = False

        # screen
        self.FULLSCREEN = False
        self.SCREEN_W = 960
        self.SCREEN_H = 540

        # 
        self.stick_speed = 500
        self.deadzone = 0.05
        self.low_speed_deadzone = .3
        self.high_speed_deadzone = .9