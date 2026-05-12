import pygame, os
from dataclasses import dataclass

@dataclass
class AudioManager():
    settings: object
    audio_dir: object
    sound_fx_dir: object

    def __post_init__(self):
        
        self.audio_muted = False
        self.old_master_value = self.settings.master_volume
        self.music_muted = False

        self.load_audio()

    def play_music(self, audio_context, loops=-1):
        '''
        plays audio if audio exists in files

        audio_name: filename of played audio
        loops: looping mechanism (-1 = forever, 0 = once)
        '''
        if audio_context not in self.MUSIC:
            print(f'Music context not found: {audio_context}')
            return
        
        self.current_track = self.MUSIC[audio_context]['track']
        self.track_volume = self.MUSIC[audio_context]['volume']

        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.load(self.current_track)
        pygame.mixer.music.play(loops)
        self.change_volume('music')
        

    def change_volume(self, type):
        '''
        volume of audio

        type: which audio type to change volume (music, sounds or narrating)
        '''
        match type:
            case 'music':
                pygame.mixer.music.set_volume(
                    self.settings.music_volume
                    * self.settings.master_volume 
                    * self.track_volume)
                
            case _:
                print('Invalid type input in change_volume')

    def toggle_mute(self):

        self.audio_muted = not self.audio_muted

        if self.audio_muted:
            pygame.mixer.music.set_volume(0)
            self.old_master_value = self.settings.master_volume
            self.settings.master_volume = 0

        else: # audio unmuted
            self.settings.master_volume = self.old_master_value
            self.change_volume('music')
            


    def toggle_music(self):

        self.music_muted = not self.music_muted

        if self.music_muted:
            pygame.mixer.music.set_volume(0)

        else: # music unmuted
            self.change_volume('music')

    def play_sfx(self, name):

        '''
        playes sound effect

        
        sound: effect_name from SFX dictionary
        
        '''
        self.SFX[name].play()
        self.SFX[name].set_volume(
            self.settings.master_volume * self.settings.sfx_volume)

    def load_audio(self):

        # music 
        pygame.mixer.init()
        self.audio = {}
        self.SFX = {}
        # audio
        self.audio['main_theme'] = os.path.join(self.audio_dir, 'main_music.ogg')
        self.audio['sea_ambiance'] = os.path.join(self.audio_dir, 'sea_ambiance.ogg')
        self.audio['smile'] = os.path.join(self.audio_dir, 'smile.ogg')
        self.audio['middle_ages'] = os.path.join(self.audio_dir, 'middle_ages.ogg')
        self.audio['mystical_forest'] = os.path.join(self.audio_dir, 'mystical_forest.ogg')
        # sound fx
        self.audio['explosion'] = os.path.join(self.sound_fx_dir, 'explosion.wav')
        self.audio['jump'] = os.path.join(self.sound_fx_dir, 'jump.aiff')
        self.audio['bump'] = os.path.join(self.sound_fx_dir, 'bump.aiff')
        self.audio['tackle'] = os.path.join(self.sound_fx_dir, 'tackle.wav')
        self.audio['menu_click'] = os.path.join(self.sound_fx_dir, 'menu_click.wav')
        self.audio['max_hit'] = os.path.join(self.sound_fx_dir, 'max_hit_cheer.wav')

        fxs = ['explosion', 'jump', 'bump', 'tackle', 'menu_click', 
               'max_hit']
        for fx in fxs:
            self.add_sfx(fx)

        self.MUSIC = {
            'menu' : 
                {'track' : self.audio['main_theme'], 'volume': 0.5},
           'ship.tmj' : 
                {'track' : self.audio['sea_ambiance'], 'volume':  1.5},
           'shipwreck.tmj' : 
                {'track' : self.audio['sea_ambiance'], 'volume':  1.5},
           'smily.tmj' : 
                {'track' : self.audio['smile'], 'volume':  0.7},
           'swords.tmj' :
                {'track' : self.audio['middle_ages'], 'volume':  1.2},
           'tree of life.tmj' :
                {'track' : self.audio['mystical_forest'], 'volume':  0.8}
        }

        self.play_music('menu')

        

    def add_sfx(self, name):
        self.SFX[name] = pygame.mixer.Sound(
            self.audio[name])