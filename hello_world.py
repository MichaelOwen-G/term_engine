
from engine.components.drawing import Drawing
from engine.components.object import Object
from engine.core import Game
from engine.effects.repeat_effect import RepeatCallbacksEffect, RepeatType
from engine.metrics.duration import Duration, DurationMetrics
from engine.metrics.vec2 import Vec2


class TextBox(Object):
    def __init__(self, text, x = 0, y = 0, priority= 0):
        drawing = Drawing(tag=text, drawingStates=[text])

        super().__init__(tags=['hello_world'], drawing=drawing, position=Vec2(x, y), priority=priority)

    def onMount(self, **kwargs):
        # add effect
        self.move_effect = RepeatCallbacksEffect(
            repeatType=RepeatType.INDEFINETLY_EVERY_DURATION, 
            duration=Duration(DurationMetrics.MILLISECONDS, 200),
            )

        self.move_effect.addCallback(self.move)
        
        self.addEffect(self.move_effect)
        return super().onMount()
    
    def move(self, **kwargs):
        object = kwargs.get('object', None)

        object.position.y -= 1



game = Game(width = 70, height = 35, debug_mode=False)

textBox = TextBox('hello world', x = 10, y = 25)

game.addObject(textBox)

game.run()