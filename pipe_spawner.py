
import random
from typing import List
from engine.components._interfaces import ObjectInterface
from engine.components.object import Object
from engine.effects.repeat_effect import RepeatEffect, RepeatType
from engine.metrics.duration import Duration
from pipe import BottomPipe, TopPipe


class PipeSpawner(RepeatEffect):

    def __init__(self, duration: Duration):
        # to keep count of spawned objects
        self.spawned_objects:int = 0

        # the space between the top and bottom pipes
        self.top_bottom_space: int = 10

        # minimum pipe height in percentage
        self.min_pipe_height:float = .2

        # max pipe height in percentage
        self.max_pipe_height: float = .6

        repeatType: RepeatType = RepeatType.ONCE_IN_DURATION

        super().__init__(repeatType, duration)

    def pipes_factory(self, dt, game) -> List[Object]:
        # randomise top pipe length
        top_pipe_height = random.randint(
            int(self.min_pipe_height * game.window_height), 
            int(self.max_pipe_height * game.window_height),
            )

        # calculate the bottom pipe height
        bottom_pipe_height =  game.window_height - (top_pipe_height + self.top_bottom_space)

        print(f'TOP HEIGHT: {top_pipe_height}')

        # create top pipe
        top_pipe = TopPipe(top_pipe_height, 
                           x = game.window_width - 11, 
                           y = 2,
                           )

        # create bottom pipe
        bottom_pipe = BottomPipe(bottom_pipe_height, 
                                 x = game.window_width - 11, 
                                 y = (top_pipe_height + self.top_bottom_space) - 5,
                                 )

        return [top_pipe, bottom_pipe]
       

    def run(self, dt: int, game, object: None) -> None:

        super().run(dt, game, object)

        # spawn the object
        spawned_objects = self.pipes_factory(dt, game)

        # add the object to the game
        game.addObjects(spawned_objects)

