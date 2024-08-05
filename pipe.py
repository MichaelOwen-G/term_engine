from typing import override
from engine.components.drawing import Drawing, DrawingStack
from engine.components.object import CollidableObject
from engine.effects.repeat_effect import RepeatCallbacksEffect, RepeatType
from engine.metrics.duration import Duration, DurationMetrics
from engine.metrics.vec2 import Vec2


''' Drawings '''
pipe_trunk = ['  |      \  ']


top_pipe_base = [
'''
 _|      |_
|__________|
'''
]


bottom_pipe_base = [
'''
 __________ 
|_       __|
  |      |
'''
]


class Pipe(CollidableObject):
    def __init__(self, pipe_height, x = 0, y = 0, tags = '',  priority = 0):
       
        pipe = self.draw_pipe(pipe_height)

        self.x = 0
        
        super().__init__(tags = tags, drawing = pipe, position=Vec2(x, y), priority=priority)

    def draw_pipe(self, **kwargs) -> DrawingStack:
        # get arguments
        # the pipe to create drawing of, either top or bottom pipe
        pipe_part: str = kwargs.get('pipe_part', '')

        # the height of the part of pipe to spawn
        pipe_height: int = kwargs.get('pipe_height', 0)

        # get which base drawing to use and create it
        if pipe_part == 'top':
            pipeBase = Drawing(tag = "pipeBase", drawingStates = top_pipe_base)
        else:
            pipeBase = Drawing(tag = "pipeBase", drawingStates = bottom_pipe_base)

        # create the pipe trunk drawing
        pipeTrunk = Drawing(tag = "top-pipeTrunk", drawingStates = pipe_trunk)

        # create pipeDrawing stack
        pipe = DrawingStack(tag = f'{pipe_part}_pipe', maxWidth = 0, maxHeight = 0)

        # get number of pipe_trunk parts b
        trunk_len: int = pipe_height - pipeBase.maxHeight

        # add base first before trunks if the pipe for bottom
        if pipe_part == 'bottom': pipe.add(pipeBase)

        # generate the pipe's trunk
        for _ in range(trunk_len): pipe.add(pipeTrunk.copy())

        # add base last before trunks if the pipe for top
        if pipe_part == 'top': pipe.add(pipeBase)

        return pipe


    @override
    def update(self, dt: float, game):
        super().update(dt, game)

        # find the player
        bird_results = game.game_screen.find_objects_by_tag('bird')

        if len(bird_results) == 0: return

        bird: CollidableObject = bird_results[0]

        # check if the player has past this
        if (bird.bounds.x_start > self.bounds.x_end):
            # add point to the player if yes
            bird.points += 1
    
    def onMount(self, **kwargs):
        self.x = self.pos.x

        ''' ANIMATIONS '''
        # define effect
        self.move_effect = RepeatCallbacksEffect(
            repeatType=RepeatType.INDEFINETLY_EVERY_DURATION, 
            duration=Duration(DurationMetrics.MILLISECONDS, 110),
            )

        self.move_effect.addCallback(self.move_pipe)
        
        self.addEffect(self.move_effect)
        return super().onMount()
    
    def move_pipe(self, **kwargs):
        object = kwargs.get('object', None)

        object.position.x -= 1


class TopPipe(Pipe):
    def __init__(self, pipe_height, x = 0, y = 0,  priority = 0):
        super().__init__(pipe_height, x = x, y = y, tags = ['pipe', 'top', ],  priority = priority)

    @override
    def draw_pipe(self, pipe_height) -> DrawingStack:
        return super().draw_pipe(pipe_height = pipe_height, pipe_part = 'top')


class BottomPipe(Pipe):
    def __init__(self, pipe_height, x = 0, y = 0, priority = 0):
        super().__init__(pipe_height, x = x, y = y, tags = ['pipe', 'bottom',],  priority = priority)

    @override
    def draw_pipe(self, pipe_height)-> DrawingStack:
        return super().draw_pipe(pipe_height = pipe_height, pipe_part = 'bottom')