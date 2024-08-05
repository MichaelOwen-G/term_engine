
import random
from typing import List
from engine.components.object import Object
from engine.effects.repeat_effect import RepeatEffect, RepeatType
from engine.metrics.duration import Duration
from pipe import BottomPipe, TopPipe


class PipeSpawner(RepeatEffect):

    def __init__(self, duration: Duration, once = True):
        # to keep count of spawned objects
        self.spawned_objects:int = 0

        # the space between the top and bottom pipes
        self.top_bottom_space: int = 12

        # minimum pipe height in percentage
        self.min_pipe_height:float = .1

        # max pipe height in percentage
        self.max_pipe_height: float = .6

        repeatType: RepeatType = RepeatType.INDEFINETLY_EVERY_DURATION

        super().__init__(repeatType, duration)

    def pipes_factory(self, dt, game) -> List[Object]:
        # randomise top pipe length
        top_pipe_height = random.randint(
            int(self.min_pipe_height * game.floor), 
            int(self.max_pipe_height * game.floor),
            )

        # calculate the bottom pipe height
        bottom_pipe_height =  game.floor - (top_pipe_height + self.top_bottom_space)

        print(f'TOP HEIGHT: {top_pipe_height}')

        # create top pipe
        top_pipe = TopPipe(top_pipe_height, 
                           x = game.window_width - 16, 
                           y = game.roof + 1,
                           )

        # create bottom pipe
        bottom_pipe = BottomPipe(bottom_pipe_height, 
                                 x = game.window_width - 16, 
                                 y = (game.floor - bottom_pipe_height) - 2,
                                 )

        return [top_pipe, bottom_pipe]
       

    def run(self, dt: int, game, object: None) -> None:

        super().run(dt, game, object)

        # spawn the object
        spawned_objects = self.pipes_factory(dt, game)

        # add the object to the game
        game.game_screen.addObjects(spawned_objects)

