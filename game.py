import time
from engine.components.object import TextBox
from engine.core import Game, GameScreen

from bird import Bird
from engine.metrics.duration import Duration, DurationMetrics
from pipe_spawner import PipeSpawner

class MyGame(Game):
    def __init__(self):

        width = 90

        height = 35

        debug_mode = False

        frame_cap = 1000

        self.game_over_tag = 'game_over'
        
        self.sound_track_path = 'sound_track.mp3'
        
        self.fail_sound_path = 'die.mp3'

        super().__init__(width, height, debug_mode=debug_mode, frame_cap = frame_cap)

    def onLaunch(self):
        self.sound_track = self.load_sound(self.sound_track_path)
        self.sound_track.play()
        
        self.fail_sound = self.load_sound(self.fail_sound_path)
        
        bird = Bird(x = 10, y = 2, tags = ['bird'])
        self.addObject(bird)

        pipe_spawner = PipeSpawner(Duration(DurationMetrics.SECONDS, 5), once=False)
        self.addEffect(pipe_spawner)

        # add hud
        # points textbox
        points = TextBox(f'{bird.points}     points', tags=['hud', 'points'], x = self.window_width - 12, y = self.roof + 2, priority=2)
        self.addObject(points)

        super().onLaunch()

    def update(self, dt:int):
        # get the bird
        bird_res = self.find_objects_by_tag('bird')

        if len(bird_res) == 0: return

        bird: Bird = bird_res[0]

        # add points to the 
        p_res = self.find_objects_by_tag('points')

        if len(p_res) == 0: return

        points = p_res[0]

        # points.text = f'{bird.points} points'

        if bird.dead:
            self.sound_track.stop()
            self.game_over_message()
            self.fail_sound.play()
            
            self.running = False

        else:
            self.remove_message()

        super().update(dt)

    def game_over_message(self):
        # if not already in the game
        if len(self.find_objects_by_tag(self.game_over_tag)) >= 1: return

        gm_mes = TextBox('GAME OVER', 
                         tags = ['game_over', 'hud'], 
                         x = int(self.window_width / 2), 
                         y = int(self.window_height / 2),
                         priority = 1)

        self.addObject(gm_mes)

    def remove_message(self):
        if len(self.find_objects_by_tag(self.game_over_tag)) >= 1:
            self.find_objects_by_tag(self.game_over_tag)[0].dispose()
            


game = MyGame()

game.run()