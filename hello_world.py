
from engine.components.drawing import Drawing
from engine.components.object import Object
from engine.core import Game
from engine.metrics.vec2 import Vec2



class TextBox(Object):
    def __init__(self, text, x = 0, y = 0, priority= 0):
        drawing = Drawing(tag=text, drawingStates=[text])

        super().__init__(tag='hello_world', drawing=drawing, position=Vec2(x, y), priority=priority)


game = Game(width = 70, height = 35, debug_mode=False)

textBox = TextBox('hello world', x = 10, y = 10)

game.addObject(textBox)

game.run()

