
from typing import override
from engine.components.drawing_stack import DrawingStack
from engine.components.drawing import Drawing
from engine.components.object import Object
from engine.effects.repeat_callbacks_effect import RepeatCallbacksEffect
from engine.effects.repeat_effect import RepeatType
from engine.metrics.duration import Duration, DurationMetrics
from engine.metrics.vec2 import Vec2


class Bird(Object):
    def __init__(self, x = 0, y = 0, priority = 0):
       
        birdDrawing = self.draw_bird()

        tags: list[str] = ['bird']
        
        super().__init__(tags=tags, drawing=birdDrawing, position=Vec2(x, y), priority=priority)


    def draw_bird(self) -> Drawing:

        ''' The body of the bird '''
        wings = Drawing(tag = "wings", drawingStates= ['/\ .',  '__ .'])
        body = Drawing(tag = "body", drawingStates=   ['    >'])

         # create the bird drawing
        birdDrawing: DrawingStack = DrawingStack()

        ''' stack the two drawings together '''
        birdDrawing.add(wings.copy())
        birdDrawing.add(body.copy())

        return birdDrawing


    @override
    def onMount(self):
        
        ''' ANIMATIONS '''
        # add the fly animation effect
        # define effect
        self.fly_effect = RepeatCallbacksEffect(
            repeatType=RepeatType.INDEFINETLY_EVERY_DURATION, 
            duration=Duration(DurationMetrics.MILLISECONDS, 250),
            )

        self.fly_effect.addCallback(self.animate_bird_flying)
        
        self.addEffect(self.fly_effect)

        # define effect
        self.move_effect = RepeatCallbacksEffect(
            repeatType=RepeatType.INDEFINETLY_EVERY_DURATION, 
            duration=Duration(DurationMetrics.SECONDS, 1),
            )

        self.move_effect.addCallback(self.move_pipe)
        
        self.addEffect(self.move_effect)
        return super().onMount()
    
    def move_pipe(self, **kwargs):
        object = kwargs.get('object', None)

        object.position.x += 1
    
    # fly animation
    def animate_bird_flying(self, **kwargs):
        
        obj: Object = kwargs.get('object', None)

        if obj == None:
            raise TypeError('game or object arguments is Null')

        obj.drawing.next_state()





