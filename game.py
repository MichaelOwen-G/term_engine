from engine.components.object import TextBox
from engine.core import Game

from bird import Bird
from engine.metrics.duration import Duration, DurationMetrics
from pipe_spawner import PipeSpawner


class FlappyGuessGame(Game):
    def __init__(self):

        width = 90

        height = 35

        debug_mode = False

        frame_cap = 1000

        self.game_over_tag = 'game_over'

        super().__init__(width, height, debug_mode=debug_mode, frame_cap = frame_cap)

    def onLaunch(self):
        bird = Bird(x = 10, y = 2, tags = ['bird'])

        self.addObject(bird)

        pipe_spawner = PipeSpawner(Duration(DurationMetrics.SECONDS, 5), once=False)

        self.addEffect(pipe_spawner)

        super().onLaunch()


    def update(self, dt:int):
        # get the bird
        bird_res = self.find_objects_by_tag('bird')

        if len(bird_res) == 0: return

        bird: Bird = bird_res[0]

        if bird.dead:
            self.running = False
            self.game_over_message()

        else:
            self.remove_message()

    def game_over_message(self):
        # if not already in the game
        if len(self.find_objects_by_tag(self.game_over_tag)) >= 1: return

        gm_mes = TextBox('GAME OVER', tags = ['game_over', 'hud'], x = int(self.window_width / 2), y = int(self.window_height / 2) )

        self.addObject(gm_mes)

    def remove_message(self):
        if len(self.find_objects_by_tag(self.game_over_tag)) >= 1:
            self.find_objects_by_tag(self.game_over_tag)[0].dispose()
            


game = FlappyGuessGame()

game.run()