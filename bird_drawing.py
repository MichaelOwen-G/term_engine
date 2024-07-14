'''
Create the bird drawing.
It will include a stack of drawings of the bird's body and wings
'''

from engine.components._interfaces import DrawingInterface
from engine.components.drawing_stack import DrawingStack
from engine.components.drawing import Drawing
from engine.components.object import Object
from engine.core import Game
from engine.effects.RepeatCallbacksEffect import RepeatCallbacksEffect
from engine.effects.RepeatEffect import RepeatType
from engine.metrics.duration import Duration, DurationMetrics
from engine.metrics.vec2 import Vec2


birdDrawing: DrawingStack = DrawingStack()

'''
Wings:
Drawing of two frames of wings flapping
'''

wings = Drawing(tag = "wings", drawingStates= [ r'-_/\__', "-____"])

'''
The body of the bird
'''
body = Drawing(tag = "body", drawingStates= ['(    >'])


''' 
stack the two drawings together
'''
birdDrawing.add(wings)
birdDrawing.add(body)

# effects
# fly animation
def animate_bird_flying(dt: int, game: Game, obj: Object):
    obj.drawing.next_state()

# define effect
fly_effect = RepeatCallbacksEffect(
    repeatType=RepeatType.INDEFINETLY_EVERY_DURATION, 
    duration=Duration(DurationMetrics.MILLISECONDS, 100),
    )

fly_effect.addCallback(animate_bird_flying)


# add effect to bird
bird = Object(tag = 'bird', drawing = birdDrawing, position=Vec2(10,8))
bird.addEffect(fly_effect)



