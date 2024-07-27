
import curses
from typing import override
from engine._interface import EngineInterface
from engine.components._interfaces import ObjectInterface
from engine.components.collider import CollisionType
from engine.components.drawing_stack import DrawingStack
from engine.components.drawing import Drawing
from engine.components.object import CollidableObject, Object
from engine.effects.repeat_callbacks_effect import RepeatCallbacksEffect
from engine.effects.repeat_effect import RepeatType
from engine.metrics.duration import Duration, DurationMetrics
from engine.metrics.vec2 import Vec2


class Bird(CollidableObject):
    def __init__(self, x = 0, y = 0, tags: list[str] = [], priority = 0):
       
        birdDrawing = self.draw_bird()

        self.dead = False

        self.key_presses =[]

        super().__init__(tags=tags, drawing=birdDrawing, position=Vec2(x, y), priority=priority, isPersistent = True)


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

        self.gravity_effect = RepeatCallbacksEffect(
            repeatType=RepeatType.INDEFINETLY_EVERY_DURATION, 
            duration=Duration(DurationMetrics.MILLISECONDS, 150),
            )

        self.gravity_effect.addCallback(self.pull_down)
        
        self.addEffect(self.gravity_effect)

        # define effect

        ''' ANIMATIONS '''
        return super().onMount()
    
    def pull_down(self, **kwargs):
        object = kwargs.get('object', None)

        object.position.y += 1

    
    def move_pipe(self, **kwargs):
        object = kwargs.get('object', None)

        object.position.x += 1
    
    # fly animation
    def animate_bird_flying(self, **kwargs):
        
        obj: Object = kwargs.get('object', None)

        if obj == None:
            raise TypeError('game or object arguments is Null')

        obj.drawing.next_state()

    def update(self, dt: float, game: EngineInterface):

        # key = game.stdscr.getch()

        # self.handle_bird_movement(key)

        self.gravity()

        super().update(dt, game)

    def listen_for_key_press(self) -> bool: return True


    def collide_with(self, other: ObjectInterface, collisionType: CollisionType):
        super().collide_with(other, collisionType)

        self.dead = True

    def handle_bird_movement(self, key):
        if key == ord('w'):
            self.pos.y -= 2

    def gravity(self):...
        # self.pos.y += 1









