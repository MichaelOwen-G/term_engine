from engine.components.drawing import Drawing
from engine.components.drawing_stack import DrawingStack
from engine.components.object import Object
from engine.core import Game
from engine.effects.repeat_callbacks_effect import RepeatCallbacksEffect
from engine.effects.repeat_effect import RepeatType
from engine.metrics.duration import Duration, DurationMetrics
from engine.metrics.vec2 import Vec2

game: Game = Game(70, 30)
wordDrawing = Drawing(tag = "wordDrawing", drawingStates=[
'''
_/\_
''',
'''
_  _
 \/
'''
    ], stripNewLines=True)

word = Object(
                tag = 'word', 
                drawing = wordDrawing, 
                position = Vec2(10, 10),
                )

word.listen_to_keys = True

change_effect = RepeatCallbacksEffect(
                                    repeatType=RepeatType.INDEFINETLY_EVERY_DURATION, 
                                    duration=Duration(DurationMetrics.MILLISECONDS, 200),
                                    )

def change_word(dt: int, game: Game, obj: Object):
    obj.drawing.next_state()
    obj.pos.x += 1

    # obj.pos.y += 1 if obj.pos.y < game.floor else -20
    # obj.drawing = Drawing(tag = "wordDrawing", drawingStates=[f'{game.floor}:{obj.bounds.y_end}'])
    pass
    

change_effect.addCallback(change_word)

word.addEffect(change_effect)

game.addObject(word)

game.run()