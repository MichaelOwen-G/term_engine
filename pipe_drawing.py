import random
from engine.components.drawing import Drawing
from engine.components.drawing_stack import DrawingStack
from engine.components.object import Object
from engine.core import Game
from engine.effects.RepeatEffect import RepeatType
from engine.effects.SpawnEffect import SpawnEffect
from engine.metrics.duration import Duration, DurationMetrics
from engine.metrics.vec2 import Vec2


pipeTrunk = Drawing(tag = "pipeTrunk", drawingStates=['|   |'])

pipeBase = Drawing(tag = "pipeBase", drawingStates=[
'''
 _|   |_    
|_______|
'''
]
)

trunk_min_height = 3

trunk_max_height = 10

top_bottom_space = 4

top_pipe_height = 0

def spawn_top_pipe( game: 'Game', dt: int,):
    print()
    print('::::::::::::: SPAWINING TOP PIPE :::::::::::::::')

    # create pipeDrawing
    pipe = DrawingStack('top_pipe')

    # randomise height of top_pipe's trunk
    top_pipe_height = random.randint(trunk_min_height, trunk_max_height)
    print('top_pipe_height: ', top_pipe_height)

    # generate the pipe's trunk
    for i in range(top_pipe_height):
        pipe.add(pipeTrunk)

    # generate the pipe's base
    pipe.add(pipeBase)

    # position at the top right
    pos = Vec2(((game.window_width - 1) - pipe.maxWidth), 7)
    

    # return pipe
    obj = Object(
        tag = 'pipe',
        drawing = pipe,
        position = pos,
    )

    print(f' DRAWING PANEL SIZE {pipe.maxWidth}, {pipe.maxHeight}:::::')

    print()

    return obj

def spawn_bottom_pipe( game: 'Game', dt: int,):
    print()
    print('::::::::::::: SPAWINING BOTTOM PIPE :::::::::::::::')
    # create pipeDrawing
    pipe = DrawingStack('bottom_pipe')

    # get bottom pipe's trunk height
    bottom_pipe_height = (game.window_height - 1) - (top_pipe_height + 4 + top_bottom_space)
    
    print(f' bottom_pipe_height: {bottom_pipe_height}')
    
    # generate the pipe's trunk
    for i in range(bottom_pipe_height):
        pipe.add(pipeTrunk)

    # generate the pipe's base
    pipe.add(pipeBase)

    # position at the top right
    pos = Vec2(((game.window_width - 1) - pipe.maxWidth), 7)
    print(f' DRAWING PANEL SIZE {pipe.maxWidth}, {pipe.maxHeight}')
    print(f' pos: {pos}')
    print()

    # return pipe
    obj = Object(
        tag = 'pipe',
        drawing = pipe,
        position = pos,
    )

    print(f' DRAWING PANEL SIZE {obj.size}:::::')
    print()

    return obj


# effects 
# spawn effects
spawn_top_pipes = SpawnEffect(
    repeatType=RepeatType.INDEFINETLY_EVERY_DURATION,
    duration=Duration(DurationMetrics.SECONDS, 1),
    object_factory=spawn_top_pipe,
)

spawn_bottom_pipes = SpawnEffect(
    repeatType=RepeatType.INDEFINETLY_EVERY_DURATION,
    duration=Duration(DurationMetrics.SECONDS, 1),
    object_factory=spawn_bottom_pipe,
)